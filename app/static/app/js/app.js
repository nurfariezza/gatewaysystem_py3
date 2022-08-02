'use strict';

/* App Module */

var app = angular.module('mvcapp', ['ngRoute', 'ngSanitize', 'ngMessages', 'ngAnimate', 'mvcappFilters', 'ui.bootstrap', 'ui.utils', 'ui.select', 'xeditable', 'ui.bootstrap.contextMenu', 'mgcrea.ngStrap', 'angular-loading-bar']);

app.config(['uibDatepickerConfig', function (uibDatepickerConfig) {
  uibDatepickerConfig.initDate = new Date();
}]);

app.run(function (editableOptions, editableThemes) {
  $('#mainContainer').show();
  $.scrollUp({ scrollImg: true });
  editableThemes.bs3.inputClass = 'input-sm';
  editableOptions.theme = 'bs3';
  $(document).on('hidden.bs.modal', function (e) {
    if ($('.modal-with-am-fade').length > 0 &&
    !$('body').hasClass('modal-open')) {
      $('body').addClass('modal-open');
    }
  });
});

utils.initDrop();
utils.initToastr();
