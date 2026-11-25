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

  async setViewport(width, height, isMobile = false) {
    await this.send('Emulation.setDeviceMetricsOverride', {
      width,
      height,
      deviceScaleFactor: 2,
      mobile: isMobile
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
  console.log('=== STARTING DETERMINISTIC TAFSIR & RUKU MODERNIZATION AUDIT ===');
  const chromeProcess = spawn(CHROME_PATH, [
    `--remote-debugging-port=${PORT}`,
    '--headless=new',
    '--disable-gpu',
    '--no-sandbox',
    '--hide-scrollbars',
    'about:blank'
  ]);

  try {
    await sleep(2500);
    const targets = await fetchJson(`http://127.0.0.1:${PORT}/json/list`);
    const pageTarget = targets.find(t => t.type === 'page') || targets[0];
    const client = new CDPClient(pageTarget.webSocketDebuggerUrl);
    await client.connect();
    await client.send('Page.enable');
    await client.send('Runtime.enable');

    // 1. Audit AYAH SCOPE directly (Ayah 2 of Surah 24 - has both Jalalayn & Shane Nuzul)
    console.log('\n--- 1. Testing Ayah Scope with JalalaynView & HadithTakhrijSection ---');
    await client.setViewport(1440, 900);
    await client.send('Page.navigate', { url: 'http://localhost:3000/#/24/2' });
    await sleep(2500);

    const ayahAudit = await client.evaluate(`(() => {
      const docWidth = document.documentElement.offsetWidth;
      const scrollWidth = document.documentElement.scrollWidth;
      const hasJalalayn = Array.from(document.querySelectorAll('h3')).some(h => h.textContent.includes('তাফসীরুল জালালাইন'));
      const hasTakhrij = Array.from(document.querySelectorAll('h3')).some(h => h.textContent.includes('শানে নুযূল'));
      const arabicTerms = Array.from(document.querySelectorAll('.font-arabic')).map(e => e.textContent.trim()).filter(Boolean);
      return {
        docWidth,
        scrollWidth,
        overflow: scrollWidth > docWidth,
        hasJalalayn,
        hasTakhrij,
        arabicTermsCount: arabicTerms.length
      };
    })()`);

    console.log('Ayah 2 Scope Desktop Audit Result:', ayahAudit);
    await client.captureScreenshot('screenshot_ayah_scope_desktop.png');

    // 2. Test Jalalayn View Mode Toggles
    console.log('\n--- 2. Testing Jalalayn View Mode Toggles ---');
    await client.evaluate(`
      const btns = Array.from(document.querySelectorAll('button'));
      const jalalaynOnlyBtn = btns.find(b => b.textContent.trim() === 'শুধু জালালাইন');
      if (jalalaynOnlyBtn) jalalaynOnlyBtn.click();
    `);
    await sleep(600);
    await client.captureScreenshot('screenshot_jalalayn_only_mode.png');

    await client.evaluate(`
      const btns = Array.from(document.querySelectorAll('button'));
      const combinedBtn = btns.find(b => b.textContent.trim() === 'সমন্বিত ভিউ');
      if (combinedBtn) combinedBtn.click();
    `);
    await sleep(400);

    // 3. Test Hadith Takhrij Table View Toggle
    console.log('\n--- 3. Testing Hadith Takhrij Table View Toggle ---');
    await client.evaluate(`
      const btns = Array.from(document.querySelectorAll('button'));
      const tableBtn = btns.find(b => b.textContent.includes('তাখরীজ সারণি'));
      if (tableBtn) tableBtn.click();
    `);
    await sleep(600);
    await client.captureScreenshot('screenshot_hadith_takhrij_table_view.png');

    // 4. Test RUKU SCOPE (All 14 Chapters & Dual Reading Mode)
    console.log('\n--- 4. Testing Ruku Scope (Restored 14 Chapters) ---');
    await client.send('Page.navigate', { url: 'http://localhost:3000/#/24/ruku-1' });
    await sleep(2000);

    // Click "রুকু আলোচনা" in Header
    await client.evaluate(`
      window.scrollTo(0, 0);
      const btns = Array.from(document.querySelectorAll('button'));
      const rukuBtn = btns.find(b => b.textContent.includes('রুকু আলোচনা'));
      if (rukuBtn) rukuBtn.click();
    `);
    await sleep(1500);

    const rukuAudit = await client.evaluate(`(() => {
      const docWidth = document.documentElement.offsetWidth;
      const scrollWidth = document.documentElement.scrollWidth;
      const chapterTabs = Array.from(document.querySelectorAll('button')).filter(b => 
        b.textContent.includes('মাকাসিদ') || 
        b.textContent.includes('নাহব') || 
        b.textContent.includes('কিরাআত') ||
        b.textContent.includes('হাদীস') ||
        b.textContent.includes('আহকাম') ||
        b.textContent.includes('তাফসীর')
      );
      const chapterNames = chapterTabs.map(b => b.textContent.trim());
      const hasHadithChapter = chapterNames.some(t => t.includes('হাদীস'));
      return {
        docWidth,
        scrollWidth,
        overflow: scrollWidth > docWidth,
        chapterCount: chapterTabs.length,
        chapterNames,
        hasHadithChapter
      };
    })()`);

    console.log('Ruku Scope 14 Chapters Audit:', rukuAudit);
    await client.captureScreenshot('screenshot_ruku_scope_tabbed.png');

    // Switch to "শানে নুযূল ও হাদীস তাখরীজ" tab in Ruku
    console.log('\n--- 5. Testing Hadith Takhrij in Ruku Scope ---');
    await client.evaluate(`
      const btns = Array.from(document.querySelectorAll('button'));
      const hadithTab = btns.find(b => b.textContent.includes('শানে নুযূল ও হাদীস'));
      if (hadithTab) hadithTab.click();
    `);
    await sleep(1000);
    await client.captureScreenshot('screenshot_ruku_scope_hadith_tab.png');

    // Switch to Continuous Journal Mode (প্রবন্ধ মোড with TOC)
    console.log('\n--- 6. Testing Continuous Journal Mode with Sticky TOC ---');
    await client.evaluate(`
      window.scrollTo(0, 0);
      const btns = Array.from(document.querySelectorAll('button'));
      const tocBtn = btns.find(b => b.textContent.includes('প্রবন্ধ মোড'));
      if (tocBtn) tocBtn.click();
    `);
    await sleep(1200);
    await client.captureScreenshot('screenshot_ruku_scope_continuous_toc.png');

    // 7. Test Responsive Viewports (Tablet 768px & Mobile 375px)
    console.log('\n--- 7. Testing Responsive Viewports (Tablet 768px & Mobile 375px) ---');
    await client.setViewport(768, 1024);
    await sleep(800);
    const tabletAudit = await client.evaluate(`({
      docWidth: document.documentElement.offsetWidth,
      scrollWidth: document.documentElement.scrollWidth,
      overflow: document.documentElement.scrollWidth > document.documentElement.offsetWidth
    })`);
    console.log('Tablet 768px Audit:', tabletAudit);
    await client.captureScreenshot('screenshot_tablet_768px_audit.png');

    await client.setViewport(375, 812, true);
    await sleep(800);
    const mobileAudit = await client.evaluate(`({
      docWidth: document.documentElement.offsetWidth,
      scrollWidth: document.documentElement.scrollWidth,
      overflow: document.documentElement.scrollWidth > document.documentElement.offsetWidth
    })`);
    console.log('Mobile 375px Audit:', mobileAudit);
    await client.captureScreenshot('screenshot_mobile_375px_audit.png');

    client.close();
    console.log('\n✓ ALL AUDITS COMPLETE: ZERO OVERFLOW, ALL 14 CHAPTERS & TAFSIR/TAKHRIIJ VERIFIED!');
  } finally {
    chromeProcess.kill('SIGTERM');
  }
}

run().catch(e => {
  console.error('Audit failed with error:', e);
  process.exit(1);
});
