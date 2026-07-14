"""Integration coverage for public website chrome data."""

import frappe
from frappe.tests import IntegrationTestCase

from fcemanager.api.website import get_public_site_navigation


# =============================================================================
# region PUBLIC WEBSITE NAVIGATION TESTS
# =============================================================================


class IntegrationTestPublicWebsiteNavigation(IntegrationTestCase):
	def test_returns_ordered_items_children_and_cta(self) -> None:
		settings = frappe.get_doc("Website Settings")
		settings.set("top_bar_items", [])
		settings.append("top_bar_items", {"label": "Explore"})
		settings.append(
			"top_bar_items",
			{"label": "Stories", "url": "/stories", "parent_label": "Explore"},
		)
		settings.append("top_bar_items", {"label": "Contact", "url": "/contact", "right": 1})
		settings.call_to_action = "Apply for DMT"
		settings.call_to_action_url = "/dmt-application"
		settings.save(ignore_permissions=True)

		result = get_public_site_navigation()

		self.assertEqual([item["label"] for item in result["items"]], ["Explore", "Contact"])
		self.assertEqual(result["items"][0]["children"][0]["url"], "/stories")
		self.assertTrue(result["items"][1]["right"])
		self.assertEqual(result["call_to_action"]["url"], "/dmt-application")


# endregion PUBLIC WEBSITE NAVIGATION TESTS
