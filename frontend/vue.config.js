const { defineConfig } = require("@vue/cli-service");

module.exports = {
  outputDir: "../static",
  indexPath: "../templates/index.html",
  publicPath: "process.ENV.NODE_ENV === production"
  ? "/static/"
  : "/"
}