function IndexCtrl($scope, $http, $timeout) {

  $scope.form = {
    accountid: '',
    ws: {},
    wslist: [],
    dateFrom: null,
    dateTo: null,
    openedDateFrom: false,
    openedDateTo: false,
    custlist: []
  };

  $scope.downloadreport_ = function (i, j) {
    var f = $scope.form;
    var dateFrom = f.dateFrom;
    var dateTo = f.dateTo;

    if (dateFrom == null || dateTo == null) {
      toastr.error('Date From and Date To are required');
      return;
    }

    var _dateFrom = utils.getDateStr(dateFrom);
    var _dateTo = utils.getDateStr(dateTo);
    var ws = f.ws.selected == null ? 0 : f.ws.selected.wholesalerkey;

    var a = [
      'id=' + i,
      'ws=' + ws,
      'fmt=' + j,
      'from=' + _dateFrom,
      'to=' + _dateTo
    ].join('&');
    var q = '?' + a;
    var url = route.topupreport.download + q;
    $('#exportFrame').attr('src', url);
  }

  $scope.downloadreport = function (i) {
    var f = $scope.form;
    var dateFrom = f.dateFrom;
    var dateTo = f.dateTo;

    if (dateFrom == null || dateTo == null) {
      toastr.error('Date From and Date To are required');
      return;
    }

    var ids = _.map(f.custlist, function (o) {
      return o.accountid;
    });
    var o = { list: ids };

    $http.post(route.topupreport.downloadtemp, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.downloadreport_(data.data, i);
      }
    });
  }

  $scope.lookup = function () {
    var params = { id: $scope.form.accountid };
    $http.get(route.topupreport.listcust, { params: params }).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.form.custlist = _.union($scope.form.custlist, data.list);
      }
    });
  }

  $scope.removecust = function ($event, o) {
    $event.stopPropagation();

    $scope.form.custlist = _.reject($scope.form.custlist, function (i) {
      return i.accountid == o.accountid;
    });
  }

  $scope.clearcust = function () {
    $scope.form.custlist = [];
    $scope.form.ws = {};
  }

  $scope.openDateFrom = function () {
    $timeout(function () {
      $scope.form.openedDateFrom = true;
    });
  }

  $scope.openDateTo = function () {
    $timeout(function () {
      $scope.form.openedDateTo = true;
    });
  }

  $scope.init = function () {
    $http.get(route.topupreport.listws).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.form.wslist = data.list;
      }
    });
  }
}

app.controller('IndexCtrl', ['$scope', '$http', '$timeout', IndexCtrl]);
