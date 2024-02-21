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

from datetime import date
import frappe
from frappe.model.document import Document

#xxx check if this date has already run before possibly running it twice
@frappe.whitelist()
def manual_run():
	leasenames = frappe.get_all('lease',filters={'status':'active'},pluck='name')
	proc_run = frappe.new_doc("daily process run")
	proc_run.run_date = date.today()
	proc_run.new_inv = []
	threshold = 0
	filters = { 'outstanding_amount': ['>', threshold], 'docstatus':1}
	fields = ['name','outstanding_amount', 'due_date']
	open_invoices = frappe.get_all('Sales Invoice', filters=filters, fields=fields)
	latefee_schedules = frappe.get_all('late fee schedule')
	for leasename in leasenames:
		lease= frappe.get_doc("lease",leasename)
		invoices = lease.get_new_scheduled_invoices(proc_run.run_date)  #list of new invoices

		for invoice in invoices:
			invoice_link = frappe.get_doc({
				'doctype': 'new_invs',
				'run_date': proc_run.run_date,
				'invoice': invoice,
			})
			
			proc_run.append("new_invs", invoice_link)

		
		latefees = lease.get_new_scheduled_latefees(proc_run.run_date,open_invoices, latefee_schedules)

		for latefee in latefees:
			latefee_link = frappe.get_doc({
				'doctype': 'new_latefees',
				'run_date': proc_run.run_date,
				'latefee': latefee,
			})
			proc_run.append("new_latefees", latefee_link)

	proc_run.num_invs = len(proc_run.new_invs)
		# proc_run.new_latefees = lease.get_new_latefees(proc_run.date)
		# proc_run.num_latefees = len(proc_run.get_new_latefees)
		# xxx create emails (perhaps in  a draft list to approve interactively?)
	proc_run.insert() 
	return True

class dailyprocessrun(Document):
	pass