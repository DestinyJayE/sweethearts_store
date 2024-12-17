const { defineConfig } = require('@vue/cli-service');
module.exports = defineConfig({
  transpileDependencies: true,

  // 配置开发服务器
  devServer: {
    port: 8081, // 自定义端口
    open: true // 启动时自动打开浏览器
  },

  // 配置路径别名
  configureWebpack: {
    resolve: {
      alias: {
        '@': require('path').resolve(__dirname, 'src')
      }
    }
  }
});