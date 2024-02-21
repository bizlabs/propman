# Copyright (c) 2024, Bizlabs and contributors
# For license information, please see license.txt

from dateutil.relativedelta import *
# import dateutil
import datetime
import frappe
from frappe.model.document import Document

# table inv_schedule last_date, next_date, period (month, day, week, year), num_per(int), $, account, desc
		# acct dimensions lease and building are obtained from the lease
# function new_lease() called from daily_runs verity is due and create new lease
# same for latefee
# table latefee_schedule can be auto-populated with selected late fee policy


class lease(Document):

	# def before_validate():
	# 	if self.renewal_draft:
	# 		status = 
	# 	meta = get_meta("lease")
	# 	meta.get_field("renewal_lease_start").reqd = status
	# 	meta.get_field("renewal_lease_end").reqd = status
		
	def validate(self):
		# perhaps use a switch/case type statement.  Add all reqrd fields
		if not self.renewal_draft:
			if not self.renewal_lease_start:
				frappe.throw("renewal lease start is required renewal is not draft")
			if not self.renewal_lease_end:
				frappe.throw("renewal lease end is required renewal is not draft")


	@frappe.whitelist()
	def Moveout(self,arg1):
		frappe.msgprint("action = Moveout")

	@frappe.whitelist()
	def Renew(self,arg1):
		# set new lease details in a queue
		# on new lease date, create a new lease history child table record from existing lease details
		# and copy lease queue into the current lease details
		# if new lease date is already passed, process this queue immediately
		# add a new blue buton for "lease renewal queued"
		# tab lease renewal hidden when no lease in que. blue button goes to tab
		frappe.msgprint("action = Renew")

	def get_new_scheduled_invoices(self,run_date):
		new_invoices = []
		for schedule in self.inv_schedule:
			#xxx change if to loop to catch up on possible missed days.
			if run_date >= schedule.next_date: #xxx use schedule.pre_inv_days to invoice b4 due date
						# items = {'amount':schedule.amount,'desc':schedule.desc,'account':schedule.account,
						# 	'date':schedule.next_date,'docstatus':schedule.docstatus}
				new_invoices.append (self.create_invoice(run_date,schedule))
				#calc next date from schedule
				schedule.next_date = self.get_next_date(run_date,schedule)
				schedule.last_date = run_date
				self.save() 				
				
		return new_invoices
	
	def create_invoice(self,run_date,items):
		settings = frappe.get_doc('property manager settings')
		# items = {'amount':schedule.amount,'desc':schedule.desc,'account':schedule.account,
		# 	 		'date':schedule.next_date,'docstatus':schedule.docstatus}
		inv = frappe.get_doc({
			'doctype':	  		'Sales Invoice',
			'customer':			self.customer,
			'company':	  		settings.company,
			'posting_date':		min(run_date,items.next_date), # earliest of run_date and due_date
			'due_date':			items.next_date,
			'docstatus': 		0 if items.docstatus == 'draft' else 1,
			'debit_to': 		settings.receivable_account,
			'building':			self.building,
			'items':[{
				# 'item':    item,
				'item_name':	items.desc,
				'qty':     		1,
				'rate':    		items.amount,
				'income_account': items.account,
				'building':		self.building,
			}]
		})

		result = inv.insert()
		return result
		

	def get_next_date(self,run_date,schedule): #given schedule.period, schedule.increment
		inc = schedule.increment
		if schedule.period == 'day':
			# next_date = next_date + increment
			next_date = schedule.next_date + datetime.timedelta(days=inc)
		elif schedule.period == 'week':
			next_date = schedule.next_date + datetime.timedelta(weeks = inc)

		elif schedule.period == 'month':
			next_date = schedule.next_date + relativedelta(months = inc)

		elif schedule.period == 'year':
			next_date = schedule.next_date + relativedelta(years = inc)
		
		return next_date

	def get_new_scheduled_latefees(self,run_date, open_invoices, latefee_schedules):
# xxx This hasn't been tested yet
		
		settings = frappe.get_doc('property manager settings')
		new_latefees = []
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
			 		'date':schedule.next_date,'docstatus':schedule.latefee_status}
				new_latefees.append (self.create_invoice(run_date,items))
				
				if schedule.repeat_per == 0:
					schedule.next_date = self.next_date + schedule.grace_per
				else:
					schedule.next_date = run_date + schedule.repeat_per

				schedule.last_date = run_date
				self.save() 				