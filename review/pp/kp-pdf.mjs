// A4 PDF of a commercial proposal: node review/pp/kp-pdf.mjs <state.json> <out.pdf> [kp.html]
// The page is opened from disk with the state handed over before any script runs (window.__KP), so uploaded pictures
// (data URIs) need no URL; CHROME_PATH points at Chromium on Railway.
import puppeteer from 'puppeteer-core';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
const here = path.dirname(fileURLToPath(import.meta.url));
const [stateFile, out, html = path.resolve(here, '../../kp.html')] = process.argv.slice(2);
const state = JSON.parse(fs.readFileSync(stateFile, 'utf8'));
const b = await puppeteer.launch({ executablePath: process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new', args: ['--no-sandbox', '--disable-dev-shm-usage', '--allow-file-access-from-files'] });
try {
  const p = await b.newPage();
  await p.setViewport({ width: 1400, height: 1000, deviceScaleFactor: 1 });
  await p.evaluateOnNewDocument(st => { window.__KP = st; }, state);
  await p.goto('file://' + html, { waitUntil: 'networkidle0', timeout: 120000 });
  await p.evaluate(async () => {
    await document.fonts.ready;
    const imgs = [...document.querySelectorAll('#doc img')];
    await Promise.all(imgs.map(i => i.complete ? null : new Promise(r => { i.onload = i.onerror = r; })));
  });
  await new Promise(r => setTimeout(r, 300));
  const n = await p.evaluate(() => document.querySelectorAll('#doc .pg').length);
  await p.emulateMediaType('print');
  await p.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true });
  console.log('pages', n, 'bytes', fs.statSync(out).size);
} finally { await b.close(); }
