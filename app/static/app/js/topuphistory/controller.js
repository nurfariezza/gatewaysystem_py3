function TopupHistoryCtrl($scope, $http) {

  $scope.clean = function () {
    $scope.list = [];
  }

  $scope.initModel = function (o) {
    $scope.clean();

    if (o.error == 1) {
      return;
    }

    $scope.list = o.topuphistory;
  }

  $scope.init = function () {
    $scope.clean();

    $scope.$on('initModel', function (e, call) {
      $scope.initModel(call);
    });
  }
}

app.controller('TopupHistoryCtrl', ['$scope', '$http', TopupHistoryCtrl]);
