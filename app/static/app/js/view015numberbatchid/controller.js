function IndexCtrl($scope, $http) {

  $scope.form = {
    batch_id: {},
    batchlist: []
  };

  $scope.download = function () {
    var f = $scope.form;
    var batch_id = f.batch_id.selected == null ? -1 : f.batch_id.selected.batch_id;

    if (batch_id == -1) {
      toastr.error('Wholesaler is required')
      return;
    }

    var q = '?batch_id=' + batch_id;
    var url = route.view015numberbatchid.download + q;
    $('#exportFrame').attr('src', url);
  }

  $scope.init = function () {
    $http.get(route.view015numberbatchid.listbatch).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.form.batchlist = data.list;
      }
    });
  }
}

app.controller('IndexCtrl', ['$scope', '$http', IndexCtrl]);
