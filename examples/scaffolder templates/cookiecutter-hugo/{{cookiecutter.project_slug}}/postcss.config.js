module.exports = {
  plugins: [
    require('stylelint'),
    require('postcss-import'),
    require('autoprefixer'),
    require('postcss-preset-env'),
    require('cssnano'),
  ]
}
