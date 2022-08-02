function GatewayCtrl($scope, $http, $modal) {

  $scope.maintype = {};
  $scope.gw = {};
  //$scope.lcrtype = {};
  //$scope.subtype = {};
  //$scope.ratetype = {};

  $scope.language = {};
  $scope.languagelist = [
    { id: 0, name: 'User Select' },
    { id: 1, name: 'B. Malaysia' },
    { id: 2, name: 'English' },
    { id: 3, name: 'Mandarin' }
  ];

  $scope.agroup = {};
  $scope.sipsubtype = {};
  $scope.siplcrtype = {};
  $scope.MaxCallAppearance = {};
  $scope.BatchDetail = {};
  $scope.Batchinfo = {};


  $scope.showpbx = false;

  $scope.updatesname = function ($data) {
    if ($data == null || $data == '')
    return 'Description is required';

    if ($scope.fer.sname == $data)
    return true;

    $scope.fer.sname = $data;

    $http.post(route.gw.ratetypeupdate, $scope.fer).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        $scope.loadRateTypes();
      }
    });
  }

  $scope.editsname = function (o) {
    $scope.fer = angular.copy(o);
  }

  $scope.addratetype = function () {
    var f = $scope.fmr;

    var o = {
      iratetype: f.iratetype,
      sname: f.sname
    };

    $http.post(route.gw.ratetypecreate, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        $scope.loadRateTypes();
      }
    });
  }

  $scope.addiratetype = function ($data) {
    if ($data == null || $data == '')
    return 'Rate type is required';

    if (isNaN(Number($data)))
    return 'Invalid rate type';

    var i = parseInt($data);
    if (i > 999)
    return 'Invalid rate type';

    $scope.fmr.iratetype = $data;
    $scope.addratetype();
  }

  $scope.addsname = function ($data) {
    if ($data == null || $data == '')
    return 'Description is required';

    $scope.fmr.sname = $data;
  }

  $scope.addmaxcallappearance = function ($data) {
    $scope.maxcallappearance = $data;
  
    $http.post(route.gw.MCAppearanceupdate, $scope.maxcallappearance).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        $scope.loadRateTypes();
      }
    });
  }


  $scope.editRateType = function () {
    $scope.fmr = {
      iratetype: '',
      sname: '',
      list: []
    };

    $scope.modal = $modal({
      scope: $scope,
      template: route.gw.formratetype,
      show: false,
      title: 'Edit Rate Type'
    });

    $http.get(route.gw.ratetype).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.fmr.list = data.list;
        $scope.modal.$promise.then($scope.modal.show);
      }
    });
  }

  $scope.loadRateTypes = function () {
    $http.get(route.gw.ratetype).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.modal.$scope.fmr.list = data.list;
        $scope.ratetypelist = data.list;
      }
    });
  }

  $scope.closeRateType = function () {
    $scope.modal.hide();
  }

  $scope.changews = function () {
    $scope.changeSubType();
  }

  $scope.changeMainType = function () {
    $scope.loadTypes($scope.maintype.selected.imaintype);
  }

  $scope.changeSubType = function () {
    var subtype = $scope.subtype.selected;
    var ws = $scope.agroup.selected;

    $scope.$emit('gateway', { ws: ws, subtype: subtype });
  }

  $scope.changeGateway = function () {
    var igatetype = $scope.gw.selected == null ? 0 : $scope.gw.selected.igatetype;
    if (igatetype == 7) {
      $scope.showpbx = true;
    }

    else {
      $scope.showpbx = false;
    }
  }

  $scope.loadTypes = function (maintype) {
    $http.get(route.gw.type + maintype).success(function (data) {
      $scope.maintypelist = data.maintype;
      $scope.gwlist = data.gatetype;
      $scope.subtypelist = data.subtype;
      $scope.ratetypelist = data.ratetype;
      $scope.lcrtypelist = data.lcrtype;
      $scope.MaxCallAppearance = data.MaxCallAppearance;
      $scope.Batchinfo = data.Batchinfo;


      $scope.initSelect(maintype);
    });
  }

  $scope.initSelect = function (maintype) {
    if (maintype == 0) {
      $scope.agroup.selected = _.size($scope.agrouplist) > 0 ? $scope.agrouplist[0] : null;
      $scope.sipsubtype.selected = _.size($scope.sipsubtypelist) > 0 ? $scope.sipsubtypelist[0] : null;
      $scope.siplcrtype.selected = _.size($scope.siplcrtypelist) > 0 ? $scope.siplcrtypelist[0] : null;

      $scope.maintype.selected = null;
      $scope.gw.selected = null;
      $scope.subtype.selected = null;
      $scope.ratetype.selected = null;
      $scope.lcrtype.selected = null;
      $scope.language.selected = null;
    }

    else {
      var o = $scope.userdetail;
      var x = o.userdetailext;
      var y = o.maxcallappearancedn;

      var agroup = _.size($scope.agrouplist) > 0 ? $scope.agrouplist[0] : null;
      var i = _.findIndex($scope.agrouplist, function (k) { return x == null ? false : x.wholesalerkey == k.wholesalerkey });
      $scope.agroup.selected = i >= 0 ? $scope.agrouplist[i] : agroup;

      var sipsubtype = _.size($scope.sipsubtypelist) > 0 ? $scope.sipsubtypelist[0] : null;
      i = _.findIndex($scope.sipsubtypelist, function (k) { return x == null ? false : x.sipsubtype == k.sipsubtype });
      $scope.sipsubtype.selected = i >= 0 ? $scope.sipsubtypelist[i] : sipsubtype;

      var siplcrtype = _.size($scope.siplcrtypelist) > 0 ? $scope.siplcrtypelist[0] : null;
      i = _.findIndex($scope.siplcrtypelist, function (k) { return x == null ? false : x.siplcrtype == k.siplcrtype });
      $scope.siplcrtype.selected = i >= 0 ? $scope.siplcrtypelist[i] : siplcrtype;

      //
      i = _.findIndex($scope.maintypelist, function (k) { return k.imaintype == maintype });
      $scope.maintype.selected = i >= 0 ? $scope.maintypelist[i] : null;

      i = _.findIndex($scope.gwlist, function (k) { return o.igatetype == null ? false : o.igatetype == k.igatetype });
      $scope.gw.selected = i >= 0 ? $scope.gwlist[i] : null;
      

      i = _.findIndex($scope.subtypelist, function (k) { return o.isubtype == null ? false : o.isubtype == k.isubtype });
      $scope.subtype.selected = i >= 0 ? $scope.subtypelist[i] : null;

      i = _.findIndex($scope.ratetypelist, function (k) { return o.iratetype == null ? false : o.iratetype == k.iratetype });
      $scope.ratetype.selected = i >= 0 ? $scope.ratetypelist[i] : null;

      i = _.findIndex($scope.lcrtypelist, function (k) { return o.lcrtype == null ? false : o.lcrtype == k.ilcrtype });
      $scope.lcrtype.selected = i >= 0 ? $scope.lcrtypelist[i] : null;

      i = _.findIndex($scope.languagelist, function (k) { return o.languagetype == null ? false : o.languagetype == k.id });
      $scope.language.selected = i >= 0 ? $scope.languagelist[i] : null;
    }

    $scope.changeSubType();
    $scope.changeGateway();
  }

  $scope.initModel = function (o) {
    if (o.error == 1) {
      $scope.userdetail = {};
      $scope.loadTypes(0);
      return;
    }

    $scope.userdetail = o.userdetail;
    $scope.loadTypes($scope.userdetail.imaintype);
  }

  $scope.init = function () {
    $scope.userdetail = {
      callerid: {},
      userdetailext: {},
      maxcallappearancedn:{}

    };

    $scope.$on('initModel', function (e, call) {
      $scope.initModel(call);
    });

    $scope.$on('getdata', function (e, call) {
      var o = {
        maintype: $scope.maintype.selected,
        gw: $scope.gw.selected,
        lcrtype: $scope.lcrtype.selected,
        subtype: $scope.subtype.selected,
        ratetype: $scope.ratetype.selected,
        language: $scope.language.selected,
        agroup: $scope.agroup.selected,
        sipsubtype: $scope.sipsubtype.selected,
        siplcrtype: $scope.siplcrtype.selected,
        // status: $scope.userdetail.userdetailext.status,
        pbxno: $scope.userdetail.pbxno,
        MaxCallAppearance: $scope.userdetail.maxcallappearancedn.MaxCallAppearance,
        callerid: $scope.userdetail.callerid,
        status: $scope.userdetail.status



      };
      $scope.$emit('gatewayinfo', o);
    });

    $http.get(route.gw.lookup).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.agrouplist = data.ws;
        $scope.sipsubtypelist = data.sipsubtype;
        $scope.siplcrtypelist = data.siplcrtype;

        $scope.initSelect(0);
        $scope.loadTypes(0);
      }
    });
  }
}

app.controller('GatewayCtrl', ['$scope', '$http', '$modal', GatewayCtrl]);
