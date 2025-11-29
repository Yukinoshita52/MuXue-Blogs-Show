document.addEventListener('contextmenu', e => {
  e.preventDefault();
  const el = document.querySelector('#search-button .site-page.social-icon.search');
  if (el) el.dispatchEvent(new MouseEvent('click', {bubbles: true}));
});
