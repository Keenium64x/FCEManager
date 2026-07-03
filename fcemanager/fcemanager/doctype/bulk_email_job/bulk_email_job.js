frappe.ui.form.on("Bulk Email Job", {

    refresh(frm) {
        _build_filter_ui(frm);
        _add_buttons(frm);
    },

    source_doctype(frm) {
        frm.set_value("email_field", "");
        frm.set_value("filters", "{}");
        frm._filter_group = null;
        _build_filter_ui(frm);
        _auto_set_email_field(frm);
    },

    email_type(frm) {
        // depends_on handles visibility — nothing needed here
    },
});


function _auto_set_email_field(frm) {
    if (!frm.doc.source_doctype) return;

    frappe.model.with_doctype(frm.doc.source_doctype, () => {
        const meta = frappe.get_meta(frm.doc.source_doctype);

        const email_fields = meta.fields.filter(f => {
            if (f.fieldtype !== "Data") return false;
            const name = (f.fieldname || "").toLowerCase();
            const label = (f.label || "").toLowerCase();
            const opts = (f.options || "").toLowerCase();
            return (
                opts === "email" ||
                name === "email" ||
                name.includes("email") ||
                label === "email" ||
                label.includes("email")
            );
        });

        if (email_fields.length === 0) {
            // nothing matched — let user type manually
            frm.set_df_property("email_field", "fieldtype", "Data");
            frm.set_df_property("email_field", "options", "");
            frappe.show_alert({
                message: `No email field found in "${frm.doc.source_doctype}" — type the fieldname manually`,
                indicator: "orange",
            });
            return;
        }

        const options = email_fields.map(f => f.fieldname).join("\n");
        frm.set_df_property("email_field", "options", options);
        frm.set_df_property("email_field", "fieldtype", "Select");

        if (email_fields.length === 1) {
            frm.set_value("email_field", email_fields[0].fieldname);
            frappe.show_alert({
                message: `Email field auto-set → "${email_fields[0].fieldname}"`,
                indicator: "green",
            });
        } else {
            frappe.show_alert({
                message: `${email_fields.length} email fields found — pick one`,
                indicator: "blue",
            });
        }
    });
}


function _build_filter_ui(frm) {
    if (!frm.doc.source_doctype) return;
    if (frm._filter_group) return;

    const field = frm.get_field("filters");
    field.$wrapper.find(".control-input").hide();

    const $container = $('<div class="filter-group-container" style="margin-top:8px"></div>')
        .appendTo(field.$wrapper);

    frappe.model.with_doctype(frm.doc.source_doctype, () => {
        frm._filter_group = new frappe.ui.FilterGroup({
            parent: $container,
            doctype: frm.doc.source_doctype,
            on_change: () => {
                const filters = frm._filter_group.get_filters();
                const filter_dict = {};
                filters.forEach(([, f, op, val]) => {
                    filter_dict[f] = op === "=" ? val : [op, val];
                });
                frm.set_value("filters", JSON.stringify(filter_dict));
            },
        });

        // restore saved filters
        const saved = frappe.parse_json(frm.doc.filters || "{}");
        if (Object.keys(saved).length) {
            const restored = Object.entries(saved).map(([f, v]) =>
                Array.isArray(v)
                    ? [frm.doc.source_doctype, f, v[0], v[1]]
                    : [frm.doc.source_doctype, f, "=", v]
            );
            frm._filter_group.add_filters_to_filter_group(restored);
        }
    });
}


function _add_buttons(frm) {
    if (frm.is_new()) return;

    frm.add_custom_button("Preview Recipients", () => {
        frm.call("preview_recipients").then(r => {
            const { count, sample } = r.message;
            const rows = sample
                .map(x => `<li>${x[frm.doc.email_field] || x.name}</li>`)
                .join("");
            frappe.msgprint({
                title: `${count} recipient(s) match filters`,
                message: `<ul>${rows}</ul>${count > 10 ? `<i>...and ${count - 10} more</i>` : ""}`,
                indicator: count > 0 ? "green" : "orange",
            });
        });
    });

    if (frm.doc.status !== "Queued") {
        frm.add_custom_button("Send", () => {
            frappe.confirm(
                "Queue emails to all matching recipients?",
                () => {
                    frm.call("enqueue_send")
                        .then(r => {
                            frappe.show_alert({
                                message: `${r.message.queued} emails queued successfully`,
                                indicator: "green",
                            });
                            frm.reload_doc();
                        })
                        .catch(() => {
                            // frappe.throw messages surface automatically
                            frm.reload_doc();
                        });
                }
            );
        }, "Actions");
    }
}