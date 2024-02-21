# Copyright (c) 2024, Bizlabs and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class new_invs(Document):
    
    @property
    def title(self):
        return frappe.get_value('Sales Invoice', self.invoice, 'title')


    @property
    def amount(self):
        return frappe.get_value('Sales Invoice', self.invoice, 'total')