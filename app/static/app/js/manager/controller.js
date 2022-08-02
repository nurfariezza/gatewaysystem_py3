function IndexCtrl($scope, $http) {

    $scope.form = {
      id: {},
      mgrlist: [],
      from: '',
      to: '',
      cnt: 0,
      remark:''
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
  
      $http.post(route.reserve015number.remove, o).success(function (data) {
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
      var id = f.id.selected == null ? -1 : f.id.selected.id;
  
      if (id == -1) {
        toastr.error('Account Manager is required')
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
        id: id,
        from: f.from,
        to: f.to,
        cnt: f.cnt,
        remark:f.remark
      };
  
      $http.post(route.reserve015number.update, o).success(function (data) {
        if (data.error == 1) {
          toastr.error(data.message);
        }
  
        else {
          toastr.success(data.message);
        }
      });
    }
  
  

  
    $scope.init = function () {
      $http.get(route.reserve015number.listmgr).success(function (data) {
        if (data.error == 1) {
          toastr.error(data.message);
        }
  
        else {
          $scope.form.mgrlist = data.list;
        }
      });
    }
  }
  
  app.controller('IndexCtrl', ['$scope', '$http', IndexCtrl]);
  