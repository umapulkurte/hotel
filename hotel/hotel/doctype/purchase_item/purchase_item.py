# Copyright (c) 2013, Wayzon and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class PurchaseItem(Document):
	pass
@frappe.whitelist()
def get_details(item1):
	q1=frappe.db.sql("""select item_name1, rate from `tabAdd Item` where item=%s""",(item1))
	return q1

@frappe.whitelist()
def get_money_in_words(n):
	from frappe.utils import money_in_words
	from frappe.utils import in_words
	x=money_in_words(n)
	return (x)