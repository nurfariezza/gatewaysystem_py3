var route = (function () {

  var home = {
    custlist: utils.getUrl('/static/app/ngview/home/custlist.html'),
    calleridlist: utils.getUrl('/static/app/ngview/home/calleridlist.html')
  };

  var cust = {
    find: utils.getUrl('/app/cust/find/'),
    copy: utils.getUrl('/app/cust/copy/'),
    create: utils.getUrl('/app/cust/create/'),
    update: utils.getUrl('/app/cust/update/'),
    del: utils.getUrl('/app/cust/delete/'),
    detail: utils.getUrl('/app/cust/detail/'),
    loadiddusage: utils.getUrl('/app/cust/iddusage/load/'),
    loadstdusage: utils.getUrl('/app/cust/stdusage/load/'),
    loadmobusage: utils.getUrl('/app/cust/mobusage/load/'),
    resetiddusage: utils.getUrl('/app/cust/iddusage/reset/'),
    resetstdusage: utils.getUrl('/app/cust/stdusage/reset/'),
    resetmobusage: utils.getUrl('/app/cust/mobusage/reset/'),
    updatecountrycode: utils.getUrl('/app/cust/countrycode/update/'),
    syncbal: utils.getUrl('/app/cust/syncbal/'),
    lookup: utils.getUrl('/app/cust/lookup/')
  };

  var gw = {
    // lookup: utils.getUrl('/app/gateway/lookup/'),
    // type: utils.getUrl('/app/gateway/type/'),
    // ratetype: utils.getUrl('/app/gateway/ratetype/list/'),
    // ratetypecreate: utils.getUrl('/app/gateway/ratetype/create/'),
    // ratetypeupdate: utils.getUrl('/app/gateway/ratetype/update/'),
    // MCAppearanceupdate: utils.getUrl('/app/gateway/mca/update/'),
    // formratetype: utils.getUrl('/static/app/ngview/gateway/formratetype.html')
  };

  var rtsms = {
    detail: utils.getUrl('/app/rtsms/detail/'),
    // create: utils.getUrl('/app/rtsms/create/'),
    update: utils.getUrl('/app/rtsms/update/')
  };

  var fax = {
    list: utils.getUrl('/app/ifaxuser/list/'),
    detail: utils.getUrl('/app/ifaxuser/detail/'),
    postpaidassignnumber: utils.getUrl('/app/ifaxuser/postpaidassignnumber/'),
    postpaidunassignnumber: utils.getUrl('/app/ifaxuser/postpaidunassignnumber/'),
    create: utils.getUrl('/app/ifaxuser/create/'),
    update: utils.getUrl('/app/ifaxuser/update/'),
    del: utils.getUrl('/app/ifaxuser/delete/'),
    formcreateuser: utils.getUrl('/static/app/ngview/fax/formcreateuser.html'),
    postpaidfreenumlist: utils.getUrl('/app/ifaxuser/postpaidfreenum/list/'),
    pickdidlist: utils.getUrl('/static/app/ngview/fax/pickdidlist.html')
  };

  var callerid = {
    del: utils.getUrl('/app/callerid/delete/'),
    list: utils.getUrl('/app/callerid/list/'),
    suspend: utils.getUrl('/app/callerid/suspend/'),
    suspendall: utils.getUrl('/app/callerid/suspend/all/'),
    create: utils.getUrl('/app/callerid/create/'),
    update: utils.getUrl('/app/callerid/update/'),
    bulkcreate: utils.getUrl('/app/callerid/bulkcreate/'),
    bulksave: utils.getUrl('/app/callerid/bulksave/'),
    listview: utils.getUrl('/app/callerid/list/view/'),
    pdfview: utils.getUrl('/app/callerid/list/pdf/'),
    search: utils.getUrl('/app/callerid/search/'),
    formbulkcreate: utils.getUrl('/static/app/ngview/callerid/formbulkcreate.html'),
    form: utils.getUrl('/static/app/ngview/callerid/form.html'),
    formimport: utils.getUrl('/static/app/ngview/callerid/formimport.html'),
    formcheckcallerid: utils.getUrl('/static/app/ngview/callerid/formcheckcallerid.html')
  };

  var bbcallerid = {
    list: utils.getUrl('/app/bbcallerid/list/'),
    del: utils.getUrl('/app/bbcallerid/delete/'),
    deltestnum: utils.getUrl('/app/bbcallerid/delete/'),
    delblocknum: utils.getUrl('/app/bbcallerid/delete/'),
    suspend: utils.getUrl('/app/bbcallerid/suspend/'),
    testnumsuspend: utils.getUrl('/app/bbcallerid/testnumsuspend/'),

    usedsuspend: utils.getUrl('/app/bbcallerid/usedsuspend/'), 
    // resume for release test,used number and blocknumber
    resume: utils.getUrl('/app/bbcallerid/resume/'), // used
    releasenumber: utils.getUrl('/app/bbcallerid/releasenumber/'),//blocked
    resumetestnum: utils.getUrl('/app/bbcallerid/resumetestnum/'), //test
    extendblocknum: utils.getUrl('/app/bbcallerid/extendblocknum/'),//blocked


    settestnumber: utils.getUrl('/app/bbcallerid/settestnumber/'),
    blocknumber: utils.getUrl('/app/bbcallerid/blocknumber/'),
    unreservenumber: utils.getUrl('/app/bbcallerid/unreservenumber/'),

    chgpwd: utils.getUrl('/app/bbcallerid/changepwd/'),
    listws: utils.getUrl('/app/bbcallerid/listws/'),
    listwsdownloadtemp: utils.getUrl('/app/bbcallerid/listws/downloadtemp/'),
    listwsdownload: utils.getUrl('/app/bbcallerid/listws/download/'),
    pstntoggle: utils.getUrl('/app/bbcallerid/pstn/toggle/'),
    pstnset: utils.getUrl('/app/bbcallerid/pstn/set/'),
    nicenumtoggle: utils.getUrl('/app/bbcallerid/nicenum/toggle/'),
    nicenumset: utils.getUrl('/app/bbcallerid/nicenum/set/'),
    addtoacc: utils.getUrl('/app/bbcallerid/addtoacc/'),
    genpwd: utils.getUrl('/app/bbcallerid/generatepwd/'),
    displaynameupdate: utils.getUrl('/app/bbcallerid/displayname/update/'),
    callfwdupdate: utils.getUrl('/app/bbcallerid/callfwd/update/'),
    MaxCallAppearanceupdate: utils.getUrl('/app/bbcallerid/mca/update/'),
   // MCAppearanceupdate: utils.getUrl('/app/bbcallerid/mca/update/'),
    pwdupdate: utils.getUrl('/app/bbcallerid/pwd/update/'),
    subnetmaskupdate: utils.getUrl('/app/bbcallerid/subnetmask/update/'),
    sippstnupdate: utils.getUrl('/app/bbcallerid/sippstn/update/'),
    sipprepaidupdate: utils.getUrl('/app/bbcallerid/sipprepaid/update/'),
    formaddnew015number: utils.getUrl('/static/app/ngview/bbcallerid/formaddnew015number.html?v=1.01')
  };

  var pin = {
    list: utils.getUrl('/app/pin/list/'),
    listview: utils.getUrl('/app/pin/list/view/'),
    importsave: utils.getUrl('/app/pin/importsave/'),
    useridupdate: utils.getUrl('/app/pin/userid/update/'),
    create: utils.getUrl('/app/pin/create/'),
    update: utils.getUrl('/app/pin/update/'),
    del: utils.getUrl('/app/pin/delete/'),
    delall: utils.getUrl('/app/pin/delete/all/'),
    form: utils.getUrl('/static/app/ngview/pin/form.html'),
    formimport: utils.getUrl('/static/app/ngview/pin/formimport.html'),
    formimportwithdesc: utils.getUrl('/static/app/ngview/pin/formimportwithdesc.html')
  };

  var topupreq = {
    list: utils.getUrl('/app/topupreq/list/'),
    del: utils.getUrl('/app/topupreq/delete/'),
    add: utils.getUrl('/app/topupreq/add/'),
    check: utils.getUrl('/app/topupreq/check/'),
    create: utils.getUrl('/app/topupreq/create/'),
    updateamount: utils.getUrl('/app/topupreq/amount/update/'),
    updatenotes: utils.getUrl('/app/topupreq/notes/update/'),
    updatetopuptype: utils.getUrl('/app/topupreq/topuptype/update/'),
    sendreq: utils.getUrl('/app/topupreq/sendreq/'),
    authoritysubmit: utils.getUrl('/app/topupreq/authority/submit/'),
    supervisorlist: utils.getUrl('/app/supervisor/list/'),
    formauth: utils.getUrl('/static/app/ngview/topuprequest/form_getauthority.html')
  };

  var remark = {
    create: utils.getUrl('/app/remark/create/'),
    list: utils.getUrl('/app/remark/list/')
  };

  var contactlist = {
    create: utils.getUrl('/app/contactlist/create/'),
    update: utils.getUrl('/app/contactlist/update/'),
    del: utils.getUrl('/app/contactlist/delete/'),
    list: utils.getUrl('/app/contactlist/list/'),
    form: utils.getUrl('/static/app/ngview/contactlist/form.html')
  };

  var techinfo = {
    lookup: utils.getUrl('/app/techinfo/lookup/'),
    del: utils.getUrl('/app/techinfo/delete/'),
    add: utils.getUrl('/app/techinfo/add/'),
    create: utils.getUrl('/app/techinfo/create/'),
    update: utils.getUrl('/app/techinfo/update/'),
    list: utils.getUrl('/app/techinfo/list/'),
    form: utils.getUrl('/static/app/ngview/techinfo/form.html?v=2')
  };

  var topupreport = {
    index: utils.getUrl('/topupreport/'),
    listws: utils.getUrl('/app/topupreport/listws/'),
    listcust: utils.getUrl('/app/topupreport/listcust/'),
    listcustws: utils.getUrl('/app/topupreport/listcust/ws/'),
    downloadtemp: utils.getUrl('/app/topupreport/downloadtemp/'),
    download: utils.getUrl('/app/topupreport/download/')
  };

  var aninewreg = {
    index: utils.getUrl('/aninewreg/'),
    listcust: utils.getUrl('/app/aninewreg/listcust/'),
    downloadtemp: utils.getUrl('/app/aninewreg/downloadtemp/'),
    download: utils.getUrl('/app/aninewreg/download/')
  };

  var topupstatus = {
    index: utils.getUrl('/topupstatus/'),
    list: utils.getUrl('/app/topupstatus/list/')
  };

  var view015number = {
    index: utils.getUrl('/view015number/'),
    // searchbyws: utils.getUrl('/viewbyws/'),

    listws: utils.getUrl('/app/view015number/listws/'),
    download: utils.getUrl('/app/view015number/download/')
  };

  var view015numberbatchid = {
    index: utils.getUrl('/view015numberbatchid/'),
    listbatch: utils.getUrl('/app/view015numberbatchid/listbatch/'),
    download: utils.getUrl('/app/view015numberbatchid/download/')
  };
  var viewmanagerid = {
    index: utils.getUrl('/viewmanagerid/'),
    listmgr: utils.getUrl('/app/viewmanagerid/listmgr/'),
    // download: utils.getUrl('/app/view015numberbatchid/download/')
  };


  var viewprepaidnumber = {
    download: utils.getUrl('/app/viewprepaidnumber/download/')
  };

  var downloadusednumber = {
    download: utils.getUrl('/app/downloadusednumber/download/')
  };
  var downloadavailnumber = {
    download: utils.getUrl('/app/downloadavailnumber/download/')
  };


  var available015number = {
    index: utils.getUrl('/available015number/'),
    count: utils.getUrl('/app/available015number/count/'),
    download: utils.getUrl('/app/used015number/download/')
  };

  var assign015number = {
    index: utils.getUrl('/assign015number/'),
    listws: utils.getUrl('/app/assign015number/listws/'),
    update: utils.getUrl('/app/assign015number/update/'),
    remove: utils.getUrl('/app/unassign015number/update/'),
  };

  var reserve015number = {
    index: utils.getUrl('/reserve015number/'),
    listmgr: utils.getUrl('/app/reserve015number/listmgr/'),
    update: utils.getUrl('/app/reserve015number/update/'),
    remove: utils.getUrl('/app/unreserve015number/update/'),
  };
  var wholesaler = {
    suspend: utils.getUrl('/app/wholesaler/suspend/'),
    reactivate: utils.getUrl('/app/wholesaler/reactivate/')
  };

  var createlogin = {
    index: utils.getUrl('/createlogin/'),
    pattern: utils.getUrl('/app/createlogin/pattern/'),
    createws: utils.getUrl('/app/createlogin/ws/create/'),
    creatertcdr: utils.getUrl('/app/createlogin/rtcdr/create/')
  };

  var setpassword = {
    index: utils.getUrl('/setpassword/'),
    listwslogin: utils.getUrl('/app/setpassword/listwslogin/'),
    listrtcdruser: utils.getUrl('/app/setpassword/listrtcdruser/'),
    pwdws: utils.getUrl('/app/setpassword/pwd/ws/'),
    pwdrtcdr: utils.getUrl('/app/setpassword/pwd/rtcdr/'),
    updatews: utils.getUrl('/app/setpassword/ws/update/'),
    updatertcdr: utils.getUrl('/app/setpassword/rtcdr/update/')
  };


  var uploadbatch = {
    index: utils.getUrl('/upload_batch/')
    
  };
  return {
    home: home,
    cust: cust,
    gw: gw,
    rtsms: rtsms,
    fax: fax,
    callerid: callerid,
    bbcallerid: bbcallerid,
    pin: pin,
    topupreq: topupreq,
    remark: remark,
    contactlist: contactlist,
    techinfo: techinfo,
    topupreport: topupreport,
    aninewreg: aninewreg,
    topupstatus: topupstatus,
    view015number: view015number,
    view015numberbatchid: view015numberbatchid,
    viewmanagerid: viewmanagerid,

    viewprepaidnumber: viewprepaidnumber,
    downloadusednumber:downloadusednumber,
    downloadavailnumber:downloadavailnumber,
    available015number: available015number,
    assign015number: assign015number,
    reserve015number: reserve015number,

    wholesaler: wholesaler,
    createlogin: createlogin,
    setpassword: setpassword
  };
}());
