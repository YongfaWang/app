const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  pluginOptions: {
    electronBuilder: {
      nodeIntegration: true, // 关键！启用 Node.js 集成
    }
  }
})

// module.exports = {
//   configureWebpack: {
//     resolve: {
//       fallback: {
//         "path": false,
//         "fs": false
//       }
//     }
//   }
// }


// import { defineConfig } from '@vue/cli-service'
// export default defineConfig({
//   transpileDependencies: true,
//   pluginOptions: {
//     electronBuilder: {
//       nodeIntegration: true, // 关键！启用 Node.js 集成
//     }
//   }
// })