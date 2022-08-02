function IndexCtrl($scope, $http) {

  $scope.form = {
    wslogin: {},
    wsloginlist: [],
    rtcdruser: {},
    rtcdruserlist: [],
    pwd1: '',
    pwd2: ''
  };

  $scope.submit1 = function () {
    var f = $scope.form;
    var s = f.wslogin.selected;

    if ($scope.fm1.$invalid || f.pwd1 == null || f.pwd1 == '' ||
        s == null) {
      toastr.error('Login and Password are required')
      return;
    }

    var o = {
      login: s.sloginname,
      pwd: f.pwd1
    };

    $http.post(route.setpassword.updatews, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
      }
    });
  }

  $scope.submit2 = function () {
    var f = $scope.form;
    var s = f.rtcdruser.selected;

    if ($scope.fm2.$invalid || f.pwd2 == null || f.pwd2 == '' ||
        s == null) {
      toastr.error('Login and Password are required')
      return;
    }

    var o = {
      login: s.loginid,
      pwd: f.pwd2
    };

    $http.post(route.setpassword.updatertcdr, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
      }
    });
  }

  $scope.changewslogin = function () {
    var s = $scope.form.wslogin.selected;
    var o = {
      login: s.sloginname,
      wskey: s.wholesalerkey
    };

    $http.post(route.setpassword.pwdws, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.form.pwd1 = data.data;
      }
    });
  }

  $scope.changertcdruser = function () {
    var s = $scope.form.rtcdruser.selected;
    var o = {
      login: s.loginid,
      wsid: s.wholesalerid
    };

    $http.post(route.setpassword.pwdrtcdr, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.form.pwd2 = data.data;
      }
    });
  }

  $scope.init = function () {
    $http.get(route.setpassword.listwslogin).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.form.wsloginlist = data.list;
      }
    });

    $http.get(route.setpassword.listrtcdruser).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.form.rtcdruserlist = data.list;
      }
    });
  }
}

app.controller('IndexCtrl', ['$scope', '$http', IndexCtrl]);
