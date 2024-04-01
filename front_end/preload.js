const { ipcRenderer, contextBridge } = require('electron');

// 向渲染进程暴露 Electron API，以便于与主进程通信
contextBridge.exposeInMainWorld('electron', {
  // 示例函数，用于与主进程通信
  sendToMainProcess: (channel, data) => {
    ipcRenderer.send(channel, data);
  }
});
