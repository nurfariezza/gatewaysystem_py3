function IndexCtrl($scope, $http) {

  $scope.form = {
    ws: {},
    wslist: []
  };

  $scope.download = function () {
    var f = $scope.form;
    var ws = f.ws.selected == null ? -1 : f.ws.selected.wholesalerkey;

    if (ws == -1) {
      toastr.error('Wholesaler is required')
      return;
    }

    var q = '?ws=' + ws;
    var url = route.view015number.download + q;
    $('#exportFrame').attr('src', url);
  }

  $scope.init = function () {
    $http.get(route.view015number.listws).success(function (data) {
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
