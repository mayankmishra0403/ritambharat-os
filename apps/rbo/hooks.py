app_name = "rbo"
app_title = "Ritam Bharat OS"
app_publisher = "Ritam Bharat"
app_description = "Ritam Bharat OS - Restaurant & Banquet Management"
app_email = "support@ritambharat.com"
app_license = "mit"

app_include_css = "/assets/rbo/css/rbo.css"
app_include_js = "/assets/rbo/js/rbo.js"

web_include_css = "/assets/rbo/css/rbo.css"
web_include_js = "/assets/rbo/js/rbo.js"

app_logo_url = "/assets/rbo/images/logo.png"
app_icon_url = "/assets/rbo/images/logo.png"
favicon_url = "/assets/rbo/images/logo.png"

boot_session = "rbo.api.boot_session"

doc_events = {
    "Email Queue": {
        "before_send": "rbo.api.before_email_send"
    }
}

after_migrate = ["rbo.api.after_migrate"]

website_theme_scss = "rbo/public/scss/website"

override_website_settings = "rbo.api.override_website_settings"
