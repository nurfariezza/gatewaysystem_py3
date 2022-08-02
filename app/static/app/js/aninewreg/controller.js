function IndexCtrl($scope, $http, $timeout) {

  $scope.form = {
    keyword: '',
    dateFrom: null,
    dateTo: null,
    openedDateFrom: false,
    openedDateTo: false,
    custlist: [],
    custpager: null,
    custpage: 1,
    list: []
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

    var a = [
      'id=' + i,
      'fmt=' + j,
      'from=' + _dateFrom,
      'to=' + _dateTo
    ].join('&');
    var q = '?' + a;
    var url = route.aninewreg.download + q;
    $('#exportFrame').attr('src', url);
  }

  $scope.downloadreport = function (i) {
    var dateFrom = $scope.form.dateFrom;
    var dateTo = $scope.form.dateTo;

    if (dateFrom == null || dateTo == null) {
      toastr.error('Date From and Date To are required');
      return;
    }

    var ids = _.map($scope.form.list, function (o) {
      return o.accountid;
    });
    var o = { list: ids };

    $http.post(route.aninewreg.downloadtemp, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.downloadreport_(data.data, i);
      }
    });
  }

  $scope.clearcust = function () {
    $scope.form.list = [];
  }

  $scope.selectcust = function (o) {
    if (o.selected == true) {
      $scope.form.list.push(o);
    }

    else {
      var list = _.reject($scope.form.list, function (x) { return x.accountid == o.accountid });
      $scope.form.list = list;
    }
  }

  $scope.search = function () {
    $scope.gotoPage(1);
  }

  $scope.custpageChanged = function () {
    $scope.gotoPage($scope.form.custpage);
  }

  $scope.gotoPage = function (page) {
    var o = {
      keyword: $scope.form.keyword,
      page: page
    }

    $http.post(route.aninewreg.listcust, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        var f = $scope.form;
        f.custlist = data.list;
        f.custpager = data.pager;
        f.custpage = data.pager.pagenum;
      }
    });
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
    $scope.gotoPage(1);
  }
}

app.controller('IndexCtrl', ['$scope', '$http', '$timeout', IndexCtrl]);
