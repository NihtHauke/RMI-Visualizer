// Runs before index.html with access to a small, sandboxed slice of Electron.
// Exposes only what the page needs: the photo and report pickers, the PDF export bridge and saved prospects.
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('rmiDesktop', {
  platform: process.platform,
  electron: process.versions.electron,
  // Native "Add photos" dialog. Resolves to [{ name, size, data: Uint8Array }] (empty when cancelled).
  // The bytes come straight from the rep's disk into the page's memory — nothing is copied or stored anywhere.
  pickPhotos: () => ipcRenderer.invoke('rmi:pick-photos'),
  // "Load sample photos": the four sample roofs bundled with the app. The page passes their names (SAMPLES in index.html);
  // main reads them out of samples/ and returns [{ name, size, data: Uint8Array }] — fetch() cannot read inside app.asar.
  samplePhotos: (names) => ipcRenderer.invoke('rmi:sample-photos', names),
  // Native "Import EagleView report" dialog. Resolves to { name, text, mtime } (null when cancelled, { name, error } when unreadable).
  // The XML is read once into the page's memory; nothing is copied, cached or written anywhere.
  pickEagleView: () => ipcRenderer.invoke('rmi:pick-eagleview'),
  // PDF export. The page has already built the document and switched the print CSS on (body.pdf); main shows the save dialog
  // (suggested name <prospect>-<date>.pdf), prints the page with printToPDF and writes the file. Resolves to
  // { path } | { canceled: true } | { error }. `footer` is the running footer text (page numbers are added).
  exportPdf: (opt) => ipcRenderer.invoke('rmi:export-pdf', opt || {}),
  // Opens the PDF this session last exported in the rep's default viewer (main only opens that file).
  openPath: (p) => ipcRenderer.invoke('rmi:open-path', p),
  // Saved prospects: one .rmiproject file per prospect in a folder chosen once and remembered (default Documents\RMI Prospects).
  // The page packs the file; main writes and reads it and keeps the recent list in the app's settings. Nothing is uploaded.
  prospects: {
    folder: () => ipcRenderer.invoke('rmi:prospect-folder'),                 // { dir, chosen }
    chooseFolder: () => ipcRenderer.invoke('rmi:prospect-choose-folder'),    // { dir } | { canceled: true }
    save: (opt) => ipcRenderer.invoke('rmi:prospect-save', opt || {}),        // { name, data: Uint8Array, replace, meta } → { path, bytes, replaced } | { error }
    pick: () => ipcRenderer.invoke('rmi:prospect-pick'),                      // native Open dialog → { path, name, data } | null | { name, error }
    read: (p) => ipcRenderer.invoke('rmi:prospect-read', p),                  // a recent (or this session's) prospect → { path, name, data } | { error }
    recent: () => ipcRenderer.invoke('rmi:prospect-recent'),                  // [{ path, name, meta, at, action }] newest first, files that still exist
    remember: (p, meta) => ipcRenderer.invoke('rmi:prospect-remember', p, meta),
    forget: (p) => ipcRenderer.invoke('rmi:prospect-forget', p),
  },
});
