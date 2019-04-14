var gulp = require('gulp');
var imageResize = require('gulp-image-resize');
var rename = require("gulp-rename");
var pathParse = require('path-parse');

gulp.task('default', function (cb) {

/* small images */
  gulp.src('./media/**/*.{jpg,jpeg,png,gif,ico,svg}')
    .pipe(imageResize({width : 320}))
    .pipe(rename(function (path) { path.basename += "-s"; }))
    .pipe(gulp.dest('./images'));


/* medium images */
    gulp.src('./media/**/*.{jpg,jpeg,png,gif,ico,svg}')
        .pipe(imageResize({width : 520}))
        .pipe(rename((path) => {path.basename += "-m";}))
        .pipe(gulp.dest('./images'));

/*large images */
gulp.src('./media/**/*.{jpg,jpeg,png,gif,ico,svg}')
    .pipe(imageResize({width : 768}))
    .pipe(rename((path) => {path.basename += "-l";}))
    .pipe(gulp.dest('./images'));


/*large images */
gulp.src('./media/**/*.{jpg,jpeg,png,gif,ico,svg}')
    .pipe(imageResize({width : 800}))
    .pipe(rename((path) => {path.basename += "-xl";}))
    .pipe(gulp.dest('./images'));


cb(); 

});


