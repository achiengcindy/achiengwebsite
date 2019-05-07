var gulp = require('gulp');
var uglify = require('gulp-uglify');
var pipeline = require('readable-stream').pipeline;

gulp.task('uglify', function(){
	  return pipeline(
        gulp.src('./src/static/js/**/*.js'),
        uglify(),
        gulp.dest('./src/static/dist/js/')
  );

});
 
 gulp.task("minify", gulp.series('uglify'));


