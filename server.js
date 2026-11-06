// The site on Railway: static files from site/ (serve-handler, as `serve` did) plus one proxied path — the team deck PDF comes
// from the editor service's published copy when EDITOR_PUB_URL is set and answers, else from the file committed in site/.
const http = require('http'), path = require('path'), fs = require('fs');
const handler = require('serve-handler');
const PORT = Number(process.env.PORT || 3000), SITE = path.join(__dirname, 'site');
const PDF = '/obiimy-podarunky-dlia-komandy.pdf', PUB = process.env.EDITOR_PUB_URL || '';

async function proxied(req, res) {
  if (!PUB) return false;
  const ctl = new AbortController(); const t = setTimeout(() => ctl.abort(), 8000);
  try {
    const r = await fetch(PUB, { method: req.method === 'HEAD' ? 'HEAD' : 'GET', signal: ctl.signal, headers: { 'User-Agent': 'obiimy-site' } });
    if (!r.ok) return false;
    res.writeHead(200, { 'Content-Type': 'application/pdf', 'Content-Length': r.headers.get('content-length') || undefined, 'Cache-Control': 'no-cache',
      'Content-Disposition': 'inline; filename="Obiimy-podarunky-dlia-komandy.pdf"' });
    if (req.method === 'HEAD' || !r.body) { res.end(); return true; }
    for await (const chunk of r.body) res.write(chunk);
    res.end(); return true;
  } catch (e) { return false; } finally { clearTimeout(t); }
}

// Subdomains that show one landing at their root (the hub stays on the Railway host) and serve nothing else but that page's assets:
// corporate.obiimy.world — the corporate-gifts landing; edem.obiimy.world — the KRAЇNA EDEM × OBIIMY sale page (04.11.2026).
const CORP = { host: /^corporate\./i, page: '/b2b-deck', pages: { '/b2b-deck': 'b2b-deck', '/b2b-team-main': 'b2b-team-main' },
  allow: /^\/(photo|img|brand|tex|thumbs|cms\.js|favicon|obiimy-podarunky-dlia-komandy\.pdf|lookbook-obiimy-2026)/ };   // what the corporate host serves besides its page
const EDEM = { host: /^edem\./i, page: '/edem-motion-light', pages: {}, allow: /^\/(photo\/edem\/|brand\/|favicon)/,
  alias: { '/en': '/edem-motion-light-en' }, canon: { '/edem-motion-light': '/', '/edem-motion-light-en': '/en' } };   // /en is the English page; the slugs redirect to the short paths
const HOSTS = [CORP, EDEM];

