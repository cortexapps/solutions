import gulp from 'gulp'
import flatten from 'gulp-flatten'
import del from 'del'
import imagemin from 'gulp-imagemin'
import sourcemaps from 'gulp-sourcemaps'
import postcss from 'gulp-postcss'
import BrowserSync from 'browser-sync'
import webpack from 'webpack'
import logger from 'fancy-log'
import { spawn } from 'child_process'

import webpackConfig from './webpack.config.js'


const browserSync = BrowserSync.create()
const buildDir = 'dist'
const stylesGlob = './assets/styles/**/*.css'
const scriptsGlob = './assets/scripts/**/*.js'
const fontsGlob = './assets/fonts/**/*'
const imagesGlob = './assets/images/**/*'
const hugoRoot = './site'
const hugoGlob = [`./${hugoRoot}/**/*`, `!./${hugoRoot}/resources/_gen/**/*`]
const hugoDefaultArgs = ['--destination', `../${buildDir}`, '--source', 'site', '-v']
const hugoPreviewArgs = hugoDefaultArgs.concat(['--buildDrafts', '--buildFuture'])
const assetsTasks = ['clean', 'webpack', 'fonts', 'images']


gulp.task('clean', () => del('dist'))

gulp.task('build', assetsTasks, (done) => runHugo(hugoDefaultArgs, done))
gulp.task('build-preview', assetsTasks, (done) => runHugo(hugoPreviewArgs, done))
gulp.task('develop', ['build'], () => runServer())
gulp.task('develop-preview', ['build-preview'], () => runServer())
gulp.task('default', ['develop'])

gulp.task('hugo', (done) => runHugo(hugoDefaultArgs, done))

gulp.task('styles', ['clean'], () =>
    gulp.src(stylesGlob)
        .pipe(sourcemaps.init())
        .pipe(postcss())
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(`./${buildDir}/styles`))
        .pipe(browserSync.stream())
)


gulp.task('webpack', ['clean'], (done) => {
    del(`./${buildDir}/assets`)
    webpack(webpackConfig, (error, stats) => {
        if (error) {
            throw new Error(error)
        }
        logger.info("[webpack]", stats.toString({
            colors: true,
            progress: true
        }))
        done()
    })
})


gulp.task('fonts', ['clean'], () =>
    gulp.src(fontsGlob)
        .pipe(flatten())
        .pipe(gulp.dest(`./${buildDir}/fonts`))
        .pipe(browserSync.stream())
)


gulp.task('images', ['clean'], () =>
    gulp.src(imagesGlob)
        .pipe(imagemin())
        .pipe(gulp.dest(`./${buildDir}/images`))
        .pipe(browserSync.stream())
)


const runServer = () => {
    browserSync.init({
        server: {
            baseDir: buildDir,
        }
    })
    gulp.watch([stylesGlob, scriptsGlob], ['webpack'])
    gulp.watch(fontsGlob, ['fonts'])
    gulp.watch(imagesGlob, ['images'])
    gulp.watch(hugoGlob, ['hugo'])
}


const runHugo = (args, done) => {
  return spawn('hugo', args, {stdio: "inherit"}).on("close", (returnCode) => {
    if (returnCode === 0) {
      browserSync.reload()
      done && done()
    } else {
      browserSync.notify("Hugo build failed.")
      done && done("Hugo build failed.")
    }
  })
}