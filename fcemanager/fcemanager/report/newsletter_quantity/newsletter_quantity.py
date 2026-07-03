import frappe


# =============================================================================
# region REPORT
# =============================================================================


def execute(filters=None):
	columns = [
		{
			"label": "Email Group",
			"fieldname": "email_group",
			"fieldtype": "Link",
			"options": "Email Group",
			"width": 260,
		},
		{
			"label": "Total Subscribers",
			"fieldname": "total_subscribers",
			"fieldtype": "Int",
			"width": 160,
		},
	]
	data = frappe.db.sql(
		"""
		select
			email_group,
			count(*) as total_subscribers
		from `tabEmail Group Member`
		where ifnull(unsubscribed, 0) = 0
		group by email_group
		order by total_subscribers desc, email_group asc
		""",
		as_dict=True,
	)
	return columns, data


# endregion REPORT
