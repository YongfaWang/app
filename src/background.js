// 'use strict'

const { app, protocol, BrowserWindow, ipcMain, dialog } = require('electron')
const { spawn, exec } = require('child_process');
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
var isShowMenu = true;
const isDev = !app.isPackaged

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
    autoHideMenuBar: isShowMenu ? false : true,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),

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
  if (!isShowMenu) { window.setMenu(null) }
  // 禁用快捷键
  window.webContents.on('before-input-event', (event, input) => {
    const isClose =
      (input.control || input.meta) && input.key.toLowerCase() === 'w'
    const isRefresh =
      (input.control || input.meta) && input.key.toLowerCase() === 'r'
    const isQuit =
      (input.control || input.meta) && input.key.toLowerCase() === 'q'
    const isZoomIn =
      (input.control || input.meta) && input.key.toLowerCase() === '+'
    const isZoomOut =
      (input.control || input.meta) && input.key.toLowerCase() === '-'

    if (isClose || isRefresh || isQuit || isZoomIn || isZoomOut) {
      event.preventDefault()
    }
  })
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

ipcMain.handle('openDirectory', async () => {
  const result = await dialog.showOpenDialog({
    properties: ['openDirectory']
  });
  return result;
});
const xml2js = require("xml2js")
async function parseXMLConfig(filepath) {
  // 读取XML文件
  var data = await fs.promises.readFile(filepath, "utf8")

  // 解析XML
  const parser = new xml2js.Parser({
    explicitArray: false,
    mergeAttrs: true,
    explicitRoot: false
  });
  const result = await parser.parseStringPromise(data)
  // parser.parseString(data, (err, result) => {
  //     // 处理解析结果，转换_options为数组

  //   });
  const processedResult = processXMLObject(result);
  return processedResult
}

function processXMLObject(obj) {
  if (obj === null || typeof obj !== 'object') {
    return obj;
  }

  // 如果是数组，递归处理每个元素
  if (Array.isArray(obj)) {
    return obj.map(item => processXMLObject(item));
  }

  const result = {};

  // 遍历对象的所有属性
  for (const key in obj) {
    if (Object.prototype.hasOwnProperty.call(obj, key)) {
      const value = obj[key];

      // 特殊处理_options，将其转换为数组
      if (key === '_options') {
        if (typeof value === 'string') {
          result[key] = value.split(',').map(item => item.trim());
        } else {
          result[key] = processXMLObject(value);
        }
      } else {
        // 递归处理其他属性
        if (typeof value === 'object' && value !== null) {
          result[key] = processXMLObject(value);
        } else {
          result[key] = value;
        }
      }
    }
  }

  return result;
}

// 保存配置对象的方法
function saveConfigToFile(config, filepath) {
  return new Promise((resolve, reject) => {
    // 将配置对象转换回XML格式
    const builder = new xml2js.Builder({
      rootName: 'data',
      renderOpts: { 'pretty': true, 'indent': '  ' },
      xmldec: { version: '1.0', encoding: 'utf-8' }
    });

    // 在保存前，将数组类型的_options转换回字符串
    const xmlReadyConfig = prepareForXML(config);
    const xml = builder.buildObject(xmlReadyConfig);

    // 写入文件
    fs.writeFile(filepath, xml, 'utf8', (err) => {
      if (err) {
        reject(err);
      } else {
        resolve();
      }
    });
  });
}

function prepareForXML(obj) {
  if (obj === null || typeof obj !== 'object') {
    return obj;
  }

  if (Array.isArray(obj)) {
    return obj.map(item => prepareForXML(item));
  }

  const result = {};

  for (const key in obj) {
    if (Object.prototype.hasOwnProperty.call(obj, key)) {
      const value = obj[key];

      // 将数组类型的_options转换回字符串
      if (key === '_options' && Array.isArray(value)) {
        result[key] = value.join(',');
      } else if (typeof value === 'object' && value !== null) {
        result[key] = prepareForXML(value);
      } else {
        result[key] = value;
      }
    }
  }

  return result;
}
ipcMain.handle('readXml', async (event, filePath) => {
  console.log(filePath);

  const dataStr = await parseXMLConfig(filePath);
  return dataStr;
})

