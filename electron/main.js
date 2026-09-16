// RMI Roof Visualizer — Electron main process.
// Opens index.html (the same file GitHub Pages serves) in a plain window: no menu bar, no browser chrome.
// Everything the page needs (three.js, GLTFLoader, fonts, models) is on relative paths, so it runs offline.
const { app, BrowserWindow, Menu, shell, dialog, ipcMain, nativeImage } = require('electron');
const path = require('path');
const fs = require('fs');

const TITLE = 'RMI Roof Visualizer';
const WIN = { width: 1400, height: 900, minWidth: 1024, minHeight: 640 };

function createWindow() {
  const win = new BrowserWindow({
    ...WIN,
    title: `${TITLE} ${app.getVersion()}`,   // version comes from package.json at runtime, so every bump shows here
    backgroundColor: '#12213A',
    autoHideMenuBar: true,
    show: false,
    icon: path.join(__dirname, '..', 'build', 'icon.png'),
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
    },
  });

  win.once('ready-to-show', () => win.show());
  // index.html sets its own <title>; keep the window named after the product and version.
  win.on('page-title-updated', (e) => e.preventDefault());
  // Any link that would open a new window goes to the rep's default browser instead.
  win.webContents.setWindowOpenHandler(({ url }) => { shell.openExternal(url); return { action: 'deny' }; });
  // No menu, so no Ctrl+Shift+I: F12 toggles DevTools for support.
  win.webContents.on('before-input-event', (_e, input) => {
    if (input.type === 'keyDown' && input.key === 'F12') win.webContents.toggleDevTools();
  });
  // RMI_DEBUG=1 mirrors the page's console to stdout (used by the build check; harmless otherwise).
  if (process.env.RMI_DEBUG) {
    win.webContents.on('console-message', ({ level, message, sourceId, lineNumber }) => {
      console.log(`[renderer:${level}] ${message} (${sourceId}:${lineNumber})`);
    });
    win.webContents.on('did-fail-load', (_e, code, desc, url) => console.log(`[did-fail-load] ${code} ${desc} ${url}`));
  }

  // RMI_SELFTEST=<png path>: build check for the packaged app. After load, pick the big-box drain, open the Drawing panel,
  // print its state (sheet number, loaded / missing) as JSON, save a screenshot of the window to that path, then quit.
  if (process.env.RMI_SELFTEST) {
    win.webContents.once('did-finish-load', async () => {
      const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
      try {
        await sleep(4000);
        await win.webContents.executeJavaScript("window.__rmi.selectBuilding('bigbox'); window.__rmi.finishCam(); window.__rmi.setStage(3,false); window.__rmi.S.prog=1;");
        await sleep(3000);
        await win.webContents.executeJavaScript("window.__rmi.goDetail('drain'); window.__rmi.finishCam(); window.__rmi.drawing.open(true);");
        await sleep(2500);
        const st = await win.webContents.executeJavaScript('JSON.stringify(window.__rmi.drawing.state())');
        console.log('[selftest] drawing panel', st);
        await sleep(500);
        console.log('[selftest] view', await win.webContents.executeJavaScript("window.__rmi.S.view + ' / ' + document.getElementById('app').className"));
        const img = await win.webContents.capturePage();
        fs.writeFileSync(process.env.RMI_SELFTEST, img.toPNG());
        console.log('[selftest] screenshot', process.env.RMI_SELFTEST);
      } catch (err) { console.log('[selftest] FAILED', err.message); }
      app.quit();
    });
  }

  // RMI_SELFTEST_PDF=<pdf path>: build check for the export. After load, pick the big-box retail building, load the four
  // sample photos, pin two of them, export every section straight to that path (no dialogs) and print the result, then quit.
  if (process.env.RMI_SELFTEST_PDF && !process.env.RMI_SELFTEST_EV) {   // with RMI_SELFTEST_EV the EagleView check below owns the export
    win.webContents.once('did-finish-load', async () => {
      const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
      try {
        await sleep(4000);
        await win.webContents.executeJavaScript("window.__rmiQuiet=true; window.__rmi.selectBuilding('bigbox'); window.__rmi.finishCam();");
        await sleep(3500);
        await win.webContents.executeJavaScript("window.__rmi.photos.samples()");
        await sleep(3500);
        await win.webContents.executeJavaScript("window.__rmi.photos.pin(0,0.64,0.5,'drain'); window.__rmi.photos.pin(0,0.28,0.74,'rtu'); window.__rmi.photos.pin(1,0.5,0.6,'coping'); window.__rmi.photos.slider(false); window.__rmi.finishCam();");
        await sleep(800);
        const r = await win.webContents.executeJavaScript("window.__rmi.pdf.export({ quiet:true, form:{ prospect:'Sample prospect', address:'123 Sample Street, Anytown', rep:'RMI rep', notes:'Selftest export from the packaged app.', sections:{ cover:true, config:true, stages:true, details:true, estimate:true, photos:true, notes:true, appendix:true } } })");
        console.log('[selftest] pdf', JSON.stringify(r));
        console.log('[selftest] state', JSON.stringify(await win.webContents.executeJavaScript('window.__rmi.pdf.state()')));
      } catch (err) { console.log('[selftest] FAILED', err.message); }
      app.quit();
    });
  }

  // RMI_SELFTEST_EV=<xml path>: build check for the EagleView import. After load, import that report the way the header button
  // would, print the import state as JSON, save a whole-roof screenshot at the finished stage to RMI_SELFTEST_PNG (or next to the
  // XML), export the PDF too when RMI_SELFTEST_PDF is set, then quit. The report stays where it is; nothing is copied.
  if (process.env.RMI_SELFTEST_EV && !process.env.RMI_SELFTEST_PROSPECT) {
    win.webContents.once('did-finish-load', async () => {
      const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
      const xml = process.env.RMI_SELFTEST_EV, png = process.env.RMI_SELFTEST_PNG || xml.replace(/\.[^.]+$/, '') + '-selftest.png';
      try {
        const [text, st] = await Promise.all([fs.promises.readFile(xml, 'utf8'), fs.promises.stat(xml)]);
        await sleep(3000);
        const ok = await win.webContents.executeJavaScript(`window.__rmiQuiet=true; window.__rmi.eagleview.import(${JSON.stringify(text)}, ${JSON.stringify(path.basename(xml))}, ${st.mtimeMs})`);
        console.log('[selftest] import', ok);
        await sleep(7000);
        await win.webContents.executeJavaScript("window.__rmi.finishCam(); window.__rmi.setStage(5,false); window.__rmi.S.prog=1;");
        await sleep(1500);
        console.log('[selftest] eagleview', await win.webContents.executeJavaScript('JSON.stringify(window.__rmi.eagleview.state())'));
        const img = await win.webContents.capturePage();
        fs.writeFileSync(png, img.toPNG());
        console.log('[selftest] screenshot', png);
        if (process.env.RMI_SELFTEST_PDF) {
          const r = await win.webContents.executeJavaScript("window.__rmi.pdf.export({ quiet:true, form:{ prospect:'Prospect roof', address:'', rep:'RMI rep', notes:'Selftest export of an EagleView prospect from the packaged app.', sections:{ cover:true, config:true, stages:true, details:true, estimate:true, photos:false, notes:true, appendix:true } } })");
          console.log('[selftest] pdf', JSON.stringify(r));
        }
      } catch (err) { console.log('[selftest] FAILED', err.message); }
      app.quit();
    });
  }

  // RMI_SELFTEST_PROSPECT=<work folder>: build check for saved prospects, in two launches of the same build. The work folder
  // is the prospects folder for the check; the rep's own settings and Documents are never touched (selftest userData).
  //   1. with RMI_SELFTEST_PROSPECT_XML=<report xml> and RMI_SELFTEST_PHOTOS=<a.jpg,b.jpg>: import the report, change the roof,
  //      finish, parapet height, one detail and Solar Post the way a rep would (form controls), empty the photo strip (the selftest
  //      profile keeps photos between runs), add the two photos and pin both,
  //      confirm five penetrations in the Penetrations panel (the first by changing its type), fill in the Save dialog and save.
  //      Writes before.json (window.__rmi.prospect.state()) and screenshots, then quits.
  //   2. without the XML: clear the photo strip and pick a plain building (nothing of the prospect left in memory), open the
  //      newest prospect from "Recent prospects" in the Open dialog, write after.json and compare it with before.json, save
  //      again (must update the same file in place), screenshots, print PASS or FAIL with the differences, then quit.
  if (process.env.RMI_SELFTEST_PROSPECT) {
    const work = path.resolve(process.env.RMI_SELFTEST_PROSPECT), xmlPath = process.env.RMI_SELFTEST_PROSPECT_XML, save = !!xmlPath;
    fs.mkdirSync(work, { recursive: true });
    if (save) fs.writeFileSync(path.join(app.getPath('userData'), 'settings.json'), JSON.stringify({ prospectsDir: work, recentProspects: [] }, null, 2));
    win.webContents.once('did-finish-load', async () => {
      const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
      const js = (code) => win.webContents.executeJavaScript(code);
      const idle = async (ms) => { await sleep(ms); for (let i = 0; i < 300 && await js('window.__rmi.prospect.busy()'); i++) await sleep(100); };
      const shot = async (name) => { const img = await win.webContents.capturePage(); fs.writeFileSync(path.join(work, name), img.toPNG()); console.log('[selftest] screenshot', name); };
      try {
        await sleep(4000);
        if (save) {
          const [text, st] = await Promise.all([fs.promises.readFile(xmlPath, 'utf8'), fs.promises.stat(xmlPath)]);
          console.log('[selftest] import', await js(`window.__rmiQuiet=true; window.__rmi.photos.clear(); window.__rmi.eagleview.import(${JSON.stringify(text)}, ${JSON.stringify(path.basename(xmlPath))}, ${st.mtimeMs})`));
          await sleep(7000);
          const change = (sel, v) => `(()=>{ const el=document.querySelector(${JSON.stringify(sel)}); el.value=${JSON.stringify(v)}; el.dispatchEvent(new Event('change')); })()`;
          await js(change('#roof', 'modbit')); await sleep(5000);
          await js("document.querySelector('#topcoat button[data-v=white]').click(); document.getElementById('solar').click();");
          await js(change('#evPH', '4')); await sleep(5000);
          await js("document.querySelectorAll('#detailChecks input')[1].click();");
          const photos = (process.env.RMI_SELFTEST_PHOTOS || '').split(',').filter(Boolean).slice(0, 2);
          const files = await Promise.all(photos.map(async (f) => ({ name: path.basename(f), b64: (await fs.promises.readFile(f)).toString('base64') })));
          await js(`window.__rmi.photos.add(${JSON.stringify(files)}.map(f=>new File([Uint8Array.from(atob(f.b64),c=>c.charCodeAt(0))],f.name,{type:'image/jpeg'})))`);
          await idle(3000);
          await js("(()=>{ const d=window.__rmi.eagleview.state().details; window.__rmi.photos.pin(0,0.32,0.46,d[0]); window.__rmi.photos.pin(0,0.7,0.62,d[d.length-1]); window.__rmi.photos.pin(1,0.5,0.55,d[Math.min(2,d.length-1)]); window.__rmi.photos.slider(false); })()");
          await js('window.__rmi.eagleview.open(true)'); await sleep(500);
          await js("(()=>{ const s=document.querySelector('#evList .evrow select'); s.value=[...s.options].map(o=>o.value).find(v=>v!==s.value); s.dispatchEvent(new Event('change')); })()"); await sleep(5000);
          for (let i = 1; i <= 4; i++) { await js(`document.querySelectorAll('#evList .evrow input[type=checkbox]')[${i}].click()`); await sleep(300); }
          await js("window.__rmi.finishCam(); document.getElementById('saveBtn').click();"); await sleep(600);
          await js("Object.entries({ sName:'Selftest prospect', sAddress:'Sample address', sRep:'RMI rep', sNotes:'Selftest round trip: two photos pinned, five penetrations confirmed.' }).forEach(([id,v])=>{ document.getElementById(id).value=v; })");
          await shot('1-save-dialog.png');
          await js("document.getElementById('sGo').click()"); await idle(800);
          console.log('[selftest] save status', await js("document.getElementById('sStatus').textContent"));
          await shot('2-saved.png');
          const before = await js('JSON.stringify(window.__rmi.prospect.state())');
          fs.writeFileSync(path.join(work, 'before.json'), before);
          const b = JSON.parse(before);
          console.log('[selftest] before', JSON.stringify({ path: b.path, building: b.building, roof: b.roof, topcoat: b.topcoat, solar: b.solar, parapet: b.eagleview && b.eagleview.parapet_height_ft, confirmed: b.eagleview && b.eagleview.confirmed, photos: b.photos.map((p) => [p.name, p.pins.length]), dirty: b.dirty }));
        } else {
          await js("window.__rmiQuiet=true; window.__rmi.photos.clear(); window.__rmi.selectBuilding('warehouse');"); await sleep(3000);
          console.log('[selftest] cleared', await js("JSON.stringify({ building: window.__rmi.S.building, photos: window.__rmi.photos.state().photos.length, report: !!window.__rmi.prospect.state().eagleview })"));
          await js("document.getElementById('openBtn').click()"); await sleep(1500);
          console.log('[selftest] recent', await js("JSON.stringify([...document.querySelectorAll('#oList .rrow')].map(r=>r.innerText.replace(/\\s+/g,' ')))"));
          await shot('3-open-dialog.png');
          await js("document.querySelector('#oList .rrow').click()"); await idle(3000); await sleep(6000);
          const after = await js('JSON.stringify(window.__rmi.prospect.state())');
          fs.writeFileSync(path.join(work, 'after.json'), after);
          await js('window.__rmi.finishCam(); window.__rmi.setStage(5,false);'); await sleep(1500);
          await shot('4-opened-roof.png');
          await js('window.__rmi.photos.select(0)'); await sleep(1200); await shot('5-opened-photo.png');
          // compare: everything except the unsaved-changes flag must match
          const before = JSON.parse(fs.readFileSync(path.join(work, 'before.json'), 'utf8')), a = JSON.parse(after), diffs = [];
          const walk = (x, y, at) => { if (at === '.dirty') return; if (x && y && typeof x === 'object' && typeof y === 'object') { new Set([...Object.keys(x), ...Object.keys(y)]).forEach((k) => walk(x[k], y[k], `${at}.${k}`)); } else if (JSON.stringify(x) !== JSON.stringify(y)) diffs.push(`${at}: ${JSON.stringify(x)} → ${JSON.stringify(y)}`); };
          walk(before, a, '');
          const again = JSON.parse(await js("(async()=>{ document.getElementById('saveBtn').click(); await new Promise(r=>setTimeout(r,500)); return JSON.stringify(await window.__rmi.prospect.save()); })()"));
          const files = fs.readdirSync(work).filter((f) => f.endsWith('.rmiproject'));
          console.log('[selftest] resave', JSON.stringify({ path: again.path, same: again.path === before.path, replaced: again.replaced, files }));
          const pass = !diffs.length && again.ok && again.path === before.path && again.replaced && files.length === 1;
          console.log('[selftest] after', JSON.stringify({ building: a.building, roof: a.roof, topcoat: a.topcoat, solar: a.solar, parapet: a.eagleview && a.eagleview.parapet_height_ft, confirmed: a.eagleview && a.eagleview.confirmed, photos: a.photos.map((p) => [p.name, p.status, p.pins.length]), dirty: a.dirty }));
          console.log(`[selftest] round trip ${pass ? 'PASS' : 'FAIL'}${diffs.length ? '\n  ' + diffs.slice(0, 40).join('\n  ') : ''}`);
          fs.writeFileSync(path.join(work, 'result.txt'), `${pass ? 'PASS' : 'FAIL'}\n${diffs.join('\n')}\n`);
        }
      } catch (err) { console.log('[selftest] FAILED', err.message); }
      app.quit();
    });
  }

  win.loadFile(path.join(__dirname, '..', 'index.html'));
  return win;
}

