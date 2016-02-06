cur_frm.cscript.mobile_no = function (doc,cdt,cdn)
{
	var num = doc.mobile_no;
	var str=String(num);
	if ((str.length) != 10)
		{ 
			frappe.throw('Enter 10 digit number!');
			cur_frm.set_value('mobile_no','');
		}
}