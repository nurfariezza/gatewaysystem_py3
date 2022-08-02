function RTSMSCtrl($scope, $http) {

  $scope.create = function () {
    if ($scope.custid == null) {
      toastr.error('Please select an account first!');
      return;
    }

    var m = $scope.rtsms_master;
    var u = $scope.rtsms_user;
    var x = $scope.userdetail.userdetailext;

    var o = {
      enterpriseid: m.enterpriseid,
      wholesalerkey: x.wholesalerkey,
      accountid: $scope.custid,
      username: u.username,
      useremail: u.useremail,
      usermobile: u.usermobile,
      loginid: u.loginid,
      admin_password: u.pwd,
      senderid: m.senderid,
      maxuser: m.maxuser,
      maxcontact_admin: m.maxcontact_admin,
      maxalert_admin: m.maxalert_admin,
      maxcontact_user: m.maxcontact_user,
      maxalert_user: m.maxalert_user
    };

    $http.post(route.rtsms.create, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);
        $scope.userdetail.userdetailext.smsmasterid = data.smsmasterid;
        $scope.load();
      }
    });
  }

  $scope.update = function () {
    var chg = {};
    var m = $scope.rtsms_master;
    var u = $scope.rtsms_user;
    var xm = $scope.u_rtsms_master;
    var xu = $scope.u_rtsms_user;
    var x = $scope.userdetail.userdetailext;

    if (u.username != xu.username)
    chg.admin_name = 'Administrator';

    if (u.usermobile != xu.usermobile)
    chg.admin_mobile = 'Admin Mobile';

    if (u.useremail != xu.useremail)
    chg.admin_email = 'Admin Email';

    if (u.loginid != xu.loginid)
    chg.admin_login = 'Admin Login';

    if (m.senderid != xm.senderid)
    chg.sender_id = 'Sender ID';

    if (m.maxuser != xm.maxuser)
    chg.max_user = 'No. of User';

    if (m.maxcontact_admin != xm.maxcontact_admin)
    chg.max_admin_contact = 'Admin Contact Limit';

    if (m.maxalert_admin != xm.maxalert_admin)
    chg.max_admin_alert = 'Admin Alert Limit';

    if (m.maxcontact_user != xm.maxcontact_user)
    chg.max_user_contact = 'User Contact Limit';

    if (m.maxalert_user != xm.maxalert_user)
    chg.max_user_alert = 'User Alert Limit';

    var o = {
      chg: chg,
      accountid: $scope.custid,
      masterid: x.smsmasterid,
      enterpriseid: m.enterpriseid,
      userid: u.userid,
      username: u.username,
      useremail: u.useremail,
      usermobile: u.usermobile,
      loginid: u.loginid,
      admin_password: u.pwd,
      senderid: m.senderid,
      maxuser: m.maxuser,
      maxcontact_admin: m.maxcontact_admin,
      maxalert_admin: m.maxalert_admin,
      maxcontact_user: m.maxcontact_user,
      maxalert_user: m.maxalert_user
    };

    $http.post(route.rtsms.update, o).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        toastr.success(data.message);

      }
    });
  }

  $scope.load = function () {
    var x = $scope.userdetail.userdetailext;

    $http.get(route.rtsms.detail + x.smsmasterid).success(function (data) {
      if (data.error == 1) {
        toastr.error(data.message);
      }

      else {
        $scope.rtsms_master = data.rtsms_master;
        $scope.rtsms_user = data.rtsms_user;
        $scope.u_rtsms_master = angular.copy($scope.rtsms_master);
        $scope.u_rtsms_user = angular.copy($scope.rtsms_user);
      }
    });
  }

  $scope.isEmptySMSMasterID = function () {
    var b = false;
    var x = $scope.userdetail.userdetailext;
    if (x != null && x.smsmasterid == '')
    b = true;

    else if (x == null)
    b = true;

    return b;
  }

  $scope.clean = function () {
    $scope.userdetail = {};
    $scope.rtsms_master = {};
    $scope.rtsms_user = {};
    $scope.custid = null;
  }

  $scope.initModel = function (o) {
    $scope.clean();

    if (o.error == 1) {
      $scope.userdetail = {};
      return;
    }

    $scope.userdetail = o.userdetail;
    var x = $scope.userdetail.userdetailext;
    $scope.custid = o.userdetail.accountid;

    if (x.smsmasterid == 0)
    $scope.userdetail.userdetailext.smsmasterid = '';
  }

  $scope.init = function () {
    $scope.clean();

    $scope.$on('initModel', function (e, call) {
      $scope.initModel(call);
    });
  }
}

app.controller('RTSMSCtrl', ['$scope', '$http', RTSMSCtrl]);
