// Print-ready PDFs of business-card faces from cards.html: trim + 3 mm bleed + crop marks, 1 CSS mm = 1 mm.
// usage: IDS=03,04,05 OUT=brand/print [PNG=dir] node review/print/vizytky-pdf.mjs
// per face: vizytka-NN-lytse.pdf = trim + 3 mm bleed, no marks (what Ukrainian digital shops ask for); -mitky.pdf = the same on a page with crop marks; -kontur.pdf = the trim outline (radius 3 mm) in magenta on the clean page.
import { writeFileSync } from 'node:fs';
import puppeteer from '/Users/ivan/obiimy/review/pp/node_modules/puppeteer-core/lib/esm/puppeteer/puppeteer-core.js';
const ROOT = '/Users/ivan/obiimy', BLEED = 3;   // mm beyond the trim
let MARGIN = BLEED;   // page margin: = bleed for the clean file, 8 mm when the page carries crop marks
const browser = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new', args: ['--no-sandbox', '--allow-file-access-from-files'] });
const src = await browser.newPage();
await src.goto(`file://${ROOT}/cards.html`, { waitUntil: 'networkidle0', timeout: 60000 });
await src.evaluate(() => document.fonts.ready);
const head = await src.evaluate(() => [...document.querySelectorAll('link[rel=stylesheet], style')].map(e => e.outerHTML).join('\n'));
const size = k => k.includes('s') ? [85, 55] : k.includes('v') ? [50, 90] : k.includes('q') ? [55, 55] : [90, 50];
const marks = (W, H) => {   // 8 crop marks, 0.1 mm, from 1 mm inside the page edge to 0.5 mm short of the bleed edge
  const L = MARGIN - BLEED - 1.5, out = [];
  for (const [x, y] of [[MARGIN, MARGIN], [MARGIN + W, MARGIN], [MARGIN, MARGIN + H], [MARGIN + W, MARGIN + H]]) {
    out.push(`<i style="left:${x}mm;top:${y < MARGIN + 1 ? 1 : y + BLEED + .5}mm;width:.1mm;height:${L}mm"></i>`);
    out.push(`<i style="top:${y}mm;left:${x < MARGIN + 1 ? 1 : x + BLEED + .5}mm;height:.1mm;width:${L}mm"></i>`);
  }
  return out.join('');
};
const page = await browser.newPage();
const TMP = process.env.TMP || '/tmp';
const show = async html => { writeFileSync(`${TMP}/sheet.html`, html); await page.goto(`file://${TMP}/sheet.html`, { waitUntil: 'load', timeout: 60000 }); await page.evaluate(() => document.fonts.ready); await new Promise(r => setTimeout(r, 400)); };
for (const id of process.env.IDS.split(',')) {
  const faces = await src.evaluate(id => [1, 2].map(n => {
    const card = document.querySelector(`#card-${id} .side:nth-child(${n}) .card`);
    return { kind: card.className, html: card.outerHTML, bg: getComputedStyle(card.querySelector('.face')).backgroundColor };
  }), id);
  const [W, H] = size(faces[0].kind);
  let PW, PH;
  const sheet = (inner, mk) => `<!DOCTYPE html><html><head><meta charset="utf-8"><base href="file://${ROOT}/">${head}
<style>html{--mm:1mm}html,body{margin:0;background:#fff}@page{size:${PW}mm ${PH}mm;margin:0}
.sheet{position:relative;width:${PW}mm;height:${PH}mm;overflow:hidden;background:#fff}
.sheet .clip{position:absolute;left:${MARGIN - BLEED}mm;top:${MARGIN - BLEED}mm;width:${W + 2 * BLEED}mm;height:${H + 2 * BLEED}mm;overflow:hidden}
.sheet .card{position:absolute;left:${BLEED}mm;top:${BLEED}mm;overflow:visible;border-radius:0;box-shadow:none;font-size:10px}
.sheet .card .face{overflow:visible;font-size:1mm}.sheet .bleed{position:absolute;inset:-${BLEED}mm;z-index:-1}.sheet .fill{left:-${BLEED}mm;top:-${BLEED}mm;width:calc(100% + ${2 * BLEED}mm);height:calc(100% + ${2 * BLEED}mm)}
.sheet i{position:absolute;background:#000}.sheet .die{position:absolute;left:${MARGIN}mm;top:${MARGIN}mm;width:${W}mm;height:${H}mm;border:.25pt solid #ff00ff;border-radius:3mm;box-sizing:border-box}</style></head>
<body><div class="sheet"><div class="clip">${inner}</div>${mk ? marks(W, H) : ''}</div></body></html>`;
  for (const [i, name] of [[0, 'lytse'], [1, 'zvorot']]) for (const mk of [false, true]) {
    MARGIN = mk ? 8 : BLEED; PW = W + 2 * MARGIN; PH = H + 2 * MARGIN;
    const f = faces[i], suffix = mk ? '-mitky' : '';
    const html = sheet(f.html.replace(/<div class="face/, `<div class="bleed" style="background:${f.bg}"></div><div class="face`), mk);
    await show(html);
    await page.pdf({ path: `${process.env.OUT}/vizytka-${id}-${name}${suffix}.pdf`, width: `${PW}mm`, height: `${PH}mm`, printBackground: true, preferCSSPageSize: true });
    if (process.env.PNG) { await page.setViewport({ width: Math.ceil(PW * 96 / 25.4), height: Math.ceil(PH * 96 / 25.4), deviceScaleFactor: 300 / 96 }); await page.screenshot({ path: `${process.env.PNG}/vizytka-${id}-${name}${suffix}.png` }); }
  }
  MARGIN = BLEED; PW = W + 2 * MARGIN; PH = H + 2 * MARGIN;
  const rk = faces[0].kind.split(' ').includes('r');
  await show(sheet(rk ? `<div class="die"></div>` : `<div class="die" style="border-radius:0"></div>`, false));
  await page.pdf({ path: `${process.env.OUT}/vizytka-${id}-kontur.pdf`, width: `${PW}mm`, height: `${PH}mm`, printBackground: false, preferCSSPageSize: true });
  console.log(id, `${W}×${H} mm, clean page ${PW}×${PH} mm, radius ${rk ? 3 : 0}`);
}
await browser.close();
