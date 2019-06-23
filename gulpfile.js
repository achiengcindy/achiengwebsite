const gulp = require("gulp");
let uglify = require("gulp-uglify");
let pipeline = require("readable-stream").pipeline;
let cleanCSS = require("gulp-clean-css");
const jshint = require("gulp-jshint");
const imageResize = require("gulp-image-resize");
const rename = require("gulp-rename");
const babel = require('gulp-babel');
const imagemin = require('gulp-imagemin');
const responsive = require('gulp-responsive-images');
const webp = require('gulp-webp');

// we write functions now in gulp 4


// process javascript
// convert to es5
function processJS() {
  return pipeline(
    gulp.src("./src/static/js/**/*.js"),
    jshint({ esversion: 6 }),
    uglify(),
    babel({ presets: ["env"] }),
    gulp.dest("./src/static/dist/js")
  );
};
//process css
function processCSS() {
  return pipeline(
    gulp.src("./src/static/css/**/*.css"),
    cleanCSS({ compatibility: "ie8" }),
    gulp.dest("./src/static/dist/css")
  );
};

//process html
function processHTML() {
  return pipeline(
  );
};

//process images
function processImages() {
  return pipeline(
    gulp.src("./src/static/img/**/*"),
    responsive({
      '*.png': [{
        width: 1080,
      height: 1080,
      gravity: 'Center',
      suffix: '-1080x1080'
    },
    {
      width: 1024,
    height: 1024,
    gravity: 'Center',
    suffix: '-1024x1024'
  },

      {
        width: 1000,
        height: 1000,
        suffix: '-992x992'
      },

      {
        width: 800,
        height: 800,
        suffix: '-800x800'
      },

      {
        width: 768,
        height: 768,
        suffix: '-768x768'
      },
      {
        width: 650,
        height: 650,
        gravity: 'Center',
        suffix: '-650x650'
      },
      {
        width: 500,
        height: 500,
        crop: true,
        suffix: '-500x500'
      },
      {
        width: 350,
        height: 350,
        suffix: '-350x350'
      }
      ]
    }),
    imagemin(),
    webp(),
    gulp.dest("./src/static/img/")
  );
};

// convert images we
function convertImage() {
  return pipeline(
    gulp.src("./src/static/img/**/*"),
    webp(),
    gulp.dest("./src/static/img/")
  );
};

exports.processJS = processJS;
exports.processCSS = processCSS;
exports.processHTML = processHTML;
exports.processImages = processImages;
exports.convertImage = convertImage;
