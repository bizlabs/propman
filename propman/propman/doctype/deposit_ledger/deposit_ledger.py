# Copyright (c) 2024, Bizlabs and contributors
# For license information, please see license.txt

# import frappe
from datetime import date
from frappe.model.document import Document


class depositledger(Document):

	def before_insert(self):
		items = {
			'due_date':		self.due_date,
			'amount':		self.amount,
			'desc':			self.desc,
			'account':		self.account,
			'docstatus':	self.status
		}
		lease = self.parent_doc
		self.invoice = lease.create_invoice(date.today(),items)
	
	def before_save():
		pass
	
	def on_update():
		pass	

	def on_submit():
		pass	

	def on_cancel():
		pass	

	def on_update_after_submit():
		pass	

	def after_delete():
		pass
