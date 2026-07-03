frappe.ready(function () {
	const exactLabels = {
		family_feelings_about_training:
			"How does your family feel about your possible training in FCE and the possibility of being involved in cross-cultural discipleship situations?",
	};

	for (const [fieldname, label] of Object.entries(exactLabels)) {
		const field = frappe.web_form.get_field(fieldname);
		if (field?.$wrapper) {
			field.$wrapper.find("label.control-label").first().text(label);
		}
	}
});
