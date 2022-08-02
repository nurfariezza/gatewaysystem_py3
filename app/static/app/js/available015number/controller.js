function IndexCtrl($scope, $http) {

  $scope.form = {
    from: '',
    to: ''
  };

  $scope.search = function () {
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

    $http.post(route.available015number.count, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        bootbox.alert(data.message);
      }
    });
  }

  $scope.download = function () {
    var f = $scope.form;

    if (f.from == null || f.to == null ||
        f.from == '' || f.to == '') {
      toastr.error('Number range are required');
      return;
    }

    var a = [
      'f=' + f.from,
      't=' + f.to
    ].join('&');
    var q = '?' + a;
    var url = route.available015number.download + q;
    $('#exportFrame').attr('src', url);
  }
}

app.controller('IndexCtrl', ['$scope', '$http', IndexCtrl]);
