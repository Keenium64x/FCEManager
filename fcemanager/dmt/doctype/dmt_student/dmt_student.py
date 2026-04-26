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

		amended_from: DF.Link | None
		application_form: DF.Link | None
		country_of_origin: DF.Link | None
		current_address: DF.Data | None
		current_country: DF.Link | None
		email: DF.Data | None
		first_name: DF.Data | None
		full_name: DF.Data | None
		highest_module_completed: DF.Literal["", "Module 7", "Module 8", "Module 9"]
		last_name: DF.Data | None
		last_time_visited: DF.Date | None
		middle_names: DF.Data | None
		note: DF.LongText | None
		payment: DF.Literal["Paid", "Pending", "Custom"]
		phone: DF.Data | None
		relation: DF.Table[DMTRelation]
		status: DF.Literal["Pending", "Accepted", "Rejected"]
		whatsapp_community: DF.Literal["Member", "Invited", "Pending"]
	# end: auto-generated types

	def validate(self):
		self.full_name = " ".join(
			part.strip() for part in [self.first_name, self.middle_names, self.last_name] if part
		)


	def autoname(self):
		parts = [self.first_name, self.middle_names, self.last_name]
		full_name = "-".join(p.strip().replace(" ", "-") for p in parts if p)

		prefix = f"DMT-{full_name}-"

		# count existing records with same prefix
		count = frappe.db.count(self.doctype, {
			"name": ["like", f"{prefix}%"]
		})

		# next number (resets automatically if all deleted)
		number = count + 1

		self.name = f"{prefix}{str(number).zfill(2)}"