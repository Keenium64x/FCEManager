function extend_listview_event(doctype, event, callback) {
    if (!frappe.listview_settings[doctype]) {
        frappe.listview_settings[doctype] = {};
    }

    const old_event = frappe.listview_settings[doctype][event];

    frappe.listview_settings[doctype][event] = function (listview) {
        if (old_event) {
            old_event(listview);
        }
        callback(listview);
    };
}

// CHANGE THIS
extend_listview_event("DMT Student", "refresh", function (listview) {
    $(document).ready(function () {

        $('span[data-filter="status,=,Pending"]')
            .removeClass('gray')
            .addClass('orange');

        $('span[data-filter="status,=,Accepted"]')
            .removeClass('gray')
            .addClass('green');

        $('span[data-filter="status,=,Rejected"]')
            .removeClass('gray')
            .addClass('red');

    });
});