"""Correct initial defaults without overwriting any staff-authored content."""

import json

import frappe

from fcemanager.website.content_schema import PAGE_SCHEMAS, get_defaults


# =============================================================================
# region UNTOUCHED CONTENT DEFAULT SYNC
# =============================================================================


def execute() -> None:
	for page_key in PAGE_SCHEMAS:
		document = frappe.get_doc("FCE Website Content", page_key)
		if document.published_version != 1 or document.has_unpublished_changes:
			continue
		defaults = json.dumps(get_defaults(page_key), ensure_ascii=False, sort_keys=True)
		document.draft_json = defaults
		document.published_json = defaults
		document.save(ignore_permissions=True)


# endregion UNTOUCHED CONTENT DEFAULT SYNC
