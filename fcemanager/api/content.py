"""Website content editing, preview and publication API."""

import json
from typing import Any

import frappe
from frappe.utils import cint, now_datetime

from fcemanager.website.content_schema import PAGE_SCHEMAS, ROUTE_TO_PAGE, get_defaults, get_page_schema, validate_content


# =============================================================================
# region WEBSITE CONTENT ACCESS
# =============================================================================


EDITOR_ROLES = {"Website Manager", "System Manager"}


def can_edit_website() -> bool:
	return frappe.session.user != "Guest" and bool(EDITOR_ROLES.intersection(frappe.get_roles()))


def require_website_editor() -> None:
	if not can_edit_website():
		frappe.throw("You need the Website Manager role to edit the FCE website.", frappe.PermissionError)


def _load_content_document(page_key: str):
	if page_key not in PAGE_SCHEMAS:
		frappe.throw("Unknown FCE website page.", frappe.DoesNotExistError)
	return frappe.get_cached_doc("FCE Website Content", page_key)


def _load_values(raw_value: str | None, page_key: str) -> dict[str, str]:
	values = get_defaults(page_key)
	values.update(validate_content(page_key, json.loads(raw_value or "{}")))
	return values


# endregion WEBSITE CONTENT ACCESS


# =============================================================================
# region PUBLIC AND PREVIEW DELIVERY
# =============================================================================


@frappe.whitelist(allow_guest=True)
def get_page_content(route: str = "/", preview: int | str = 0) -> dict[str, Any]:
	"""Return published content, or an authenticated editor's draft preview."""
	page_key = ROUTE_TO_PAGE.get(route.rstrip("/") or "/")
	if not page_key:
		return {"page_key": None, "values": {}, "can_edit": can_edit_website()}

	document = _load_content_document(page_key)
	preview_allowed = bool(cint(preview)) and can_edit_website()
	raw_values = document.draft_json if preview_allowed else document.published_json

	return {
		"page_key": page_key,
		"values": _load_values(raw_values, page_key),
		"mode": "draft" if preview_allowed else "published",
		"can_edit": can_edit_website(),
		"editor_url": f"/app/fce-website-editor/{page_key}",
		"has_unpublished_changes": bool(document.has_unpublished_changes),
		"published_version": document.published_version,
	}


@frappe.whitelist(allow_guest=True)
def get_global_content(preview: int | str = 0) -> dict[str, Any]:
	document = _load_content_document("global")
	preview_allowed = bool(cint(preview)) and can_edit_website()
	raw_values = document.draft_json if preview_allowed else document.published_json
	return {"values": _load_values(raw_values, "global"), "mode": "draft" if preview_allowed else "published"}


# endregion PUBLIC AND PREVIEW DELIVERY


# =============================================================================
# region EDITOR OPERATIONS
# =============================================================================


@frappe.whitelist()
def get_editor_boot(page_key: str = "home") -> dict[str, Any]:
	require_website_editor()
	document = _load_content_document(page_key)
	schema = get_page_schema(page_key)
	return {
		"pages": [
			{"value": key, "label": value["label"], "route": value["route"]}
			for key, value in PAGE_SCHEMAS.items()
		],
		"page_key": page_key,
		"label": schema["label"],
		"route": schema["route"],
		"description": schema["description"],
		"fields": schema["fields"],
		"draft": _load_values(document.draft_json, page_key),
		"has_unpublished_changes": bool(document.has_unpublished_changes),
		"published_version": document.published_version,
		"published_at": document.published_at,
		"published_by": document.published_by,
	}


@frappe.whitelist()
def save_draft(page_key: str, values: str) -> dict[str, Any]:
	require_website_editor()
	document = frappe.get_doc("FCE Website Content", page_key)
	clean_values = get_defaults(page_key)
	clean_values.update(validate_content(page_key, json.loads(values or "{}")))
	document.draft_json = json.dumps(clean_values, ensure_ascii=False, sort_keys=True)
	document.has_unpublished_changes = int(document.draft_json != document.published_json)
	document.save(ignore_permissions=True)
	return {"saved": True, "has_unpublished_changes": bool(document.has_unpublished_changes)}


@frappe.whitelist()
def publish_page_content(page_key: str) -> dict[str, Any]:
	"""Atomically promote the current validated draft to the public website."""
	require_website_editor()
	document = frappe.get_doc("FCE Website Content", page_key)
	document.published_json = document.draft_json
	document.has_unpublished_changes = 0
	document.published_version = cint(document.published_version) + 1
	document.published_at = now_datetime()
	document.published_by = frappe.session.user
	document.save(ignore_permissions=True)
	frappe.clear_cache()
	return {
		"published": True,
		"published_version": document.published_version,
		"published_at": document.published_at,
	}


@frappe.whitelist()
def discard_draft(page_key: str) -> dict[str, Any]:
	require_website_editor()
	document = frappe.get_doc("FCE Website Content", page_key)
	document.draft_json = document.published_json
	document.has_unpublished_changes = 0
	document.save(ignore_permissions=True)
	return {"discarded": True}


# endregion EDITOR OPERATIONS
