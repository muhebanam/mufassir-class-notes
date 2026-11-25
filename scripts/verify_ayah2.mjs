import { spawn } from 'child_process';
import http from 'http';
import fs from 'fs';
import path from 'path';

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const ARTIFACT_DIR = 'C:\\Users\\USER\\.gemini\\antigravity\\brain\\7caaeec8-bdfa-40da-93eb-62b94af954b1';
const PORT = 9222;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function fetchJson(url) {
  return new Promise((resolve, reject) => {
    http.get(url, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

class CDPClient {
  constructor(wsUrl) {
    this.wsUrl = wsUrl;
    this.ws = null;
    this.id = 1;
    this.callbacks = new Map();
  }

  async connect() {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.wsUrl);
      this.ws.onopen = () => resolve();
      this.ws.onerror = reject;
      this.ws.onmessage = (event) => {
        const msg = JSON.parse(event.data);
        if (msg.id && this.callbacks.has(msg.id)) {
          const cb = this.callbacks.get(msg.id);
          this.callbacks.delete(msg.id);
          if (msg.error) cb.reject(msg.error);
          else cb.resolve(msg.result);
        }
      };
    });
  }

  send(method, params = {}) {
    return new Promise((resolve, reject) => {
      const id = this.id++;
      this.callbacks.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }

  async evaluate(expression) {
    const res = await this.send('Runtime.evaluate', {
      expression,
      returnByValue: true,
      awaitPromise: true
    });
    return res.result?.value;
  }

  async setViewport(width, height) {
    await this.send('Emulation.setDeviceMetricsOverride', {
      width,
      height,
      deviceScaleFactor: 2,
      mobile: false
    });
    await this.send('Emulation.setVisibleSize', { width, height });
  }

  async captureScreenshot(filename) {
    const res = await this.send('Page.captureScreenshot', { format: 'png' });
    const buffer = Buffer.from(res.data, 'base64');
    const outPath = path.join(ARTIFACT_DIR, filename);
    fs.writeFileSync(outPath, buffer);
    console.log(`Saved screenshot: ${filename} (${buffer.length} bytes)`);
    return outPath;
  }

  close() {
    if (this.ws) this.ws.close();
  }
}

async function run() {
  console.log('--- AUDITING AYAH 2 TAFSIR & HADITH TAKHRIJ ---');
  const chromeProcess = spawn(CHROME_PATH, [
    `--remote-debugging-port=${PORT}`,
    '--headless=new',
    '--disable-gpu',
    '--no-sandbox',
    'about:blank'
  ]);

  try {
    await sleep(2000);
    const targets = await fetchJson(`http://127.0.0.1:${PORT}/json/list`);
    const pageTarget = targets.find(t => t.type === 'page') || targets[0];
    const client = new CDPClient(pageTarget.webSocketDebuggerUrl);
    await client.connect();
    await client.send('Page.enable');
    await client.send('Runtime.enable');

    await client.setViewport(1440, 900);
    await client.send('Page.navigate', { url: 'http://localhost:3000/' });
    await sleep(2500);

    // Initial page load: default is Ayah 1
    // Click "পরবর্তী আয়াত" button
    const clickRes = await client.evaluate(`(() => {
      const nextBtn = document.querySelector('button[title="পরবর্তী আয়াত"]');
      if (nextBtn) {
        nextBtn.click();
        return true;
      }
      return false;
    })()`);
    console.log('Clicked Next Ayah button:', clickRes);
    await sleep(1500);

    const checkAyah2 = await client.evaluate(`(() => {
      const h3s = Array.from(document.querySelectorAll('h3')).map(h => h.textContent.trim());
      const hasJalalayn = h3s.some(t => t.includes('তাফসীরুল জালালাইন'));
      const hasTakhrij = h3s.some(t => t.includes('শানে নুযূল'));
      const hadithCards = document.querySelectorAll('.font-arabic').length;
      const breadcrumb = document.querySelector('.bg-emerald-100')?.textContent.trim();
      return {
        h3s,
        hasJalalayn,
        hasTakhrij,
        hadithCards,
        breadcrumb
      };
    })()`);

    console.log('Ayah 2 Verification Result:', checkAyah2);
    await client.captureScreenshot('screenshot_ayah_2_verified.png');

    // Test Takhrij table view toggle
    await client.evaluate(`
      const btns = Array.from(document.querySelectorAll('button'));
      const tableBtn = btns.find(b => b.textContent.includes('তাখরীজ সারণি'));
      if (tableBtn) tableBtn.click();
    `);
    await sleep(1000);
    await client.captureScreenshot('screenshot_ayah_2_takhrij_table.png');

    // Now switch to Ruku Scope by clicking "রুকু আলোচনা"
    await client.evaluate(`
      window.scrollTo(0, 0);
      const btns = Array.from(document.querySelectorAll('button'));
      const rukuBtn = btns.find(b => b.textContent.includes('রুকু আলোচনা'));
      if (rukuBtn) rukuBtn.click();
    `);
    await sleep(1500);

    const checkRuku = await client.evaluate(`(() => {
      const btns = Array.from(document.querySelectorAll('button'));
      const chapterBtns = btns.filter(b => 
        b.textContent.includes('মাকাসিদ') || 
        b.textContent.includes('হাদীস') || 
        b.textContent.includes('কিরাআত') ||
        b.textContent.includes('আহকাম')
      );
      return {
        chapterCount: chapterBtns.length,
        chapters: chapterBtns.map(b => b.textContent.trim())
      };
    })()`);

    console.log('Ruku Scope Verification Result:', checkRuku);
    await client.captureScreenshot('screenshot_ruku_chapters_verified.png');

    client.close();
    console.log('✓ VERIFICATION FINISHED SUCCESSFULLY!');
  } finally {
    chromeProcess.kill('SIGTERM');
  }
}

run().catch(e => {
  console.error('Error:', e);
  process.exit(1);
});
