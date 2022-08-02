function FaxCtrl($scope, $http, $modal) {

  $scope.didprefix = '015';
  $scope.didnum = null;

  $scope.selectDIDRow = function ($event, o) {
    $event.stopPropagation();

    if ($scope.didnum != null)
    $scope.didnum.select = false;

    o.select = true;
    $scope.didnum = o;
  }

  $scope.selectDID = function ($event, o) {
    $event.stopPropagation();

    $scope.selectDIDRow($event, o);
    $scope.model.ddi = o.faxnum;
    $scope.modaldid.hide();

    var x = $scope.userdetail.userdetailext;
    var f = $scope.faxuser;

    var o = {
      guseridx: f.guseridx,
      ddi: $scope.model.ddi,
      wholesalerkey: x.wholesalerkey
    };

    $http.post(route.fax.postpaidassignnumber, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
      }
    });
  }

  $scope.reloadDID = function () {
    var x = $scope.userdetail.userdetailext;

    var o = {
      didprefix: $scope.didprefix,
      wholesalerkey: x.wholesalerkey
    };

    $http.post(route.fax.postpaidfreenumlist, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.didlist = data.list;
        $scope.modaldid.$scope.didlist = $scope.didlist;
      }
    });
  }

  $scope.loadDID = function () {
    $scope.modaldid = $modal({
      scope: $scope,
      template: route.fax.pickdidlist,
      show: false,
      title: 'Pick iFax DID'
    });
    $scope.modaldid.$promise.then($scope.modaldid.show);
  }

  $scope.save = function () {
    var m = $scope.model;
    var f = $scope.faxuser;

    if (f == null) {
      return;
    }

    var o = {
      guseridx: f.guseridx,
      disable_in_fax: m.disable_in_fax,
      in_notify_num: m.in_notify_num,
      in_format: m.in_format,
      fwdemail: m.fwdemail,
      disable_out_fax: m.disable_out_fax,
      out_dailylimit: m.out_dailylimit,
      out_notify_email: m.out_notify_email,
      email: m.email,
      disable_ifax: m.disable_ifax,
      tsi: m.tsi,
      custom_header: m.custom_header,
      password_retry: m.password_retry
    };

    $http.post(route.fax.update, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
      }
    });
  }

  $scope.deleteUser_ = function (x) {
    var o = {
      guseridx: x.guseridx,
      accountid: $scope.custid
    };

    $http.post(route.fax.del, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        $scope.list = data.list;
        $scope.model = {};
        $scope.faxuser = null;
      }
    });
  }

  $scope.deleteUser = function () {
    var list = $scope.list;
    var lx = _.where(list, { select: true });
    var x = null;
    if (lx.length > 0)
    x = lx[0];

    if (x == null)
    return;

    bootbox.confirm("Are you sure want to delete Fax User: " + x.username + " ?", function (result) {
      if (result == true)
      $scope.deleteUser_(x);
    });
  }

  $scope.ok = function () {
    var f = $scope.form;
    var x = $scope.userdetail.userdetailext;

    var valid = $scope.modal.$scope.fm.$valid;
    if (!valid)
    return;

    var o = {
      accountid: $scope.custid,
      masterid: x.smsmasterid,
      username: f.username,
      loginid: f.loginid,
      password: f.password,
      email: f.email
    };

    $http.post(route.fax.create, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        $scope.list = data.list;
        $scope.modal.hide();
      }
    });
  }

  $scope.createUser = function () {
    var x = $scope.userdetail.userdetailext;
    if (x != null && x.smsmasterid == 0) {
      toastr.error('You must need to create an SMS Account first, then only can create iFax User');
      return;
    }

    $scope.form = {};

    $scope.modal = $modal({
      scope: $scope,
      template: route.fax.formcreateuser,
      show: false,
      title: 'Create New Fax User'
    });
    $scope.modal.$promise.then($scope.modal.show);
  }

  $scope.deleteNumber_ = function () {
    var x = $scope.userdetail.userdetailext;
    var f = $scope.faxuser;

    var o = {
      guseridx: f.guseridx,
      ddi: $scope.model.ddi,
      wholesalerkey: x.wholesalerkey
    };

    $http.post(route.fax.postpaidunassignnumber, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
      }
    });
  }

  $scope.deleteNumber = function () {
    if ($scope.model.ddi == null)
    return;

    bootbox.confirm("Are you sure want to remove Fax DID " + $scope.model.ddi + " ?", function (result) {
      if (result == true)
      $scope.deleteNumber_();
    });
  }

  $scope.loadUser = function () {
    if ($scope.faxuser == null) {
      $scope.model = {};
      return;
    }

    $http.get(route.fax.detail + $scope.faxuser.guseridx).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.model = data.model;
      }
    });
  }

  $scope.selectRow = function ($event, o) {
    $event.stopPropagation();

    if ($scope.faxuser != null)
    $scope.faxuser.select = false;

    o.select = true;
  }

  $scope.selectUser = function ($event, o) {
    $scope.selectRow($event, o);
    $scope.faxuser = o;
    $scope.loadUser();
  }

  $scope.reload = function () {
    $http.get(route.fax.list + $scope.custid).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.list = data.list;
      }
    });
  }

  $scope.clean = function () {
    $scope.userdetail = {};
    $scope.list = [];
    $scope.model = {};
    $scope.faxuser = null;
    $scope.custid = null;
  }

  $scope.initModel = function (o) {
    $scope.clean();

    if (o.error == 1) {
      return;
    }

    $scope.userdetail = o.userdetail;
    $scope.custid = o.userdetail.accountid;
  }

  $scope.init = function () {
    $scope.clean();

    $scope.$on('initModel', function (e, call) {
      $scope.initModel(call);
    });
  }
}

app.controller('FaxCtrl', ['$scope', '$http', '$modal', FaxCtrl]);
