"""Guest-safe website chrome data shared by Vue and Frappe pages."""

from typing import Any

import frappe
from frappe.website.doctype.website_settings.website_settings import get_items


# =============================================================================
# region PUBLIC WEBSITE NAVIGATION
# =============================================================================


def _serialize_navigation_item(item: frappe._dict) -> dict[str, Any]:
	return {
		"label": item.label,
		"url": item.url or "",
		"open_in_new_tab": bool(item.open_in_new_tab),
		"right": bool(item.right),
		"children": [
			_serialize_navigation_item(child)
			for child in (item.get("child_items") or [])
		],
	}


@frappe.whitelist(allow_guest=True)
def get_public_site_navigation() -> dict[str, Any]:
	"""Return the published website menu and CTA from Website Settings."""
	settings = frappe.get_cached_doc("Website Settings")
	items = [
		_serialize_navigation_item(item)
		for item in get_items("top_bar_items")
		if not item.parent_label
	]

	return {
		"items": items,
		"call_to_action": {
			"label": settings.call_to_action or "",
			"url": settings.call_to_action_url or "",
		},
	}


# endregion PUBLIC WEBSITE NAVIGATION
