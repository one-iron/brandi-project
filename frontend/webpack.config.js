const VueLoaderPlugin = require("vue-loader/lib/plugin");
const path = require("path");
const env = process.env.ENV || "development";
// 개발모드와 배포모드 설정을 분리하기 위해 사용 
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

const config = {
  mode: env,
  resolve: {
    extensions: [".js", ".vue"],
  },
  entry: {
    app: path.join(__dirname, "main.js"),
  },
  module: {
    rules: [
      {
        test: /\.vue$/,
        use: "vue-loader",
      },
      {
        test: /\.(sa|sc|c)ss$/,
        use: ["vue-style-loader", "css-loader", "sass-loader"],
      },
      {
        test: /\.(png|jpg|gif)$/i,
        loader: "file-loader",
        options: {
          publicPath: "/some/path/",
          postTransformPublicPath: (p) => `__webpack_public_path__ + ${p}`,
        },
      },
    ],
  },
  plugins: [
    new VueLoaderPlugin()
  ],
  output: {
    filename: `[name].js`,
    path: path.join(__dirname, "dist"),
    publicPath: "/dist",
  },
};

if (env === "development") {
  // 개발환경에서만 웹팩 devtool 을 활성화한다. 

  config.devtool = "eval";
  config.devServer = {
    historyApiFallback: true,
  };

  // 배포환경에서만 css 를 style.css 로 따로 번들링한다. 
} else if (env === "production") {
  config.module.rules = [
    {
      test: /\.vue$/,
      use: "vue-loader",
    },
    {
      test: /\.(sa|sc|c)ss$/,
      use: [MiniCssExtractPlugin.loader, "css-loader", "sass-loader"],
    },
  ];


  config.plugins.push(new MiniCssExtractPlugin({
    filename: 'style.css'
  }));
}

module.exports = config;
