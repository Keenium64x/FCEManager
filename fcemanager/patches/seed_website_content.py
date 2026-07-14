"""Create neutral website content records from the approved source defaults."""

import frappe

from fcemanager.fcemanager.doctype.fce_website_content.fce_website_content import create_content_document
from fcemanager.website.content_schema import PAGE_SCHEMAS


# =============================================================================
# region WEBSITE CONTENT SEED
# =============================================================================


def execute() -> None:
	for page_key, schema in PAGE_SCHEMAS.items():
		if frappe.db.exists("FCE Website Content", page_key):
			continue
		document = create_content_document(page_key, schema["route"], schema["label"])
		document.insert(ignore_permissions=True)


# endregion WEBSITE CONTENT SEED
