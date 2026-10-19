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

// corporate.obiimy.world: the corporate-gifts landing at the root (the hub stays on the Railway host); every other path is shared
const CORP = { host: /^corporate\./i, page: '/b2b-deck', pages: { '/b2b-deck': 'b2b-deck', '/b2b-team-main': 'b2b-team-main' },
  allow: /^\/(photo|img|brand|tex|thumbs|cms\.js|favicon|obiimy-podarunky-dlia-komandy\.pdf|lookbook-obiimy-2026)/ };   // what the corporate host serves besides its page

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

const server = http.createServer(async (req, res) => {
  const u = new URL(req.url, 'http://x');
  if (CORP.host.test(req.headers.host || '')) {       // the corporate host: its page at the root, its assets and PDFs, nothing else
    if (u.pathname === '/' || u.pathname === '/index.html' || u.pathname === CORP.page || u.pathname === CORP.page + '.html') req.url = CORP.page + u.search;
    else if (!CORP.allow.test(u.pathname)) { res.writeHead(302, { Location: '/' }); return res.end(); }
  }
  const slug = CORP.pages[req.url.split('?')[0].replace(/\.html$/, '')];
  if (slug && (req.method === 'GET' || req.method === 'HEAD') && await corpPage(req, res, u, slug)) return;
  if (u.pathname === PDF && (req.method === 'GET' || req.method === 'HEAD') && await proxied(req, res)) return;
  return handler(req, res, { public: SITE, cleanUrls: true, directoryListing: false });
});
if (require.main === module) server.listen(PORT, () => console.log(`obiimy site on :${PORT}` + (PUB ? ` · deck PDF from ${PUB}` : '')));
