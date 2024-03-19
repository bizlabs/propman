# Copyright (c) 2024, Bizlabs and contributors
# For license information, please see license.txt

from frappe.utils import today, getdate
from dateutil.relativedelta import *
# import dateutil
import datetime
from datetime import date
import frappe
from frappe.model.document import Document

# table inv_schedule last_date, next_date, period (month, day, week, year), num_per(int), $, account, desc
		# acct dimensions lease and building are obtained from the lease
# function new_lease() called from daily_runs verity is due and create new lease
# same for latefee
# table latefee_schedule can be auto-populated with selected late fee policy


def test_minute():
	frappe.msgprint("test minute good")
	print("test outside class")

class lease(Document):

	@frappe.whitelist()
	def do_renewal(self):
		frappe.msgprint("starting function do_renewal") # xxx delete after debug
		# rotate lease details to history and renewal to lease
		# this is called from daily_run on lease renewal date (or directly from lease_received workflow if its time)
		self.workflow_status = "Active"
		# xxx remove non-renewal penalty inv_schedule
		newlist = [x for x in self.inv_schedule if x.penalty != True]
		self.inv_schedule = newlist

		other_description = ""
		other_charges = 0
		for si in self.inv_schedule:
			if si.desc != "Rent":
				other_description += si.desc + " $" + str(si.amount) + "\n"
				other_charges += si.amount
									  
		lease_history = {
			'start_date': self.lease_start,
			'end_date': self.lease_end,
			'renewal_date': date.today(),
			'period': self.period,
			'increment': self.increment,
			'rent': self.rent,
			'other_description': other_description,
			'other_charges': other_charges, 
			#'notes': "add notes here if desired" # perhaps start a note here that user can edit?
		}
		self.append('lease_history',lease_history)

		self.lease_start = self.renewal_lease_start
		self.lease_end = self.renewal_lease_end
		self.period = self.renewal_period
		self.increment = self.renewal_increment
		self.rent = self.renewal_rent
		#xxx convert draft addit. deposit invoice to confirmed (docstatus 1)
		self.reset_renewal_fields()
		self.save()

	def reset_renewal_fields(self):
		self.renewal_lease_start = self.renewal_lease_end = None
		self.renewal_period = self.renewal_increment = None
		self.renewal_rent = self.renewal_deposit = None
		self.renewal_penalty = None


	def on_update_after_submit(self):
		# move these to the switch/case in validate xxx
		if self.workflow_status == "Renewal received":
			# cancel lease and amend to a new lease
			frappe.msgprint ("from here, we'll create an amended lease")
		if self.workflow_status == "Moveout complete":
			# archive
			frappe.msgprint("Moveout complete.  Archive me now")
		
	def validate(self):
		# process new or updated one-time inv/credit schedules when entered.
		#	eg, enter invoice charge for a repair
		# create invoice if it's time, else record future date for processing
		# in daily process run
		invs = []
		settings = frappe.get_doc('property manager settings')
		for x in self.inv_schedule:
			if x.period == "one-time":
				if x.isnew or x.isupdate:
					process_now = True
					if x.next_date != None:
						delay = getdate(x.next_date) - date.today()
						if delay.days > 0:
							process_now = False
					else:
						x.next_date = date.today()
					if process_now:
						invs.append(self.create_invoice(x.next_date, x,settings))
					else:
						frappe.msgprint("new item will be processed in  " + str(delay.days) + " day(s)")
						x.isnew = x.isupdate = False
			else:
				x.isnew = x.isupdate = False
		newlist = [x for x in self.inv_schedule if not (x.isnew or x.isupdate)]
		self.inv_schedule = newlist
		num_invs = len(invs)
		if num_invs > 0:
			frappe.msgprint(str(num_invs) + " invoice/credit(s) have been created")

	#do something according to workflow status.  move to js where I can just do it on transistion
	# to new workflow state instead of every validation
		match self.workflow_status:
			case "Draft":
				# xxx update or create deposit invoice
				if self.deposit_invoice:
					self.update_deposit_invoice(self.deposit, self.deposit_inv)
				else:
					self.create_deposit_invoice(self.deposit, settings)
				
			case "Active":
				pass
			case "Renewal Needed":
				pass
			case "Renewal sent":
				pass
			case "Renewal received":
				pass
			case "Moveout notice received":
				pass
			case "Moveout vacated":
				pass
			case "Moveout complete":
				pass
			case "Archived":
				pass
			case _:
				pass

	def create_deposit_invoice(self, amount, settings):
		items = {
			'xxx':	'xxx'
		}
		posting_date = 'xxx'
		self.create_invoice(posting_date, items, settings)
		pass #xxx

	def update_deposit_invoice(amount, inv_name):
		inv = frappe.get_doc('Sales Invoice',inv_name)
		inv.items[0].rate = amount
		#xxx inv.save()
		pass #xxx
	
	@frappe.whitelist()
	def Moveout(self,arg1):
		frappe.msgprint("action = Moveout")

	@frappe.whitelist()
	def do_renew(self,arg1): #xxx delete me
		# rotate lease details to history and renewal to lease
		# this is called from daily_run on lease renewal date (or directly from lease_received workflow if its time)
		# include non-renewal penalty to add to invoice

		# on new lease date, create a new lease history child table record from existing lease details
		# and copy lease queue into the current lease details
		# if new lease date is already passed, process this queue immediately
		# add a new blue buton for "lease renewal queued"
		# tab lease renewal hidden when no lease in que. blue button goes to tab
		frappe.msgprint("action = Renew")

	def get_new_scheduled_invoices(self,run_date):
		new_invoices = []
		settings = frappe.get_doc('property manager settings')
		for schedule in self.inv_schedule:
			while run_date >= schedule.next_date - datetime.timedelta(days=settings.pre_inv):
						# items = {'amount':schedule.amount,'desc':schedule.desc,'account':schedule.account,
						# 	'date':schedule.next_date,'docstatus':schedule.docstatus}
				new_invoices.append (self.create_invoice(run_date,schedule,settings))
				#calc next date from schedule
				if schedule.period == "one-time":
					schedule.amount = 0.00  # mark for later deletion
				if schedule.desc == "Rent":
					self.next_date = schedule.next_date = self.get_next_date(run_date,schedule)
					self.last_date = run_date
				else:
					schedule.next_date = self.get_next_date(run_date,schedule)
					schedule.last_date = run_date
		
		# one-time items were set to amount = 0 above so they can be removed here...
		newlist = [x for x in self.inv_schedule if x.amount > 0.00]
		self.inv_schedule = newlist

		self.save() 				
		return new_invoices
	
	@frappe.whitelist()
	def set_penalty_schedule(self):
		settings = frappe.get_doc('property manager settings')
		items = {
			'next_date':	self.renewal_lease_start,
			'period':		self.renewal_period,
			'increment':	self.renewal_increment,
			'desc':			"additional rent for non-renewed lease", #DON'T CHANGE DESCRIPTION.  it triggers delete when lease renewed
			'penalty':		True,
			'account':		settings.rent_income_acct,
			'type':			"Other",
			'amount': 		self.renewal_penalty,
			'inv_status':	"draft"
		}
		self.append('inv_schedule',items)
		self.save()
	
	def create_invoice(self,posting_date,items,settings):
		# settings = frappe.get_doc('property manager settings')
		# items = {'amount':schedule.amount,'desc':schedule.desc,'account':schedule.account,
		# 	 		'date':schedule.next_date,'docstatus':schedule.docstatus}
		
		inv = frappe.get_doc({
			'doctype':	  		'Sales Invoice',
			'is_return':		1 if items.type == "credit" else 0,
			'customer':			self.customer,
			'company':	  		settings.company,
			'posting_date':		min(getdate(posting_date),getdate(items.next_date)), # earliest of posting_date and due_date
			'due_date':			items.next_date,
			'docstatus': 		0 if items.inv_status == 'draft' else 1,
			'debit_to': 		settings.receivable_account,
			'building':			self.building,
			'lease':			self.name,
			'items':[{
				# 'item':    item,
				'item_name':	items.desc,
				'qty':     		-1 if items.type == "credit" else 1,
				'rate':    		items.amount,
				'income_account': items.account,
				'building':		self.building,
				'lease':		self.name,
			}]
		})

		result = inv.insert()
		return result
		

	def get_next_date(self,run_date,schedule): #given schedule.period, schedule.increment
		inc = schedule.increment
		if schedule.period == 'day':
			next_date = schedule.next_date + datetime.timedelta(days=inc)
		elif schedule.period == 'week':
			next_date = schedule.next_date + datetime.timedelta(weeks = inc)

		elif schedule.period == 'month':
			next_date = schedule.next_date + relativedelta(months = inc)

		elif schedule.period == 'year':
			next_date = schedule.next_date + relativedelta(years = inc)
		
		return next_date

	def get_new_scheduled_latefees(self,proc_run, open_invoices, latefee_schedules):
