import frappe
from frappe.model.document import Document
from frappe.utils import get_datetime, getdate, add_to_date, today, date_diff

class DMTPeriod(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		dmt_type: DF.Literal["Standard", "Condense", "Extended", "Advance"]
		duration: DF.Duration | None
		end_date: DF.Date
		start_date: DF.Date
	# end: auto-generated types

	def autoname(self):
		if not self.start_date or not self.end_date:
			frappe.throw("Start Date and End Date are mandatory for naming")

		start_date = get_datetime(self.start_date)
		year = start_date.year

		sd = getdate(self.start_date)
		ed = getdate(self.end_date)

		start_month = sd.strftime("%B")   # Full month name → August
		end_month = ed.strftime("%B")     # Full month name → September

		self.name = f"{year} {start_month} {sd.day} to {end_month} {ed.day}"

	def validate(self):
		start = get_datetime(self.start_date)
		end = get_datetime(self.end_date)

		self.duration = (end - start).total_seconds()