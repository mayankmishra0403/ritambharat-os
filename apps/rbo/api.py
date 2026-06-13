import frappe
from frappe import _

GST_RATES = {
    "GST 5%": {"cgst": 2.5, "sgst": 2.5, "igst": 5.0},
    "GST 12%": {"cgst": 6.0, "sgst": 6.0, "igst": 12.0},
    "GST 18%": {"cgst": 9.0, "sgst": 9.0, "igst": 18.0},
    "GST 28%": {"cgst": 14.0, "sgst": 14.0, "igst": 28.0},
}

def boot_session(bootinfo):
    try:
        bootinfo.app_name = 'Ritam Bharat OS'
        bootinfo.app_title = 'Ritam Bharat OS'
        bootinfo.product_name = 'Ritam Bharat OS'
        bootinfo.product_version = '1.0.0'
        bootinfo.system_name = 'Ritam Bharat OS'
        bootinfo.app_logo = '/assets/rbo/images/logo.png'
        bootinfo.app_logo_url = '/assets/rbo/images/logo.png'
        bootinfo.favicon = '/assets/rbo/images/logo.png'
        bootinfo.brand_html = '<img src="/assets/rbo/images/logo.png" style="max-height:28px;margin-right:8px;"><span style="font-weight:600;color:#fff;font-size:15px;">Ritam Bharat OS</span>'
        bootinfo.brand_logo = '/assets/rbo/images/logo.png'
        if hasattr(bootinfo, 'version'):
            bootinfo.version = '1.0.0'
        if hasattr(bootinfo, 'system_settings') and bootinfo.system_settings:
            bootinfo.system_settings.app_name = 'Ritam Bharat OS'
            bootinfo.system_settings.app_logo = '/assets/rbo/images/logo.png'
    except Exception:
        frappe.log_error(frappe.get_traceback(), 'rbo.boot_session')

def before_email_send(doc, method):
    if doc and hasattr(doc, 'message') and doc.message:
        doc.message = doc.message.replace('Sent via ERPNext', 'Sent via Ritam Bharat OS')
        doc.message = doc.message.replace('ERPNext', 'Ritam Bharat OS')
        doc.message = doc.message.replace('erpnext.com', 'ritambharat.com')

def after_migrate():
    try:
        frappe.db.set_value("System Settings", "System Settings", "app_name", "Ritam Bharat OS")
        frappe.db.set_value("System Settings", "System Settings", "app_logo", "/assets/rbo/images/logo.png")
    except Exception:
        frappe.log_error(frappe.get_traceback(), 'rbo.after_migrate.ss')

    try:
        frappe.db.set_value("Website Settings", "Website Settings", "app_name", "Ritam Bharat OS")
        frappe.db.set_value("Website Settings", "Website Settings", "brand_html", '<img src="/assets/rbo/images/logo.png" style="max-height:28px;margin-right:8px;"><span style="font-weight:600;color:#fff;font-size:15px;">Ritam Bharat OS</span>')
        frappe.db.set_value("Website Settings", "Website Settings", "app_logo", "/assets/rbo/images/logo.png")
        frappe.db.set_value("Website Settings", "Website Settings", "favicon", "/assets/rbo/images/logo.png")
        frappe.db.set_value("Website Settings", "Website Settings", "splash_image", "/assets/rbo/images/logo.png")
    except Exception:
        frappe.log_error(frappe.get_traceback(), 'rbo.after_migrate.ws')

    try:
        frappe.db.delete("Property Setter", {
            "property": "mandatory_depends_on",
            "value": ""
        })
    except Exception:
        frappe.log_error(frappe.get_traceback(), 'rbo.after_migrate.ps')
    _create_custom_fields()
    _setup_gst_templates()
    _create_print_formats()
    frappe.db.commit()


def _setup_gst_templates():
    company = frappe.db.get_single_value("Global Defaults", "default_company")
    if not company:
        return

    cgst_account = "Output Tax CGST - R"
    sgst_account = "Output Tax SGST - R"
    igst_account = "Output Tax IGST - R"

    if not frappe.db.exists("Account", cgst_account):
        return

    for label, rates in GST_RATES.items():
        _create_template(company, f"{label} (In-state)", [
            {"account_head": cgst_account, "rate": rates["cgst"], "description": f"CGST @ {rates['cgst']}%"},
            {"account_head": sgst_account, "rate": rates["sgst"], "description": f"SGST @ {rates['sgst']}%"},
        ])
        _create_template(company, f"{label} (Out-state)", [
            {"account_head": igst_account, "rate": rates["igst"], "description": f"IGST @ {rates['igst']}%"},
        ])


def _create_template(company, template_name, taxes):
    company_abbr = frappe.db.get_value("Company", company, "abbr")
    full_name = f"{template_name} - {company_abbr}" if company_abbr else template_name
    if frappe.db.exists("Sales Taxes and Charges Template", full_name):
        return
    try:
        doc = frappe.get_doc({
            "doctype": "Sales Taxes and Charges Template",
            "title": template_name,
            "company": company,
            "taxes": [
                {
                    "charge_type": "On Net Total",
                    "account_head": t["account_head"],
                    "rate": t["rate"],
                    "description": t["description"],
                }
                for t in taxes
            ],
        })
        doc.insert(ignore_permissions=True)
    except Exception:
        pass


def _create_custom_fields():
    fields = [
        ("Customer", "gstin", "GSTIN", "Data", "tax_id"),
        ("Customer", "gst_category", "GST Category",
         "Select", "gstin",
         "\nRegistered Regular\nRegistered Composition\nUnregistered\nSEZ\nOverseas\nConsumer\nTax Deductor\nTax Collector\nUIN Holders"),
        ("Company", "gstin", "GSTIN/UIN", "Data", "company_name"),
        ("Company", "pan", "PAN", "Data", "gstin"),
        ("Item", "gst_hsn_code", "HSN/SAC Code", "Data", "item_code"),
    ]
    for dt, fn, label, ftype, after, *opts in fields:
        if frappe.db.exists("Custom Field", {"dt": dt, "fieldname": fn}):
            continue
        frappe.get_doc({
            "doctype": "Custom Field",
            "dt": dt,
            "fieldname": fn,
            "label": label,
            "fieldtype": ftype,
            "insert_after": after,
            "options": opts[0] if opts else None,
        }).insert(ignore_permissions=True)


def _create_print_formats():
    pf_name = "GST Tax Invoice"
    if frappe.db.exists("Print Format", pf_name):
        return

    import os
    template_path = os.path.join(frappe.get_app_path("rbo"), "print_format", "gst_tax_invoice", "gst_tax_invoice.html")
    if not os.path.exists(template_path):
        frappe.log_error(f"Print format template not found at {template_path}", "rbo.print_format")
        return
    with open(template_path) as f:
        html = f.read()

    doc = frappe.get_doc({
        "doctype": "Print Format",
        "name": pf_name,
        "doc_type": "Sales Invoice",
        "html": html,
        "standard": "No",
        "custom_format": 1,
        "module": "Selling",
    })
    doc.insert(ignore_permissions=True)
