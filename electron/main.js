// RMI Roof Visualizer — Electron main process.
// Opens index.html (the same file GitHub Pages serves) in a plain window: no menu bar, no browser chrome.
// Everything the page needs (three.js, GLTFLoader, fonts, models) is on relative paths, so it runs offline.
const { app, BrowserWindow, Menu, shell } = require('electron');
const path = require('path');

const TITLE = 'RMI Roof Visualizer';
const WIN = { width: 1400, height: 900, minWidth: 1024, minHeight: 640 };

function createWindow() {
  const win = new BrowserWindow({
    ...WIN,
    title: TITLE,
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
  // index.html sets its own <title>; keep the window named after the product.
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
  app.whenReady().then(createWindow);
  app.on('window-all-closed', () => app.quit());
}
