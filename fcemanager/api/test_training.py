"""Integration coverage for the public training catalogue."""

from random import randint

import frappe
from frappe.tests import IntegrationTestCase
from frappe.utils import add_days, today

from fcemanager.api.training import get_public_training_periods


# =============================================================================
# region PUBLIC TRAINING CATALOGUE TESTS
# =============================================================================


class IntegrationTestPublicTrainingCatalogue(IntegrationTestCase):
	def test_returns_future_period_with_normalized_centre(self) -> None:
		start_date = add_days(today(), randint(3000, 6000))
		end_date = add_days(start_date, 69)
		centre_label = f"Website Test Centre {frappe.generate_hash(length=8)}"

		period = frappe.get_doc(
			{
				"doctype": "DMT Period",
				"dmt_type": "Standard",
				"start_date": start_date,
				"end_date": end_date,
			}
		).insert(ignore_permissions=True)
		centre = frappe.get_doc(
			{
				"doctype": "Training Centre",
				"centre": centre_label,
				"adress": "1 Test Road",
			}
		).insert(ignore_permissions=True)
		frappe.get_doc(
			{
				"doctype": "Training Intake",
				"period": period.name,
				"training_centre": centre.name,
			}
		).insert(ignore_permissions=True)

		result = get_public_training_periods()
		published = next(item for item in result["periods"] if item["name"] == period.name)

		self.assertEqual(published["dmt_type"], "Standard")
		self.assertEqual(published["centres"][0]["centre"], centre_label)
		self.assertEqual(published["centres"][0]["address"], "1 Test Road")
		self.assertNotIn("adress", published["centres"][0])

	def test_excludes_expired_periods(self) -> None:
		period = frappe.get_doc(
			{
				"doctype": "DMT Period",
				"dmt_type": "Condense",
				"start_date": add_days(today(), -90),
				"end_date": add_days(today(), -30),
			}
		).insert(ignore_permissions=True)

		period_names = {item["name"] for item in get_public_training_periods()["periods"]}

		self.assertNotIn(period.name, period_names)


# endregion PUBLIC TRAINING CATALOGUE TESTS
