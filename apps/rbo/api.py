import frappe

def boot_session(bootinfo):
    bootinfo.app_name = 'Ritam Bharat OS'
    bootinfo.app_title = 'Ritam Bharat OS'
    bootinfo.product_name = 'Ritam Bharat OS'
    bootinfo.product_version = '1.0.0'
    bootinfo.system_name = 'Ritam Bharat OS'
    if hasattr(bootinfo, 'version'):
        bootinfo.version = '1.0.0'
    if hasattr(bootinfo, 'system_settings') and bootinfo.system_settings:
        bootinfo.system_settings.app_name = 'Ritam Bharat OS'

def before_email_send(doc, method):
    if doc and hasattr(doc, 'message') and doc.message:
        doc.message = doc.message.replace('Sent via ERPNext', 'Sent via Ritam Bharat OS')
        doc.message = doc.message.replace('ERPNext', 'Ritam Bharat OS')
        doc.message = doc.message.replace('erpnext.com', 'ritambharat.com')

def after_migrate():
    ss = frappe.get_single('System Settings')
    ss.app_name = 'Ritam Bharat OS'
    ss.save(ignore_permissions=True)
    ws = frappe.get_single('Website Settings')
    ws.app_name = 'Ritam Bharat OS'
    ws.brand_html = '<img src="/assets/rbo/images/logo.png" style="max-height:28px;margin-right:8px;"><span style="font-weight:600;color:#fff;font-size:15px;">Ritam Bharat OS</span>'
    ws.website_theme = 'Ritam Bharat Theme'
    ws.app_logo = '/assets/rbo/images/logo.png'
    ws.app_icon_url = '/assets/rbo/images/logo.png'
    ws.favicon = '/assets/rbo/images/logo.png'
    ws.splash_image = '/assets/rbo/images/logo.png'
    ws.save(ignore_permissions=True)
    ss.app_logo = '/assets/rbo/images/logo.png'
    ss.app_icon_url = '/assets/rbo/images/logo.png'
    ss.save(ignore_permissions=True)
    frappe.db.commit()
