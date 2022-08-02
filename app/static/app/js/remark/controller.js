function RemarkCtrl($scope, $http) {

  $scope.loadList = function () {
    var id = $scope.custid;

    $http.get(route.remark.list + id).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.list = data.list;
      }
    });
  }

  $scope.addRemark_ = function () {
    var o = {
      accountid: $scope.custid,
      remark: $scope.remark
    };

    $http.post(route.remark.create, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        $scope.loadList();
      }
    });
  }

  $scope.addRemark = function () {
    if ($scope.remark == null || $scope.remark == '') {
      toastr.error('Please key the remark content');
      return;
    }

    bootbox.confirm("Confirm to add following Remark to account?<br>" + $scope.remark, function (result) {
      if (result == true)
      $scope.addRemark_();
    });
  }

  $scope.clean = function () {
    $scope.list = [];
  }

  $scope.initModel = function (o) {
    $scope.clean();

    if (o.error == 1) {
      return;
    }

    $scope.list = o.remark;
    $scope.custid = o.userdetail.accountid;
  }

  $scope.init = function () {
    $scope.clean();

    $scope.$on('initModel', function (e, call) {
      $scope.initModel(call);
    });
  }
}

app.controller('RemarkCtrl', ['$scope', '$http', RemarkCtrl]);
