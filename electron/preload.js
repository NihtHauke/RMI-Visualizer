// Runs before index.html with access to a small, sandboxed slice of Electron.
// Exposes only what the page needs; PDF export hooks land here later.
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('rmiDesktop', {
  platform: process.platform,
  electron: process.versions.electron,
  // Native "Add photos" dialog. Resolves to [{ name, size, data: Uint8Array }] (empty when cancelled).
  // The bytes come straight from the rep's disk into the page's memory — nothing is copied or stored anywhere.
  pickPhotos: () => ipcRenderer.invoke('rmi:pick-photos'),
});
