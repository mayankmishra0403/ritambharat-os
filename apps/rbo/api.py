import frappe

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
        frappe.db.set_value("Website Settings", "Website Settings", "website_theme", "Ritam Bharat Theme")
        frappe.db.set_value("Website Settings", "Website Settings", "app_logo", "/assets/rbo/images/logo.png")
        frappe.db.set_value("Website Settings", "Website Settings", "favicon", "/assets/rbo/images/logo.png")
        frappe.db.set_value("Website Settings", "Website Settings", "splash_image", "/assets/rbo/images/logo.png")
    except Exception:
        frappe.log_error(frappe.get_traceback(), 'rbo.after_migrate.ws')

    frappe.db.commit()
