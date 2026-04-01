# Copyright (c) 2026, Keenan Solomon and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from frappe.utils import get_datetime

class DMTGroup(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from fcemanager.dmt.doctype.dmt_student.dmt_student import DMTStudent
		from frappe.types import DF

		dmt_period: DF.Link | None
		students: DF.Table[DMTStudent]
	# end: auto-generated types

	def autoname(self):
		self.name = self.dmt_period.split(" ")[0] + " " + self.dmt_period.split(" ")[1] + " Group"

