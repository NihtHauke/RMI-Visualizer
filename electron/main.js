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
  if (process.env.RMI_SELFTEST_PDF) {
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

  win.loadFile(path.join(__dirname, '..', 'index.html'));
  return win;
}

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
  app.whenReady().then(createWindow);
  app.on('window-all-closed', () => app.quit());
}
