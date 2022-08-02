from django.urls import path, re_path

from . import views

urlpatterns = [

    #re_path(r'^cust/detail/(?P<pid>^([a-zA-Z0-9]+[_-])*[a-zA-Z0-9]+\.[a-zA-Z0-9]+)$', views.cust_detail, name='cust_detail'),
    re_path(r'^cust/detail/(?P<pid>[0-9a-zA-Z][0-9a-zA-Z]+)$', views.cust_detail, name='cust_detail'),
    re_path(r'^cust/loginemail/(?P<pid>[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', views.loginemail, name='loginemail'),

    # re_path(r'auth/(?P<pid>[0-9a-zA-Z][0-9a-zA-Z]+)$', views.auth, name='auth'),

    path('cust/find/', views.cust_find, name='cust_find'),
    path('cust/copy/', views.cust_copy, name='cust_copy'),
    path('cust/create/', views.cust_create, name='cust_create'),
    path('cust/update/', views.cust_update, name='cust_update'),
    path('cust/delete/', views.cust_delete, name='cust_delete'),
    re_path(r'^cust/mobusage/load/(?P<pid>[0-9]+)$', views.cust_loadmobusage, name='cust_loadmobusage'),
    re_path(r'^cust/stdusage/load/(?P<pid>[0-9]+)$', views.cust_loadstdusage, name='cust_loadstdusage'),
    re_path(r'^cust/iddusage/load/(?P<pid>[0-9]+)$', views.cust_loadiddusage, name='cust_loadiddusage'),
    re_path(r'^cust/mobusage/reset/(?P<pid>[0-9]+)$', views.cust_resetmobusage, name='cust_resetmobusage'),
    re_path(r'^cust/stdusage/reset/(?P<pid>[0-9]+)$', views.cust_resetstdusage, name='cust_resetstdusage'),
    re_path(r'^cust/iddusage/reset/(?P<pid>[0-9]+)$', views.cust_resetiddusage, name='cust_resetiddusage'),
    path('cust/countrycode/update/', views.wscountries_update, name='wscountries_update'),
    path('cust/syncbal/', views.cust_sync_balance, name='cust_sync_balance'), 
    path('cust/lookup/', views.cust_lookup, name='cust_lookup'),
    
    path('gateway/lookup/', views.gateway_lookup, name='gateway_lookup'),
    re_path(r'^gateway/type/(?P<pid>[0-9]+)$', views.gateway_type, name='gateway_type'),
    path('gateway/ratetype/list/', views.gateway_ratetpe, name='gateway_ratetpe'),
    path('gateway/ratetype/create/', views.gateway_ratetype_create, name='gateway_ratetype_create'),
    path('gateway/ratetype/update/', views.gateway_ratetype_update, name='gateway_ratetype_update'),
    
    re_path(r'^callerid/list/(?P<pid>[0-9]+)$', views.callerid_list, name='callerid_list'),
    path('callerid/delete/', views.callerid_delete, name='callerid_delete'),
    path('callerid/suspend/', views.callerid_suspend, name='callerid_suspend'),
    path('callerid/suspend/all/', views.callerid_suspendall, name='callerid_suspendall'),
    path('callerid/create/', views.callerid_create, name='callerid_create'),
    path('callerid/update/', views.callerid_update, name='callerid_update'),
    path('callerid/bulkcreate/', views.callerid_bulkcreate, name='callerid_bulkcreate'),
    path('callerid/bulksave/', views.callerid_bulksave, name='callerid_bulksave'),
    re_path(r'^callerid/list/view/(?P<pid>[0-9]+)$', views.callerid_list_view, name='callerid_list_view'),
    re_path(r'^callerid/list/pdf/(?P<pid>[0-9]+)$', views.callerid_list_pdf, name='callerid_list_pdf'),
    path('callerid/search/', views.callerid_search, name='callerid_search'),
    
    re_path(r'^bbcallerid/list/(?P<pid>[0-9]+)$', views.bbcallerid_list, name='bbcallerid_list'),
    path('bbcallerid/delete/', views.bbcallerid_delete, name='bbcallerid_delete'),
    path('bbcallerid/suspend/', views.bbcallerid_suspend, name='bbcallerid_suspend'),
    path('bbcallerid/usedsuspend/', views.bbcallerid_suspend_used, name='bbcallerid_suspend_used'),
    path('bbcallerid/testnumsuspend/', views.bbcallerid_suspend_testnum, name='bbcallerid_suspend_testnum'),


    path('bbcallerid/resume/', views.bbcallerid_resume, name='bbcallerid_resume'),
    path('bbcallerid/resumetestnum/', views.bbcallerid_resumetestnum, name='bbcallerid_resumetestnum'),
    path('bbcallerid/releasenumber/', views.releasenumber, name='releasenumber'),
    path('bbcallerid/extendblocknum/', views.extendblocknum, name='extendblocknum'),

    path('bbcallerid/settestnumber/', views.bbcallerid_settestnumber, name='bbcallerid_settestnumber'),
    path('bbcallerid/unreservenumber/', views.bbcallerid_unreservednumber, name='bbcallerid_unreservednumber'),


    path('bbcallerid/changepwd/', views.bbcallerid_changepwd, name='bbcallerid_changepwd'),
    path('bbcallerid/listws/', views.bbcallerid_listws, name='bbcallerid_listws'),
    path('bbcallerid/listws/downloadtemp/', views.bbcallerid_listws_downloadtemp, name='bbcallerid_listws_downloadtemp'),
    path('bbcallerid/listws/download/', views.bbcallerid_listws_download, name='bbcallerid_listws_download'),
    path('bbcallerid/pstn/toggle/', views.bbcallerid_pstntoggle, name='bbcallerid_pstntoggle'),
    path('bbcallerid/pstn/set/', views.bbcallerid_pstnset, name='bbcallerid_pstnset'),
    path('bbcallerid/nicenum/toggle/', views.bbcallerid_nicenumtoggle, name='bbcallerid_nicenumtoggle'),
    path('bbcallerid/nicenum/set/', views.bbcallerid_nicenumset, name='bbcallerid_nicenumset'),
    path('bbcallerid/addtoacc/', views.bbcallerid_addtoacc, name='bbcallerid_addtoacc'),
    path('bbcallerid/generatepwd/', views.bbcallerid_generatepwd, name='bbcallerid_generatepwd'),
    path('bbcallerid/displayname/update/', views.bbcallerid_displayname_update, name='bbcallerid_displayname_update'),
    path('bbcallerid/mca/update/', views.bbcallerid_mca_update, name='bbcallerid_mca_update'),
    path('bbcallerid/callfwd/update/', views.bbcallerid_callfwd_update, name='bbcallerid_callfwd_update'),
    path('bbcallerid/pwd/update/', views.bbcallerid_password_update, name='bbcallerid_password_update'),
    path('bbcallerid/subnetmask/update/', views.bbcallerid_subnetmaskset, name='bbcallerid_subnetmaskset'),
    path('bbcallerid/sippstn/update/', views.bbcallerid_sippstnset, name='bbcallerid_sippstnset'),
    path('bbcallerid/sipprepaid/update/', views.bbcallerid_sipprepaidset, name='bbcallerid_sipprepaidset'),
    
    re_path(r'^pin/list/(?P<pid>[0-9]+)$', views.pin_list, name='pin_list'),
    re_path(r'^pin/list/view/(?P<pid>[0-9]+)$', views.pin_list_view, name='pin_list_view'),
    path('pin/importsave/', views.pin_importsave, name='pin_importsave'),
    path('pin/userid/update/', views.pin_userid_update, name='pin_userid_update'),
    path('pin/create/', views.pin_create, name='pin_create'),
    path('pin/update/', views.pin_update, name='pin_update'),
    path('pin/delete/', views.pin_delete, name='pin_delete'),
    path('pin/delete/all/', views.pin_deleteall, name='pin_deleteall'),
    
    re_path(r'^topupreq/list/(?P<pid>[0-9]+)$', views.topuprequest_list, name='topuprequest_list'),
    path('topupreq/delete/', views.topupreqest_delete, name='topupreqest_delete'),
    path('topupreq/add/', views.topuprequest_add, name='topuprequest_add'),
    path('topupreq/check/', views.topuprequest_check, name='topuprequest_check'),
    path('topupreq/create/', views.topuprequest_create, name='topuprequest_create'),
    path('topupreq/amount/update/', views.topuprequest_amount_update, name='topuprequest_amount_update'),
    path('topupreq/notes/update/', views.topuprequest_notes_update, name='topuprequest_notes_update'),
    path('topupreq/topuptype/update/', views.topuprequest_topuptype_update, name='topuprequest_topuptype_update'),
    path('topupreq/sendreq/', views.topuprequest_sendreq, name='topuprequest_sendreq'),
    path('topupreq/authority/submit/', views.topuprequest_authority_submit, name='topuprequest_authority_submit'),
    path('supervisor/list/', views.supervisor_list, name='supervisor_list'),
    
    re_path(r'^contactlist/list/(?P<pid>[0-9]+)$', views.contactlist_list, name='contactlist_list'),
    path('contactlist/create/', views.contactlist_create, name='contactlist_create'),
    path('contactlist/update/', views.contactlist_update, name='contactlist_update'),
    path('contactlist/delete/', views.contactlist_delete, name='contactlist_delete'),
    
    re_path(r'^remark/list/(?P<pid>[0-9]+)$', views.remark_list, name='remark_list'),
    path('remark/create/', views.remark_create, name='remark_create'),
    
    re_path(r'^rtsms/detail/(?P<pid>[0-9]+)$', views.rtsms_detail, name='rtsms_detail'),
    path('rtsms/create/', views.rtsms_create, name='rtsms_create'),
    path('rtsms/update/', views.rtsms_update, name='rtsms_update'),
    
    path('techinfo/lookup/', views.techinfo_lookup, name='techinfo_lookup'),
    re_path(r'^techinfo/list/(?P<pid>[0-9]+)$', views.techinfo_list, name='techinfo_list'),
    path('techinfo/add/', views.techinfo_add, name='techinfo_add'),
    path('techinfo/create/', views.techinfo_create, name='techinfo_create'),
    path('techinfo/update/', views.techinfo_update, name='techinfo_update'),
    path('techinfo/delete/', views.techinfo_delete, name='techinfo_delete'),
    
    re_path(r'^ifaxuser/list/(?P<pid>[0-9]+)$', views.ifaxuser_list, name='ifaxuser_list'),
    re_path(r'^ifaxuser/detail/(?P<pid>[0-9]+)$', views.ifaxuser_detail, name='ifaxuser_detail'),
    path('ifaxuser/postpaidassignnumber/', views.ifax_postpaiduserassignnumber, name='ifax_postpaiduserassignnumber'),
    path('ifaxuser/postpaidunassignnumber/', views.ifax_postpaiduserunassignnumber, name='ifax_postpaiduserunassignnumber'),
    path('ifaxuser/create/', views.ifaxuser_create, name='ifaxuser_create'),
    path('ifaxuser/delete/', views.ifaxuser_delete, name='ifaxuser_delete'),
    path('ifaxuser/update/', views.ifaxuser_update, name='ifaxuser_update'),
    path('ifaxuser/postpaidfreenum/list/', views.postpaidfreenumber_list, name='postpaidfreenumber_list'),
    
    path('topupreport/listws/', views.topupreport_listws, name='topupreport_listws'),
    path('topupreport/listcust/', views.topupreport_listcust, name='topupreport_listcust'),
    re_path(r'^topupreport/listcust/ws/(?P<pid>[0-9]+)$', views.topupreport_listcust_by_ws, name='topupreport_listcust_by_ws'),
    path('topupreport/downloadtemp/', views.topupreport_downloadtemp, name='topupreport_downloadtemp'),
    path('topupreport/download/', views.topupreport_download, name='topupreport_download'),
    
    path('aninewreg/listcust/', views.aninewreg_listcust, name='aninewreg_listcust'),
    path('aninewreg/downloadtemp/', views.aninewreg_downloadtemp, name='aninewreg_downloadtemp'),
    path('aninewreg/download/', views.aninewreg_download, name='aninewreg_download'),
    
    path('topupstatus/list/', views.topupstatus_list, name='topupstatus_list'),

    path('view015number/listws/', views.view015number_listws, name='view015number_listws'),
    path('view015number/download/', views.view015number_download, name='view015number_download'),
    
    path('view015numberbatchid/listbatch/', views.view015number_listbatch, name='view015number_listbatch'),
    path('view015numberbatchid/download/', views.view015number_download_batchid, name='view015number_download_batchid'),
    
    path('reserve015number/listmgr/', views.viewmgr_list, name='viewmgr_list'),


    path('available015number/count/', views.available015number_count, name='available015number_count'),
    path('used015number/download/', views.used015numbers_download, name='used015numbers_download'),

    path('assign015number/listws/', views.assign015number_listws, name='assign015number_listws'),
    path('assign015number/update/', views.assign015number_update, name='assign015number_update'),
    path('unassign015number/update/', views.unassign015number_update, name='unassign015number_update'),

    path('reserve015number/update/', views.reserve015number_update, name='reserve015number_update'),
    path('unreserve015number/update/', views.unreserve015number_update, name='unreserve015number_update'),

    path('wholesaler/suspend/', views.wholesaler_acstatus_suspend, name='wholesaler_acstatus_suspend'),
    path('wholesaler/reactivate/', views.wholesaler_acstatus_reactivate, name='wholesaler_acstatus_reactivate'),

    re_path(r'^createlogin/pattern/(?P<pid>[0-9]+)$', views.custid_pattern_get, name='custid_pattern_get'),
    path('createlogin/ws/create/', views.wslogin_create, name='wslogin_create'),
    path('createlogin/rtcdr/create/', views.rtcdruser_create, name='rtcdruser_create'),

    path('setpassword/listwslogin/', views.setpassword_listwslogin, name='setpassword_listwslogin'),
    path('setpassword/listrtcdruser/', views.setpassword_listrtcdruser, name='setpassword_listrtcdruser'),
    path('setpassword/pwd/ws/', views.setpassword_getwspassword, name='setpassword_getwspassword'),
    path('setpassword/pwd/rtcdr/', views.setpassword_getrtcdruserpassword, name='setpassword_getrtcdruserpassword'),
    path('setpassword/ws/update/', views.setpassword_ws_update, name='setpassword_ws_update'),
    path('setpassword/rtcdr/update/', views.setpassword_rtcdruser_update, name='setpassword_rtcdruser_update'),

    path('upload/', views.createbatch, name='createbatch'),
    #path('upload_batch/', views.upload_batch, name='upload_batch'),
    path('uploadbatch/', views.uploadbatch, name='uploadbatch'),
    path('assignnumberstate/', views.assignnumberstate, name='assignnumberstate'),
    # path('assignnumberstate_/', views.assignnumberstate_, name='assignnumberstate_'),
    path('viewprepaidnumber/download/', views.viewprepaidnumber_download, name='viewprepaidnumber_download'),

    # path('view015numberbatchid/listws/', views.view015numberbatchid_listws, name='view015numberbatchid_listws'),

    path('downloadusednumber/download/', views.usednumber_download, name='usednumber_download'),

    path('downloadavailnumber/download/', views.availnumber_download, name='availnumber_download'),


]