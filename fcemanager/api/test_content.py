"""Integration coverage for safe website draft and publication behavior."""

import json

import frappe
from frappe.tests import IntegrationTestCase

from fcemanager.api.content import get_page_content, publish_page_content, save_draft
from fcemanager.website.content_schema import PAGE_SCHEMAS, get_defaults


# =============================================================================
# region WEBSITE CONTENT WORKFLOW TESTS
# =============================================================================


class IntegrationTestWebsiteContentWorkflow(IntegrationTestCase):
	def setUp(self) -> None:
		frappe.set_user("Administrator")

	def test_unchanged_content_does_not_create_a_false_draft(self) -> None:
		document = frappe.get_doc("FCE Website Content", "home")
		result = save_draft("home", document.published_json)

		self.assertFalse(result["has_unpublished_changes"])

	def test_untouched_records_match_approved_defaults(self) -> None:
		for page_key in PAGE_SCHEMAS:
			document = frappe.get_doc("FCE Website Content", page_key)
			self.assertEqual(json.loads(document.published_json), get_defaults(page_key))

	def test_draft_is_not_public_until_published(self) -> None:
		document = frappe.get_doc("FCE Website Content", "home")
		original_draft = document.draft_json
		original_published = document.published_json
		original_has_changes = document.has_unpublished_changes
		original_version = document.published_version
		original_published_at = document.published_at
		original_published_by = document.published_by
		values = json.loads(original_draft)
		values["hero.kicker"] = "Draft-only editor test"

		try:
			save_draft("home", json.dumps(values))
			frappe.set_user("Guest")
			public_result = get_page_content("/", 0)
			preview_as_guest = get_page_content("/", 1)

			self.assertNotEqual(public_result["values"]["hero.kicker"], "Draft-only editor test")
			self.assertEqual(preview_as_guest["mode"], "published")

			frappe.set_user("Administrator")
			preview_result = get_page_content("/", 1)
			self.assertEqual(preview_result["values"]["hero.kicker"], "Draft-only editor test")

			publish_page_content("home")
			frappe.set_user("Guest")
			self.assertEqual(get_page_content("/", 0)["values"]["hero.kicker"], "Draft-only editor test")
		finally:
			frappe.set_user("Administrator")
			document.reload()
			document.draft_json = original_draft
			document.published_json = original_published
			document.has_unpublished_changes = original_has_changes
			document.published_version = original_version
			document.published_at = original_published_at
			document.published_by = original_published_by
			document.save(ignore_permissions=True)


# endregion WEBSITE CONTENT WORKFLOW TESTS
