frappe.pages["fce-website-editor"].on_page_load = (wrapper) => {
	frappe.ui.make_app_page({
		parent: wrapper,
		title: __("FCE Website Editor"),
		single_column: true,
	});
	wrapper.fce_editor = new FCEWebsiteEditor(wrapper);
};

frappe.pages["fce-website-editor"].on_page_show = (wrapper) => {
	wrapper.fce_editor?.show_route_page();
};

// =============================================================================
// region GUIDED WEBSITE EDITOR
// =============================================================================

class FCEWebsiteEditor {
	constructor(wrapper) {
		this.wrapper = wrapper;
		this.page = wrapper.page;
		this.currentPageKey = "home";
		this.makeLayout();
		this.loadPage(this.routePageKey());
	}

	makeLayout() {
		this.body = $("<div class='fce-editor'></div>").appendTo(this.page.main);
		this.summary = $("<div class='fce-editor__summary'></div>").appendTo(this.body);
		this.formArea = $("<div class='fce-editor__form'></div>").appendTo(this.body);
		this.page.set_primary_action(__("Save draft"), () => this.saveDraft());
		this.page.add_inner_button(__("Preview draft"), () => this.previewDraft());
		this.page.add_inner_button(__("Publish changes"), () => this.confirmPublish());
		this.page.add_menu_item(__("Discard draft changes"), () => this.confirmDiscard());
		this.page.add_menu_item(__("Edit navigation"), () => frappe.set_route("Form", "Website Settings"));
		this.page.add_menu_item(__("Manage training dates"), () => frappe.set_route("List", "DMT Period"));
		this.page.add_menu_item(__("Manage training locations"), () => frappe.set_route("List", "Training Centre"));
		this.page.add_menu_item(__("Manage additional pages"), () => this.openAdditionalPages());
	}

	openAdditionalPages() {
		if (frappe.boot.versions?.builder) {
			window.open("/builder", "_blank", "noopener");
			return;
		}
		frappe.set_route("List", "Web Page");
	}

	routePageKey() {
		const route = frappe.get_route();
		return route[1] || new URLSearchParams(window.location.search).keys().next().value || "home";
	}

	showRoutePage() {
		const pageKey = this.routePageKey();
		if (pageKey !== this.currentPageKey) this.loadPage(pageKey);
	}

	async loadPage(pageKey) {
		frappe.dom.freeze(__("Loading website content…"));
		try {
			const response = await frappe.call({
				method: "fcemanager.api.content.get_editor_boot",
				args: { page_key: pageKey },
			});
			this.renderEditor(response.message);
		} finally {
			frappe.dom.unfreeze();
		}
	}

	renderEditor(data) {
		this.currentPageKey = data.page_key;
		this.boot = data;
		this.renderPageSelector(data.pages);
		this.renderSummary(data);
		this.renderFields(data);
	}

	renderPageSelector(pages) {
		if (!this.pageSelector) {
			this.pageSelector = this.page.add_field({
				fieldname: "website_page",
				label: __("Page to edit"),
				fieldtype: "Select",
				options: pages.map((page) => ({ label: __(page.label), value: page.value })),
				change: () => this.requestPageChange(this.pageSelector.get_value()),
			});
		}
		this.pageSelector.set_value(this.currentPageKey);
	}

	requestPageChange(pageKey) {
		if (!pageKey || pageKey === this.currentPageKey) return;
		if (!this.fieldGroup?.dirty) {
			frappe.set_route("fce-website-editor", pageKey);
			return;
		}
		frappe.confirm(
			__("You have unsaved changes. Leave this page without saving them?"),
			() => {
				this.fieldGroup.dirty = false;
				frappe.set_route("fce-website-editor", pageKey);
			},
			() => this.pageSelector.set_value(this.currentPageKey),
		);
	}

	renderSummary(data) {
		const status = data.has_unpublished_changes
			? `<span class="indicator-pill orange">${__("Draft changes not published")}</span>`
			: `<span class="indicator-pill green">${__("Public website is up to date")}</span>`;
		this.summary.html(`
			<div>
				<p class="text-muted">${frappe.utils.escape_html(data.description)}</p>
				<div class="fce-editor__status">${status}<span>${__("Published version")} ${data.published_version}</span></div>
			</div>
			<a class="btn btn-default btn-sm" href="${data.route}" target="_blank">${__("Open public page")}</a>
		`);
	}

	renderFields(data) {
		this.formArea.empty();
		const fields = [];
		let previousSection = null;
		data.fields.forEach((definition) => {
			if (definition.section !== previousSection) {
				fields.push({ fieldtype: "Section Break", label: __(definition.section) });
				previousSection = definition.section;
			}
			fields.push({
				fieldname: definition.fieldname,
				label: __(definition.label),
				fieldtype: definition.fieldtype,
				description: __(definition.description || ""),
				make_attachment_public: definition.fieldtype === "Attach Image",
				options: definition.fieldtype === "Attach Image"
					? { allow_toggle_private: false }
					: undefined,
			});
		});
		this.fieldGroup = new frappe.ui.FieldGroup({ fields, body: this.formArea });
		this.fieldGroup.make();
		this.fieldGroup.set_values(data.draft);
		this.fieldGroup.dirty = false;
	}

	async saveDraft(showMessage = true) {
		const values = this.fieldGroup.get_values();
		if (!values) return false;
		const response = await frappe.call({
			method: "fcemanager.api.content.save_draft",
			args: { page_key: this.currentPageKey, values: JSON.stringify(values) },
			freeze: true,
			freeze_message: __("Saving draft…"),
		});
		if (showMessage) frappe.show_alert({ message: __("Draft saved"), indicator: "green" });
		await this.loadPage(this.currentPageKey);
		return response.message;
	}

	async previewDraft() {
		const previewWindow = window.open("about:blank", "fce-website-preview");
		if (!(await this.saveDraft(false))) {
			previewWindow?.close();
			return;
		}
		if (previewWindow) previewWindow.location = `${this.boot.route}?fce_preview=1`;
		else frappe.msgprint(__("Your browser blocked the preview window. Allow popups for this site and try again."));
	}

	confirmPublish() {
		frappe.confirm(
			__("Publish the current draft to everyone visiting this page?"),
			async () => {
				if (!(await this.saveDraft(false))) return;
				await frappe.call({ method: "fcemanager.api.content.publish_page_content", args: { page_key: this.currentPageKey }, freeze: true, freeze_message: __("Publishing…") });
				frappe.show_alert({ message: __("Website changes published"), indicator: "green" });
				this.loadPage(this.currentPageKey);
			},
		);
	}

	confirmDiscard() {
		frappe.confirm(__("Discard all draft changes and return to the published wording?"), async () => {
			await frappe.call({ method: "fcemanager.api.content.discard_draft", args: { page_key: this.currentPageKey }, freeze: true });
			this.loadPage(this.currentPageKey);
		});
	}
}

// endregion GUIDED WEBSITE EDITOR
