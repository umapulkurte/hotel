from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Documents"),
			"icon": "icon-star",
			"items": [
				{
					"type": "doctype",
					"name": "Sale",
					#"description": _("Assign tables to waiters.")
				},
				{
					"type": "doctype",
					"name": "Search Hotel Order",
					#"description": _("Generate order table wise")
				},
				{
					"type": "doctype",
					"name": "Purchase Item",
					#"description": _("Purchase Item")
				},
				{
					"type": "doctype",
					"name": "Item List",
					#"description": _("Loose Bottels.")
				},
				{
					"type": "doctype",
					"name": "Party",
					#"description": _("Details of each Order id.")
				},
			]
		},
	{
		"label":_("Standard Reports"),
		"icon": "icon-star",
		"items" : [
				{
					"type":"report",
					"name" :"Daily Sale Report",
					"doctype": "Sale",
					"is_query_report": True,
				},
				{
					"type":"report",
					"name" :"Hotel Cash Sheet",
					"doctype": "Sale",
					"is_query_report": True,
				},
		]
	}
]