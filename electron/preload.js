// Runs before index.html with access to a small, sandboxed slice of Electron.
// Exposes only what the page needs: the photo picker and the PDF export bridge.
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('rmiDesktop', {
  platform: process.platform,
  electron: process.versions.electron,
  // Native "Add photos" dialog. Resolves to [{ name, size, data: Uint8Array }] (empty when cancelled).
  // The bytes come straight from the rep's disk into the page's memory — nothing is copied or stored anywhere.
  pickPhotos: () => ipcRenderer.invoke('rmi:pick-photos'),
  // PDF export. The page has already built the document and switched the print CSS on (body.pdf); main shows the save dialog
  // (suggested name <prospect>-<date>.pdf), prints the page with printToPDF and writes the file. Resolves to
  // { path } | { canceled: true } | { error }. `footer` is the running footer text (page numbers are added).
  exportPdf: (opt) => ipcRenderer.invoke('rmi:export-pdf', opt || {}),
  // Opens the PDF this session last exported in the rep's default viewer (main only opens that file).
  openPath: (p) => ipcRenderer.invoke('rmi:open-path', p),
});
