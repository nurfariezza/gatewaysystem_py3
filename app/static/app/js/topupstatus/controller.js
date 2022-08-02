function IndexCtrl($scope, $http, $timeout) {

  $scope.form = {
    ws: {},
    wslist: [],
    dateFrom: new Date(),
    openedDateFrom: false,
    list: []
  };

  $scope.search = function () {
    var f = $scope.form;
    var dateFrom = f.dateFrom;

    if (dateFrom == null) {
      toastr.error('Date From is required');
      return;
    }

    var _dateFrom = utils.getDateStr(dateFrom);
    var ws = f.ws.selected == null ? 0 : f.ws.selected.wholesalerkey;

    var o = {
      wholesalerkey: ws,
      from: _dateFrom
    };

    $http.post(route.topupstatus.list, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.form.list = data.list;
      }
    });
  }

  $scope.openDateFrom = function () {
    $timeout(function () {
      $scope.form.openedDateFrom = true;
    });
  }

  $scope.init = function () {
    $http.get(route.topupreport.listws).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.form.wslist = data.list;
        $scope.form.ws.selected = data.list[0];
      }
    });
  }
}

app.controller('IndexCtrl', ['$scope', '$http', '$timeout', IndexCtrl]);
