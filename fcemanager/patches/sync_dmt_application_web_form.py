import json
from pathlib import Path

import frappe


# =============================================================================
# region DMT APPLICATION WEB FORM SYNC
# =============================================================================


APP_ROOT = Path(frappe.get_app_path("fcemanager")).parent
FIXTURE_PATH = APP_ROOT / "fcemanager/dmt/web_form/dmt_application/dmt_application.json"


def execute():
	fixture = json.loads(FIXTURE_PATH.read_text())
	for fieldname, value in fixture.items():
		if fieldname in {"doctype", "name", "creation", "modified", "modified_by", "owner", "web_form_fields", "list_columns"}:
			continue
		frappe.db.set_value("Web Form", "dmt-application", fieldname, value, update_modified=False)
	frappe.db.delete("Web Form Field", {"parent": "dmt-application"})
	for idx, row in enumerate(fixture.get("web_form_fields", []), start=1):
		doc = frappe.new_doc("Web Form Field")
		doc.update(row)
		doc.parent = "dmt-application"
		doc.parenttype = "Web Form"
		doc.parentfield = "web_form_fields"
		doc.idx = idx
		doc.insert(ignore_permissions=True)
	frappe.clear_cache()


# endregion DMT APPLICATION WEB FORM SYNC
