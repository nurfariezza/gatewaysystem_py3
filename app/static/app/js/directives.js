'use strict';

/* http://cgeers.com/2013/05/03/angularjs-file-upload/ */
app.directive('upload', ['uploadManager', function factory(uploadManager) {
  return {
    restrict: 'A',
    link: function (scope, element, attrs) {
      var opt = scope.$eval(attrs.upload);
      $(element).fileupload({
        url: opt.url,
        dataType: 'json',
        add: function (e, data) {
          uploadManager.add(data);
        },
        progressall: function (e, data) {
          var progress = parseInt(data.loaded / data.total * 100, 10);
          uploadManager.setProgress(progress);
        },
        done: function (e, data) {
          uploadManager.setProgress(0);
        }
      });
      $(element).bind('fileuploadsubmit', function (e, data) {
        data.formData = scope.uploadFormData();
      }).bind('fileuploaddone', function (e, data) {
        scope.uploadDone(e, data);
      });
    }
  };
}]);
