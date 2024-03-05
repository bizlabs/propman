# Copyright (c) 2024, Bizlabs and contributors
# For license information, please see license.txt

#table next_lease_inv with next_date, last_date, lease_id, lease_name?, inv_schedule_id 
	# direct poiter to inv_schedule_id so maybe don't have to even open the lease
#table next_latefee_inv with next date, last date, lease_id, lease_name?, lafefee_schedule_id
#lease has tables for scheduled_invoices, scheduled_latefees)	
    # do the actual lease and latefee generation in lease.py.  run those functions from here.
# perhaps start with check_lease(lease_id)
    #checks one lease for due inv and latefees 
    #this should be run after any changes to latefee or inv sched
    #and could be run in a loop over all leases overnight if it's not too long

from datetime import date, datetime
import frappe
from frappe.model.document import Document
# frappe.utils.logger.set_log_level("DEBUG")
# logger = frappe.logger("propman", allow_site=False, file_count=10)

@frappe.whitelist()
def manual_run():
	proc_run = frappe.new_doc("daily process run")
	proc_run.daily_run()
	frappe.msgprint("finished daily process run @ " + str(datetime.now()) )

class dailyprocessrun(Document):
	def daily_run(self):
		time_start = datetime.now()
		leasenames = frappe.get_all('lease',filters={'auto_rent':True},pluck='name')
		self.run_date = date.today()
		self.new_inv = []
		threshold = 0
		filters = { 'outstanding_amount': ['>', threshold], 'docstatus':1}
		fields = ['name','outstanding_amount', 'due_date']
		open_invoices = frappe.get_all('Sales Invoice', filters=filters, fields=fields)
		fields = ['parent','next_date','last_date','grace_per','repeat_per','created_status','flat_fee','pct',]
		latefee_schedules = frappe.get_all('late fee schedule',fields=fields)
		for leasename in leasenames:
			lease= frappe.get_doc("lease",leasename)

			if self.run_date > lease.lease_end:
				lease.inv_status = "draft"
				lease.expired = True
				
			invoices = lease.get_new_scheduled_invoices(self.run_date)  #list of new invoices

			for invoice in invoices:
				invoice_link = frappe.get_doc({
					'doctype': 'new_invs',
					'run_date': self.run_date,
					'invoice': invoice,
				})
				
				self.append("new_invs", invoice_link)

			
			latefees = lease.get_new_scheduled_latefees(self,open_invoices, latefee_schedules)

			# for latefee in latefees:
			# 	latefee_link = frappe.get_doc({
			# 		'doctype': 'new_latefees',
			# 		'run_date': self.run_date,
			# 		'latefee': latefee,
			# 	})
			# 	self.append("new_latefees", latefee_link)

			lease.save()
		self.num_invs = len(self.new_invs)
		# self.num_latefees = len(self.new_latefees)
			# xxx create emails (perhaps in  a draft list to approve interactively?)
		self.elapsed_time = (datetime.now()-time_start).seconds
		self.insert()
		return True