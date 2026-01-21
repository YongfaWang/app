// 'use strict'

const { app, protocol, BrowserWindow, Menu, ipcMain, dialog } = require('electron')
const { spawn } = require('child_process');
const path = require('path')
const fs = require('fs')
const ini = require('ini')
const { URL } = require('url')
// ############ 测试环境在打包时注释 ############
// const { default: installExtension, VUEJS3_DEVTOOLS } = require('electron-devtools-installer/dist');
// ############ 测试环境在打包时注释 ############
// const { createProtocol } = require('vue-cli-plugin-electron-builder/lib')
const isDevelopment = process.env.NODE_ENV !== 'production'
var window;

function createProtocol(scheme, customProtocol) {
  (customProtocol || protocol).registerBufferProtocol(
    scheme,
    (request, respond) => {
      let pathName = new URL(request.url).pathname
      pathName = decodeURI(pathName) // Needed in case URL contains spaces

      fs.readFile(path.join(__dirname, pathName), (error, data) => {
        if (error) {
          console.error(
            `Failed to read ${pathName} on ${scheme} protocol`,
            error
          )
        }
        const extension = path.extname(pathName).toLowerCase()
        let mimeType = ''

        if (extension === '.js') {
          mimeType = 'text/javascript'
        } else if (extension === '.html') {
          mimeType = 'text/html'
        } else if (extension === '.css') {
          mimeType = 'text/css'
        } else if (extension === '.svg' || extension === '.svgz') {
          mimeType = 'image/svg+xml'
        } else if (extension === '.json') {
          mimeType = 'application/json'
        } else if (extension === '.wasm') {
          mimeType = 'application/wasm'
        }

        respond({ mimeType, data })
      })
    }
  )
}

// Scheme must be registered before the app is ready
protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { secure: true, standard: true } }
])
async function createWindow() {
  // Create the browser window.
  window = new BrowserWindow({
    width: 1200,
    height: 700,
    minHeight: 650,
    minWidth: 1150,
    webPreferences: {

      // Use pluginOptions.nodeIntegration, leave this alone
      // See nklayman.github.io/vue-cli-plugin-electron-builder/guide/security.html#node-integration for more info
      nodeIntegration: process.env.ELECTRON_NODE_INTEGRATION,
      contextIsolation: !process.env.ELECTRON_NODE_INTEGRATION
    }
  })
  if (process.env.WEBPACK_DEV_SERVER_URL) {
    // Load the url of the dev server if in development mode
    await window.loadURL(process.env.WEBPACK_DEV_SERVER_URL)
    // 打开开发者工具
    // if (!process.env.IS_TEST) window.webContents.openDevTools()
    console.log("aaaaaaaaaaaaaa");
  } else {
    console.log("bbbbbbbbbbbbbb");

    // ############ 测试环境在打包时注释 ############
    createProtocol('app')
    // Load the index.html when not in development
    window.loadURL('app://./index.html')
    // window.loadURL('http://localhost:8080/')
  }
  // 关闭菜单栏
  // Menu.setApplicationMenu(null);
}

// Quit when all windows are closed.
app.on('window-all-closed', () => {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') {
    app.quit()
  }
})
ipcMain.on('quit', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})
ipcMain.on('fullScreen', (event, data) => {
  window.setFullScreen(data.isFullScreen)
})

ipcMain.handle('getAppPath', () => {
  return app.getAppPath()
})
ipcMain.handle('readIni', async (event, filePath) => {
  try {
    const dataStr = await fs.promises.readFile(filePath, "utf8");
    return ini.parse(dataStr); // 直接返回解析结果
  } catch (err) {
    return reject(err.message);
  }
})
ipcMain.handle('saveXml', async (event, { filePath, content }) => {
  console.log("filePath: ", filePath);
  console.log("content: ", content);
  try {
    const iniString = ini.stringify(content);
    console.log(iniString);
    fs.writeFileSync(filePath, iniString, 'utf-8');
    return true;
  } catch (error) {
    return false;
  }
})

/**
 * 执行Python脚本
 */
ipcMain.handle('run-python', (event, scriptPath) => {
  console.log("scriptPath: ", scriptPath);
  const pythonProcess = spawn('python', [scriptPath]);

  pythonProcess.stdout.on('data', (data) => {
    event.sender.send('python-output', data.toString());
  });

  pythonProcess.stderr.on('data', (data) => {
    event.sender.send('python-output', data.toString());
  });

  pythonProcess.on('close', () => {
    event.sender.send('python-end');
  });

  return new Promise((resolve) => {
    pythonProcess.on('exit', resolve);
  });
});

app.on('activate', () => {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) createWindow()
})

ipcMain.on('openH5', (event) => {
  dialog.showOpenDialog({
    properties: ['openFile']
  }).then(result => {
    if (!result.canceled) {
      event.sender.send('openH5Complete', result.filePaths);
    }
  }).catch(err => {
    console.log(err);
  });
})

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', async () => {
  // ############ 测试环境在打包时注释 ############
  // if (isDevelopment && !process.env.IS_TEST) {
  //   // Install Vue Devtools
  //   try {
  //     await installExtension(VUEJS3_DEVTOOLS)
  //   } catch (e) {
  //     console.error('Vue Devtools failed to install:', e.toString())
  //   }
  // }
  createWindow()
})

// Exit cleanly on request from parent process in development mode.
if (isDevelopment) {
  if (process.platform === 'win32') {
    process.on('message', (data) => {
      if (data === 'graceful-exit') {
        app.quit()
      }
    })
  } else {
    process.on('SIGTERM', () => {
      app.quit()
    })
  }
}
