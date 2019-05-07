let gulp = require('gulp');
let uglify = require('gulp-uglify');
let pipeline = require('readable-stream').pipeline;
let cleanCSS = require('gulp-clean-css');
const imagemin = require('gulp-imagemin');

gulp.task('minify-js', () => {
	  return pipeline(
        gulp.src('./src/static/dev/js/**/*.js'),
        uglify(),
        gulp.dest('./src/static/js/')
  );

});


gulp.task('minify-css', () => {
	return pipeline(
		gulp.src('./src/static/dev/css/**/*.css'),
        cleanCSS({compatibility: 'ie8'}),
        gulp.dest('./src/static/css/')


		);
});


gulp.task('resize-image', () => {
	return pipeline(
		gulp.src('./src/static/dev/images/**/*.css'),
        imagemin(),
        gulp.dest('./src/static/images/')


		);
});

 
gulp.task("minify", gulp.series('minify-js', 'minify-css', 'resize-image'));






 
