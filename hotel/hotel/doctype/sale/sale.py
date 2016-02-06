# Copyright (c) 2013, Wayzon and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Sale(Document):
	pass

@frappe.whitelist()
def get_item():
	list1=[]
	q9=frappe.db.sql("""select item_name from `tabItem List`""")
	l1=len(q9)
	for j in range(0, l1):
		list1.append(q9[j])
	return (list1)

@frappe.whitelist()
def get_rate(item):
	q1=frappe.db.sql("""select item_name,rate from `tabItem List` where item_name=%s""",(item))
	return (q1)

@frappe.whitelist()
def show_table(d):
	q=frappe.db.sql("""select table_no from `tabTable`""")
	l=len(q)
	dict={}
	str1=''
	for i in range(0, l):
		str2="""
		<input type="hidden" name="d" id="d" value="%s">
		<button class="abc" id="btn%s" type="button" value=%s onclick=myFunction(this.value)>%s</button>""" %(d,i,q[i][0],q[i][0])
		str1=str1+str2

	html="""
		<html>
			<head>
				<script>
					function myFunction(x)
					{
						var date=document.getElementById('d').value;
						var id=x;
						var tbl;
						var wtr;
						frappe.call({
								method:'hotel.hotel.doctype.sale.sale.get_info',
								args:{id1:id,date:date},
								callback:function(r)
								{
									var doclist=frappe.model.sync(r.message);
									cur_frm.set_value("table_no",doclist[0][0][1]);
									cur_frm.set_value("waiter_name",doclist[0][0][0]);
									cur_frm.set_value('order_status','Running');
									cur_frm.set_value('is_lodge_client','');
									cur_frm.set_value('select_room','');
									cur_frm.set_value('customer_name','');
									var w=doclist[0][0][0];
									var t=doclist[0][0][1];
									var date=doclist[1];
									frappe.call
									({
										method:'hotel.hotel.doctype.sale.sale.get_order_id',
										args:{date:date,tbl:t,wtr:w},
										callback:function(r)
										{
											var doclist1=frappe.model.sync(r.message)
											set_field_options('test1',doclist1[1])
											cur_frm.set_value('order_id',doclist1[0])
										}
									})
								}
						});
					}
				</script>
			</head>
		</html>
	"""
	com=html+str1
	return (com,l)

@frappe.whitelist()
def get_info(id1,date):
	q1=frappe.db.sql("""select waiter,table_no from `tabAssignTableData` where date=%s and table_no=%s""",(date,id1))
	return q1,date

@frappe.whitelist()
def get_order_id(date,tbl,wtr):
	q0=frappe.db.sql("""select max(order_id) from `tabHotelorder` where table_no=%s and date=%s and order_status='Running' limit 1""",(tbl,date))[0][0]
	if q0:
		o=int(q0)
		a=''
		q=frappe.db.sql("""select name,item,quantity,rate,amount from `tabHotelorder` 
		where order_id=%s and date=%s and table_no=%s and waiter_name=%s and order_status='Running'""",(o,date,tbl,wtr))
		l=len(q)
		t_amt=0
		for i in range(0, l):
			html_str="""
			<tr align=center id=%s><td id='n2'>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td width=45 id=%s><button id="b%s" type="button" value=%s onclick=delete_record(this.value)><font color='red'>x</button></td></tr>""" %(i,q[i][0],q[i][1],q[i][2],q[i][3],q[i][4],i,i,i)
			a=a+html_str
			t_amt=t_amt+q[i][4]
		ttl_str="""
		<tr align=center><td id='n2'></td><td>Total</td><td>%s</td><td>%s</td><td>%s</td><td></td>""" %('','',t_amt)
		table=(show_list()+a+ttl_str)
		return (o,table,t_amt)
	else:
		q=frappe.db.sql("""select max(order_id) from `tabHotelorder`""")[0][0]
		if q:
			o=int(q)+1
		else:
			o=1
		return (o,show_list())

