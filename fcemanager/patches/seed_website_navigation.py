"""Seed the first shared FCE navigation without overwriting later edits."""

import frappe


# =============================================================================
# region WEBSITE NAVIGATION SEED
# =============================================================================


INITIAL_ITEMS = [
	("About", "/about"),
	("Training", "/training"),
	("Locations", "/locations"),
	("Get involved", "/get-involved"),
	("Projects", "/projects"),
	("Resources", "/resources"),
	("Contact", "/contact"),
]


def execute() -> None:
	settings = frappe.get_doc("Website Settings")
	if not settings.top_bar_items:
		for label, url in INITIAL_ITEMS:
			settings.append(
				"top_bar_items",
				{"label": label, "url": url, "right": int(label == "Contact")},
			)

	if not settings.call_to_action:
		settings.call_to_action = "Apply for DMT"
		settings.call_to_action_url = "/dmt-application"
	if not settings.brand_html:
		settings.brand_html = (
			'<img src="/assets/fcemanager/fce-website/media/logo.webp" '
			'alt="Foundation for Cross-cultural Education" style="max-height:3rem">'
		)

	settings.save(ignore_permissions=True)
	frappe.clear_cache()


# endregion WEBSITE NAVIGATION SEED
