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
    return outPath;
  }

  close() {
    if (this.ws) this.ws.close();
  }
}

async function runAudit() {
  console.log('--- STARTING COMPREHENSIVE UI & DATA ISOLATION AUDIT ---');
  
  // 1. Launch Headless Chrome
  const chromeProcess = spawn(CHROME_PATH, [
    `--remote-debugging-port=${PORT}`,
    '--headless=new',
    '--disable-gpu',
    '--no-first-run',
    '--no-default-browser-check',
    '--user-data-dir=C:\\Users\\USER\\AppData\\Local\\Temp\\chrome-audit-profile',
    'http://localhost:3000/#/24/1'
  ]);

  await sleep(2500);

  try {
    const targets = await fetchJson(`http://127.0.0.1:${PORT}/json/list`);
    const pageTarget = targets.find(t => t.type === 'page') || targets[0];
    if (!pageTarget) throw new Error('No page target found');

    const cdp = new CDPClient(pageTarget.webSocketDebuggerUrl);
    await cdp.connect();
    console.log('Connected to Chrome DevTools Protocol page target successfully.');

    await cdp.send('Page.enable');
    await cdp.send('Runtime.enable');
    await cdp.send('DOM.enable');

    await sleep(2000); // Allow react data to load

    const auditResults = {
      viewports: {},
      rukuIsolation: {},
      tierIsolation: {}
    };

    // =========================================================================
    // TEST 1: VIEWPORT AUDIT (1440px, 768px, 375px)
    // =========================================================================
    console.log('\n--- 1. Testing Viewports & Horizontal Overflow ---');
    const viewports = [
      { name: 'Desktop', width: 1440, height: 900, mobile: false },
      { name: 'Tablet', width: 768, height: 1024, mobile: false },
      { name: 'Mobile', width: 375, height: 812, mobile: true }
    ];

    for (const vp of viewports) {
      await cdp.setViewport(vp.width, vp.height, vp.mobile);
      await sleep(1000);

      const metrics = await cdp.evaluate(`
        (() => {
          const docEl = document.documentElement;
          const body = document.body;
          const scrollW = Math.max(docEl.scrollWidth, body.scrollWidth);
          const innerW = window.innerWidth;
          const hasOverflow = scrollW > innerW + 1; // 1px tolerance for subpixel

          // Check overflowing elements
          const overflowing = [];
          document.querySelectorAll('*').forEach(el => {
            if (el.scrollWidth > el.clientWidth && 
                getComputedStyle(el).overflowX === 'visible' && 
                el.clientWidth > 0 &&
                el.scrollWidth > innerW) {
              overflowing.push({
                tag: el.tagName,
                className: el.className,
                scrollWidth: el.scrollWidth,
                clientWidth: el.clientWidth
              });
            }
          });

          // Check Arabic typography classes & line-height
          const uthmani = document.querySelector('.uthmani-text');
          const uthmaniStyle = uthmani ? {
            fontSize: getComputedStyle(uthmani).fontSize,
            lineHeight: getComputedStyle(uthmani).lineHeight,
            direction: getComputedStyle(uthmani).direction,
            fontFamily: getComputedStyle(uthmani).fontFamily
          } : null;

          return {
            scrollWidth: scrollW,
            innerWidth: innerW,
            hasOverflow,
            overflowingCount: overflowing.length,
            overflowingSample: overflowing.slice(0, 3),
            uthmaniStyle
          };
        })()
      `);

      const screenshotName = `screenshot_${vp.name.toLowerCase()}_${vp.width}px.png`;
      await cdp.captureScreenshot(screenshotName);

      auditResults.viewports[vp.name] = {
        viewport: `${vp.width}x${vp.height}`,
        ...metrics,
        screenshot: screenshotName
      };

      console.log(`✓ [${vp.name} ${vp.width}px]: scrollWidth=${metrics.scrollWidth}, innerWidth=${metrics.innerWidth}, hasOverflow=${metrics.hasOverflow}`);
      if (metrics.uthmaniStyle) {
        console.log(`  - Arabic Line-Height: ${metrics.uthmaniStyle.lineHeight}, Direction: ${metrics.uthmaniStyle.direction}`);
      }
    }

    // =========================================================================
    // TEST 2: DATA ISOLATION (RUKU 1 -> RUKU 2 RAPID SWITCH)
    // =========================================================================
    console.log('\n--- 2. Testing Data Isolation: Ruku 1 -> Ruku 2 ---');
    
    // First, verify Ruku 1 Ayahs
    await cdp.evaluate(`window.location.hash = '#/24/1'`);
    await sleep(1500);

    const ruku1Ayahs = await cdp.evaluate(`
      (() => {
        // Collect ayahs present in DOM
        const text = document.body.innerText;
        return {
          hasAyah1: text.includes('سُورَةٌ أَنزَلْنَـٰهَا') || text.includes('سُورَةٌ أَنْزَلْنَاهَا'),
          hasAyah2: text.includes('الزَّانِيَةُ') || text.includes('الزَّانِي'),
          hasAyah11: text.includes('إِنَّ الَّذِينَ جَاءُوا بِالْإِفْكِ')
        };
      })()
    `);
    console.log('Ruku 1 state:', ruku1Ayahs);

    // Rapid switch to Ruku 2 via UI selector
    await cdp.evaluate(`
      (() => {
        const select = document.querySelector('select[aria-label="রুকু নির্বাচন করুন"]');
        if (select) {
          select.value = '2';
          select.dispatchEvent(new Event('change', { bubbles: true }));
        } else {
          window.location.hash = '#/24/11';
        }
      })()
    `);
    await sleep(2000);

    const ruku2State = await cdp.evaluate(`
      (() => {
        const text = document.body.innerText;
        // Verify Ruku 2 ayah 11 is present
        const hasAyah11 = text.includes('إِنَّ الَّذِينَ جَاءُوا بِالْإِفْكِ') || text.includes('جَاءُوا بِالْإِفْكِ');
        
        // STRICT CHECK: Verify Ayah 1 or Ayah 2 text from Ruku 1 does NOT leak into Ruku 2 Ayah card
        const mainCardText = document.querySelector('.uthmani-text')?.innerText || '';
        const hasLeakedAyah1 = mainCardText.includes('سُورَةٌ أَنزَلْنَـٰهَا') || mainCardText.includes('سُورَةٌ أَنْزَلْنَاهَا');
        const hasLeakedAyah2 = mainCardText.includes('الزَّانِيَةُ');

        // Check breadcrumb
        const breadcrumbText = document.querySelector('header')?.innerText || '';
        const bodyText = document.body.innerText;

        return {
          hasAyah11,
          hasLeakedAyah1,
          hasLeakedAyah2,
          currentAyahTextSample: mainCardText.substring(0, 60),
          isRuku2Active: bodyText.includes('রুকু ২') || bodyText.includes('আয়াত ১১')
        };
      })()
    `);

    auditResults.rukuIsolation = ruku2State;
    console.log(`✓ Ruku 2 Loaded: hasAyah11=${ruku2State.hasAyah11}, hasLeakedAyah1=${ruku2State.hasLeakedAyah1}, hasLeakedAyah2=${ruku2State.hasLeakedAyah2}`);
    console.log(`  Current displayed verse: "${ruku2State.currentAyahTextSample}..."`);

    // =========================================================================
    // TEST 3: 3-TIER SCOPE ISOLATION (SURAH, RUKU, AYAH)
    // =========================================================================
    console.log('\n--- 3. Testing 3-Tier Scope Isolation ---');

    // Tier 1: Surah Scope
    await cdp.evaluate(`
      (() => {
        // Click 'সূরা আলোচনা' button in Header
        const btns = Array.from(document.querySelectorAll('button'));
        const surahBtn = btns.find(b => b.innerText.includes('সূরা আলোচনা') || b.innerText.includes('সূরা'));
        if (surahBtn) surahBtn.click();
      })()
    `);
    await sleep(1500);

    const tier1State = await cdp.evaluate(`
      (() => {
        const text = document.body.innerText;
        const hasSurahBanner = text.includes('সূরা আন-নূর (২৪)') || text.includes('সূরা আন-নূরের পূর্ণাঙ্গ');
        const hasMindMap = text.includes('মাইন্ড ম্যাপ') || !!document.querySelector('svg');
        const hasRukuList = text.includes('সূরার রুকুভিত্তিক রূপরেখা') || text.includes('মোট ৯টি রুকু');
        
        // Strict guard: In Surah Scope, there should NOT be an individual Ayah card (.uthmani-text with ayah-end-symbol)
        const hasAyahCard = !!document.querySelector('.ayah-end-symbol');

        return {
          tier: 'surah',
          hasSurahBanner,
          hasMindMap,
          hasRukuList,
          hasAyahCardLeaked: hasAyahCard
        };
      })()
    `);
    console.log('Tier 1 (Surah Scope):', tier1State);

    // Tier 2: Ruku Scope
    await cdp.evaluate(`
      (() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const rukuBtn = btns.find(b => b.innerText.includes('রুকু আলোচনা') || b.innerText.includes('রুকু'));
        if (rukuBtn) rukuBtn.click();
      })()
    `);
    await sleep(1500);

    const tier2State = await cdp.evaluate(`
      (() => {
        const text = document.body.innerText;
        const hasMakasid = text.includes('ভূমিকা ও মাকাসিদ') || text.includes('মাকাসিদুশ শরীয়াহ');
        const hasMunasabat = text.includes('রাবত ও মুনাসাবাত');
        const hasAhkam = text.includes('ফিকহী আহকাম') || text.includes('আহকাম');
        const hasQiraatTab = text.includes('১০ কিরাআত সারণি');
        
        // Strict guard: In Ruku Scope, there should NOT be an individual Ayah card
        const hasAyahCard = !!document.querySelector('.ayah-end-symbol');

        return {
          tier: 'ruku',
          hasMakasid,
          hasMunasabat,
          hasAhkam,
          hasQiraatTab,
          hasAyahCardLeaked: hasAyahCard
        };
      })()
    `);
    console.log('Tier 2 (Ruku Scope):', tier2State);

    // Tier 3: Ayah Scope
    await cdp.evaluate(`
      (() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const ayahBtn = btns.find(b => b.innerText.includes('আয়াত স্টাডি') || b.innerText.includes('আয়াত'));
        if (ayahBtn) ayahBtn.click();
      })()
    `);
    await sleep(1500);

    const tier3State = await cdp.evaluate(`
      (() => {
        const text = document.body.innerText;
        const hasUthmani = !!document.querySelector('.uthmani-text');
        const hasJalalayn = text.includes('তাফসীরুল জালালাইন') || text.includes('আল-মাহাল্লী');
        const hasTahqeeqTable = text.includes('শাব্দিক তাহকীক') || !!document.querySelector('table');
        const hasTranslation = text.includes('বঙ্গানুবাদ');
        const hasWordTranslation = text.includes('শব্দানুগ অনুবাদ');

        return {
          tier: 'ayah',
          hasUthmani,
          hasJalalayn,
          hasTahqeeqTable,
          hasTranslation,
          hasWordTranslation
        };
      })()
    `);
    console.log('Tier 3 (Ayah Scope):', tier3State);

    auditResults.tierIsolation = {
      tier1_surah: tier1State,
      tier2_ruku: tier2State,
      tier3_ayah: tier3State
    };

    // =========================================================================
    // TEST 4: INTERLINEAR WORD TILES & CLICK-TO-TAHQEEQ INSPECTOR
    // =========================================================================
    console.log('\n--- 4. Testing Interlinear Word Tiles & Word Inspector ---');
    
    // Switch to Ayah 1 of Ruku 1
    await cdp.evaluate(`
      (() => {
        const select = document.querySelector('select[aria-label="রুকু নির্বাচন করুন"]');
        if (select) {
          select.value = '1';
          select.dispatchEvent(new Event('change', { bubbles: true }));
        }
      })()
    `);
    await sleep(1500);

    const wordTilesState = await cdp.evaluate(`
      (() => {
        const tiles = Array.from(document.querySelectorAll('.font-quran')).filter(el => !el.classList.contains('uthmani-text'));
        const tileTexts = tiles.map(t => t.innerText.trim());
        
        // Click the first word tile (e.g. سُورَةٌ)
        if (tiles.length > 0) {
          tiles[0].click();
        }

        return {
          tileCount: tiles.length,
          sampleTiles: tileTexts.slice(0, 5)
        };
      })()
    `);
    console.log('Word tiles count:', wordTilesState.tileCount, wordTilesState.sampleTiles);
    await sleep(1000);

    // Capture screenshot of Word Inspector Modal
    await cdp.captureScreenshot('screenshot_word_inspector_modal.png');

    // Check if Word Inspector Modal opened
    const modalState = await cdp.evaluate(`
      (() => {
        const hasModalTitle = document.body.innerText.includes('শাব্দিক তাহকীক ও রূপতত্ত্ব');
        const text = document.body.innerText;
        const hasRoot = text.includes('মূলবর্ণ (মাদ্দাহ)');
        const hasSighah = text.includes('সীগাহ ও বহছ') || text.includes('সীগা');
        
        // Close modal
        const closeBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('বন্ধ করুন') || b.title?.includes('বন্ধ'));
        if (closeBtn) closeBtn.click();

        return {
          isModalOpened: hasModalTitle,
          hasRoot,
          hasSighah
        };
      })()
    `);
    console.log('Word Inspector Modal state:', modalState);
    auditResults.wordInspector = {
      ...wordTilesState,
      ...modalState,
      screenshot: 'screenshot_word_inspector_modal.png'
    };

    // Save audit results to JSON
    fs.writeFileSync(
      path.join(ARTIFACT_DIR, 'audit_report.json'),
      JSON.stringify(auditResults, null, 2),
      'utf8'
    );
    console.log('\nAudit report saved to:', path.join(ARTIFACT_DIR, 'audit_report.json'));

    cdp.close();
  } catch (err) {
    console.error('Audit Error:', err);
  } finally {
    chromeProcess.kill();
  }
}

runAudit();
