function rboRebrand() {
  var brand = 'Ritam Bharat OS';
  var replacements = [
    ['Starting Frappe', 'Starting ' + brand],
    ['ERPNext Settings', 'Settings'],
    ['Frappe Support', 'Help & Support'],
    ['Frappe Framework', brand],
    ['Powered by Frappe', 'Powered by ' + brand],
    ['ERPNext', brand],
  ];

  function walk(node) {
    if (!node) return;
    if (node.nodeType === 3) {
      var t = node.textContent;
      for (var i = 0; i < replacements.length; i++) {
        if (t.indexOf(replacements[i][0]) !== -1) {
          node.textContent = t.replace(new RegExp(replacements[i][0], 'g'), replacements[i][1]);
          t = node.textContent;
        }
      }
      return;
    }
    if (node.nodeType === 1 && node.tagName !== 'SCRIPT' && node.tagName !== 'STYLE') {
      for (var c = node.firstChild; c; c = c.nextSibling) walk(c);
    }
  }

  function fixNavbarLogo() {
    document.querySelectorAll('.navbar-brand img, .app-logo img, [class*="logo"] img').forEach(function(img) {
      var s = img.src || '';
      if (s.indexOf('/assets/') !== -1 && s.indexOf('/assets/rbo/') === -1) {
        img.src = '/assets/rbo/images/logo.png';
      }
    });
  }

  function run() {
    document.title = document.title.replace(/ERPNext/g, brand).replace(/Frappe/g, brand);
    walk(document.body);
    fixNavbarLogo();
    document.querySelectorAll('[data-label="ERPNext Settings"], [data-label="Frappe Support"]').forEach(function(el) {
      if (el.style) el.style.display = 'none';
    });
  }

  run();
  setTimeout(run, 500);
  setTimeout(run, 1500);
  setTimeout(fixNavbarLogo, 3000);

  var obs = new MutationObserver(function() { run(); });
  if (document.body) obs.observe(document.body, { childList: true, subtree: true, characterData: true });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', rboRebrand);
} else {
  rboRebrand();
}
