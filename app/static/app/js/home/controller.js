function HomeCtrl($scope, $http, $timeout, $modal, $window) {

  $scope.cust = {
    searchby: 0,
    keyword: ''
  };
  $scope.custpage = 1;
  $scope.customer = null;
  $scope.caption = '';
  $scope.custid = null;

  $scope.custkeywordChange = function () {
    var s = $scope.cust.keyword;
    if (s == null)
    s = '';

    var n = s.length;
    var c = '';
    if (n == 1)
    c = s.charAt(0);

    else if (n == 2) {
      c = s.charAt(0);
      if (c == '%')
      c = s.charAt(1);
    }

    if (c == '' || c == '%')
    return;

    if (c == '0')
    $scope.cust.searchby = 1;

    else if ('0123456789'.indexOf(c) < 0)
    $scope.cust.searchby = 2;

    else
    $scope.cust.searchby = 0;
  }

  $scope.getCustDetail = function () {
    var custinfo = $scope.custinfo;
    var u = custinfo.userdetail;
    var x = u.userdetailext == null ? {} : u.userdetailext;
    var gatewayinfo = $scope.gatewayinfo;
    var techinfo = $scope.techinfo;
    var k = $scope.userdetail == null ? {} : $scope.userdetail;

    var o = {
      batch_id: k.batch_id == null ? $scope.custid : k.batch_id,

    };

    return o;
  }

  $scope.deleteCust_ = function () {
    var o = {
      batch_id: $scope.userdetail.batch_id
    };

    $http.post(route.cust.del, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        $scope.custid = null;
        $scope.loadCust();
      }
    });
  }

  $scope.deleteCust = function () {
    bootbox.confirm("Delete this record ?", function (result) {
      if (result == true) {
        $scope.deleteCust_();
      }
    });
  }

  $scope.updateCust_ = function (cfm) {
    var o = $scope.getCustDetail();
    o['confirm'] = cfm;

    $http.post(route.cust.update, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else if (data.success == 0) {
        bootbox.confirm(data.prompt, function (result) {
          if (result == true) {
            $scope.updateCust_(true);
          }
        });
      }

      else {
        toastr.success(data.message);
        $scope.loadCust();
      }
    });
  }

  $scope.updateCust = function () {
    $scope.action = 2;
    $scope.$broadcast('getdata', {});
  }

  $scope.addCust_ = function () {
    var o = $scope.getCustDetail();

    if (o.wholesalerkey == null) {
      toastr.error('Please select a Agent Group for this account');
      return;
    }

    if (o.batch_id == null || o.batch_id == '' ) {
      toastr.error('Data not Complete (Customer Name or Customer AccountID)...');
      return;
    }

    $http.post(route.cust.create, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        $scope.loadCust();
      }
    });
  }

  $scope.addCust = function () {
    $scope.action = 0;
    $scope.$broadcast('getdata', {});
  }

  $scope.findCust = function () {
    $scope.gotoPage(1, true);
  }

  $scope.custpageChanged = function () {
    $scope.gotoPage($scope.modal.$scope.custpage, false);
  }

  $scope.gotoPage = function (page, i) {
    var o = {
      searchby: $scope.cust.searchby,
      keyword: $scope.cust.keyword,
      page: page
    };

    $http.post(route.cust.find, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.list = data.list;
        $scope.custpager = data.pager;
        $scope.custpage = $scope.custpager.pagenum;

        if (i) {
          if ($scope.cust.searchby == 1) {
            $scope.modal = $modal({
              scope: $scope,
              template: route.home.calleridlist,
              show: true,
              title: 'Caller ID List'
            });
          }

          else {
            $scope.modal = $modal({
              scope: $scope,
              template: route.home.custlist,
              show: true,
              title: 'Customer List'
            });
          }
        }

        else {
          $scope.modal.$scope.list = $scope.list;
          $scope.modal.$scope.custpager = $scope.custpager;
          $scope.modal.$scope.custpage = $scope.custpager.pagenum;
        }
      }
    });
  }


 $scope.selectRow = function ($event, o) {
    $event.stopPropagation();

    if ($scope.customer != null)
    $scope.customer.select = false;

    o.select = true;
    $scope.customer = o;
  }

  $scope.selectCust = function ($event, o) {
    $event.stopPropagation();

    $scope.selectRow($event, o);
    $scope.custid = o.batch_id;
    $scope.modal.hide();
    $scope.loadCust();
  }

  $scope.ok = function () {
    if ($scope.customer != null) {
      $scope.custid = $scope.customer.batch_id;
      $scope.modal.hide();
      $scope.loadCust();
      return;
    }

    $scope.modal.hide();
  }

  $scope.loadCust = function () {
    if ($scope.custid == null || $scope.custid == '') {
      $scope.$broadcast('initModel', { error: 1 });
      return;
    }

    $http.get(route.cust.detail + $scope.custid).success(function (data) {
      if (data.error == 1) {
        $scope.caption = '';
        $scope.$broadcast('initModel', data);
        toastr.error(data.message);
      }

      else {
        $scope.caption = data.userdetail.caption;
        $scope.userdetail = data.userdetail;
        $scope.availablenum = data.availablenum;
        $scope.usednum = data.usednum;
        $scope.assignednum = data.assignednum;

        $scope.suspendnum = data.suspendnum;
        $scope.testnum = data.testnum;
        $scope.reservenum = data.reservenum;



        $scope.$broadcast('initModel', data);
      }
    });
  }

  $scope.copyacc_ = function () {
    var o = $scope.getCustDetail();
    o['srcaccountid'] = $scope.srcaccountid;

    $http.post(route.cust.copy, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
      }
    });
  }

  $scope.copyacc = function () {
    if (_.isEmpty($scope.custid)) {
      toastr.error('Please select an account to copy');
      return;
    }

    bootbox.prompt("Please enter the new account ID", function (result) {
      if (!_.isNull(result) && !_.isEmpty(result)) {
        $scope.action = 1;
        $scope.srcaccountid = result;
        $scope.$broadcast('getdata', {});
      }
    });
  }

  $scope.aninewreg = function () {
    $window.open(route.aninewreg.index, '_blank');
  }

  $scope.topupreport = function () {
    $window.open(route.topupreport.index, '_blank');
  }

  $scope.checktopupstatus = function () {
    $window.open(route.topupstatus.index, '_blank');
  }

  $scope.reactivateByWholesaler_ = function () {
    var x = $scope.gateway.ws;
    var o = {
      wholesalerkey: x.wholesalerkey
    };

    $http.post(route.wholesaler.reactivate, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
      }
    });
  }

  $scope.reactivateByWholesaler = function () {
    var x = $scope.gateway.ws;

    bootbox.confirm("Are you sure to reactivate account by wholesaler " + x.wholesalername + " ?", function (result) {
      if (result == true) {
        $scope.reactivateByWholesaler_();
      }
    });
  }

  $scope.suspendByWholesaler_ = function () {
    var x = $scope.gateway.ws;
    var o = {
      wholesalerkey: x.wholesalerkey
    };

    $http.post(route.wholesaler.suspend, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
      }
    });
  }

  $scope.suspendByWholesaler = function () {
    var x = $scope.gateway.ws;

    bootbox.confirm("Are you sure to suspend account by wholesaler " + x.wholesalername + " ?", function (result) {
      if (result == true) {
        $scope.suspendByWholesaler_();
      }
    });
  }

  $scope.syncbal = function () {
    bootbox.confirm("Synchronize credit balance ?", function (result) {
      if (result == true) {
        $scope.action = 3;
        $scope.$broadcast('getdata', {});
      }
    });
  }

  $scope.syncbal_ = function () {
    var gatewayinfo = $scope.gatewayinfo;
    var igatetype = gatewayinfo.gw == null ? 0 : gatewayinfo.gw.igatetype;
    var k = $scope.userdetail;
    var o = {
      accountid: k.accountid,
      igatetype: igatetype,
      creditlimit: k.creditlimit
    };

    $http.post(route.cust.syncbal, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        $scope.loadCust();
      }
    });
  }

  $scope.view015number = function () {
    $window.open(route.view015number.index, '_blank');
  }

  $scope.view015numberbatchid = function () {
    $window.open(route.view015numberbatchid.index, '_blank');
  }

  $scope.viewprepaidnumber = function () {
    var url = route.viewprepaidnumber.download;
    $('#exportFrame').attr('src', url);
  }
  $scope.downloadusednumber = function () {
    var url = route.downloadusednumber.download;
    $('#exportFrame').attr('src', url);
  }

  $scope.downloadavailnumber = function () {
    var url = route.downloadavailnumber.download;
    $('#exportFrame').attr('src', url);
  }

  $scope.available015number = function () {
    $window.open(route.available015number.index, '_blank');
  }

  $scope.available015number = function () {
    $window.open(route.available015number.index, '_blank');
  }

  $scope.assign015number = function () {
    $window.open(route.assign015number.index, '_blank');
  }

  $scope.reserve015number = function () {
    $window.open(route.reserve015number.index, '_blank');
  }

  $scope.createlogin = function () {
    $window.open(route.createlogin.index, '_blank');
  }

  $scope.setpassword = function () {
    $window.open(route.setpassword.index, '_blank');
  }

  $scope.getCustIDList = function (a) {
    var o = {
      a: a
    };

    return $http.post(route.cust.lookup, o).then(function (data) {
      return data.data;
    });
  }

  $scope.init = function () {
    $scope.techinfo = { pbxmodel: '', supportteam: {}, technicalnotes: '' };
    $scope.custinfo = {};
    $scope.gatewayinfo = {};
    $scope.gateway = {};

    $scope.$on('gateway', function (e, call) {
      $scope.gateway = call;
      $scope.$broadcast('gateway_home', call);
    });

    $scope.$on('techinfo', function (e, call) {
      $scope.techinfo = call;
      if ($scope.action == 0)
      $scope.addCust_();

      else if ($scope.action == 1)
      $scope.copyacc_();

      else if ($scope.action == 2)
      $scope.updateCust_(false);

      else if ($scope.action == 3)
      $scope.syncbal_();
    });

    $scope.$on('gatewayinfo', function (e, call) {
      $scope.gatewayinfo = call;
    });

    $scope.$on('custinfo', function (e, call) {
      $scope.custinfo = call;
    });

    $scope.$on('loadcust', function (e, call) {
      $scope.custid = call.accountid;
      $scope.loadCust();
    })
  }
}

app.controller('HomeCtrl', ['$scope', '$http', '$timeout', '$modal', '$window', HomeCtrl]);
