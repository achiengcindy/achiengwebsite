const gulp = require("gulp");
let uglify = require("gulp-uglify");
let pipeline = require("readable-stream").pipeline;
let cleanCSS = require("gulp-clean-css");
const jshint = require("gulp-jshint");
const imageResize = require("gulp-image-resize");
const rename = require("gulp-rename");
const babel = require('gulp-babel');


gulp.task("ProcessJS", () => {
  return pipeline(
    gulp.src("./src/static/js/**/*.js"),
    jshint({ esversion: 6 }),
    uglify(),
    babel({ presets: ["env"] }),
    gulp.dest("./src/static/dist/js")
  );
});


gulp.task('processHTML', () => {

});

gulp.task("processCSS", () => {
  return pipeline(
    gulp.src("./src/static/css/**/*.css"),
    cleanCSS({ compatibility: "ie8" }),
    gulp.dest("./src/static/dist/css")
  );
});

gulp.task("resize-image", () => {
  return pipeline(
      gulp.src("./src/static/**/*.{jpg,jpeg,png,gif,ico,svg}"),
    imageResize({ width:320}),
    rename((path) =>  {path.basename += "-s";}),
    gulp.dest("./src/static/dist/images")
    );
   return pipeline(
      gulp.src("./src/static/**/*.{jpg,jpeg,png,gif,ico,svg}"),
    imageResize({ width:480}),
    rename((path) =>  {path.basename += "-m";}),
    gulp.dest("./src/static/dist/images")
    );
    return pipeline(
      gulp.src("./src/static/**/*.{jpg,jpeg,png,gif,ico,svg}"),
    imageResize({ width:800}),
    rename((path) =>  {path.basename += "-l";}),
    gulp.dest("./src/static/dist/images")
    );
     return pipeline(
      gulp.src("./src/static/**/*.{jpg,jpeg,png,gif,ico,svg}"),
    imageResize({ width:1000}),
    rename((path) =>  {path.basename += "-xl";}),
    gulp.dest("./src/static/dist/images")
    );
    

});


gulp.task("minify", gulp.series("ProcessJS", "processCSS", "resize-image"));
