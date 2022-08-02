function BBCalleridblockCtrl($scope, $http, $modal) {


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

  $scope.selectedbb = {
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

  $scope.getSelected015 = function () {
    var list = $scope.rmodal.$scope.list;
    
    var lx = _.where(list, { selected: true });
    var ids = _.map(lx, function (o) {
      return o.bb_rt015;
    });
    return ids;
  }

  $scope.addtoacc_ = function () {
    var list = $scope.rmodal.$scope.list;
    var lx = _.where(list, { selected: true });
    var ids = _.map(lx, function (o) {
      return { callerid: o.bb_rt015, allowpstn: o.bb_allowpstn, pwd: o.bb_015pwd };
    });

    var o = {
      idxlist: ids,
      accountid: $scope.custid
    };

    $http.post(route.bbcallerid.addtoacc, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        $scope.reloadFormList(1);
        $scope.loadList();
      }
    });
  }

  $scope.addtoacc = function () {
    if ($scope.selectedbb.count < 1)
    return;

    bootbox.confirm("Register the selected 015/03 number to ac: " + $scope.custid + " ?", function (result) {
      if (result == true)
      $scope.addtoacc_();
    });
  }

  $scope.genpwd_ = function () {
    var ids = $scope.getSelected015();

    $http.post(route.bbcallerid.genpwd, { idxlist: ids, accountid: $scope.custid }).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        $scope.reloadFormList($scope.rmodal.$scope.bbpage);
      }
    });
  }

  $scope.genpwd = function () {
    if ($scope.selectedbb.count < 1)
    return;

    bootbox.confirm("Generate new password for the selected 015/03 numbers ?", function (result) {
      if (result == true) {
        $scope.genpwd_();
      }
    });
  }

  $scope.nicenumset = function (i) {
    if ($scope.selectedbb.count < 1)
    return;

    var ids = $scope.getSelected015();

    $http.post(route.bbcallerid.nicenumset, { idxlist: ids, nicenum: i }).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        $scope.reloadFormList($scope.rmodal.$scope.bbpage);
      }
    });
  }

  $scope.nicenumtoggle = function () {
    if ($scope.selectedbb.count < 1)
    return;

    var ids = $scope.getSelected015();

    $http.post(route.bbcallerid.nicenumtoggle, { idxlist: ids }).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        $scope.reloadFormList($scope.rmodal.$scope.bbpage);
      }
    });
  }

  $scope.bbpstnset = function (i) {
    if ($scope.selectedbb.count < 1)
    return;

    var ids = $scope.getSelected015();

    $http.post(route.bbcallerid.pstnset, { idxlist: ids, pstn: i }).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        $scope.reloadFormList($scope.rmodal.$scope.bbpage);
      }
    });
  }

  $scope.bbpstntoggle = function () {
    if ($scope.selectedbb.count < 1)
    return;

    var ids = $scope.getSelected015();

    $http.post(route.bbcallerid.pstntoggle, { idxlist: ids }).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        $scope.reloadFormList($scope.rmodal.$scope.bbpage);
      }
    });
  }

  $scope.selectbbRow = function ($event, o) {
    $event.stopPropagation();

    if (o.selected)
    ++$scope.selectedbb.count;

    else
    --$scope.selectedbb.count;
  }

  $scope.selectbbAll = function ($event) {
    $event.stopPropagation();

    var list = null;
    var n = 0;

    if ($scope.rmodal.$scope.list != null)
    list = $scope.rmodal.$scope.list;

    if (list != null)
    n = list.length;

    for (var i = 0; i < n; i++) {
      var o = list[i];
      o.selected = $scope.selectedbb.all;
    }

    if ($scope.selectedbb.all)
    $scope.selectedbb.count = n;

    else
    $scope.selectedbb.count = 0;
  }

  $scope.reloadFormList = function (page) {
    $scope.gotoPageForm(page, false);
  }

  $scope.bbpageChanged = function () {
    $scope.gotoPageForm($scope.rmodal.$scope.bbpage, false);
  }

  $scope.gotoPageForm = function (page, i) {
    var x = $scope.gateway.ws;
    $scope.selectedbb.reset();

    var v = {
      wholesalerkey: x.wholesalerkey,
      nicenum: $scope.rform.nicenum,
      search: $scope.rform.search,
      page: page
    };

    $http.post(route.bbcallerid.listws, v).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        if (i) {
          $scope.rmodal = $modal({
            scope: $scope,
            template: route.bbcallerid.formaddnew015number,
            show: false,
            title: 'Add RT015/03 Number'
          });
          $scope.rmodal.$scope.list = data.list;
          $scope.rmodal.$scope.bbpager = data.pager;
          $scope.rmodal.$scope.bbpage = data.pager.pagenum;
          $scope.rmodal.$promise.then($scope.rmodal.show);
        }

        else {
          $scope.rmodal.$scope.list = data.list;
          $scope.rmodal.$scope.bbpager = data.pager;
          $scope.rmodal.$scope.bbpage = data.pager.pagenum;
        }
      }
    });
  }

  $scope.download_ = function (i) {
    var a = 'id=' + i;
    var q = '?' + a;
    var url = route.bbcallerid.listwsdownload + q;
    $('#exportFrame').attr('src', url);
  }

  $scope.download = function () {
    var x = $scope.gateway.ws;
    var v = {
      wholesalerkey: x.wholesalerkey,
      nicenum: $scope.rform.nicenum,
      search: $scope.rform.search
    };

    $http.post(route.bbcallerid.listwsdownloadtemp, v).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.download_(data.data);
      }
    });
  }

  $scope.updateDisplayname = function ($data) {
    var f = $scope.editdisplay.data;

    if ($.trim($data) == $.trim(f.bb_displayname))
    return false;

    var o = {
      name: $.trim($data),
      callerid: f.authentication.callerid
    };

    $http.post(route.bbcallerid.displaynameupdate, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        f.bb_displayname = o.name;
      }
    });
  }

  $scope.editDisplayname = function (o) {
    $scope.editdisplay = { data: o };
  }

  $scope.updateMCA_ = function ($data) {
    var f = $scope.editmca.data;

    var o = {
      DirectoryNumber: f.maxcallappearancedn.DirectoryNumber,
      callerid: f.authentication.callerid,
      MaxCallAppearance: $.trim($data)
    };

    $http.post(route.bbcallerid.MaxCallAppearanceupdate, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        f.MaxCallAppearance = o.MaxCallAppearance;
        $scope.reloadFormList($scope.rmodal.$scope.bbpage);
      }
    });
  }

  $scope.updateMCA = function ($data) {
    var f = $scope.editmca.data;

    if ($.trim($data) == $.trim(f.MaxCallAppearance))
    return false;

    bootbox.confirm("Change the MCA port of " + f.authentication.callerid + " ?", function (result) {
      if (result == true) {
        $scope.updateMCA_($data);
      }
    });
    return false;
  }

  $scope.editmca = function (o) {
    $scope.editmca = { data: o };
  }


  
  $scope.updatecallfwd_ = function (x) {
    var f = $scope.editcallfwd.data;

    var o = {
      accountid: $scope.custid,
      callerid: f.authentication.callerid,
      callfwd: x
    };

    $http.post(route.bbcallerid.callfwdupdate, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        f.bb_forward = o.callfwd;
      }
    });
    return false;
  }

  $scope.updatecallfwd = function ($data) {
    var f = $scope.editcallfwd.data;
    var x = $.trim($data);

    if (x == $.trim(f.bb_forward))
    return false;

    var s = x == '' ? 'Remove' : 'Set';

    bootbox.confirm(s + " the call forwarding for " + f.authentication.callerid + " ?", function (result) {
      if (result == true) {
        $scope.updatecallfwd_(x);
      }
    });
    return false;
  }

  $scope.editcallfwd = function (o) {
    $scope.editcallfwd = { data: o };
  }

  $scope.updatePwd_ = function ($data) {
    var f = $scope.editpwd.data;

    var o = {
      accountid: $scope.custid,
      callerid: f.authentication.callerid,
      pwd: $.trim($data)
    };

    $http.post(route.bbcallerid.pwdupdate, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        f.bb_015pwd = o.pwd;
      }
    });
  }

  $scope.updatePwd = function ($data) {
    var f = $scope.editpwd.data;

    if ($.trim($data) == $.trim(f.bb_015pwd))
    return false;

    bootbox.confirm("Change the password of " + f.authentication.callerid + " ?", function (result) {
      if (result == true) {
        $scope.updatePwd_($data);
      }
    });
    return false;
  }

  $scope.editPwd = function (o) {
    $scope.editpwd = { data: o };
  }

  $scope.updateSubnetmask = function ($data) {
    var f = $scope.editsubnetmask.data;

    if ($.trim($data) == $.trim(f.subnetmask))
    return false;

    var o = {
      callerid: f.authentication.callerid,
      subnetmask: $.trim($data)
    };

    $http.post(route.bbcallerid.subnetmaskupdate, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        f.subnetmask = o.subnetmask;
      }
    });
    return false;
  }

  $scope.editSubnetmask = function (o) {
    $scope.editsubnetmask = { data: o };
  }

  $scope.updatePstn_ = function ($data) {
    var f = $scope.editpstn.data;

    var o = {
      batchid: $scope.custid,
      callerid: f.callerid,
      wskey: $data == true ? 1 : 0
    };

    $http.post(route.bbcallerid.sippstnupdate, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        f.wskey = o.wskey;
      }
    });
    return false;
  }

  $scope.updatePstn = function ($data) {
    var s = $data == true ? 1 : 0;

    if (s == $scope.editpstn.data.wskey)
    return false;

    bootbox.confirm("Extend Blocking Date to " + s + " ?", function (result) {
      if (result == true) {
        $scope.updatePstn_($data);
      }
    });
    return false;
  }

  $scope.editPstn = function (o) {
    $scope.editpstn = { data: o };
  }

  $scope.updatePrepaid_ = function ($data) {
    var f = $scope.editprepaid.data;

    var o = {
      accountid: $scope.custid,
      callerid: f.authentication.callerid,
      prepaid: $data == true ? 1 : 0
    };

    $http.post(route.bbcallerid.sipprepaidupdate, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        f.bb_prepaid = o.prepaid;
      }
    });
  }

  $scope.updatePrepaid = function ($data) {
    var s = $data == true ? "Set" : "Unset";
    var x = $data == true ? 1 : 0;

    if (x == $scope.editprepaid.data.bb_prepaid)
    return false;

    bootbox.confirm(s + " this sip number to prepaid mode ?", function (result) {
      if (result == true) {
        $scope.updatePrepaid_($data);
      }
    });
    return false;
  }

  $scope.editPrepaid = function (o) {
    $scope.editprepaid = { data: o };
  }

  $scope.add = function () {
    var o = $scope.userdetail;
    var x = $scope.gateway.ws;

    $scope.rform = {
      acc: o.accountid + '-' + o.name,
      wskey: x.wholesalername
    };

    $scope.gotoPageForm(1, true);
  }

  $scope.generatepwd_ = function () {
    var list = $scope.list;
    var lx = _.where(list, { selected: true });
    var ids = _.map(lx, function (o) {
      return o.authentication.callerid;
    });

    $http.post(route.bbcallerid.chgpwd, { idxlist: ids, accountid: $scope.custid }).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        $scope.loadList();
      }
    });
  }

  $scope.generatepwd = function () {
    if ($scope.selected.count < 1)
    return;

    bootbox.confirm("Change the selected 015/03 passwords ?", function (result) {
      if (result == true) {
        $scope.generatepwd_();
      }
    });
  }

  $scope.resume_ = function () {
    var listused = $scope.listused;
    var lx = _.filter(listused, function (o) {
      return o.selected == true && o.status == 1;
    });
    var ids = _.map(lx, function (o) {
      return { callerid: o.callerid};
    });

    var o = {
      idxlist: ids,
      batchid: $scope.custid
    };

    $http.post(route.bbcallerid.resume, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        $scope.loadList();
      }
    });
  }

  $scope.resume = function () {
    if ($scope.selected.count < 1)
    return;

    bootbox.confirm("Resume the selected numbers ?", function (result) {
      if (result == true) {
        $scope.resume_();
      }
    });
  }

  
  $scope.resumetestnum_ = function () {
    var listtest = $scope.listtest;
    var lx = _.filter(listtest, function (o) {
      return o.selected == true && o.status == 3;
    });
    var ids = _.map(lx, function (o) {
      return { callerid: o.callerid};
    });

    var o = {
      idxlist: ids,
      batchid: $scope.custid
    };

    $http.post(route.bbcallerid.resumetestnum, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        $scope.loadList();
      }
    });
  }

  $scope.resumetestnum = function () {
    if ($scope.selected.count < 1)
    return;

    bootbox.confirm("Release testing number to available numbers ?", function (result) {
      if (result == true) {
        $scope.resumetestnum_();
      }
    });
  }

    
  $scope.releasenumber_ = function () {
    var listblock = $scope.listblock;
    var lx = _.filter(listblock, function (o) {
      return o.selected == true && o.status == 2;
    });
    var ids = _.map(lx, function (o) {
      return { callerid: o.callerid};
    });

    var o = {
      idxlist: ids,
      batchid: $scope.custid
    };

    $http.post(route.bbcallerid.releasenumber, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        $scope.loadList();
      }
    });
  }

  $scope.releasenumber = function () {
    if ($scope.selected.count < 1)
    return;

    bootbox.confirm("Release selected numbers?", function (result) {
      if (result == true) {
        $scope.releasenumber_();
      }
    });
  }


  $scope.extendblocknum_ = function () {
    var listblock = $scope.listblock;
    var lx = _.filter(listblock, function (o) {
      return o.selected == true && o.status == 2;
    });
    var ids = _.map(lx, function (o) {
      return { callerid: o.callerid};
    });

    var o = {
      idxlist: ids,
      batchid: $scope.custid
    };

    $http.post(route.bbcallerid.extendblocknum, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        $scope.loadList();
      }
    });
  }

  $scope.extendblocknum = function () {
    if ($scope.selected.count < 1)
    return;

    bootbox.confirm("Confirm to extend blocking to 12 Month?", function (result) {
      if (result == true) {
        $scope.extendblocknum_();
      }
    });
  }

  $scope.settestnumber_ = function () {
    var list = $scope.list;
    var lx = _.filter(list, function (o) {
      return o.selected == true && o.status == 0;
    });
    var ids = _.map(lx, function (o) {
      return { callerid: o.callerid};
    });

    var o = {
      idxlist: ids,
      batchid: $scope.custid
    };

    $http.post(route.bbcallerid.settestnumber, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        $scope.loadList();
      }
    });
  }

  $scope.settestnumber = function () {
    if ($scope.selected.count < 1)
    return;

    bootbox.confirm("Set as Test Number?", function (result) {
      if (result == true) {
        $scope.settestnumber_();
      }
    });
  }

  $scope.suspend_ = function () {
    var list = $scope.list;
    var lx = _.filter(list, function (o) {
      return o.selected == true && o.status != 2;
    });
    var ids = _.map(lx, function (o) {
      return { callerid: o.callerid};
    });

    var o = {
      idxlist: ids,
      batchid: $scope.custid
    };

    $http.post(route.bbcallerid.suspend, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        $scope.loadList();
      }
    });
  }

  $scope.suspend = function () {
    if ($scope.selected.count < 1)
    return;

    bootbox.confirm("Block the selected number?", function (result) {
      if (result == true) {
        $scope.suspend_();
      }
    });
  }

  $scope.usedsuspend_ = function () {
    var listused = $scope.listused;
    var lx = _.filter(listused, function (o) {
      return o.selected == true && o.status != 2;
    });
    var ids = _.map(lx, function (o) {
      return { callerid: o.callerid};
    });

    var o = {
      idxlist: ids,
      batchid: $scope.custid
    };

    $http.post(route.bbcallerid.usedsuspend, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        $scope.loadList();
      }
    });
  }

  $scope.usedsuspend = function () {
    if ($scope.selected.count < 1)
    return;

    bootbox.confirm("Block the selected number?", function (result) {
      if (result == true) {
        $scope.usedsuspend_();
      }
    });
  }




  $scope.testnumsuspend_ = function () {
    var listtest = $scope.listtest;
    var lx = _.filter(listtest, function (o) {
      return o.selected == true && o.status != 2;
    });
    var ids = _.map(lx, function (o) {
      return { callerid: o.callerid};
    });

    var o = {
      idxlist: ids,
      batchid: $scope.custid
    };

    $http.post(route.bbcallerid.testnumsuspend, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        $scope.loadList();
      }
    });
  }

  $scope.testnumsuspend = function () {
    if ($scope.selected.count < 1)
    return;

    bootbox.confirm("Block the selected number?", function (result) {
      if (result == true) {
        $scope.testnumsuspend_();
      }
    });
  }

  // $scope.suspend_ = function () {
  //   var list = $scope.list;
  //   var lx = _.filter(list, function (o) {
  //     return o.selected == true && o.status == 2;
  //   });
  //   var ids = _.map(lx, function (o) {
  //     return { callerid: o.callerid};
  //   });


  //   // var ids = _.map(lx, function (o) {
  //   //   return { callerid: o.callerid};
  //   // });

  //   var o = {
  //     idxlist: ids,
  //     batchid: $scope.custid
  //   };


  //   $http.post(route.bbcallerid.suspend, o).success(function (data) {
  //     if (data.error == 1) {
  //       toastr.error(data.message);
  //     }

  //     else {
  //       toastr.success(data.message);
  //       $scope.loadList();
  //     }
  //   });
  // }

  // $scope.suspend = function () {
  //   if ($scope.selected.count < 1)
  //   return;

  //   bootbox.confirm("Block the selected 015/03 numbers ?", function (result) {
  //     if (result == true) {
  //       $scope.suspend_();
  //     }
  //   });
  // }

  $scope.loadList = function () {
    var id = $scope.custid;
    $scope.selected.reset();

    $http.get(route.bbcallerid.list + id).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.list = data.list;
      }
    });
  }

