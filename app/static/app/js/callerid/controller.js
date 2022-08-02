function CalleridCtrl($scope, $http, $modal, $window) {

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

  $scope.showList = function () {
    return $scope.list != null && $scope.list.length > 0;
  }

  $scope.checkCallerIDSearch_ = function (list) {
    var o = {
      list: list
    };

    $http.post(route.callerid.search, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.chkcalleridmodal.$scope.rlist = data.list;
        $scope.chkcalleridmodal.$scope.index = 1;
        $('.nav-tabs a[href="#tab2"]').tab('show');
      }
    });
  }

  $scope.checkCallerIDSearch = function () {
    var list = $scope.chkcalleridform.list;
    $scope.checkCallerIDSearch_(list);
  }

  $scope.checkCallerID = function () {
    if (!$scope.chkcalleridmodal) {
      $scope.chkcalleridform = {};
      $scope.chkcalleridmodal = $modal({
        scope: $scope,
        template: route.callerid.formcheckcallerid,
        show: false,
        title: 'Check CallerID'
      });
    }

    $scope.chkcalleridmodal.$promise.then(function () {
      $scope.chkcalleridmodal.show();
      if ($scope.chkcalleridmodal.$scope.index == 1) {
        $('.nav-tabs a[href="#tab2"]').tab('show');
      }
    });
  }

  $scope.loadCust = function (accountid) {
    $scope.$emit('loadcust', { accountid: accountid });
    $scope.chkcalleridmodal.hide();
  }

  $scope.bulkSave_ = function (list, modal) {
    var o = {
      accountid: $scope.custid,
      list: list
    };

    $http.post(route.callerid.bulksave, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        modal.hide();
        $scope.loadList();
      }
    });
  }

  $scope.importSave = function () {
    var list = $scope.impform.list;
    $scope.bulkSave_(list, $scope.impmodal);
  }

  $scope.import = function () {
    $scope.impform = {};

    $scope.impmodal = $modal({
      scope: $scope,
      template: route.callerid.formimport,
      show: false,
      title: 'Import Caller ID'
    });
    $scope.impmodal.$promise.then($scope.impmodal.show);
  }

  $scope.copy = function () {
    $window.open(route.callerid.listview + $scope.custid, '_blank');
  }

  $scope.viewpdf = function () {
    $window.open(route.callerid.pdfview + $scope.custid, '_blank');
  }

  $scope.updateCallerID = function ($data) {
    var f = $scope.edit.data;

    var o = {
      accountid: $scope.custid,
      oldcallerid: f.callerid,
      callerid: $data,
      status: f.status
    };

    $http.post(route.callerid.update, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        f.callerid = $data;
      }
    });
    return false;
  }

  $scope.editCallerID = function (o) {
    $scope.edit = { data: o };
  }

  $scope.add = function () {
    var f = $scope.form;

    var o = {
      accountid: $scope.custid,
      callerid: f.callerid,
      status: f.status == true ? 1 : 0
    };

    $http.post(route.callerid.create, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        $scope.form = { status: true };
        $scope.loadList();
      }
    });
  }

  $scope.bulkSave = function () {
    var list = $scope.bulkmodal.$scope.list;
    $scope.bulkSave_(list, $scope.bulkmodal);
  }

  $scope.loadBulkList = function (data) {
    $scope.bulkmodal.$scope.list = data.list;
  }

  $scope.bulkCreate = function () {
    var f = $scope.bform;
    var valid = $scope.bulkmodal.$scope.fm.$valid;
    if (!valid)
    return;

    var o = {
      startcallerid: f.startcallerid,
      qty: f.qty,
      fromline: $scope.list.length
    };

    $http.post(route.callerid.bulkcreate, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.loadBulkList(data);
      }
    });
  }

  $scope.bulkCallerID = function () {
    if ($scope.gateway.subtype.isubtype == 630) {
      toastr.error('This feature is prohibited for Kiosk & mini Kisok customer!');
      return;
    }

    $scope.bform = {};

    $scope.bulkmodal = $modal({
      scope: $scope,
      template: route.callerid.formbulkcreate,
      show: false,
      title: 'Generate Caller ID'
    });
    $scope.bulkmodal.$scope.list = '';
    $scope.bulkmodal.$promise.then($scope.bulkmodal.show);
  }

  $scope.suspend = function (status) {
    var list = $scope.list;
    var lx = _.where(list, { selected: true });
    var ids = _.map(lx, function (o) {
      return o.callerid;
    });

    var o = {
      idxlist: ids,
      accountid: $scope.custid,
      status: status
    };

    $http.post(route.callerid.suspend, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        $scope.loadList();
      }
    });
  }

  $scope.suspendAll = function (status) {
    $http.post(route.callerid.suspendall, { accountid: $scope.custid, status: status }).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        $scope.loadList();
      }
    });
  }

  $scope.loadList = function () {
    var id = $scope.custid;
    $scope.selected.reset();

    $http.get(route.callerid.list + id).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.list = data.list;
      }
    });
  }

  $scope.deleteCallerid = function() {
    var list = $scope.list;
    var lx = _.where(list, { selected: true });
    var ids = _.map(lx, function (o) {
      return o.callerid;
    });

    $http.post(route.callerid.del, { idxlist: ids }).success(function (data) {
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

    bootbox.confirm("Delete the selected callerids ?", function (result) {
      if (result == true) {
        $scope.deleteCallerid();
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

  $scope.clean = function () {
    $scope.list = [];
    $scope.gateway = { ws: {}, subtype: {} };
    $scope.userdetail = {};
    $scope.form = { status: true };
  }

  $scope.initModel = function (o) {
    $scope.clean();

    if (o.error == 1) {
      return;
    }

    $scope.list = o.callerid;
    $scope.custid = o.userdetail.accountid;
    $scope.userdetail = o.userdetail;
  }

  $scope.init = function () {
    $scope.clean();

    $scope.$on('initModel', function (e, call) {
      $scope.initModel(call);
    });

    $scope.$on('gateway_home', function (e, call) {
      $scope.gateway = call;
    });
  }
}

app.controller('CalleridCtrl', ['$scope', '$http', '$modal', '$window', CalleridCtrl]);