// Content edits made on the landing itself (cms.js, «?edit») are kept by the editor service as /pub/corp.json and applied here
// to every element the generator marked with data-cms / data-cms-img, so the page is served already edited (no flicker, SEO
// sees the edited text). The JSON is cached briefly; «?raw» serves the generator's page untouched (the editor reads originals there).
const LOCAL = /(^|\.)(localhost|127\.0\.0\.1|\[::1\])(:|$)/;
function corpUrl(host, slug) { return (process.env.CORP_CONTENT_URL || (LOCAL.test(host || '') ? 'http://127.0.0.1:8770/pub/corp.json' : 'https://deck-editor-production.up.railway.app/pub/corp.json')) + '?page=' + slug; }
const corpCache = {};
async function corpContent(host, slug) {
  const url = corpUrl(host, slug), c = corpCache[url];
  if (c && Date.now() - c.at < 15000) return c.data;
  const ctl = new AbortController(); const t = setTimeout(() => ctl.abort(), 4000);
  try {
    const r = await fetch(url, { signal: ctl.signal, headers: { 'User-Agent': 'obiimy-site' } });
    const data = r.ok ? await r.json() : null;
    corpCache[url] = { at: Date.now(), data }; return data;
  } catch (e) { corpCache[url] = { at: Date.now(), data: c ? c.data : null }; return c ? c.data : null; } finally { clearTimeout(t); }
}
function esc(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
function applyCorp(html, data) {
  if (!data) return html;
  for (const [key, v] of Object.entries(data.text || {})) {
    if (!v || typeof v.html !== 'string') continue;
    html = html.replace(new RegExp('(<(h1|h2|h3|p|li|figcaption|small|td|th|dt|dd|label|a|button)\\b[^>]*\\bdata-cms="' + esc(key) + '"[^>]*>)[\\s\\S]*?(</\\2>)'), (m, open, tag, close) => open + v.html + close);
  }
  for (const [key, v] of Object.entries(data.img || {})) {
    if (!v || typeof v.src !== 'string' || /["'<>]/.test(v.src)) continue;
    html = html.replace(new RegExp('<img\\b[^>]*\\bdata-cms-img="' + esc(key) + '"[^>]*>'), m => m.replace(/\s(srcset|sizes)="[^"]*"/g, '').replace(/\ssrc="[^"]*"/, ' src="' + v.src + '"'));
  }
  return html;
}
async function corpPage(req, res, u, slug) {
  const file = path.join(SITE, slug + '.html');
  let html; try { html = fs.readFileSync(file, 'utf8'); } catch (e) { return false; }
  if (!u.searchParams.has('raw')) html = applyCorp(html, await corpContent(req.headers.host, slug));
  res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-cache' });
  res.end(req.method === 'HEAD' ? undefined : html); return true;
}
module.exports = { applyCorp };

// The visitor comes back from WayForPay's payment page to /pay/return (the returnUrl of every Edem order, 06.11.2026): the
// gateway posts the result as a form, the site reads the reference and the status and sends the browser on to the sale page,
// which shows the order's state (and confirms it with the editor service). ?lang=en returns to the English page.
function payReturn(req, res, u, own) {
  let raw = ''; const done = () => {
    const b = new URLSearchParams(raw), ref = String(b.get('orderReference') || u.searchParams.get('orderReference') || u.searchParams.get('ref') || '').replace(/[^A-Za-z0-9-]/g, '').slice(0, 40);
    const st = String(b.get('transactionStatus') || u.searchParams.get('transactionStatus') || '').toLowerCase();
    const pay = st === 'approved' ? 'paid' : (st === 'declined' || st === 'expired') ? 'declined' : st ? 'pending' : 'cancel';   // no status at all = the visitor cancelled on the payment page
    const en = u.searchParams.get('lang') === 'en', page = own ? (en ? '/en' : '/') : (en ? '/edem-motion-light-en' : '/edem-motion-light');
    res.writeHead(303, { Location: page + (ref ? '?order=' + ref + '&pay=' + pay : '') + '#order', 'Cache-Control': 'no-store' }); res.end();
  };
  if (req.method === 'POST') { req.on('data', c => { if (raw.length < 65536) raw += c; }); req.on('end', done); } else done();
}

const server = http.createServer(async (req, res) => {
  const u = new URL(req.url, 'http://x');
  const own = HOSTS.find(h => h.host.test(req.headers.host || ''));
  if (u.pathname === '/pay/return') return payReturn(req, res, u, own && own === EDEM ? own : null);
  if (own) {       // a landing's own host: its page at the root, its assets, nothing else
    const bare = u.pathname.replace(/\.html$/, ''), canon = own.canon && own.canon[bare], alias = own.alias && own.alias[bare];
    if (canon) { res.writeHead(301, { Location: canon + u.search }); return res.end(); }
    if (alias) req.url = alias + u.search;
    else if (u.pathname === '/' || u.pathname === '/index.html' || u.pathname === own.page || u.pathname === own.page + '.html') req.url = own.page + u.search;
    else if (!own.allow.test(u.pathname)) { res.writeHead(302, { Location: '/' }); return res.end(); }
  }
  const slug = CORP.pages[req.url.split('?')[0].replace(/\.html$/, '')];
  if (slug && (req.method === 'GET' || req.method === 'HEAD') && await corpPage(req, res, u, slug)) return;
  if (u.pathname === PDF && (req.method === 'GET' || req.method === 'HEAD') && await proxied(req, res)) return;
  return handler(req, res, { public: SITE, cleanUrls: true, directoryListing: false });
});
if (require.main === module) server.listen(PORT, () => console.log(`obiimy site on :${PORT}` + (PUB ? ` · deck PDF from ${PUB}` : '')));
