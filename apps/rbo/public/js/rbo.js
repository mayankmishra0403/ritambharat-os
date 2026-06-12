$(document).ready(function() {
    setTimeout(function() {
        document.title = document.title.replace(/ERPNext/g, 'Ritam Bharat OS');
        document.title = document.title.replace(/Frappe/g, 'Ritam Bharat OS');
        jQuery("a[href*='erpnext.com'], a[href*='frappe.io'], a[href*='frappecloud']").hide();
        var observer = new MutationObserver(function() {
            document.title = document.title.replace(/ERPNext/g, 'Ritam Bharat OS');
            document.title = document.title.replace(/Frappe/g, 'Ritam Bharat OS');
        });
        observer.observe(document.querySelector('head title') || document.head, {
            subtree: true, childList: true, characterData: true
        });
    }, 500);
});
