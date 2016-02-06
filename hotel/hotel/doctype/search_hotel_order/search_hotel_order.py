# Copyright (c) 2013, Wayzon and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class SearchHotelOrder(Document):
	pass

def show_list(d,t,c,w):
	header="""
	<style>
		#n1{
		display:none;
		}
		#n2{
		display:none;
		}
	</style>
	<table border=5 id="Tbl1">
	<tr align=left><th colspan="1">Date:%s</th><th></th><th colspan="3">Table No:%s</th></tr>
	<tr align=left><th colspan="1">Customer Name:%s</th><th></th><th colspan="3">Waiter Name:%s</th></tr>
	<tr bgcolor=LightGrey align=center><td width=150 id='n2'>Name</td><td width=200 ><b>Item</td>
	<td width=100 ><b>Qty</td><td width=100><b>Rate</td><td width=100><b>Amount</td></tr>"""  %(d,t,c,w)
	return header
@frappe.whitelist()
def get_order_details(o):
	a=''
	m=frappe.db.sql("""select name,item,quantity,rate,amount,date,table_no,customer_name,waiter_name from `tabHotelorder` where order_id=%s and order_status='Completed'""",(o))
	if m:
		l=len(m)
		t_amt=0
		for i in range(0, l):
			html_str="""
			<tr align=center id=%s><td id='n2'>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>""" %(i,m[i][0],m[i][1],m[i][2],m[i][3],m[i][4])
			a=a+html_str
			t_amt=t_amt+int(m[i][4])
		ttl_str="""
		<tr align=center><td id='n2'></td><td>Total</td><td>%s</td><td>%s</td><td>%s</td><td></td>""" %('','',t_amt)
		return (show_list(m[0][5],m[0][6],m[0][7],m[0][8])+a+ttl_str)
	else:
		frappe.msgprint('Entered Order Id does not exist')
		return(show_list('','','',''))