//test code==
// $scope.search = function (page) {
//   $scope.gotoPage(page, false);
// }

// $scope.custpageChanged = function () {
//   $scope.gotoPage($scope.bbpage, false);
// }

// $scope.gotoPage = function (page) {
//   var o = {
//     accountid: $scope.custid,
//     page:page
//   };

//   $http.post(route.bbcallerid.list, o).success(function (data) {
//     if (data.error == 1) {
//       toastr.error(data.message);
//     }

//     else {
 
//       $scope.list = data.list;
//       $scope.bbpager = data.pager;
//       $scope.bbpage = data.pager.pagenum;



//     }
//   });
// }


//end test code

// test code
$scope.clearcust = function () {
  $scope.list = [];
}

$scope.selectcust = function (o) {
  if (o.selected == true) {
    $scope.list.push(o);
  }

  else {
    var list = _.reject($scope.list, function (x) { return x.batchid == o.batchid });
    $scope.list = list;
  }
}

$scope.search = function () {
  $scope.gotoPage(1);
}

$scope.custpageChanged = function () {
  $scope.gotoPage($scope.custpage,false);
}

$scope.gotoPage = function (page,i) {
  var o = {
   // keyword: $scope.keyword,
    page: page
  }

  $http.post(route.bbcallerid.list, o).success(function (data) {
    if (data.error == 1) {
      toastr.error(data.message);
    }

    else {
      $scope.list = data.list;
      $scope.custpager = data.pager;
      $scope.custpage = data.pager.pagenum;

    }
  });
}
//end test code
  $scope.delete015 = function() {
    var list = $scope.list;
    var lx = _.filter(list, function (o) {
      return o.selected == true && o.status != 1;
    });
    var ids = _.map(lx, function (o) {
      return { callerid: o.callerid};
    });

    var o = {
      idxlist: ids,
      batchid: $scope.custid
    };

    $http.post(route.bbcallerid.del, o).success(function (data) {
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

    bootbox.confirm("Delete the selected numbers ?", function (result) {
      if (result == true) {
        $scope.delete015();
      }
    });
  }

//end test code
$scope.deletetestnum = function() {
  var listtest = $scope.listtest;
  var lx = _.filter(listtest, function (o) {
    return o.selected == true && o.status != 1;
  });
  var ids = _.map(lx, function (o) {
    return { callerid: o.callerid};
  });

  var o = {
    idxlist: ids,
    batchid: $scope.custid
  };

  $http.post(route.bbcallerid.deltestnum, o).success(function (data) {
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

$scope.removetestnum = function () {
  if ($scope.selected.count < 1)
  return;

  bootbox.confirm("Delete the selected numbers ?", function (result) {
    if (result == true) {
      $scope.deletetestnum();
    }
  });
}


$scope.deleteblocknum = function() {
  var listblock = $scope.listblock;
  var lx = _.filter(listblock, function (o) {
    return o.selected == true && o.status != 1;
  });
  var ids = _.map(lx, function (o) {
    return { callerid: o.callerid};
  });

  var o = {
    idxlist: ids,
    batchid: $scope.custid
  };

  $http.post(route.bbcallerid.delblocknum, o).success(function (data) {
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

$scope.removeblocknum = function () {
  if ($scope.selected.count < 1)
  return;

  bootbox.confirm("Delete the selected numbers ?", function (result) {
    if (result == true) {
      $scope.deleteblocknum();
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
    //$scope.show015pwd = show015pwd;
    //$scope.pager ={};


  }

  $scope.initModel = function (o) {
    $scope.clean();

    if (o.error == 1) {
      return;
    }

    $scope.list = o.rt015num;
    $scope.listused = o.rt015used;
    $scope.listblock = o.rt015block;
    $scope.listtest = o.rt015test;
    $scope.listreserved = o.rt015reserve;
    $scope.listusedbyaccntid = o.rt015usedbyaccntid


    $scope.custid = o.userdetail.batchid;
    // $scope.userdetail = o.userdetail;
    $scope.availablenum = o.availablenum;
    $scope.usednum = o.usednum;
    $scope.suspendnum = o.suspendnum;
    $scope.testnum = o.testnum;


    $scope.list.$scope.pager = o.pager;
    $scope.list.$scope.pager = o.pager.pagenum;
    $scope.custlist= [];
    $scope.custpager= o.pager.pagenum;
   // $scope.custpage= 1,
   

    //document.write(o.rt015num)

    //document.write($scope.list.$scope.pager)

  
  }

  $scope.init = function () {
    $scope.clean();
    $scope.gotoPage(1);

    $scope.$on('initModel', function (e, call) {
      $scope.initModel(call);
    });

    $scope.$on('gateway_home', function (e, call) {
      $scope.gateway = call;
    });
  }
}

app.controller('BBCalleridblockCtrl', ['$scope', '$http', '$modal', BBCalleridblockCtrl]);
