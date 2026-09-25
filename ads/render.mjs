import puppeteer from '/Users/ivan/obiimy/review/pp/node_modules/puppeteer-core/lib/esm/puppeteer/puppeteer-core.js';
import { fileURLToPath } from 'url';
import path from 'path';
const here = path.dirname(fileURLToPath(import.meta.url));
const browser = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new', args: ['--no-sandbox', '--allow-file-access-from-files'] });
const page = await browser.newPage();
await page.setViewport({ width: 1200, height: 2000, deviceScaleFactor: 1 });
await page.goto('file://' + path.join(here, process.env.ADS || 'ads.html'), { waitUntil: 'networkidle0', timeout: 60000 });
await page.evaluate(() => document.fonts.ready);
await new Promise(r => setTimeout(r, 1200));
const ids = await page.$$eval('.ad', els => els.map(e => e.id));
for (const id of ids) {
  const el = await page.$('#' + id);
  await el.screenshot({ path: path.join(here, process.env.OUT || 'out', `${id}.jpg`), type: 'jpeg', quality: 92 });
  console.log('rendered', id);
}
await browser.close();