# xxx This hasn't been tested yet
		run_date = proc_run.run_date
		settings = frappe.get_doc('property manager settings')
		proc_run.new_latefees = []
			# filter only those latefee_schedules belonging to this lease
		myscheds = [i for i in latefee_schedules if i.parent == self.name]
		my_open_invoices = [i for i in open_invoices if i.lease == self]
			#xxx This will require lease accounting dimension (and haven't verified this is how filter on dimension)
		open_balance=0
		for inv in my_open_invoices:
			open_balance += inv.outstanding_amaount
		
		for schedule in myscheds:
			if run_date > schedule.next_date: 
					# get the invoice schedule this latefee schedule refers to
				
				threshold = 0 #xxx make this programmable
				if open_balance > threshold:
					fee = schedule.flat_fee + schedule.pct * open_balance
				else:
					schedule.next_date = self.next_date + schedule.grace_per
					continue

				items = {'amount':fee,'desc':"Late Fee",'account':settings.late_fee_acct,
			 		'date':schedule.next_date,'docstatus':schedule.created_status}
				latefee = self.create_invoice(run_date,items,settings)

				latefee_link = frappe.get_doc({
					'doctype': 'new_latefees',
					'run_date': proc_run.run_date,
					'latefee': latefee,
				})
				proc_run.append("new_latefees", latefee_link)
				
				if schedule.repeat_per == 0:
					schedule.next_date = self.next_date + schedule.grace_per
				else:
					schedule.next_date = run_date + schedule.repeat_per

				schedule.last_date = run_date
				self.save() 
		return proc_run				