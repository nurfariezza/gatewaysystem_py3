function CustCtrl($scope, $http) {

  $scope.acstatus = {};
  $scope.acstatuslist = [
    { id: 0, name: 'Active' },
    { id: 1, name: 'Used' },
    { id: 2, name: 'Suspended' },
    { id: 3, name: 'Testing' }
  ];

  $scope.state = {};
  $scope.statelist = ['',
  'Johor', 'Kedah', 'Kelantan', 'Terengganu', 'Melaka',
  'Negeri Sembilan', 'Pahang', 'Perak', 'Perlis', 'Pulau Pinang',
  'Sabah', 'Sarawak', 'Selangor Darul Ehsan', 'Wilayah Persekutuan'
];

$scope.ucategory = {};
$scope.ucategorylist = [
  'UNDEFINED', 'PLATINUM', 'GOLD', 'SILVER', 'BRONZE', 'OTHERS', 'ODC', 'METASWITCH'
];

$scope.disableCountryCode = function () {
  var w = $scope.userdetail.wscountries;
  var a = w != null ? !w.isenabled : false;
  return a;
}

$scope.updateCountryCode = function () {
  if ($scope.userdetail.accountid == null) {
    toastr.error('Please select an account first');
    return;
  }

  // var w = $scope.userdetail.wscountries;

  var o = {
    custid: $scope.userdetail.batch_id
    // enabled: w.isenabled,
    // allow: w.iscountryallow,
    // country: w.country
  };

  // $http.post(route.cust.updatecountrycode, o).success(function (data) {
  //   if (data.error == 1) {
  //     toastr.error(data.message);
  //   }

  //   else {
  //     toastr.success(data.message);
  //   }
  // });
}

$scope.refreshMOBUsage = function () {
  if ($scope.userdetail.accountid == null) {
    toastr.error('Please select an account first');
    return;
  }

  $http.get(route.cust.loadmobusage + $scope.userdetail.accountid).success(function (data) {
    if (data.error == 1) {
      toastr.error(data.message);
    }

    else {
      $scope.MOBUsage = data.data;
    }
  });
}

$scope.refreshSTDUsage = function () {
  if ($scope.userdetail.accountid == null) {
    toastr.error('Please select an account first');
    return;
  }

  $http.get(route.cust.loadstdusage + $scope.userdetail.accountid).success(function (data) {
    if (data.error == 1) {
      toastr.error(data.message);
    }

    else {
      $scope.STDUsage = data.data;
    }
  });
}

$scope.refreshIDDUsage = function () {
  if ($scope.userdetail.accountid == null) {
    toastr.error('Please select an account first');
    return;
  }

  $http.get(route.cust.loadiddusage + $scope.userdetail.accountid).success(function (data) {
    if (data.error == 1) {
      toastr.error(data.message);
    }

    else {
      $scope.IDDUsage = data.data;
    }
  });
}

$scope.resetMOBUsage_ = function () {
  $http.get(route.cust.resetmobusage + $scope.userdetail.accountid).success(function (data) {
    if (data.error == 1) {
      toastr.error(data.message);
    }

    else {
      toastr.success(data.message);
    }
  });
}

$scope.resetSTDUsage_ = function () {
  $http.get(route.cust.resetstdusage + $scope.userdetail.accountid).success(function (data) {
    if (data.error == 1) {
      toastr.error(data.message);
    }

    else {
      toastr.success(data.message);
    }
  });
}

$scope.resetIDDUsage_ = function () {
  $http.get(route.cust.resetiddusage + $scope.userdetail.accountid).success(function (data) {
    if (data.error == 1) {
      toastr.error(data.message);
    }

    else {
      toastr.success(data.message);
    }
  });
}

$scope.resetMOBUsage = function () {
  if ($scope.userdetail.accountid == null) {
    toastr.error('Please select an account first');
    return;
  }

  bootbox.confirm("Are you sure want to reset this account's MOB Usage??", function (result) {
    if (result == true) {
      $scope.resetMOBUsage_();
    }
  });
}

$scope.resetSTDUsage = function () {
  if ($scope.userdetail.accountid == null) {
    toastr.error('Please select an account first');
    return;
  }

  bootbox.confirm("Are you sure want to reset this account's STD Usage??", function (result) {
    if (result == true) {
      $scope.resetSTDUsage_();
    }
  });
}

$scope.resetIDDUsage = function () {
  if ($scope.userdetail.accountid == null) {
    toastr.error('Please select an account first');
    return;
  }

  bootbox.confirm("Are you sure want to reset this account's IDD Usage??", function (result) {
    if (result == true) {
      $scope.resetIDDUsage_();
    }
  });
}

$scope.initSelect = function () {
  $scope.acstatus.selected = $scope.acstatuslist[1];
  $scope.state.selected = $scope.statelist[0];
  // $scope.ucategory.selected = $scope.ucategorylist[0];

  $scope.userdetail = {
    userdetailext: {
      // iddusagealert: 2000,
      // iddusagebar: 10000,
      // stdusagealert: 0,
      // stdusagebar: 0,
      // mobusagealert: 0,
      // mobusagebar: 0
    }
  };
}

$scope.initModel = function (o) {
  if (o.error == 1) {
    $scope.userdetail = {};
    $scope.initSelect();
    return;
  }

  $scope.userdetail = o.userdetail;
  var x = $scope.userdetail.userdetailext;

  var acstatus = _.findWhere($scope.acstatuslist, { id: x.acstatus });
  if (acstatus != null)
  $scope.acstatus.selected = acstatus;

  var state = _.find($scope.statelist, function (i) {
    return i == x.State;
  });
  if (state != null)
  $scope.state.selected = state;

  $scope.ucategory.selected = $scope.ucategorylist[x.usagecategory];
}

$scope.init = function () {
  $scope.userdetail = {
    batch_id: '',
    batch_qty:'',
    assign_date: '',
    assignee: '',

    
    userdetailext: {
      callerid: '',
      state: '',
      code_area: '',
      status: '',
      wskey: '',
      assigndate: '',
      blockdate: '',
      releasedate: '',
    }
  };
  $scope.initSelect();

  $scope.$on('initModel', function (e, call) {
    $scope.initModel(call);
  });

  $scope.$on('getdata', function (e, call) {
    var ucategory = $scope.ucategory.selected == null ? null : _.indexOf($scope.ucategorylist, $scope.ucategory.selected);

    var o = {
      userdetail: $scope.userdetail,
      acstatus: $scope.acstatus.selected,
      state: $scope.state.selected,
      ucategory: ucategory
    };
    $scope.$emit('custinfo', o);
  });
}
}

app.controller('CustCtrl', ['$scope', '$http', CustCtrl]);
