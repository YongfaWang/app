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
        extraResources: [
          {
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
        // win: {
        //   target: 'nsis'
        // }
      }
    }
  }
}