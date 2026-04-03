# Copyright (c) 2026, Keenan Solomon and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe
from datetime import datetime

class DMTStudent(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from fcemanager.dmt.doctype.dmt_relation.dmt_relation import DMTRelation
		from frappe.types import DF

		application_form: DF.Link | None
		country_of_origin: DF.Data | None
		current_address: DF.Data | None
		current_country: DF.Link | None
		email: DF.Data | None
		first_name: DF.Data | None
		full_name: DF.Data | None
		highest_module_completed: DF.Literal["Module 7", "Module 8", "Module 9"]
		last_name: DF.Data | None
		middle_names: DF.Data | None
		phone: DF.Data | None
		relation: DF.Table[DMTRelation]
		status: DF.Literal["Accepted", "Rejected", "Pending"]
	# end: auto-generated types

