function TopupReqCtrl($scope, $http, $modal, $filter) {

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

  $scope.form = null;

  $scope.fm = {
    amount: '0',
    topuptypeid: 1,
    sdesc: '',
    notes: '',
    update: false,
    updatetype: 0,
    topuptypelist: []
  }

  $scope.fe = {
    amount: '0',
    topuptypeid: 1,
    sdesc: '',
    notes: '',
    update: true,
    updatetype: 0,
    indexkey: 0,
    topuptypelist: []
  }

  $scope.$watch('fm.topuptypeid', function (newVal, oldVal) {
    if (newVal !== oldVal) {
      var selected = $filter('filter')($scope.fm.topuptypelist, {topuptypeid: $scope.fm.topuptypeid});
      $scope.fm.sdesc = selected.length ? selected[0].sdesc : null;
    }
  });

  $scope.updateamount_ = function () {
    var f = $scope.form;

    var o = {
      amount: f.amount,
      regkey: f.indexkey
    };

    $http.post(route.topupreq.updateamount, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
        $scope.eamount.data.amount = $scope.eamount.amount;
      }

      else {
        toastr.success(data.message);
        $scope.loadList();
      }
    });
  }

  $scope.updateamount = function ($data) {
    var f = $scope.eamount.data;
    $scope.form = $scope.fe;

    if (f.posted != 0)
    return 'Unable to update this topup request because it just has been posted';

    var b = $scope.isvalidateamount($data);

    if (b != true)
    return b;

    $scope.fe.amount = $data;
    $scope.fe.indexkey = $scope.eamount.data.indexkey;
    $scope.form = $scope.fe;
    $scope.updateamount_();
  }

  $scope.editamount = function (o) {
    $scope.eamount = { data: o, amount: o.amount };
  }

  $scope.updatenotes_ = function () {
    var f = $scope.form;

    var o = {
      notes: f.notes,
      regkey: f.indexkey
    };

    $http.post(route.topupreq.updatenotes, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
        $scope.enotes.data.notes = $scope.enotes.notes;
      }

      else {
        toastr.success(data.message);
        $scope.loadList();
      }
    });
  }

  $scope.updatenotes = function ($data) {
    var f = $scope.enotes.data;

    if (f.posted != 0)
    return 'Unable to update this topup request because it just has been posted';

    var b = isvalidnotes($data);

    if (b != true)
    return b;

    $scope.fe.notes = $data;
    $scope.fe.indexkey = $scope.enotes.data.indexkey;
    $scope.form = $scope.fe;
    $scope.updatenotes_();
  }

  $scope.editnotes = function (o) {
    $scope.enotes = { data: o, notes: o.notes };
  }

  $scope.updatetopuptype_ = function ($data) {
    $scope.fe.topuptypeid = $data;
    $scope.fe.indexkey = $scope.etopuptype.data.indexkey;
    var k = _.find($scope.fm.topuptypelist, function (x) {
      return $data == x.topuptypeid;
    });
    if (k != null)
    $scope.fe.sdesc = k.sdesc;

    $scope.form = $scope.fe;
    $scope.submit();
  }

  $scope.updatetopuptype = function ($data) {
    var f = $scope.etopuptype.data;

    if (f.posted != 0)
    return 'Unable to update this topup request because it just has been posted';

    $scope.updatetopuptype_($data);
  }

  $scope.addamount = function ($data) {
    var b = $scope.isvalidateamount($data);
    $scope.form = $scope.fm;

    if (b != true)
    return b;

    $scope.fm.amount = $data;
    $scope.form = $scope.fm;
    $scope.submit();
  }

  $scope.addnotes = function ($data) {
    var b = $scope.isvalidnotes($data);

    if (b != true)
    return b;

    $scope.fm.notes = $data;
    $scope.form = $scope.fm;
  }

  $scope.isvalidateamount = function ($data) {
    var b = true;

    if ($data == null || $data == '')
    return 'Amount is required';

    if ($data.length > 10)
    return 'The maximum length is 10 characters';

    if (isNaN(Number($data)))
    return 'Invalid amount';

    if ($scope.form.update == false && $scope.form.topuptypelist.length < 1)
    b = false;

    return b;
  }

  $scope.isvalidnotes = function ($data) {
    var b = true;

    if ($data == null || $data == '')
    return 'Notes is required';

    if ($data.length > 255)
    return 'The maximum length is 255 characters';

    return b;
  }

  $scope.loadtopuptypes = function (o) {
    if (o != null)
    $scope.etopuptype = { data: o };

    $http.get(route.topupreq.add).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.fm.topuptypelist = data.list;
        $scope.fe.topuptypelist = data.list;
      }
    });
  }

  $scope.submit = function () {
    var f = $scope.form;
    var list = f.topuptypelist;
    var topuptype = _.find(list, function (x) {
      return x.topuptypeid == f.topuptypeid
    });
    var isnonepaymenttopup = topuptype.requirepayment == 0 ? true : false;
    var x = $scope.gateway.ws;

    var o = {
      isnonepaymenttopup: isnonepaymenttopup,
      amount: f.amount,
      colagency: 'REDTONE',
      topuptype: f.topuptypeid,
      topuptypedesc: topuptype.sdesc,
      wholesalerkey: x.wholesalerkey
    };

    $http.post(route.topupreq.check, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        if (isnonepaymenttopup) {
          bootbox.confirm("This will post the " + topuptype.sdesc + " request immediately, confirm to post ? Record cannot be changed once posted, if you need to put some notes, please select 'Cancel' and key in some notes first", function (result) {
            if (result == true) {
              if (data.paylater != 1)
              $scope.showFormAuth(isnonepaymenttopup, topuptype, data);
              //$scope.submit_(true);
            }
          });
        }

        else {
          $scope.submit_(isnonepaymenttopup, topuptype, '', '', data);
        }
      }
    });
  }

  $scope.showFormAuth = function (isnonepaymenttopup, topuptype, res) {
    $http.get(route.topupreq.supervisorlist).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.formauth = {
          supervisor: '',
          ip: '',
          psw: '',
          remark: '',
          supervisorlist: data.list,
          isnonepaymenttopup: isnonepaymenttopup,
          topuptype: topuptype,
          res: res
        };

        $scope.modalauth = $modal({
          scope: $scope,
          template: route.topupreq.formauth,
          show: true,
          title: 'Get Authority for topup:' + res.colagency
        });
      }
    });
  }

  $scope.changeSupervisor = function () {
    var o = _.find($scope.formauth.supervisorlist, function (x) {
      return x.sloginname == $scope.formauth.supervisor;
    });
    $scope.formauth.ip = o.ip;
  }

  $scope.sendReq = function () {
    if ($scope.formauth.remark == '')
    toastr.error('Please enter the remark');

    else {
      var o = {
        accountid: $scope.custid,
        accountname: $scope.custname,
        amount: $scope.fm.amount,
        topuptype: $scope.formauth.topuptype.sdesc,
        remark: $scope.formauth.remark,
        ip: $scope.formauth.ip
      };

      $http.post(route.topupreq.sendreq, o).success(function (data) {
        if (data.error == 1) {
          toastr.error(data.message);
        }

        else {
          $scope.formauth.psw = data.psw;
        }
      });
    }
  }

  $scope.submitAuth = function () {
    var f = $scope.formauth;

    var o = {
      supervisor: f.supervisor,
      psw: f.psw,
      remark: f.remark
    };

    $http.post(route.topupreq.authoritysubmit, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.submit_(f.isnonepaymenttopup, f.topuptype, f.supervisor, f.remark, f.res);
      }
    });
  }

  $scope.submit_ = function (isnonepaymenttopup, topuptype, authority, authorityremark, res) {
    var f = $scope.form;

    var o = {
      isnonepaymenttopup: isnonepaymenttopup,
      accountid: $scope.custid,
      amount: res.amt,
      colagency: res.colagency,
      topuptype: topuptype.topuptypeid,
      notes: f.notes,
      wholesalerkey: $scope.gateway.ws.wholesalerkey,
      authority: authority,
      authorityremark: authorityremark,
      batchupload: $scope.batchupload,
      subtype: $scope.gateway.subtype.isubtype
    };

    if (f.update == false) {
      $http.post(route.topupreq.create, o).success(function (data) {
        if (data.error == 1) {
          toastr.error(data.message);
        }

        else {
          toastr.success(data.message);
          $scope.loadList();
        }
      });
    }

    else {
      o['regkey'] = f.indexkey;
      if (f.updatetype == 2) { //topuptype
        $http.post(route.topupreq.updatetopuptype, o).success(function (data) {
          if (data.error == 1) {
            toastr.error(data.message)
          }

          else {
            toastr.success(data.message);
            $scope.loadList();
          }
        });
      }
    }
  }

  $scope.loadList = function () {
    var id = $scope.custid;
    $scope.selected.reset();

    $http.get(route.topupreq.list + id).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.list = data.list;
      }
    });
  }

  $scope.deletereq = function () {
    var list = $scope.list;
    var lx = _.where(list, { selected: true });
    var ids = _.map(lx, function (o) {
      return o.indexkey;
    });

    $http.post(route.topupreq.del, { idxlist: ids }).success(function (data) {
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

    bootbox.confirm("Remove the selected topup requests ?", function (result) {
      if (result == true) {
        $scope.deletereq();
      }
    });
  }

  $scope.selectRow = function ($event, o) {
    $event.stopPropagation();

    if (o.posted != 0) {
      o.selected = false;
      return;
    }

    if (o.selected)
    ++$scope.selected.count;

    else
    --$scope.selected.count;
  }

  $scope.selectAll = function ($event) {
    $event.stopPropagation();

    var list = null;
    var x = 0;

    if ($scope.list != null)
    list = $scope.list;

    _.each(list, function (o, i, l) {
      if (o.posted != 0)
      o.selected = false;

      else {
        o.selected = $scope.selected.all;
        ++x;
      }
    });

    if ($scope.selected.all)
    $scope.selected.count = x;

    else
    $scope.selected.count = 0;
  }

  $scope.clean = function () {
    $scope.list = [];
    $scope.gateway = { ws: {}, subtype: {} };
  }

  $scope.initModel = function (o) {
    $scope.clean();

    if (o.error == 1) {
      return;
    }

    $scope.custid = o.userdetail.accountid;
    $scope.custname = o.userdetail.name;
    $scope.list = o.topuprequest;
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

app.controller('TopupReqCtrl', ['$scope', '$http', '$modal', '$filter', TopupReqCtrl]);
