# Copyright (c) 2024, Bizlabs and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class pm_charges(Document):
	pass

	# @property
	# def open_bal(self):
	# 	frappe.get_value('Sales Invoice',self.invoice,'outstanding_amount')
		
		# perhaps don't do running total here? Might be really slow with all the db queries
	# @property
	# def total(self):
	# 	lease = self.parent_doc
	# 	charges = frappe.get_all('charges',filters={},fields=[],order_by='posting_date')

	# def before_insert(self):
	# 	items = {
	# 		'due_date':		self.due_date,
	# 		'amount':		self.amount,
	# 		'desc':			self.desc,
	# 		'account':		self.account,
	# 		'docstatus':	self.status
	# 	}
	# 	lease = self.parent_doc
	# 	self.invoice = lease.create_invoice(self.posting_date,items)
	
	# def before_save():
	# 	frappe.msgprint("before saving charges")
	# 	pass
	
	# def on_update():
	# 	frappe.msgprint("debug")
	# 	pass	

	# def on_submit():
	# 	frappe.msgprint("debug")

	# def on_cancel():
	# 	frappe.msgprint("debug")

	# def on_update_after_submit():
	# 	frappe.msgprint("debug")

	# def after_delete():
	# 	frappe.msgprint("debug")
