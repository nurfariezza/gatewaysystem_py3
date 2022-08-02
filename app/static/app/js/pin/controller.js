function PinCtrl($scope, $http, $modal, $window) {

  $scope.selected = {
    all: false,
    count: 0,
    message: function () {
      return this.count + ' item' + (this.count > 1 ? 's': '') + ' selected'
    },
    reset: function () {
      this.all = false;
      this.count = 0;
    }
  }

  $scope.getSelected = function () {
    var list = $scope.list;
    var lx = _.where(list, { selected: true });
    var ids = _.map(lx, function (o) {
      return o.pin;
    });
    return ids;
  }

  $scope.loadList = function () {
    var id = $scope.custid;

    $http.get(route.pin.list + id).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.list = data.list;
      }
    });
  }

  $scope.deleteAllPin = function () {
    $http.post(route.pin.delall, { accountid: $scope.custid }).success(function (data) {
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

  $scope.removeAll = function () {
    bootbox.confirm("Delete all the pins ?", function (result) {
      if (result == true) {
        $scope.deleteAllPin();
      }
    });
  }

  $scope.deletePin = function () {
    var ids = $scope.getSelected();

    $http.post(route.pin.del, { idxlist: ids, accountid: $scope.custid }).success(function (data) {
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

    bootbox.confirm("Delete the selected pins ?", function (result) {
      if (result == true) {
        $scope.deletePin();
      }
    });
  }

  $scope.saveuserid = function (o, newuserid) {
    var o = {
      accountid: $scope.custid,
      pin: o.pin,
      userid: o.userid,
      newuserid: newuserid
    };

    $http.post(route.pin.useridupdate, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        $scope.loadList();
      }
    });
  }

  $scope.confirmedituserid = function (o, newuserid) {
    if (newuserid.length > 4) {
      toastr.error("UserID's maximum length is 4 digit");
      return;
    }

    bootbox.confirm("Change UserID from " + o.userid + " to " + newuserid + " for account " + $scope.custid + " ?", function (result) {
      if (result == true)
      $scope.saveuserid(o, newuserid);
    })
  }

  $scope.submitCreate = function () {
    var f = $scope.form;

    var o = {
      custid: $scope.custid,
      pin: f.pin,
      description: f.description,
      creditlimit: f.creditlimit
    };

    $http.post(route.pin.create, o).success(function (data) {
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

    $http.post(route.pin.update, f).success(function (data) {
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
    $scope.form = {};
    $scope.edit = false;

    $scope.modal = $modal({
      scope: $scope,
      template: route.pin.form,
      show: true,
      title: 'Create Pin'
    });
  }

  $scope.editpin = function (o) {
    $scope.form = angular.copy(o);
    $scope.form['oldpin'] = o.pin;

    $scope.edit = true;

    $scope.modal = $modal({
      scope: $scope,
      template: route.pin.form,
      show: true,
      title: 'Edit Pin'
    });
  }

  $scope.edituserid = function ($event, o) {
    $event.stopPropagation();

    bootbox.prompt("Please enter the new UserID", function (result) {
      if (result == null)
      return;

      else if (result != '')
      $scope.confirmedituserid(o, result);
    });
  }

  $scope.importdescSave = function () {
    var f = $scope.impdform;

    var o = {
      accountid: $scope.custid,
      list: f.list,
      withdesc: true
    };

    $http.post(route.pin.importsave, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        $scope.impdmodal.hide();
        $scope.loadList();
      }
    });
  }

  $scope.importSave = function () {
    var f = $scope.impform;

    var o = {
      accountid: $scope.custid,
      pinlength: f.pinlength,
      list: f.list
    };

    $http.post(route.pin.importsave, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        $scope.impmodal.hide();
        $scope.loadList();
      }
    });
  }

  $scope.importWithDesc = function () {
    $scope.impdform = {
      list: ''
    };

    $scope.impdmodal = $modal({
      scope: $scope,
      template: route.pin.formimportwithdesc,
      show: false,
      title: 'Import Pin With Desc'
    });
    $scope.impdmodal.$promise.then($scope.impdmodal.show);
  }

  $scope.import = function () {
    $scope.impform = {
      pinlength: 6,
      list: ''
    };

    $scope.impmodal = $modal({
      scope: $scope,
      template: route.pin.formimport,
      show: false,
      title: 'Import Pin'
    });
    $scope.impmodal.$promise.then($scope.impmodal.show);
  }

  $scope.copywd = function () {
    $window.open(route.pin.listview + $scope.custid + '?d=1', '_blank');
  }

  $scope.copy = function () {
    $window.open(route.pin.listview + $scope.custid, '_blank');
  }

  $scope.showList = function () {
    return $scope.list != null && $scope.list.length > 0;
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

  $scope.clean = function () {
    $scope.list = [];
  }

  $scope.initModel = function (o) {
    $scope.clean();

    if (o.error == 1) {
      return;
    }

    $scope.list = o.pin;
    $scope.custid = o.userdetail.accountid;
    $scope.userdetail = o.userdetail;
  }

  $scope.init = function () {
    $scope.clean();

    $scope.$on('initModel', function (e, call) {
      $scope.initModel(call);
    });
  }
}

app.controller('PinCtrl', ['$scope', '$http', '$modal', '$window', PinCtrl]);