// The build checks (RMI_SELFTEST*) run in their own userData folder: they never touch the rep's photo store, and they do not
// collide with an installed copy of the app that may be open (the single-instance lock is per userData folder).
if (process.env.RMI_SELFTEST || process.env.RMI_SELFTEST_PDF || process.env.RMI_SELFTEST_EV || process.env.RMI_SELFTEST_PROSPECT) app.setPath('userData', path.join(app.getPath('temp'), 'rmi-roof-visualizer-selftest'));
// One window per machine: a second launch focuses the running one.
if (!app.requestSingleInstanceLock()) {
  app.quit();
} else {
  app.on('second-instance', () => {
    const [win] = BrowserWindow.getAllWindows();
    if (win) { if (win.isMinimized()) win.restore(); win.focus(); }
  });
  Menu.setApplicationMenu(null);
  // Prospect photos: the page asks for a native open dialog (window.rmiDesktop.pickPhotos) and gets the files back as
  // bytes. They are read once into the page's memory; nothing is copied, cached or written anywhere (phase 1: in memory only).
  ipcMain.handle('rmi:pick-photos', async (e) => {
    const win = BrowserWindow.fromWebContents(e.sender);
    const r = await dialog.showOpenDialog(win, {
      title: 'Add prospect photos',
      properties: ['openFile', 'multiSelections'],
      filters: [{ name: 'Photos (JPG, PNG, HEIC)', extensions: ['jpg', 'jpeg', 'png', 'heic', 'heif'] }, { name: 'All files', extensions: ['*'] }],
    });
    if (r.canceled) return [];
    const out = [];
    for (const fp of r.filePaths) {
      try { const data = await fs.promises.readFile(fp); out.push({ name: path.basename(fp), size: data.length, data }); }
      catch (err) { out.push({ name: path.basename(fp), size: 0, data: null, error: err.message }); }
    }
    return out;
  });
  // EagleView import: the page asks for a native open dialog (window.rmiDesktop.pickEagleView) and gets the report XML back as
  // text with the file's date (the XML itself carries no report date). Read once into the page's memory; nothing is stored.
  ipcMain.handle('rmi:pick-eagleview', async (e) => {
    const win = BrowserWindow.fromWebContents(e.sender);
    const r = await dialog.showOpenDialog(win, {
      title: 'Import EagleView report',
      properties: ['openFile'],
      filters: [{ name: 'EagleView report (XML)', extensions: ['xml'] }, { name: 'All files', extensions: ['*'] }],
    });
    if (r.canceled || !r.filePaths.length) return null;
    const fp = r.filePaths[0];
    try { const [text, st] = await Promise.all([fs.promises.readFile(fp, 'utf8'), fs.promises.stat(fp)]); return { name: path.basename(fp), text, mtime: st.mtimeMs, size: st.size }; }
    catch (err) { return { name: path.basename(fp), error: err.message }; }
  });
  // PDF export: the page has built the document into #pdfDoc and set body.pdf, so print media shows only that. Ask where to
  // save (Documents by default, the page's suggested <prospect>-<date>.pdf), print with Chromium's printToPDF (Letter,
  // CSS @page margins, a running footer with page numbers) and write the bytes. RMI_SELFTEST_PDF skips the dialog and
  // writes straight to that path (the build check). Only the file written here can be opened back through rmi:open-path.
  let lastPdf = null;
  ipcMain.handle('rmi:export-pdf', async (e, opt) => {
    const win = BrowserWindow.fromWebContents(e.sender);
    const suggested = String((opt && opt.suggested) || 'prospect.pdf').replace(/[\/:*?"<>|]+/g, '-');
    let file = process.env.RMI_SELFTEST_PDF || null;
    if (!file) {
      const r = await dialog.showSaveDialog(win, {
        title: 'Export PDF', defaultPath: path.join(app.getPath('documents'), suggested),
        filters: [{ name: 'PDF', extensions: ['pdf'] }],
      });
      if (r.canceled || !r.filePath) return { canceled: true };
      file = r.filePath;
    }
    try {
      const footer = String((opt && opt.footer) || 'RMI Roof Visualizer').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
      // The window's navy backgroundColor would fill the page margins, so the print runs on white (the page covers the window
      // completely, so nothing visible changes).
      win.setBackgroundColor('#FFFFFF');
      // Running header: the RMI logo, top right. Header templates can't load files, so it goes in as a small data URI.
      const logo = nativeImage.createFromPath(path.join(__dirname, '..', 'assets', 'rmi-logo.png'));
      const logoTag = logo.isEmpty() ? '' : `<img src="${logo.resize({ height: 72 }).toDataURL()}" style="height:24px;width:auto">`;
      const data = await win.webContents.printToPDF({
        pageSize: 'Letter', printBackground: true, preferCSSPageSize: true, displayHeaderFooter: true,
        headerTemplate: `<div style="width:100%;margin:0 0.6in;display:flex;justify-content:flex-end;-webkit-print-color-adjust:exact">${logoTag}</div>`,
        footerTemplate: `<div style="width:100%;margin:0 0.6in;font-family:Arial,Helvetica,sans-serif;font-size:7.5px;color:#6B7684;display:flex;justify-content:space-between"><span>${footer}</span><span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>`,
      });
      win.setBackgroundColor('#12213A');
      await fs.promises.writeFile(file, data);
      lastPdf = file;
      return { path: file, bytes: data.length };
    } catch (err) { win.setBackgroundColor('#12213A'); return { error: err.message }; }
  });
  ipcMain.handle('rmi:open-path', async (_e, p) => { if (!lastPdf || p !== lastPdf) return 'not a file exported this session'; return shell.openPath(lastPdf); });

  // Saved prospects (§2 #11): the page packs one .rmiproject file per prospect (a zip: prospect.json, the EagleView XML, the
  // photos) and main writes it into the prospects folder — chosen once and remembered in settings.json in userData, default
  // Documents\RMI Prospects — where the recent list lives too. main reads only files the rep picked or saved this session or
  // that are on the recent list, and never overwrites another prospect's file. Nothing leaves the machine.
  const EXT = '.rmiproject', RECENT_MAX = 12;
  const settingsFile = () => path.join(app.getPath('userData'), 'settings.json');
  const readSettings = () => { try { return JSON.parse(fs.readFileSync(settingsFile(), 'utf8')) || {}; } catch (_) { return {}; } };
  const writeSettings = (s) => { fs.mkdirSync(path.dirname(settingsFile()), { recursive: true }); fs.writeFileSync(settingsFile(), JSON.stringify(s, null, 2)); };
  const defaultDir = () => path.join(app.getPath('documents'), 'RMI Prospects');
  const prospectDir = () => readSettings().prospectsDir || defaultDir();
  // the same file-name rule as prFileName() in index.html
  const safeName = (n) => String(n || '').replace(/[\\/:*?"<>|\x00-\x1f]+/g, '-').replace(/\s+/g, ' ').replace(/-+/g, '-').trim().slice(0, 80).replace(/^[-. ]+|[-. ]+$/g, '') || 'Prospect';
  const same = (a, b) => path.resolve(a).toLowerCase() === path.resolve(b).toLowerCase();   // Windows paths ignore case
  const touched = [];   // prospect files picked or written this session
  const known = (p) => typeof p === 'string' && p.toLowerCase().endsWith(EXT) && (touched.some((t) => same(t, p)) || (readSettings().recentProspects || []).some((r) => same(r.path, p)));
  const remember = (p, meta, action) => {
    const s = readSettings(), list = (s.recentProspects || []).filter((r) => !same(r.path, p));
    list.unshift({ path: p, name: (meta && meta.name) || path.basename(p, EXT), meta: meta || null, at: Date.now(), action });
    s.recentProspects = list.slice(0, RECENT_MAX); writeSettings(s);
  };
  ipcMain.handle('rmi:prospect-folder', () => { const s = readSettings(); return { dir: s.prospectsDir || defaultDir(), chosen: !!s.prospectsDir }; });
  ipcMain.handle('rmi:prospect-choose-folder', async (e) => {
    const win = BrowserWindow.fromWebContents(e.sender), cur = prospectDir();
    const r = await dialog.showOpenDialog(win, { title: 'Folder for saved prospects', defaultPath: fs.existsSync(cur) ? cur : app.getPath('documents'), properties: ['openDirectory', 'createDirectory'] });
    if (r.canceled || !r.filePaths.length) return { canceled: true };
    const s = readSettings(); s.prospectsDir = r.filePaths[0]; writeSettings(s);
    return { dir: s.prospectsDir };
  });
  ipcMain.handle('rmi:prospect-save', async (_e, opt) => {
    try {
      const data = opt && opt.data; if (!data || !data.length) return { error: 'nothing to save' };
      const s = readSettings(), dir = s.prospectsDir || defaultDir();
      await fs.promises.mkdir(dir, { recursive: true });
      const base = safeName(opt.name); let file = path.join(dir, base + EXT), replaced = false;
      if (opt.replace && known(opt.replace) && same(opt.replace, file)) replaced = fs.existsSync(file);   // the file this prospect was opened from or last saved to: update it in place
      else for (let i = 2; fs.existsSync(file); i++) file = path.join(dir, `${base} (${i})${EXT}`);   // any other file of that name belongs to another prospect
      const buf = Buffer.from(data.buffer, data.byteOffset, data.byteLength), tmp = file + '.saving';
      await fs.promises.writeFile(tmp, buf);
      try { await fs.promises.rename(tmp, file); }   // a finished file or none: a crash mid-write never leaves half a prospect
      catch (_) { await fs.promises.writeFile(file, buf); await fs.promises.unlink(tmp).catch(() => {}); }   // a sync client holding the old file: write over it directly
      if (!s.prospectsDir) { s.prospectsDir = dir; writeSettings(s); }   // the first save settles the default as the chosen folder
      touched.push(file); remember(file, opt.meta, 'saved');
      return { path: file, bytes: buf.length, replaced };
    } catch (err) { return { error: err.message }; }
  });
  ipcMain.handle('rmi:prospect-pick', async (e) => {
    const win = BrowserWindow.fromWebContents(e.sender), dir = prospectDir();
    const r = await dialog.showOpenDialog(win, { title: 'Open prospect', defaultPath: fs.existsSync(dir) ? dir : app.getPath('documents'), properties: ['openFile'], filters: [{ name: 'RMI prospect', extensions: ['rmiproject'] }] });
    if (r.canceled || !r.filePaths.length) return null;
    const fp = r.filePaths[0];
    try { const data = await fs.promises.readFile(fp); touched.push(fp); return { path: fp, name: path.basename(fp), data }; }
    catch (err) { return { name: path.basename(fp), error: err.message }; }
  });
  ipcMain.handle('rmi:prospect-read', async (_e, p) => {
    if (!known(p)) return { error: 'not a prospect saved or opened on this computer' };
    try { const data = await fs.promises.readFile(p); return { path: p, name: path.basename(p), data }; }
    catch (err) { return { error: err.code === 'ENOENT' ? 'the file is no longer there (moved, renamed or deleted)' : err.message }; }
  });
  ipcMain.handle('rmi:prospect-recent', async () => {
    const list = readSettings().recentProspects || [];
    const here = await Promise.all(list.map((r) => fs.promises.access(r.path).then(() => true, () => false)));
    return list.filter((_, i) => here[i]);   // a file on a shared drive that is offline stays in settings and shows again when the drive is back
  });
  ipcMain.handle('rmi:prospect-remember', (_e, p, meta) => { if (!known(p)) return false; remember(p, meta, 'opened'); return true; });
  ipcMain.handle('rmi:prospect-forget', (_e, p) => { const s = readSettings(); s.recentProspects = (s.recentProspects || []).filter((r) => typeof p === 'string' && !same(r.path, p)); writeSettings(s); return true; });
  app.whenReady().then(createWindow);
  app.on('window-all-closed', () => app.quit());
}
