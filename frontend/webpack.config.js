const HtmlWebpackPlugin = require('html-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const webpack = require('webpack');
const path = require('path');

const PATHS = {
    src: path.join(__dirname, './src'),
    dist: path.join(__dirname, './dist')
};

module.exports = {
    context: __dirname,
    mode: 'production',
    entry: {
        app: [PATHS.src]
    },
    output: {
        path: PATHS.dist,
        filename: '[name].[chunkhash].js',
        publicPath: './'
    },
    optimization: {
        runtimeChunk: 'single',
        splitChunks: {
            cacheGroups: {
                vendors: {
                    test: /[\\/]node_modules[\\/]/,
                    name: 'vendors',
                    enforce: true,
                    chunks: 'all'
                }
            }
        }
    },
    module: {
        rules: [{
            test: /\.js$/,
            exclude: /node_modules/,
            use: [{
                loader: 'babel-loader',
                options: {
                    plugins: ["angularjs-annotate"]
                }
            }]
        }, {
            test: /\.html$/,
            use: [{
                loader: 'html-loader'
            }]
        }, {
            test: /\.scss$/,
            loaders: [
                MiniCssExtractPlugin.loader,
                'css-loader?sourceMap',
                'sass-loader?sourceMap'
            ]
        }, {
            test: /\.css$/,
            loaders: [
                MiniCssExtractPlugin.loader,
                'css-loader?sourceMap'
            ]
        }, {
            test: /\.coffee$/,
            use: ['coffee-loader']
        }, {
            test: /\.(png|jpg|gif|svg|ttf|woff|woff2|eot|otf)$/,
            use: [{
                loader: 'file-loader',
                options: {
                    name: '[name].[ext]'
                }
            }]
        }]

    },
    plugins: [
        new HtmlWebpackPlugin({
            template: './src/index.html',
            chunksSortMode: 'dependency',
            minify: {
                collapseWhitespace: true,
                conservativeCollapse: true,
                preserveLineBreaks: true,
                useShortDoctype: true,
                html5: true
            },
            mobile: true,
        }),
        new CopyWebpackPlugin([
            {
                from: path.join(PATHS.src, 'app/favicons/'),
                to: path.join(PATHS.dist, 'app/favicons/')
            },
            {
                from: path.join(PATHS.src, 'app/favicons/favicon.ico'),
                to: path.join(PATHS.dist, 'favicon.ico')
            }
        ]),
        new MiniCssExtractPlugin({
            filename: '[name].[chunkhash].css'
        }),
        new webpack.ProvidePlugin({
            _: 'underscore',
            "window.jQuery": "jquery"
        }),
        new webpack.DefinePlugin({
            PRODUCTION: JSON.stringify(true),
            VERSION: JSON.stringify('1.2.0'),
            DEBUG: false
        })
    ],
    devServer: {
        contentBase: PATHS.dist,
        compress: true,
        headers: {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY'
        },
        open: true,
        overlay: {
            warnings: true,
            errors: true
        },
        port: 8080,
        publicPath: 'http://localhost:8080/',
        hot: true
    }
};
