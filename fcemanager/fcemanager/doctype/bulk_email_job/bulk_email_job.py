import frappe
from frappe.model.document import Document
from frappe.utils.background_jobs import enqueue


class BulkEmailJob(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        email_field: DF.Data | None
        email_template: DF.Link | None
        email_type: DF.Literal["Personal", "Template"]
        filters: DF.JSON | None
        mailing_name: DF.Data | None
        message: DF.TextEditor | None
        recipient_count: DF.Int
        sender: DF.Link | None
        source_doctype: DF.Link | None
        status: DF.Literal["Draft", "Queued", "Sent", "Failed"]
        subject: DF.Data | None
    # end: auto-generated types

    @frappe.whitelist()
    def preview_recipients(self):
        recipients = self._get_recipients()
        # don't db_set — just return, let JS show count
        return {
            "count": len(recipients),
            "sample": recipients[:10],
        }

    @frappe.whitelist()
    def enqueue_send(self):
        # check outgoing email account exists
        if not frappe.db.exists("Email Account", {"enable_outgoing": 1, "default_outgoing": 1}):
            frappe.throw(
                "No default outgoing Email Account configured. "
                "Go to Email Account and set one as default outgoing before sending.",
                title="Email Not Configured",
            )

        recipients = self._get_recipients()
        if not recipients:
            frappe.throw("No recipients match the current filters.")

        self.db_set("status", "Queued")
        enqueue(
            "fcemanager.fcemanager.doctype.bulk_email_job.bulk_email_job.execute_send",
            queue="long",
            timeout=3600,
            job_name=f"bulk_email_{self.name}",
            doc_name=self.name,
        )
        return {"queued": len(recipients)}

    def _get_recipients(self):
        if not self.source_doctype or not self.email_field:
            frappe.throw("Set Source Doctype and Email Field first.")

        filters = frappe.parse_json(self.filters or "{}")
        records = frappe.get_all(
            self.source_doctype,
            filters=filters,
            fields=["name", self.email_field],
            ignore_permissions=True,
        )
        return [r for r in records if r.get(self.email_field)]


def execute_send(doc_name):
    doc = frappe.get_doc("Bulk Email Job", doc_name)
    recipients = doc._get_recipients()

    try:
        for r in recipients:
            email = r[doc.email_field]
            subject, message = _render_content(doc, r)
            frappe.sendmail(
                recipients=[email],
                subject=subject,
                message=message,
                # removed sender entirely — uses default outgoing account
                reference_doctype="Bulk Email Job",
                reference_name=doc_name,
                delayed=True,
                queue_separately=True,
            )

        doc.db_set("status", "Draft")

    except Exception:
        doc.db_set("status", "Failed")
        frappe.log_error(frappe.get_traceback(), f"Bulk Email Job {doc_name}")
        raise


def _render_content(doc, record):
    if doc.email_type == "Template":
        template = frappe.get_doc("Email Template", doc.email_template)
        ctx = frappe.get_doc(doc.source_doctype, record["name"]).as_dict()
        return (
            frappe.render_template(template.subject, ctx),
            frappe.render_template(template.response_, ctx),
        )
    return doc.subject, doc.message