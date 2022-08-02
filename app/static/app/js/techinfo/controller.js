function TechInfoCtrl($scope, $http, $modal) {

  $scope.supportteam = {};

  $scope.selected = {
    all: false,
    count: 0,
    message: function () {
      return this.count + ' item' + (this.count > 1 ? 's' : '') + ' selected'
    },
    reset: function () {
      this.all = false;
      this.count = 0;
    }
  }

  $scope.changetechinfo = function () {

  }

  $scope.loadList = function () {
    var id = $scope.custid;

    $http.get(route.techinfo.list + id).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.list = data.list;
      }
    });
  }

  $scope.deleteDevice = function () {
    var list = $scope.list;
    var lx = _.where(list, { selected: true });
    var ids = _.map(lx, function (o) {
      return o.idx;
    });

    $http.post(route.techinfo.del, { idxlist: ids }).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        $scope.selected.reset();
        $scope.loadList();
      }
    });
  }

  $scope.removeItems = function () {
    if ($scope.selected.count < 1)
    return;

    bootbox.confirm("Delete the selected devices ?", function (result) {
      if (result == true) {
        $scope.deleteDevice();
      }
    });
  }

  $scope.submitCreate = function () {
    var f = $scope.form;
    var o = angular.copy(f);
    delete o['devicelist'];
    delete o['device'];
    o.deviceid = f.device.selected == null ? 1 : f.device.selected.deviceid;

    $http.post(route.techinfo.create, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        $scope.modal.hide();
        $scope.loadList();
      }
    });
  }

  $scope.submitUpdate = function () {
    var f = $scope.form;
    var o = angular.copy(f);
    delete o['devicelist'];
    delete o['device'];
    o.deviceid = f.device.selected == null ? 1 : f.device.selected.deviceid;

    $http.post(route.techinfo.update, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        $scope.modal.hide();
        $scope.loadList();
      }
    });
  }

  $scope.save = function () {
    if ($scope.edit == true)
    $scope.submitUpdate();

    else
    $scope.submitCreate();
  }

  $scope.add = function () {
    $scope.form = { device: {}, accountid: $scope.custid };
    $scope.edit = false;

    $scope.modal = $modal({
      scope: $scope,
      template: route.techinfo.form,
      show: false,
      title: 'Create Device'
    });

    $http.get(route.techinfo.add).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.form.devicelist = data.list;
        $scope.form.device.selected = data.list[0];
        $scope.modal.$promise.then($scope.modal.show);
      }
    });
  }

  $scope.editdevice = function (o) {
    $scope.form = angular.copy(o);
    $scope.form.device = {};
    $scope.edit = true;

    $scope.modal = $modal({
      scope: $scope,
      template: route.techinfo.form,
      show: false,
      title: 'Edit Device'
    });

    $http.get(route.techinfo.add).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.form.devicelist = data.list;
        var device = _.findWhere(data.list, { deviceid: o.deviceid });
        if (device != null)
        $scope.form.device.selected = device;

        $scope.modal.$promise.then($scope.modal.show);
      }
    });
  }

  $scope.selectRow = function ($event, o) {
    $event.stopPropagation();

    if (o.selected)
    ++$scope.selected.count;

    else
    --$scope.selected.count;
  }

  $scope.selectAll = function ($event) {
    $event.stopPropagation();

    var list = null;
    var n = 0;

    if ($scope.list != null)
    list = $scope.list;

    if (list != null)
    n = list.length;

    for (var i = 0; i < n; i++) {
      var o = list[i];
      o.selected = $scope.selected.all;
    }

    if ($scope.selected.all)
    $scope.selected.count = n;

    else
    $scope.selected.count = 0;
  }

  $scope.initSelect = function () {
    var o = $scope.userdetail;
    var x = o.userdetailext;

    if (x == null)
    return;

    var i = _.findIndex($scope.supportteamlist, { teamid: x.supportteam });
    if (i >= 0)
    $scope.supportteam.selected = $scope.supportteamlist[i];
  }

  $scope.clean = function () {
    $scope.list = [];
    $scope.userdetail = {
      userdetailext: {
        pbxmodel: '',
        supportteam: 1,
        technicalnotes: ''
      }
    };
  }

  $scope.initModel = function (o) {
    $scope.clean();

    if (o.error == 1) {
      return;
    }

    $scope.userdetail = o.userdetail;
    $scope.list = o.devicelist;
    $scope.custid = o.userdetail.accountid;
    $scope.initSelect();
  }

  $scope.init = function () {
    $scope.clean();

    $scope.$on('initModel', function (e, call) {
      $scope.initModel(call);
    });

    $scope.$on('getdata', function (e, call) {
      var x = $scope.userdetail.userdetailext;
      var pbxmodel = x.pbxmodel;
      var supportteam = $scope.supportteam.selected;
      var technicalnotes = x.technicalnotes;

      $scope.$emit('techinfo', { pbxmodel: pbxmodel, supportteam: supportteam, technicalnotes: technicalnotes });
    });

    $http.get(route.techinfo.lookup).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.supportteamlist = data.supportteam;
        $scope.initSelect();
      }
    });
  }
}

app.controller('TechInfoCtrl', ['$scope', '$http', '$modal', TechInfoCtrl]);
