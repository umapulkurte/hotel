cur_frm.cscript.onload=function(doc,cdt,cdn)
{
	var g_order_id;
	Date.prototype.yyyymmdd = function() 
	{
   	var yyyy = this.getFullYear().toString();
  	var mm = (this.getMonth()+1).toString(); // getMonth() is zero-based
   	var dd  = this.getDate().toString();
   	return yyyy +'-'+ (mm[1]?mm:"0"+mm[0]) +'-'+ (dd[1]?dd:"0"+dd[0]); // padding
  	};

	d = new Date();
	m=d.yyyymmdd();
	doc.date=m
	frappe.call({
		method:'hotel.hotel.doctype.sale.sale.show_table',
		args:{d:m},
		callback:function(r)
		{
			var doclist=frappe.model.sync(r.message)
			set_field_options('test',doclist[0])
			g_tables=doclist[1]
			cur_frm.set_value('waiter_name',doclist[2])
		}
	})
	frappe.call({
		method:'hotel.hotel.doctype.sale.sale.get_item',
		args:{},
		callback:function(r)
		{
			set_field_options('item',r.message)	
		}
	})
}
var gtotal_amt;
cur_frm.cscript.add_item=function(doc,cdt,cdn)
{
	var o_id=doc.order_id;
	var item=doc.item;
	var qty=doc.quantity;
	var rate1=doc.rate;
	var d=doc.date;
	var t=doc.table_no;
	var w=doc.waiter_name;
	var o_sts=doc.order_status
	var room=doc.select_room
	var customer=doc.customer_name;
	if(doc.is_lodge_client=='')
	{
		alert('Is Lodge Client field can not be blank');
	}
	frappe.call({
		method:'hotel.hotel.doctype.sale.sale.insert_item',
		args:{o:o_id,i:item,q:qty,r:rate1,d:d,tbl:t,w:w,o_sts:o_sts,room:room,customer:customer},
		callback:function(r)
		{
			set_field_options('test1',r.message);
		}
	})
	cur_frm.set_value('item','');
	cur_frm.set_value('quantity','');
	cur_frm.set_value('rate','');
}
cur_frm.cscript.item=function(doc,cdt,cdn)
{
	var item=doc.item;
	frappe.call({
		method:'hotel.hotel.doctype.sale.sale.get_rate',
		args:{item:item},
		callback:function(r)
		{
			var doclist1=frappe.model.sync(r.message);
			cur_frm.set_value('rate',doclist1[0][1])
		}
	})
}
cur_frm.cscript.submit_list=function(doc,cdt,cdn)
{
	var d=doc.date;
	var t=doc.table_no;
	var w=doc.waiter_name;
	var o=doc.order_id;
	var o_sts=doc.order_status;
	frappe.call
	({
		method:'hotel.hotel.doctype.sale.sale.record_submission',
		args:{d:d,t:t,w:w,o:o,o_sts:o_sts},
		callback:function()
		{
			cur_frm.set_value('order_status','Completed')
		}
	})
}
cur_frm.cscript.print_bill=function(doc,cdt,cdn)
{
  
  var d=doc.date;
  var tbl=doc.table_no;
  var wtr=doc.waiter_name;
  var order_id=doc.order_id
  frappe.call({
  	method:'hotel.hotel.doctype.sale.sale.get_div',
  	args:{d:d,tbl:tbl,wtr:wtr,order_id:order_id},
  	callback:function(r)
  	{
  		var doclist=frappe.model.sync(r.message);
  		set_field_options('test1',doclist[0]);
  		var length1=doclist[1];
  		var divToPrint1=document.getElementById('d1');
        var col =1;
        if (isNaN(col) || col == "") 
        	{
        		alert("Invalid Column");
                return;
            }
        col = parseInt(col, 10);
        col = col - 1;
        var tbl = document.getElementById("Tbl1");
         if (tbl != null) 
         {
         	if (col < 0 || col >= tbl.rows.length - 1) 
         	{
			   alert("Invalid Column");
               return;
            }
        	for (var i = 0; i < tbl.rows.length; i++) 
        	{
        		 for (var j = 0; j < tbl.rows[i].cells.length; j++) 
        		 {
                    tbl.rows[i].cells[j].style.display = "";
                     if (j == col)
                     tbl.rows[i].cells[j].style.display = "none";
                  }
            }

         }
  		newWin= window.open("");
  		//newWin.document.write(divToPrint.outerHTML);
  		newWin.document.write(divToPrint1.outerHTML);
 		newWin.print();
  		newWin.close();
 	}
 	
  })
  
}
cur_frm.cscript.is_lodge_client=function(doc,cdt,cdn)
{
	if(doc.is_lodge_client=='Yes')
	{
		cur_frm.toggle_enable('select_room',true);
		cur_frm.set_value('customer_name','');
		frappe.call({
			method:'hotel.hotel.doctype.sale.sale.get_room',
			args:{},
			callback:function(r)
			{
				set_field_options('select_room',r.message);
			}
		})
		cur_frm.cscript.select_room=function(doc,cdt,cdn)
		{
			var room=doc.select_room;
			frappe.call({
				method:'hotel.hotel.doctype.sale.sale.get_customer',
				args:{room:room},
				callback:function(r)
				{
					if(r.message==null)
							{
								cur_frm.set_value('customer_name',0);
							}
							else
							{
								cur_frm.set_value('customer_name',r.message);
							}
				}
			})
		}
	}
	if(doc.is_lodge_client=='No')
	{
		cur_frm.toggle_enable('select_room')
		cur_frm.set_value('select_room',0)
		cur_frm.set_value('customer_name',0)
	}
}
