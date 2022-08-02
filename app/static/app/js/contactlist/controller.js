function ContactListCtrl($scope, $http, $modal) {

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

  $scope.loadList = function () {
    var id = $scope.custid;
    $scope.selected.reset();

    $http.get(route.contactlist.list + id).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.list = data.list;
      }
    });
  }

  $scope.deleteContact = function () {
    var list = $scope.list;
    var lx = _.where(list, { selected: true });
    var ids = _.map(lx, function (o) {
      return o.idx;
    });

    $http.post(route.contactlist.del, { idxlist: ids }).success(function (data) {
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

    bootbox.confirm("Delete the selected contacts ?", function (result) {
      if (result == true) {
        $scope.deleteContact();
      }
    });
  }

  $scope.submitCreate = function () {
    var f = $scope.form;

    var o = {
      accountid: $scope.custid,
      sname: f.sname,
      ipersonincharge: f.ipersonincharge,
      srace: f.srace,
      sposition: f.sposition,
      sphone: f.sphone,
      sfax: f.sfax,
      smobile: f.smobile,
      semail: f.semail
    };

    $http.post(route.contactlist.create, o).success(function (data) {
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

    $http.post(route.contactlist.update, f).success(function (data) {
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
    $scope.form  = {};
    $scope.edit = false;

    $scope.modal = $modal({
      scope: $scope,
      template: route.contactlist.form,
      show: true,
      title: 'Create Contact'
    });
  }

  $scope.editcontact = function (o) {
    $scope.form = angular.copy(o);
    $scope.edit = true;

    $scope.modal = $modal({
      scope: $scope,
      template: route.contactlist.form,
      show: true,
      title: 'Edit Contact'
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
  }

  $scope.initModel = function (o) {
    $scope.clean();

    if (o.error == 1) {
      return;
    }

    $scope.list = o.contactlist;
    $scope.custid = o.userdetail.accountid;
  }

  $scope.init = function () {
    $scope.clean();

    $scope.$on('initModel', function (e, call) {
      $scope.initModel(call);
    });
  }
}

app.controller('ContactListCtrl', ['$scope', '$http', '$modal', ContactListCtrl]);
