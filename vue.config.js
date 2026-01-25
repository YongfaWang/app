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
            from: 'dist_electron/h5_reader.py',
            to: 'h5_reader.py'
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