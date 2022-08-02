function IndexCtrl($scope, $http) {

  $scope.form = {
    ws: {},
    wslist: [],
    from: '',
    to: '',
    cnt: 0
  };

  $scope.submitremove = function () {
    var f = $scope.form;

    if (f.from == null || f.to == null ||
        f.from == '' || f.to == '') {
      toastr.error('Number range are required');
      return;
    }

    var o = {
      from: f.from,
      to: f.to
    };

    $http.post(route.assign015number.remove, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
      }
    });
  }

  $scope.submit = function () {
    var f = $scope.form;
    var ws = f.ws.selected == null ? -1 : f.ws.selected.wholesalerkey;

    if (ws == -1) {
      toastr.error('Wholesaler is required')
      return;
    }

    if (f.from == null || f.to == null ||
        f.from == '' || f.to == '') {
      toastr.error('Number range are required');
      return;
    }

    if (f.cnt == null || f.cnt == '') {
      toastr.error('Total Number is required');
      return;
    };

    var o = {
      wskey: ws,
      from: f.from,
      to: f.to,
      cnt: f.cnt
    };

    $http.post(route.assign015number.update, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
      }
    });
  }

  $scope.init = function () {
    $http.get(route.assign015number.listws).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.form.wslist = data.list;
      }
    });
  }
}

app.controller('IndexCtrl', ['$scope', '$http', IndexCtrl]);
