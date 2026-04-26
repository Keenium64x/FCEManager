# Copyright (c) 2026, Keenan Solomon and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class TrainingIntake(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		period: DF.Link | None
		training_centre: DF.Link | None
	# end: auto-generated types

	def autoname(self):
		self.name = self.period.split(" ")[0] + " " + self.period.split(" ")[1] + " " + self.training_centre + " Intake"
