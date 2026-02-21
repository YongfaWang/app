const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('electronAPI', {
  runPython: ({ pythonPath, scriptPath }) =>
    ipcRenderer.invoke('runPython', { pythonPath, scriptPath }),
  getAppPath: () =>
    ipcRenderer.invoke('getAppPath'),
  saveXml: ({ filePath, content }) =>
    ipcRenderer.invoke('saveXml', { filePath, content }),
  pythonOutput: (callback) =>
    ipcRenderer.on('pythonOutput', (event, data) => callback(data)),
  pythonEnd: (callback) =>
    ipcRenderer.on('pythonEnd', (event, data) => callback(data)),
  readXml: (filePath) =>
    ipcRenderer.invoke('readXml', filePath),
  readResourcesFileToString: (filePath) =>
    ipcRenderer.invoke('readResourcesFileToString', filePath),
  removeAllListeners: (channel) =>
    ipcRenderer.removeAllListeners(channel),
  openH5Complete: (callback) =>
    ipcRenderer.on('openH5Complete', (event, files) =>
      callback(event, files)),
  openH5: () =>
    ipcRenderer.send('openH5'),
  readH5Dataset: ({ filePath, datasetPath }) =>
    ipcRenderer.invoke("readH5Dataset", { filePath, datasetPath }),
  readH5: ({ filePath }) =>
    ipcRenderer.invoke("readH5", { filePath }),
  fullScreen: (data) =>
    ipcRenderer.send('fullScreen', data),
  quit: () =>
    ipcRenderer.send('quit'),
  searchPythonPaths: () =>
    ipcRenderer.invoke('searchPythonPaths'),
  openDirectory: () =>
    ipcRenderer.invoke('openDirectory'),
})
