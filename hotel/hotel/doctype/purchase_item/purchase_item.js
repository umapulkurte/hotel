cur_frm.cscript.item=function(doc,cdt,cdn)
{
	var d=locals[cdt][cdn];
	var item=d.item;
	frappe.call({
		method:'hotel.hotel.doctype.purchase_item.purchase_item.get_details',
		args:{ item1:item },
		callback:function(r)
		{
			var doclist=frappe.model.sync(r.message);
			d.item_name1=doclist[0][0];
			d.rate=doclist[0][1];
			refresh_field('item_table');
		}
	});
}
cur_frm.cscript.quantity=function(doc,cdt,cdn)
{
	var d=locals[cdt][cdn];
	var rate=d.rate;
	var quantity=d.quantity;
	var amt=(rate*quantity);
	d.amount=amt;
	refresh_field('item_table');
}

cur_frm.cscript.bill=function(doc,cdt,cdn)
{
	var m=doc.item_table;
	var len=m.length;
	var amt=0;
	for(i=0;i<len;i++)
	{
		amt=amt+m[i].amount;
	}
	cur_frm.set_value('net_pay',amt);
	frappe.call({
		method:'hotel.hotel.doctype.purchase_item.purchase_item.get_money_in_words',
		args:{n:amt},
		callback:function(r)
		{
			cur_frm.set_value('net_pay_in_words',r.message)
		}
	})
}