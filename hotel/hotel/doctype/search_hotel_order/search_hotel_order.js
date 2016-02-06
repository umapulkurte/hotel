cur_frm.cscript.order_id=function(doc,cdt,cdn)
{
	var order_id=doc.order_id;
	frappe.call({
		method:'hotel.hotel.doctype.search_hotel_order.search_hotel_order.get_order_details',
		args:{o:order_id},
		callback:function(r)
		{
			set_field_options('test',r.message)
		}
	})
}