module.exports = {
  pluginOptions: {
    electronBuilder: {
      preload: 'src/preload.js',
      // 不要写 mainProcessFile
      builderOptions: {
        // extraFiles: [
        //   {
        //     from: 'src/preload.js',
        //     to: 'preload.js'
        //   }
        // ],
        extraResources: [process.platform === 'win32' ? {
          from: 'dist/h5_reader.exe', // 项目根目录的路径
          to: 'h5_reader.exe'    // 打包后在应用资源目录中的路径
        } : {
          from: 'dist/h5_reader', // 项目根目录的路径
          to: 'h5_reader'    // 打包后在应用资源目录中的路径
        }

        ],
        // linux: {
        //   target: ['deb', 'rpm', 'snap', 'dir']
        // },
        linux: {
          target: ['deb']
        },
        win: {
          target: 'nsis'
        },
        nsis: {
          oneClick: false, // 启用自定义安装界面
          perMachine: true, // 安装为所有用户
          allowToChangeInstallationDirectory: true, // 允许用户选择安装目录
          createDesktopShortcut: true, // 是否创建桌面快捷方式
          createStartMenuShortcut: true, // 是否创建开始菜单快捷方式
          runAfterFinish: true, // 安装完成后是否启动应用
        }
      }
    }
  }
}