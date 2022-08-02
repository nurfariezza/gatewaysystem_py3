function CalleridCtrl($scope, $http, $modal, $window) {
	
//    $scope.menuOptions = [
//                          ['Copy', function ($itemScope) {
//                        	  $window.open(route.callerid.listview + $scope.custid, '_blank');
//                          }],
//                          ['Import', function ($itemScope) {
//                        	  $scope.import();
//                          }], null,
//                          ['Bulk CallerID Creation', function ($itemScope) {
//                        	  $scope.bulkCallerID();
//                          }], null,
//                          ['Suspend All', function ($itemScope) {
//                        	  $scope.suspendAll(0);
//                          }],
//                          ['Enable All', function ($itemScope) {
//                        	  $scope.suspendAll(1);
//                          }]
//    ];

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
    
    $scope.selected015 = {
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
            
            else if (data.error == 2) {
                bootbox.alert(data.message);
            }

            else {
                toastr.success(data.message);
                $scope.reloadFormList(1);
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
    
    $scope.pstnset = function (i) {
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
    
    $scope.pstntoggle = function () {
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
                    $scope.rmodal.$scope.bbpage = $scope.bbpager.pagenum;
                }
            }
        });
    }
    
    $scope.add015 = function () {
        var o = $scope.userdetail;
        var x = $scope.gateway.ws;
        
        $scope.rform = {
            acc: o.accountid + '-' + o.name,
            wskey: x.wholesalername
        };
        
        $scope.gotoPageForm(1, true);
    }
    
    $scope.showList = function () {
        return $scope.list != null && $scope.list.length > 0;
    }
    
    $scope.generatepwd_ = function () {
        var list = $scope.list015;
        var lx = _.where(list, { selected: true });
        var ids = _.map(lx, function (o) {
            return o.authentication.callerid;
        });
        
        $http.post(route.bbcallerid.chgpwd, { idxlist: ids, accountid: $scope.custid }).success(function (data) {
            if (data.error == 1) {
                toastr.error(data.message);
            }
            
            else if (data.error == 2) {
                bootbox.alert(data.message);
            }

            else {
                toastr.success(data.message);
                $scope.loadList015();
            }
        });
    }
    
    $scope.generatepwd = function () {
        if ($scope.selected015.count < 1)
            return;
        
        bootbox.confirm("Change the selected 015/03 passwords ?", function (result) {
            if (result == true) {
                $scope.generatepwd_();
            }  
        });
    }
    
    $scope.resume015_ = function () {
        var list = $scope.list015;
        var lx = _.filter(list, function (o) {
            return o.selected == true && o.authentication.status == 0;
        });
        var ids = _.map(lx, function (o) {
            return { callerid: o.authentication.callerid, allowpstn: o.bb_allowpstn, pwd: o.bb_015pwd };
        });
        
        var o = {
            idxlist: ids,
            accountid: $scope.custid
        };
        
        $http.post(route.bbcallerid.resume, o).success(function (data) {
            if (data.error == 1) {
                toastr.error(data.message);
            }
            
            else if (data.error == 2) {
                bootbox.alert(data.message);
            }

            else {
                toastr.success(data.message);
                $scope.loadList015();
            }
        });
    }
    
    $scope.resume015 = function () {
        if ($scope.selected015.count < 1)
            return;
        
        bootbox.confirm("Resume the selected 015/03 numbers ?", function (result) {
            if (result == true) {
                $scope.resume015_();
            }  
        });
    }
    
    $scope.suspend015_ = function () {
        var list = $scope.list015;
        var lx = _.filter(list, function (o) {
            return o.selected == true && o.authentication.status == 1;
        });
        var ids = _.map(lx, function (o) {
            return o.authentication.callerid;
        });
        
        $http.post(route.bbcallerid.suspend, { idxlist: ids, suspend: 1 }).success(function (data) {
            if (data.error == 1) {
                toastr.error(data.message);
            }
            
            else if (data.error == 2) {
                bootbox.alert(data.message);
            }

            else {
                toastr.success(data.message);
                $scope.loadList015();
            }
        });
    }
    
    $scope.suspend015 = function () {
        if ($scope.selected015.count < 1)
            return;
        
        bootbox.confirm("Suspend the selected 015/03 numbers ?", function (result) {
            if (result == true) {
                $scope.suspend015_();
            }  
        });
    }
    
    $scope.loadList015 = function () {
        var id = $scope.custid;
        $scope.selected015.reset();

        $http.get(route.bbcallerid.list + id).success(function (data) {
            if (data.error == 1) {
                toastr.error(data.message);
            }

            else {
                $scope.list015 = data.list;
            }
        });
    }
    
    $scope.delete015 = function() {
        var list = $scope.list015;
        var lx = _.where(list, { selected: true });
        var ids = _.map(lx, function (o) {
            return o.authentication.callerid;
        });
        
        $http.post(route.bbcallerid.del, { idxlist: ids }).success(function (data) {
            if (data.error == 1) {
                toastr.error(data.message);
            }
            
            else if (data.error == 2) {
                bootbox.alert(data.message);
            }

            else {
                toastr.success(data.message);
                $scope.loadList015();
            }
        });
    }
    
    $scope.remove015Items = function () {
        if ($scope.selected015.count < 1)
            return;
        
        bootbox.confirm("Remove the selected 015/03 numbers ?", function (result) {
            if (result == true) {
                $scope.delete015();
            }  
        });
    }

    $scope.select015Row = function ($event, o) {
        $event.stopPropagation();

        if (o.selected)
            ++$scope.selected015.count;

        else
            --$scope.selected015.count;
    }
    
    $scope.select015All = function ($event) {
        $event.stopPropagation();

        var list = null;
        var n = 0;

        if ($scope.list015 != null)
            list = $scope.list015;

        if (list != null)
            n = list.length;

        for (var i = 0; i < n; i++) {
            var o = list[i];
            o.selected = $scope.selected015.all;
        }

        if ($scope.selected015.all)
            $scope.selected015.count = n;

        else
            $scope.selected015.count = 0;
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
    
    $scope.save = function () {
        var f = $scope.form;
        var valid = $scope.editmodal.$scope.fm.$valid;
        if (!valid)
            return;
        
        var o = {
            accountid: $scope.custid,
            callerid: f.callerid,
            newcallerid: f.newcallerid,
            status: f.status
        };
        
        $http.post(route.callerid.update, o).success(function (data) {
            if (data.error == 1) {
                toastr.error(data.message);
            }
            
            else {
                toastr.success(data.message);
                $scope.loadList();
            }
        });
    }
    
    $scope.editCallerID = function ($event, o) {
        $event.stopPropagation();
        
        $scope.form = {
            callerid: o.callerid,
            newcallerid: o.callerid,
            status: o.status
        };
        
        $scope.editmodal = $modal({
    	    scope: $scope,
    	    template: route.callerid.form,
    	    show: false,
    	    title: 'Edit Caller ID'
    	});
    	$scope.editmodal.$promise.then($scope.editmodal.show);
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
    
    $scope.suspendAll = function (status) {
        $http.post(route.callerid.suspend, { accountid: $scope.custid, status: status }).success(function (data) {
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
        $scope.list015 = [];
        $scope.gateway = { ws: {}, subtype: {} };
        $scope.userdetail = {};
    }

    $scope.initModel = function (o) {
        $scope.clean();
        
        if (o.error == 1) {
            return;
        }

        // $scope.list = o.callerid;
        $scope.list015 = o.rt015num;
        $scope.custid = o.userdetail.accountid;
        $scope.userdetail = o.userdetail;
    }

    $scope.init = function () {
        $scope.clean();

        $scope.$on('initModel', function (e, call) {
            $scope.initModel(call);
        });
        
        $scope.$on('gateway', function (e, call) {
            $scope.gateway = call;
        });
    }
}

app.controller('CalleridCtrl', ['$scope', '$http', '$modal', '$window', CalleridCtrl]);
