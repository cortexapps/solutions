const path = require('path')
var ManifestPlugin = require('webpack-manifest-plugin')
const webpack = require('webpack')
const merge = require('webpack-merge')
const MiniCssExtractPlugin = require("mini-css-extract-plugin")
const UglifyJsPlugin = require('uglifyjs-webpack-plugin')

const env = process.env.NODE_ENV


let config = {
    entry: {
        bundle: [
            './assets/scripts/app.js',
            './assets/styles/app.css',
        ],
    },
    output: {
        filename: '[name].[chunkhash].js',
        path: path.resolve(__dirname, './dist/assets'),
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /(node_modules|bower_components)/,
                use: [
                    {
                        loader: 'babel-loader',
                        options: {
                            cacheDirectory: true,
                        }
                    },
                    'eslint-loader',
                ]
            },
            {
                test: /\.css$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    {
                        loader: 'css-loader',
                        options: {
                            importLoaders: 2,
                        }
                    },
                    'postcss-loader',
                ],
            },

        ]
    },
    plugins: [
        new webpack.HashedModuleIdsPlugin(),
        new MiniCssExtractPlugin({
            filename: '[name].[chunkhash].css',
            chunkFilename: '[name].[hash].css',
        }),
        new ManifestPlugin({
            fileName: '../../site/data/assets.json',
        }),
    ],
    optimization: {
        runtimeChunk: 'single',
        splitChunks: {
            chunks: 'all',
        },
    },
}


if (env === 'production') {
    config = merge.smart(config, {
        mode: 'production',
        plugins: [
            new webpack.DefinePlugin({
                'process.env.NODE_ENV': JSON.stringify('production')
            }),
        ],
        optimization: {
            minimizer: [
                new UglifyJsPlugin({}),
            ],
        },
    })
} else {
    config = merge.smart(config, {
        mode: 'development',
        devtool: 'inline-source-map',
        plugins: [
            new webpack.DefinePlugin({
                'process.env.NODE_ENV': JSON.stringify('development')
            }),
        ],
    })
}

module.exports = config