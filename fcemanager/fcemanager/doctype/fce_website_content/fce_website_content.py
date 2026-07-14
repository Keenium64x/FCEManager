import json

import frappe
from frappe.model.document import Document

from fcemanager.website.content_schema import get_defaults, validate_content


# =============================================================================
# region FCE WEBSITE CONTENT DOCUMENT
# =============================================================================


class FCEWebsiteContent(Document):
	def autoname(self) -> None:
		self.name = self.page_key

	def validate(self) -> None:
		self.route = self.route or "/"
		self.draft_json = _normalize_json(self.page_key, self.draft_json)
		self.published_json = _normalize_json(self.page_key, self.published_json)


def _normalize_json(page_key: str, raw_value: str | None) -> str:
	values = json.loads(raw_value or "{}")
	return json.dumps(validate_content(page_key, values), ensure_ascii=False, sort_keys=True)


def create_content_document(page_key: str, route: str, label: str) -> FCEWebsiteContent:
	defaults = get_defaults(page_key)
	return frappe.get_doc(
		{
			"doctype": "FCE Website Content",
			"page_key": page_key,
			"page_label": label,
			"route": route,
			"draft_json": json.dumps(defaults, ensure_ascii=False, sort_keys=True),
			"published_json": json.dumps(defaults, ensure_ascii=False, sort_keys=True),
			"published_version": 1,
		}
	)


# endregion FCE WEBSITE CONTENT DOCUMENT
