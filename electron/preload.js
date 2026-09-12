// Runs before index.html with access to a small, sandboxed slice of Electron.
// Exposes only what the page might want to know; file dialogs / PDF export hooks land here later.
const { contextBridge } = require('electron');

contextBridge.exposeInMainWorld('rmiDesktop', {
  platform: process.platform,
  electron: process.versions.electron,
});
