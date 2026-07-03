import json
from pathlib import Path

import frappe


# =============================================================================
# region PRODUCTION NAVIGATION SYNC
# =============================================================================


APP_ROOT = Path(frappe.get_app_path("fcemanager")).parent


def execute():
	sync_desktop_icon("fcemanager/desktop_icon/fcemanager_app.json")
	sync_desktop_icon("fcemanager/desktop_icon/fcemanager.json")
	sync_workspace_sidebar()
	sync_workspace_sidebar_items_on_workspace()
	clear_navigation_cache()


def sync_desktop_icon(relative_path):
	fixture = load_json(relative_path)
	icon = get_or_create_document("Desktop Icon", fixture["name"])
	for fieldname, value in fixture.items():
		if fieldname in {"doctype", "name", "creation", "modified", "modified_by", "owner"}:
			continue
		icon.set(fieldname, value)
	icon.flags.ignore_permissions = True
	icon.flags.ignore_mandatory = True
	icon.save(ignore_version=True)


def sync_workspace_sidebar():
	fixture = load_json("fcemanager/workspace_sidebar/fcemanager.json")
	sidebar = get_or_create_document("Workspace Sidebar", "FCEManager")
	delete_child_rows("Workspace Sidebar", "FCEManager")
	for fieldname in ["app", "header_icon", "module", "module_onboarding", "title"]:
		sidebar.set(fieldname, fixture.get(fieldname))
	sidebar.set("items", [])
	for row in fixture.get("items", []):
		sidebar.append("items", row)
	sidebar.flags.ignore_permissions = True
	sidebar.flags.ignore_mandatory = True
	sidebar.save(ignore_version=True)


def sync_workspace_sidebar_items_on_workspace():
	if not frappe.db.exists("Workspace", "FCEManager"):
		return
	fixture = load_json("fcemanager/workspace_sidebar/fcemanager.json")
	workspace = frappe.get_doc("Workspace", "FCEManager")
	delete_child_rows("Workspace", "FCEManager", exclude_parentfields={"charts", "custom_blocks", "links", "number_cards", "quick_lists", "roles", "shortcuts"})
	workspace.module_onboarding = fixture.get("module_onboarding")
	workspace.set("sidebar_items", [])
	for row in fixture.get("items", []):
		workspace.append("sidebar_items", row)
	workspace.flags.ignore_permissions = True
	workspace.flags.ignore_mandatory = True
	workspace.save(ignore_version=True)


def get_or_create_document(doctype, name):
	if frappe.db.exists(doctype, name):
		return frappe.get_doc(doctype, name)
	document = frappe.new_doc(doctype)
	document.name = name
	return document


def load_json(relative_path):
	return json.loads((APP_ROOT / relative_path).read_text())


def delete_child_rows(doctype, parent, exclude_parentfields=None):
	exclude_parentfields = exclude_parentfields or set()
	for field in frappe.get_meta(doctype).get_table_fields():
		if field.fieldname in exclude_parentfields:
			continue
		frappe.db.delete(field.options, {"parent": parent})


def clear_navigation_cache():
	frappe.clear_cache()
	frappe.cache.delete_key("bootinfo")


# endregion PRODUCTION NAVIGATION SYNC
