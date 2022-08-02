function IndexCtrl($scope, $http) {

  $scope.form = {
    ws: {},
    wslist: [],
    pattern: ''
  };

  $scope.form1 = {
    loginid: '',
    pwd: ''
  };

  $scope.submit1 = function () {
    var f = $scope.form;
    var ws = f.ws.selected;
    var f1 = $scope.form1;

    var o = {
      wsid: ws.wholesalerkey,
      pattern: f.pattern,
      loginid: f1.loginid,
      pwd: f1.pwd,
      wsname: ws.wholesalername
    };

    $http.post(route.createlogin.createws, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        bootbox.alert(data.message);
      }
    });
  }

  $scope.submit2 = function () {
    var f = $scope.form;
    var ws = f.ws.selected;
    var f1 = $scope.form1;

    var o = {
      wsid: ws.wholesalerkey,
      pattern: f.pattern,
      loginid: f1.loginid,
      pwd: f1.pwd,
      wsname: ws.wholesalername
    };

    $http.post(route.createlogin.creatertcdr, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        bootbox.alert(data.message);
      }
    });
  }

  $scope.changews = function () {
    var s = $scope.form.ws.selected;
    $http.get(route.createlogin.pattern + s.wholesalerkey).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.form.pattern = data.data;
      }
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

app.controller('IndexCtrl', ['$scope', '$http', IndexCtrl]);
