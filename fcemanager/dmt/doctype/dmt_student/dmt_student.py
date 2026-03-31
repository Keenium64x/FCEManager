# Copyright (c) 2026, Keenan Solomon and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class DMTStudent(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		adress: DF.Data | None
		asd: DF.Data | None
		country: DF.Data | None
		country_of_residence: DF.Link | None
		data_bpms: DF.Data | None
		email_adress: DF.Data | None
		name1: DF.Data | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		phone_number: DF.Data | None
	# end: auto-generated types

	pass
