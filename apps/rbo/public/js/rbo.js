function rboRebrand() {
  var brand = 'Ritam Bharat OS';

  var replaceText = function(node, from, to) {
    if (node && node.nodeType === 3) {
      node.textContent = node.textContent.replace(new RegExp(from, 'g'), to);
    } else if (node && node.childNodes) {
      for (var i = 0; i < node.childNodes.length; i++) {
        replaceText(node.childNodes[i], from, to);
      }
    }
  };

  var replaceDOM = function() {
    document.title = document.title.replace(/ERPNext/g, brand);
    document.title = document.title.replace(/Frappe/g, brand);

    document.querySelectorAll('*').forEach(function(el) {
      if (el.childNodes && el.childNodes.length === 1 && el.childNodes[0].nodeType === 3) {
        if (el.textContent.trim() === 'Starting Frappe' || el.textContent.trim() === 'Starting Frappe ...') {
          el.textContent = 'Starting ' + brand + ' ...';
        }
      }
    });
  };

  var delayedReplace = function() {
    setTimeout(function() {
      replaceDOM();
    }, 100);
    setTimeout(function() {
      replaceDOM();
      document.querySelectorAll('[data-desk-sidebar] a, .list-row-col, .page-title, .section-title, .form-section-head, .control-label, .module-heading, h1, h2, h3, h4, h5, h6, span, li, td, th, label, .dropdown-menu a, .navbar-brand').forEach(function(el) {
        if (el && el.innerHTML) {
          el.innerHTML = el.innerHTML.replace(/ERPNext Settings/g, 'Settings');
          el.innerHTML = el.innerHTML.replace(/Frappe Support/g, 'Help & Support');
          el.innerHTML = el.innerHTML.replace(/Frappe Framework/g, brand);
          el.innerHTML = el.innerHTML.replace(/Powered by Frappe/g, 'Powered by ' + brand);
          el.innerHTML = el.innerHTML.replace(/Frappe/g, brand);
        }
      });
    }, 1000);
    setTimeout(function() {
      replaceDOM();
      document.querySelectorAll('.navbar-brand img, .app-logo img, img[alt*="erpnext"], img[alt*="Frappe"], img[alt*="ERPNext"]').forEach(function(img) {
        if (img && img.src && (img.src.indexOf('erpnext') > -1 || img.src.indexOf('frappe') > -1 || img.clientWidth > 100)) {
          img.src = '/assets/rbo/images/logo.png';
        }
      });
    }, 2000);
  };

  var observer = new MutationObserver(function(mutations) {
    mutations.forEach(function() {
      delayedReplace();
    });
  });
  observer.observe(document.body || document.documentElement, { childList: true, subtree: true, characterData: true });

  replaceDOM();
  delayedReplace();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', rboRebrand);
} else {
  rboRebrand();
}