def show_list():
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
	<tr bgcolor=LightGrey align=center><td width=150 id='n2'>Name</td><td width=200 ><b>Item</td>
	<td width=100 ><b>Qty</td><td width=100 ><b>Rate</td><td width=100 ><b>Amount</td><td width=35><b>X</td></tr>""" 
	html_function="""
				<html>
					<head>
						<script>
							function delete_record(y)
							{
								var arr=[];
								var a=y;
								var row=document.getElementById(a);
								var i=row.getElementsByTagName('td');	
								var j=i.length;
								for(k=0;k<j-1;k++)
								{
									var cell=i[k].innerHTML;
									arr.push(cell);
								}
								var brand=arr[1]
								var type=arr[2]
								var qty=arr[3]
								frappe.call
								({
									method:'hotel.hotel.doctype.sale.sale.delete_order_item',
									args:{x:arr[0],brand:brand,type1:type,qty:qty},
									callback:function(r)
									{
										set_field_options('test1',r.message);
									}
								})
							}
						</script>
					</head>
				</html>
			"""
	return (header+html_function)

@frappe.whitelist()
def delete_order_item(x,brand,type1,qty):
	a=''
	q0=frappe.db.sql("""select item,quantity,order_id from `tabHotelorder` where name=%s""",(x))
	#if(q0[0][2]==0):
	#	total_qty=int(q0[0][3])*int(q0[0][4])
	#	q1=frappe.db.sql("""update `tabLoose Stock` set stock_ml=stock_ml+%s where brand=%s and type=%s""",(total_qty,brand,type1))
		#frappe.msgprint("Loose Stock Updated")
	#else:
	#	total_qty=int(q0[0][2])
	#	q2=frappe.db.sql("""update `tabStock` set stock_quantity=stock_quantity+%s where brand_name=%s and type_name=%s""",(total_qty,brand,type1))
		#frappe.msgprint("Stock Updated")
	sql=frappe.db.sql("""delete from `tabHotelorder` where name=%s and order_status='Running'""",(x))
	m=frappe.db.sql("""select name,item,quantity,rate,amount from `tabHotelorder` where order_id=%s and order_status='Running'""",(q0[0][2]))
	l=len(m)
	t_amt=0
	for i in range(0, l):
		html_str="""
		<tr align=center id=%s><td id='n2'>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td width=45 id=%s><button id="b%s" type="button" value=%s onclick=delete_record(this.value)><font color='red'>x</button></td></tr>""" %(i,m[i][0],m[i][1],m[i][2],m[i][3],m[i][4],i,i,i)
		a=a+html_str
		t_amt=t_amt+m[i][4]
	ttl_str="""
	<tr align=center><td id='n2'></td><td>Total</td><td>%s</td><td>%s</td><td>%s</td><td></td>""" %('','',t_amt)
	return show_list()+a+ttl_str

@frappe.whitelist()
def insert_item(o,i,q,r,d,tbl,w,o_sts,room,customer):
	amt=int(q)*int(r)
	#-----Inserting Record in `tabHotelorder`-------------
	a=''
	q12=frappe.db.sql("""select max(cast(name as int)) from `tabHotelorder`""")[0][0]
	if q12:
		n=int(q12)+1
	else:
		n=1
	q11=frappe.db.sql("""insert into `tabHotelorder` set name=%s,order_id=%s,item=%s,quantity=%s,rate=%s,amount=%s,
	date=%s,table_no=%s,waiter_name=%s,order_status=%s,select_room=%s,customer_name=%s""",(n,o,i,q,r,amt,d,tbl,w,o_sts,room,customer))
	#------Dispalting HTML table----------------------------
	m=frappe.db.sql("""select name,item,quantity,rate,amount from `tabHotelorder` where order_id=%s and order_status='Running'""",(o))
	l=len(m)
	t_amt=0
	for i in range(0, l):
		html_str="""
		<tr align=center id=%s><td id='n2'>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td width=45 id=%s><button id="b%s" type="button" value=%s onclick=delete_record(this.value)><font color='red'>x</button></td></tr>""" %(i,m[i][0],m[i][1],m[i][2],m[i][3],m[i][4],i,i,i)
		a=a+html_str
		t_amt=t_amt+int(m[i][4])
	ttl_str="""
	<tr align=center><td id='n2'></td><td>Total</td><td>%s</td><td>%s</td><td>%s</td><td></td>""" %('','',t_amt)
	return (show_list()+a+ttl_str)

@frappe.whitelist()
def record_submission(d,t,w,o,o_sts):
	total_amt=frappe.db.sql("""select sum(amount) from `tabHotelorder` where order_id=%s""",(o))[0][0]
	q=frappe.db.sql("""update `tabHotelorder` set order_status='Completed' ,total_amount=%s where
	date=%s and table_no=%s and waiter_name=%s and order_id=%s and order_status=%s""",(total_amt,d,t,w,o,o_sts))

@frappe.whitelist()
def get_div(d,tbl,wtr,order_id):
	str11="""
	<style>
		#n1{
		display:none;
		}
		#n2{
		display:none;
		}
		#n3{
		display:none;
		}
		#n4{
		display:none;
		}
	</style>
	<div id='d1' align=center>
	<h3>Hotel Amrut</h3>
	<h5>Opp. LIC Office</h5>
	<h5>Gandhi Nagar,Nanded</h5>
	<h5>Contact No:20462-2012541</h5>
	<table border=5 id="Tbl1">
	<tr align=left><th></th><th colspan="2">Date:%s</th><th colspan="3">Table No:%s</th></tr>
	<tr align=left><th></th><th colspan="2">Order No:%s</th><th colspan="3">Waiter Name:%s</th></tr>
	<tr bgcolor=LightGrey align=center><td width=150 id='n2'>Name</td><td width=200 ><b>Item</td>
	<td width=100 ><b>Qty</td><td width=100 ><b>Rate</td><td width=100 ><b>Amount</td></tr>
	""" %(d,tbl,order_id,wtr)
	a=''
	m=frappe.db.sql("""select name,item,quantity,rate,amount from `tabHotelorder` where order_id=%s and order_status='Completed'""",(order_id))
	l=len(m)
	t_amt=0
	for i in range(0, l):
		html_str="""
		<tr align=center id='n1'><td id='n4'>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>""" %(m[i][0],m[i][1],m[i][2],m[i][3],m[i][4])
		a=a+html_str
		t_amt=t_amt+m[i][4]
	ttl_str="""
	<tr align=center id='n1'><td></td><td>Total</td><td>%s</td><td>%s</td><td>%s</td></table></div>""" %('','',t_amt)
	return(str11+a+ttl_str,l)

@frappe.whitelist()
def get_room():
	q=frappe.db.sql("""select room_no from `tabBooking` where room_status='Allocated' and flag=1""")
	return (q)

@frappe.whitelist()
def get_customer(room):
	q=frappe.db.sql("""select customer_name from `tabBooking` where room_no=%s and flag=1""",(room))
	if q:
		return (q[0][0])
	else:
		return 0