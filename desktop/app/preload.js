const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('desk', {
  setInteractive: (on) => ipcRenderer.send('interactive', !!on),
  savePhoto: (name, dataUrl) => ipcRenderer.invoke('save-photo', name, dataUrl),
  onCfg: (cb) => ipcRenderer.on('cfg', (_e, cfg) => cb(cfg)),
});