ipcMain.handle('readIni', async (event, filePath) => {
  try {
    const dataStr = await fs.promises.readFile(filePath, "utf8");
    return ini.parse(dataStr); // 直接返回解析结果
  } catch (err) {
    return err.message;
  }


  // try {
  //   const dataStr = await fs.promises.readFile(filePath, "utf8");
  //   console.log(dataStr.replaceAll("\\\n", "").replace(/\([^)]*\)/g, match => match.replace(/,\n/g, ',')));
  //   return ini.parse(dataStr); // 直接返回解析结果
  // } catch (err) {
  //   return reject(err.message);
  // }

})
ipcMain.handle('saveXml', async (event, { filePath, content }) => {
  try {
    const iniString = ini.stringify(content);
    console.log(iniString);
    fs.writeFileSync(filePath, iniString, 'utf-8');
    saveConfigToFile(content, filePath)
    return true;
  } catch (error) {
    return false;
  }
})
/**
 * 执行Python脚本
 */
ipcMain.handle('runPython', (event, { pythonPath, scriptPath }) => {
  const pythonProcess = spawn(pythonPath, [scriptPath]);

  pythonProcess.stdout.on('data', (data) => {
    event.sender.send('pythonOutput', data.toString());
  });

  pythonProcess.stderr.on('data', (data) => {
    event.sender.send('pythonOutput', data.toString());
  });

  pythonProcess.on('close', () => {
    event.sender.send('pythonEnd');
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
    properties: ['openFile'],
    filters: [
      { name: 'H5 File', extensions: ['h5'] }
    ]
  }).then(result => {
    if (!result.canceled) {
      event.sender.send('openH5Complete', result.filePaths);
      console.log("选中的文件为: ", result.filePaths);
    }
  }).catch(err => {
    console.log(err);
  });
})
// 查找系统中所有的python路径
ipcMain.handle('searchPythonPaths', async () => {
  const cmd = 'which -a python; which -a python3';
  return new Promise((resolve, reject) => {
    exec(cmd, (error, stdout, stderr) => {
      stderr; // 忽略stderr输出
      if (error) {
        reject(error.message);
        return;
      }
      const paths = stdout
        .split('\n')
        .map(line => line.trim())
        .filter(Boolean);

      resolve(paths);
    });
  });
});
class H5FileReader {
  constructor() {
    const isWindows = process.platform === 'win32';
    const exeSuffix = isWindows ? '.exe' : '';      // 可执行文件后缀
    this.h5ReaderPath = isDev
      ? path.resolve(__dirname, `../dist/h5_reader${exeSuffix}`)
      : path.join(process.resourcesPath, `h5_reader${exeSuffix}`);
  }

  async executePythonScript(command, filePath, datasetPath = null) {
    return new Promise((resolve, reject) => {
      const args = [command, filePath];
      if (datasetPath) {
        args.push(datasetPath);
      }

      const pythonProcess = spawn(this.h5ReaderPath, args);
      let stdout = '';
      let stderr = '';

      pythonProcess.stdout.on('data', (data) => {
        stdout += data.toString();
      });

      pythonProcess.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      pythonProcess.on('close', (code) => {
        if (code === 0) {
          try {
            const result = JSON.parse(stdout);
            resolve(result);
          } catch (error) {
            reject(new Error(`解析Python输出失败: ${error.message}`));
          }
        } else {
          reject(new Error(`Python脚本执行失败: ${stderr || `退出码: ${code}`}`));
        }
      });

      pythonProcess.on('error', (error) => {
        reject(new Error(`启动Python进程失败: ${error.message}`));
      });
    });
  }

  // async checkFileExists(filePath) {
  //     try {
  //         await fs.accessSync(filePath)
  //         return true;
  //     } catch {
  //         return false;
  //     }
  // }
}

const h5Reader = new H5FileReader();

// 读取HDF5文件结构的IPC处理器
ipcMain.handle('readH5', async (event, { filePath }) => {
  try {
    /**
     * 一般选择的文件一定是存在的，所以不需要验证文件是否存在，另外这一处代码有问题
     */
    // 检查文件是否存在
    // console.log(await h5Reader.checkFileExists(filePath));

    // if (!await h5Reader.checkFileExists(filePath)) {
    //     return { error: `文件不存在: ${filePath}` };
    // }

    // 读取HDF5文件结构
    const structure = await h5Reader.executePythonScript('structure', filePath);
    return structure;
  } catch (error) {
    return { error: error.message };
  }
});

// 单独读取数据集的IPC处理器
ipcMain.handle('readH5Dataset', async (event, { filePath, datasetPath }) => {
  try {
    // 检查文件是否存在
    // if (!await h5Reader.checkFileExists(filePath)) {
    //     return { error: `文件不存在: ${filePath}` };
    // }

    // 读取指定数据集
    const datasetData = await h5Reader.executePythonScript('dataset', filePath, datasetPath);
    return datasetData;
  } catch (error) {
    return { error: error.message };
  }
});
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
