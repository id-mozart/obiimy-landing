// Content editing of the corporate landing, on the page itself: open «…/b2b-team-main?edit» (or corporate.obiimy.world/?edit),
// click a text to edit it, click a picture to replace it, «Опублікувати» sends the differences from the generator's page to the
// editor service (/api/corp), which keeps them as /pub/corp.json; the site server applies them to the page for everyone.
// «Оригінал» puts the generator's text or picture back for the selected element. Nothing here touches the generator or git.
(function () {
  'use strict';
  var LOCAL = /^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname);
  var API = LOCAL ? 'http://127.0.0.1:8770' : 'https://deck-editor-production.up.railway.app';
  var KEY_STORE = 'obiimy-corp-key';
  var PAGE = (document.querySelector('main[data-cms-page]') || {}).dataset ? document.querySelector('main[data-cms-page]').dataset.cmsPage : 'b2b-deck';
  var orig = { text: {}, img: {} }, selected = null, busy = false;

  var css = document.createElement('style');
  css.textContent = [
    '[data-cms] { outline: 1px dashed rgba(242,183,5,.75); outline-offset: 2px; cursor: text; min-height: 1em; }',
    '[data-cms]:hover { outline-color: #F2B705; background: rgba(242,183,5,.08); }',
    '[data-cms].cms-sel { outline: 2px solid #F2B705; background: rgba(242,183,5,.1); }',
    '[data-cms].cms-changed { outline: 2px solid #2b7a3d; }',
    '[data-cms-img] { cursor: pointer; outline: 1px dashed rgba(242,183,5,.75); outline-offset: -2px; }',
    '[data-cms-img].cms-sel { outline: 3px solid #F2B705; outline-offset: -3px; }',
    '[data-cms-img].cms-changed { outline: 3px solid #2b7a3d; outline-offset: -3px; }',
    'body { padding-bottom: 120px !important; }',
    '#cms-bar { position: fixed; left: 0; right: 0; bottom: 0; z-index: 99999; background: #141110; color: #F3EADB; font: 14px/1.4 Montserrat, Arial, sans-serif; box-shadow: 0 -6px 24px rgba(0,0,0,.35); }',
    '#cms-bar .in { max-width: 1200px; margin: 0 auto; padding: 12px 20px; display: flex; flex-wrap: wrap; gap: 10px 14px; align-items: center; }',
    '#cms-bar b { color: #F2B705; font-weight: 600; }',
    '#cms-bar button { font: inherit; font-weight: 600; border: 0; border-radius: 999px; padding: 9px 16px; cursor: pointer; background: #2A2320; color: #F3EADB; }',
    '#cms-bar button:hover { background: #3A3530; } #cms-bar button[disabled] { opacity: .5; cursor: default; }',
    '#cms-bar button.pub { background: #F2B705; color: #141110; }',
    '#cms-bar input { font: inherit; padding: 8px 12px; border-radius: 8px; border: 1px solid #3A3530; background: #1F1B19; color: #F3EADB; width: 170px; }',
    '#cms-bar .st { flex: 1; min-width: 200px; color: #B9B0A3; } #cms-bar .st.ok { color: #7CC58E; } #cms-bar .st.err { color: #F08C8C; }',
    '#cms-file { display: none; }',
    '@media (max-width: 700px) { #cms-bar .in { padding: 10px 12px; gap: 8px; } #cms-bar .st { flex-basis: 100%; } }'
  ].join('\n');
  document.head.appendChild(css);

  var bar = document.createElement('div'); bar.id = 'cms-bar';
  bar.innerHTML = '<div class="in"><span><b>Редагування</b> · клікніть на текст або фото</span><span class="st" id="cms-st"></span>' +
    '<input type="password" id="cms-key" placeholder="Пароль редагування" autocomplete="off">' +
    '<button type="button" id="cms-orig" disabled>Оригінал</button><button type="button" id="cms-reset">Скинути незбережене</button>' +
    '<button type="button" class="pub" id="cms-pub">Опублікувати</button><button type="button" id="cms-exit">Вийти</button></div>' +
    '<input type="file" id="cms-file" accept="image/jpeg,image/png,image/webp">';
  document.body.appendChild(bar);
  var st = document.getElementById('cms-st'), keyIn = document.getElementById('cms-key'), fileIn = document.getElementById('cms-file');
  var origBtn = document.getElementById('cms-orig'), pubBtn = document.getElementById('cms-pub');
  try { keyIn.value = sessionStorage.getItem(KEY_STORE) || ''; } catch (e) {}
  keyIn.addEventListener('change', function () { try { sessionStorage.setItem(KEY_STORE, keyIn.value); } catch (e) {} });
  function status(t, cls) { st.textContent = t; st.className = 'st' + (cls ? ' ' + cls : ''); }

  function norm(h) { return (h || '').replace(/\s+/g, ' ').trim(); }
  function abs(u) { try { return new URL(u, location.href).href; } catch (e) { return u; } }
  function texts() { return [].slice.call(document.querySelectorAll('[data-cms]')); }
  function imgs() { return [].slice.call(document.querySelectorAll('[data-cms-img]')); }
  function textChanged(el) { var o = orig.text[el.dataset.cms]; return o !== undefined && norm(el.innerHTML) !== norm(o); }
  function imgChanged(el) { var o = orig.img[el.dataset.cmsImg]; return o !== undefined && abs(el.getAttribute('src')) !== abs(o.src); }
  function refresh() {
    var n = 0;
    texts().forEach(function (el) { var c = textChanged(el); el.classList.toggle('cms-changed', c); if (c) n++; });
    imgs().forEach(function (el) { var c = imgChanged(el); el.classList.toggle('cms-changed', c); if (c) n++; });
    pubBtn.textContent = n ? 'Опублікувати (' + n + ')' : 'Опублікувати';
    return n;
  }

  // the generator's page («?raw») gives the originals: what «Оригінал» restores and what the differences are measured against
  function loadOriginals() {
    var u = new URL(location.href); u.searchParams.delete('edit'); u.searchParams.set('raw', '1');
    return fetch(u.toString(), { cache: 'no-store' }).then(function (r) { return r.text(); }).then(function (html) {
      var d = new DOMParser().parseFromString(html, 'text/html');
      d.querySelectorAll('[data-cms]').forEach(function (el) { orig.text[el.dataset.cms] = el.innerHTML; });
      d.querySelectorAll('[data-cms-img]').forEach(function (el) { orig.img[el.dataset.cmsImg] = { src: el.getAttribute('src'), srcset: el.getAttribute('srcset'), sizes: el.getAttribute('sizes') }; });
    });
  }

  function select(el) {
    if (selected) { selected.classList.remove('cms-sel'); if (selected.hasAttribute('data-cms')) selected.removeAttribute('contenteditable'); }
    selected = el;
    if (!el) { origBtn.disabled = true; return; }
    el.classList.add('cms-sel'); origBtn.disabled = false;
    if (el.hasAttribute('data-cms')) { el.setAttribute('contenteditable', 'true'); el.focus(); }
  }

  document.addEventListener('click', function (e) {
    if (bar.contains(e.target)) return;
    var t = e.target.closest('[data-cms]'), im = e.target.closest('[data-cms-img]');
    if (t) { if (t.closest('a') || t.tagName === 'A' || t.tagName === 'BUTTON') e.preventDefault(); if (selected !== t) select(t); return; }
    if (im) { e.preventDefault(); select(im); fileIn.click(); return; }
    if (e.target.closest('a[href]')) { e.preventDefault(); }       // links do not navigate in edit mode
    select(null);
  }, true);
  document.addEventListener('submit', function (e) { e.preventDefault(); status('У режимі редагування форма не надсилається.'); }, true);
  document.addEventListener('input', function (e) { if (e.target.closest && e.target.closest('[data-cms]')) refresh(); });
  document.addEventListener('keydown', function (e) {
    if (!selected || !selected.hasAttribute('data-cms')) return;
    if (e.key === 'Escape') { select(null); return; }
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); document.execCommand('insertLineBreak'); }
  });
  document.addEventListener('paste', function (e) {
    if (!selected || !selected.hasAttribute('data-cms')) return;
    e.preventDefault(); document.execCommand('insertText', false, (e.clipboardData || window.clipboardData).getData('text/plain'));
  });

  fileIn.addEventListener('change', function () {
    var f = fileIn.files && fileIn.files[0], im = selected; fileIn.value = '';
    if (!f || !im || !im.hasAttribute('data-cms-img')) return;
    if (f.size > 25 * 1048576) return status('Файл завеликий (понад 25 МБ).', 'err');
    status('Завантажую фото…'); busy = true;
    fetch(API + '/api/corp-upload?name=' + encodeURIComponent(f.name), { method: 'POST', headers: headers(), body: f })
      .then(function (r) { return r.json(); })
      .then(function (j) {
        if (!j.ok) throw new Error(j.error || 'не вдалося');
        im.removeAttribute('srcset'); im.removeAttribute('sizes'); im.src = j.src; im.loading = 'eager';
        var pic = im.closest('picture'); if (pic) pic.querySelectorAll('source').forEach(function (s) { s.remove(); });
        refresh(); status('Фото замінено — не забудьте «Опублікувати».', 'ok');
      })
      .catch(function (e) { status('Фото не завантажилось: ' + e.message, 'err'); })
      .then(function () { busy = false; });
  });

  origBtn.addEventListener('click', function () {
    if (!selected) return;
    if (selected.hasAttribute('data-cms')) { var o = orig.text[selected.dataset.cms]; if (o !== undefined) selected.innerHTML = o; }
    else { var oi = orig.img[selected.dataset.cmsImg]; if (oi) { selected.src = oi.src; if (oi.srcset) selected.setAttribute('srcset', oi.srcset); if (oi.sizes) selected.setAttribute('sizes', oi.sizes); } }
    refresh(); status('Повернуто оригінал — «Опублікувати», щоб це побачили всі.');
  });
  document.getElementById('cms-reset').addEventListener('click', function () { if (!refresh() || confirm('Скинути всі незбережені зміни на цій сторінці?')) location.reload(); });
  document.getElementById('cms-exit').addEventListener('click', function () {
    if (refresh() && !confirm('Є неопубліковані зміни — вийти без публікації?')) return;
    var u = new URL(location.href); u.searchParams.delete('edit'); location.href = u.toString();
  });

  function headers() { var h = {}; if (keyIn.value) h['X-Corp-Key'] = keyIn.value; return h; }
  function clean(el) {       // the editable copy without our own classes and attributes
    var c = el.cloneNode(true); c.removeAttribute('contenteditable'); c.classList.remove('cms-sel', 'cms-changed'); if (!c.getAttribute('class')) c.removeAttribute('class');
    return c.innerHTML;
  }
  pubBtn.addEventListener('click', function () {
    if (busy) return;
    var body = { page: PAGE, text: {}, img: {} };
    texts().forEach(function (el) { if (textChanged(el)) body.text[el.dataset.cms] = { html: clean(el) }; });
    imgs().forEach(function (el) { if (imgChanged(el)) body.img[el.dataset.cmsImg] = { src: abs(el.getAttribute('src')) }; });
    var n = Object.keys(body.text).length + Object.keys(body.img).length;
    status(n ? 'Публікую…' : 'Публікую (повернення до оригіналу)…'); busy = true; pubBtn.disabled = true;
    fetch(API + '/api/corp', { method: 'POST', headers: Object.assign({ 'Content-Type': 'application/json' }, headers()), body: JSON.stringify(body) })
      .then(function (r) { return r.json(); })
      .then(function (j) {
        if (!j.ok) throw new Error(j.error || 'не вдалося');
        status('Опубліковано ✓ ' + (j.saved || '') + ' — сторінка оновиться для всіх за ~15 секунд.', 'ok');
      })
      .catch(function (e) { status('Не опубліковано: ' + e.message, 'err'); })
      .then(function () { busy = false; pubBtn.disabled = false; });
  });

  status('Завантажую оригінали…');
  loadOriginals().then(function () { refresh(); status('Готово. Зелена рамка — змінене, жовта — вибране.'); })
    .catch(function () { status('Не вдалося прочитати оригінали сторінки — «Оригінал» недоступний.', 'err'); });
})();
