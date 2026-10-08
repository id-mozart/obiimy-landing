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

http.createServer(async (req, res) => {
  const u = new URL(req.url, 'http://x');
  if (u.pathname === PDF && (req.method === 'GET' || req.method === 'HEAD') && await proxied(req, res)) return;
  return handler(req, res, { public: SITE, cleanUrls: true, directoryListing: false });
}).listen(PORT, () => console.log(`obiimy site on :${PORT}` + (PUB ? ` · deck PDF from ${PUB}` : '')));
