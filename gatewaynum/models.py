import decimal, datetime, math
from . import message
from django.db import models
from django.db.models.fields import related

from wheezy.validation import Validator
from wheezy.validation.rules import required, range, length

LANGUAGE_DIC = {
    0: 'User Select',
    1: 'B. Malaysia',
    2: 'English',
    3: 'Mandarin'
}

ACSTATUS_DIC = {
    0: 'Undefined',
    1: 'Active',
    2: 'Suspended',
    3: 'Terminated'
}

def getdict(o):
    dic = {}
    
    if o is None:
        return None
    
    for k, v in o.__dict__.items():
        if isinstance(v, decimal.Decimal):
            dic[k] = float(v)
            
        elif isinstance(v, datetime.datetime):
            dic[k] = str(v)
            
        else:
            dic[k] = v
            
    return dic

class JsonModel(object):
    
    def tojson(self):
        return getdict(self)
    
class Pager(JsonModel):
    
    def __init__(self, total, pagenum, pagesize):
        self.total = total
        self.pagenum = pagenum
        self.setpagesize(pagesize)
        
    def tojson(self):
        m = super(Pager, self).tojson()
        m['pagesize'] = self.pagesize
        m['lowerbound'] = self.lowerbound
        m['upperbound'] = self.upperbound
        m['hasnext'] = self.hasnext
        m['hasprev'] = self.hasprev
        m['totalpages'] = self.totalpages
        m['itemmessage'] = self.itemmessage
        return m
        
    @property
    def pagesize(self):
        return self._pagesize
    
    @pagesize.setter
    def pagesize(self, v):
        self.setpagesize(v)
        
    @property
    def lowerbound(self):
        return (self.pagenum - 1) * self.pagesize
    
    @property
    def upperbound(self):
        upperbound = self.pagenum * self.pagesize
        
        if self.total < upperbound:
            upperbound = self.total
            
        return upperbound
    
    @property
    def hasnext(self):
        return True if self.total > self.upperbound else False
    
    @property
    def hasprev(self):
        return True if self.lowerbound > 0 else False
        
    @property
    def totalpages(self):
        return int(math.ceil(self.total / float(self.pagesize)))
    
    @property
    def itemmessage(self):
        return self.getitemmessage(self.total, self.pagenum, self.pagesize)
        
    def setpagesize(self, pagesize):
        if (self.total < pagesize or pagesize < 1) and self.total > 0:
            self._pagesize = self.total
            
        else:
            self._pagesize = pagesize
            
        if self.totalpages < self.pagenum:
            self.pagenum = self.totalpages
            
        if self.pagenum < 1:
            self.pagenum = 1
            
    def getitemmessage(self, total, pagenum, pagesize):
        x = (pagenum - 1) * pagesize + 1
        y = pagenum * pagesize
        
        if total < y:
            y = total
            
        if total < 1:
            return ''
        
        s = 'items' if total > 1 else 'item'
        return '{0} to {1} of {2} {3}'.format(x, y, total, s)

class Authentication(JsonModel):
    
    def __init__(self):
        self.callerid = None
        self.accountid = None
        self.status = 0
        
    def setfromdic(self, d):
        self.callerid = d.get('callerid', '')
        self.accountid = d.get('accountid', '')
        self.status = d.get('status', 1)
        self.status = 1 if self.status != 0 else 0
        
    def validate(self):
        v = Validator({
            'callerid': [required(message_template=message.required_msg('New Phone No'))]
        })
        errors = {}
        b = v.validate(self, results=errors)
        l = message.get_error_list(errors)
        
        return l
        
class BBAuthentication(JsonModel):
    
    def __init__(self):
        self.bb_rt015 = None
        self.bb_015pwd = None
        self.bb_creationdate = None
        self.bb_allowpstn = 0
        self.bb_status = 0
        self.bb_nicenum = 0
        self.bb_wskey = 0
        self.bb_displayname = None
        self.bb_deregisterdate = None
        self.bb_prepaid = 0
        self.usagetype = 0
        self.bb_forward = None
        
        self.authentication = None
        self.subnetmask = None
        
    def tojson(self):
        m = super(BBAuthentication, self).tojson()
        m['bb_deregisterdatestr'] = self.bb_deregisterdatestr
        m['allowpstn'] = self.allowpstn
        m['prepaid'] = self.prepaid
        return m
        
    @property
    def bb_deregisterdatestr(self):
        s = None
        
        if self.bb_deregisterdate is not None:
            s = self.bb_deregisterdate.strftime('%Y %b %d %H:%M:%S')
            
        return s
    
    @property
    def allowpstn(self):
        return True if self.bb_allowpstn == 1 else False
    
    @property
    def prepaid(self):
        return True if self.bb_prepaid == 1 else False


class MaxCallAppearanceDN(JsonModel):
    
    def __init__(self):
        self.DirectoryNumber = None
        self.MaxCallAppearance = None  

    def setfromdic(self, d):
        self.DirectoryNumber = d.get('DirectoryNumber', '')
        self.MaxCallAppearance = d.get('MaxCallAppearance', '')




class DeviceList(JsonModel):
    
    def __init__(self):
        self.deviceid = 0
        self.devicename = None
        
class GateType(JsonModel):
    
    def __init__(self):
        self.igatetype = 0
        
    def tojson(self):
        m = super(GateType, self).tojson()
        m['sname'] = self.sname
        return m
        
    @property
    def sname(self):
        return self._sname.replace('<', '(').replace('>', ')')
    
    @sname.setter
    def sname(self, val):
        self._sname = val
    
class LCRType(JsonModel):
    
    def __init__(self):
        self.ilcrtype = 0
        self.sname = None
        
class MainType(JsonModel):
    
    def __init__(self):
        self.imaintype = 0
        self.sname = None
        
class PinUserID(JsonModel):
    
    def __init__(self):
        self.custid = None
        self.pin = None
        self.userid = None
        self.description = None
        self.creditlimit = 0
        
    def setfromdic(self, d):
        self.custid = d['custid']
        self.userid = d.get('userid', '')
        self.pin = d.get('pin', '')
        self.description = d.get('description', '')
        self.creditlimit = d.get('creditlimit', 0)
        
    def validate(self):
        v = Validator({
            'pin': [required(message_template=message.required_msg('Pin'))]
        })
        errors = {}
        b = v.validate(self, results=errors)
        l = message.get_error_list(errors)
        
        return l
        
class RateType(JsonModel):
    
    def __init__(self):
        self.iratetype = 0
        
    def tojson(self):
        m = super(RateType, self).tojson()
        m['sname'] = self.sname
        return m
        
    @property
    def sname(self):
        return self._sname.replace('<', '(').replace('>', ')')
    
    @sname.setter
    def sname(self, val):
        self._sname = val
        
    def setfromdic(self, d):
        self.iratetype = int(d.get('iratetype', 0))
        self.sname = d.get('sname', '')
        
    def validate(self):
        v = Validator({
            'iratetype': [required(message_template=message.required_msg('Rate Type'))],
            'sname': [required(message_template=message.required_msg('Description'))]
        })
        errors = {}
        b = v.validate(self, results=errors)
        l = message.get_error_list(errors)
        
        return l
    
class RTSMSMaster(JsonModel):
    
    def __init__(self):
        self.masterid = 0
        self.enterpriseid = None
        self.wholesalerid = None
        self.rtaccount = None
        self.rtaccounttype = None
        self.smscredit = 0
        self.status = 0
        self.ip = None
        self.accounttype = 0
        self.createdate = None
        self.maxuser = 0
        self.maxcontact_admin = 0
        self.maxcontact_user = 0
        self.maxalert_admin = 0
        self.maxalert_user = 0
        self.monthlyfee = 0
        self.senderid = None
        
    def tojson(self):
        m = super(RTSMSMaster, self).tojson()
        m['createdatestr'] = self.createdatestr
        return m
        
    @property
    def createdatestr(self):
        s = None
        
        if self.createdate is not None:
            s = self.createdate.strftime('%Y-%m-%d %H:%M:%S')
            
        return s
    
    def setfromdic(self, d):
        self.masterid = d.get('masterid', 0)
        self.enterpriseid = d.get('enterpriseid', '').strip()
        self.senderid = d.get('senderid', '').strip()
        self.maxuser = int(d.get('maxuser', 0))
        self.maxcontact_admin = d.get('maxcontact_admin', 0)
        self.maxalert_admin = d.get('maxalert_admin', 0)
        self.maxcontact_user = d.get('maxcontact_user', 0)
        self.maxalert_user = d.get('maxalert_user', 0)
    
    def validate(self):
        v = Validator({
            'enterpriseid': [required(message_template=message.required_msg('Enterprise ID'))],
            'maxuser': [range(min=1, message_template=message.min_msg('No. of User', 1))],
            'senderid': [required(message_template=message.required_msg('Sender ID'))]
        })
        errors = {}
        b = v.validate(self, results=errors)
        l = message.get_error_list(errors)
                
        return l
            
class RTSMSUser(JsonModel):
    
    def __init__(self):
        self.userid = 0
        self.masterid = 0
        self.username = None
        self.loginid = None
        self.loginpwd = None
        self.useremail = None
        self.usermobile = None
        self.usericno = None
        self.userlevel = 0
        self.lastlogin = None
        self.createdate = None
        self.failedcount = 0
        self.status = 0
        self.monthlimit = 0
        self.maxcontact = 0
        self.maxalert = 0
        self.senderid = None
        self.wcuseridx = 0
        self.createdby = 0
        self.callback = 0
        self.voicecast015id = 0
        
    def setfromdic(self, d):
        self.userid = d.get('userid', 0)
        self.username = d.get('username', '').strip()
        self.useremail = d.get('useremail', '').strip()
        self.usermobile = d.get('usermobile', '').strip()
        self.loginid = d.get('loginid', '').strip()
        self.loginpwd = d.get('admin_password', '').strip()
        
    def validate(self, validate_loginpwd=True):
        m = {
            'usermobile': [required(message_template=message.required_msg('Admin Mobile'))],
            'useremail': [required(message_template=message.required_msg('Admin Email'))],
            'username': [required(message_template=message.required_msg('Administrator name'))],
            'loginid': [required(message_template=message.required_msg('Admin Web Login ID')), 
                        length(min=6, message_template=message.minlen_msg('Admin Web Login ID', 6))]
        }
        
        if validate_loginpwd:
            m['loginpwd'] = [required(message_template=message.required_msg('Admin Web Login Password')), 
                             length(min=6, message_template=message.minlen_msg('Admin Web Login Password', 6))]
            
        v = Validator(m)
        errors = {}
        b = v.validate(self, results=errors)
        l = message.get_error_list(errors)
            
        return l
        
class SipLCRType(JsonModel):
    
    def __init__(self):
        self.siplcrtype = 0
        self.sdesc = None
        
class SipSubType(JsonModel):
    
    def __init__(self):
        self.sipsubtype = 0
        self.sdesc = None
        
class SubType(JsonModel):
    
    def __init__(self):
        self.isubtype = 0
        self.sname = None
        self.sfeaturescode = None
        
class SupportTeamList(JsonModel):
    
    def __init__(self):
        self.teamid = 0
        self.teamname = None
        
class TopupLog(JsonModel):
    
    def __init__(self):
        self.indexkey = 0
        self.accountid = None
        self.topupdate = 0
        self.topupdatetime = None
        self.topupvalue = 0
        self.oldcreditlimit = 0
        self.newcreditlimit = 0
        self.topupby = None
        self.paylater = 0
        self.topuprequestkey = 0
        
    def tojson(self):
        m = super(TopupLog, self).tojson()
        m['topupdatetimestr'] = self.topupdatetimestr
        m['paylaterstr'] = self.paylaterstr
        return m
        
    @property
    def topupdatetimestr(self):
        s = None
        
        if self.topupdatetime is not None:
            s = self.topupdatetime.strftime('%d %b %Y')
            
        return s
        
    @property
    def paylaterstr(self):
        return '$' if self.paylater == 1 else ''
        
class TopupType(JsonModel):
    
    def __init__(self):
        self.topuptypeid = 0
        self.sdesc = None
        self.requirepayment = 0
        
class TopupRequest(JsonModel):
    
    def __init__(self):
        self.indexkey = 0
        self.requestdate = None
        self.accountid = None
        self.amount = 0
        self.balance = 0
        self.creator = None
        self.notes = None
        self.posted = 0
        self.topuptype = 0
        self.topuptyperef = None
        
    def tojson(self):
        m = super(TopupRequest, self).tojson()
        m['requestdatestr'] = self.requestdatestr
        return m
    
    @property
    def requestdatestr(self):
        s = None
        
        if self.requestdate is not None:
            s = self.requestdate.strftime('%d/%m/%y %H:%M:%S')
            
        return s
    
class Topup(JsonModel):
    
    def __init__(self):
        self.isnonepaymenttopup = False
        self.accountid = None
        self.amount = 0
        self.colagency = None
        self.topuptype = 1
        self.notes = None
        self.wholesalerkey = None
        self.regkey = None
        self.authority = None
        self.authorityremark = None
        self.batchupload = False
        self.username = None
        
    def setfromdic(self, d):
        self.isnonepaymenttopup = d.get('isnonepaymenttopup', False)
        self.accountid = d.get('accountid', '')
        self.amount = float(d.get('amount', 0))
        self.colagency = d.get('colagency', '')
        self.topuptype = d.get('topuptype', 1)
        self.notes = d.get('notes', '')
        self.wholesalerkey = d.get('wholesalerkey', 1)
        self.regkey = d.get('regkey', '')
        self.authority = d.get('authority', '')
        self.authorityremark = d.get('authorityremark', '')
        self.batchupload = d.get('batchupload', False)
        
    def validate(self):
        v = Validator({
            'amount': [required(message_template=message.required_msg('Amount'))],
            'topuptype': [required(message_template=message.required_msg('Topup Type'))],
            'notes': [length(max=255, message_template=message.maxlen_msg('Notes', 255))]
        })
        errors = {}
        b = v.validate(self, results=errors)
        l = message.get_error_list(errors)
        
        return l
    
    def validateamount(self):
        v = Validator({
            'amount': [required(message_template=message.required_msg('Amount'))]
        })
        errors = {}
        b = v.validate(self, results=errors)
        l = message.get_error_list(errors)
        
        return l
    
    def validatenotes(self):
        v = Validator({
            'notes': [length(max=255, message_template=message.maxlen_msg('Notes', 255))]
        })
        errors = {}
        b = v.validate(self, results=errors)
        l = message.get_error_list(errors)
        
        return l
    
class TopupStatus(JsonModel):
    
    def __init__(self):
        self.accountid = None
        self.topupdatetime = None
        self.topupvalue = None
        self.topupby = None
        self.igatetype = 0
        self.uploaddate = None
        self.uploadby = None
        
    def tojson(self):
        m = super(TopupStatus, self).tojson()
        m['topupdatetimestr'] = self.topupdatetimestr
        m['uploaddatestr'] = self.uploaddatestr
        return m
        
    @property
    def topupdatetimestr(self):
        s = None
        
        if self.topupdatetime is not None:
            s = self.topupdatetime.strftime('%d-%m-%Y %H:%M:%S')
            
        return s
    
    @property
    def uploaddatestr(self):
        s = None
        
        if self.uploaddate is not None:
            s = self.uploaddate.strftime('%d-%m-%Y %H:%M:%S')
            
        return s

# class BatchDetail(JsonModel):
        
#     def __init__(self):
#         self.batch_id = None
#         self.uploadby = None
#         self.batch_remark = None
#         self.batch_date = None
       
#         # self.userdetailext = None
        
#         # self.maxcallappearancedn = None
        
#     def tojson(self):
#         m = super(BatchDetail, self).tojson()
#         m['uploadby'] = self.uploadby
#         m['batch_remark'] = self.batch_remark
#         return m

class BatchDetail(JsonModel):
    
    def __init__(self):
        self.batch_id = None
        self.uploadby = None
        self.batch_remark = None
        self.batch_date = None
        self.batch_qty = None
        # self.availablenum = None
        # self.usednum = None
        # self.suspendnum = None


        
    def setfromdic(self, d):
        self.batch_id = d.get('batch_id', '')
        self.uploadby = d.get('uploadby', '')
        self.batch_date = d.get('batch_date', '')
        self.batch_qty = d.get('batch_qty', '')
        # self.availablenum = d.get('availablenum', '')
        # self.usednum = d.get('usednum', '')
        # self.suspendnum = d.get('suspendnum', '')




class callerid_detail(JsonModel):
    
    def __init__(self):
        self.batchid = None
        self.scallerid = None
        self.callerid = None

        self.tcallerid = None
        self.cnt = None


        self.assigndate = None
        self.assignee = None

        self.blockdate = None
        self.blockperiod = None

        self.releasedate = None

        self.wskey = None
        self.status = None
        self.code_area = None
        self.state = None
        self.remark = None

    def setfromdic(self, d):
        self.batchid = d.get('batchid', '')
        self.scallerid = d.get('tfrom', '')
        self.callerid = d.get('callerid', '')

        self.tcallerid = d.get('to', '')
        self.cnt = d.get('cnt', '')

        self.assigndate = d.get('assigndate', '')
        self.assignee = d.get('assignee', '')

        self.blockdate = d.get('blockdate', '')
        self.blockperiod = d.get('blockperiod', '')

        self.releasedate = d.get('releasedate', '')

        self.wskey = d.get('wskey', '')
        self.status = d.get('status', '')
        self.code_area = d.get('code_area', '')
        self.state = d.get('state', '')
        self.remark = d.get('remark', '')

           
class UserDetail(JsonModel):
        
    def __init__(self):
        self.accountid = None
        self.name = None
        self.address = None
        self.creditlimit = 0
        self.creditusage = 0
        self.imaintype = 0
        self.isubtype = 0
        self.sfeaturescode = None
        self.igatetype = 0
        self.iratetype = 0
        self.ilang = 0
        self.pbxno = None
        self.callerid = None
        self.userdetailext = None
        self.wscountries = None
        self.ilcrtype = 0
        self.maxcallappearancedn = None
        
    def tojson(self):
        m = super(UserDetail, self).tojson()
        m['creditbalance'] = float(self.creditbalance)
        m['language'] = self.language
        m['languagetype'] = self.languagetype
        m['lcrtype'] = self.lcrtype
        m['caption'] = self.caption
        return m
        
    @property
    def creditbalance(self):
        return self.creditlimit - self.creditusage
    
    @property
    def language(self):
        s = 'User Select'
        x = self.languagetype
        d = LANGUAGE_DIC
        
        if x in d:
            s = d[x]
        
        return s
    
    @property
    def languagetype(self):
        x = self.ilang % 10
        return x
    
    @property
    def lcrtype(self):
        x = self.ilang // 10
        return x
    
    @property
    def caption(self):
        if self.userdetailext is None:
            return None
        
        s = '-{0}-Created by {1} on {2}'.format(self.accountid, self.userdetailext.createdby,
                                                self.userdetailext.creationdate.strftime('%d-%b-%Y, %I:%M:%S %p'))
        return s
    
    def setfromdic(self, d):
        self.accountid = d['accountid'].strip()
        self.name = d['name'].strip()
        self.address = d.get('address', '')
        self.creditlimit = float(d.get('creditlimit', 0)) if d.get('creditlimit', 0) not in [None, ''] else 0
        self.creditusage = float(d.get('creditusage', 0)) if d.get('creditusage', 0) not in [None, ''] else 0
        self.imaintype = int(d.get('imaintype', 0))
        self.isubtype = int(d.get('isubtype', 0)) if d.get('isubtype', 0) not in [None, ''] else 0
        self.sfeaturescode = d.get('sfeaturescode', '')
        self.igatetype = int(d.get('igatetype', 0))
        self.iratetype = int(d.get('iratetype', 0))
        self.ilang = int(d.get('ilang', 0))
        self.pbxno = d.get('pbxno')
        self.ilcrtype = int(d.get('ilcrtype', 0))
        
class UserDetailExt(JsonModel):
    
    def __init__(self):
        self.accountid = None
        self.creationdate = None
        self.createdby = None
        self.note = None
        self.wholesalerkey = 0
        self.status = 0
        self.emailaddress = None
        self.addr1 = None
        self.addr2 = None
        self.addr3 = None
        self.city = None
        self.state = None
        self.postcode = None
        self.acstatus = 0
        self.acmanager = None
        self.usagecategory = 0
        self.pbxmodel = None
        self.supportteam = 0
        self.technicalnotes = None
        self.sipsubtype = 0
        self.siplcrtype = 0
        self.smsmasterid = 0
        self.iddusagealert = 0
        self.iddusagebar = 0
        self.mobusagealert = 0
        self.mobusagebar = 0
        self.stdusagealert = 0
        self.stdusagebar = 0
        
    def setfromdic(self, d):
        self.accountid = d['accountid'].strip()
        self.note = d.get('note', '')
        self.wholesalerkey = d['wholesalerkey']
        self.status = int(d['status'])
        self.emailaddress = d.get('emailaddress', '')
        self.addr1 = d.get('addr1', None)
        self.addr2 = d.get('addr2', None)
        self.addr3 = d.get('addr3', None)
        self.city = d.get('city', None)
        self.state = d.get('state', '')
        self.postcode = d.get('postcode', None)
        self.acstatus = int(d['acstatus'])
        self.acmanager = d.get('acmanager', None)
        self.usagecategory = int(d.get('usagecategory', 0))
        self.pbxmodel = d.get('pbxmodel', '')
        self.supportteam = int(d.get('supportteam', 1))
        self.technicalnotes = d.get('technicalnotes', None)
        self.sipsubtype = int(d.get('sipsubtype', 0))
        self.siplcrtype = int(d.get('siplcrtype', 0))
        self.iddusagealert = int(d.get('iddusagealert', 0)) if d.get('iddusagealert', 0) not in [None, ''] else 0
        self.iddusagebar = int(d.get('iddusagebar', 0)) if d.get('iddusagebar', 0) not in [None, ''] else 0
        self.mobusagealert = int(d.get('mobusagealert', 0)) if d.get('mobusagealert', 0) not in [None, ''] else 0
        self.mobusagebar = int(d.get('mobusagebar', 0)) if d.get('mobusagebar', 0) not in [None, ''] else 0
        self.stdusagealert = int(d.get('stdusagealert', 0)) if d.get('stdusagealert', 0) not in [None, ''] else 0
        self.stdusagebar = int(d.get('stdusagebar', 0)) if d.get('stdusagebar', 0) not in [None, ''] else 0
        
class UserDetailContactList(JsonModel):
    
    def __init__(self):
        self.idx = 0
        self.accountid = None
        self.sname = None
        self.ipersonincharge = 0
        self.srace = None
        self.sposition = None
        self.sphone = None
        self.sfax = None
        self.smobile = None
        self.semail = None
        
    def setfromdic(self, d):
        self.idx = d.get('idx', 0)
        self.accountid = d.get('accountid', '')
        self.sname = d.get('sname', '')
        self.ipersonincharge = d.get('ipersonincharge', 0)
        self.srace = d.get('srace', '')
        self.sposition = d.get('sposition', '')
        self.sphone = d.get('sphone', '')
        self.sfax = d.get('sfax', '')
        self.smobile = d.get('smobile', '')
        self.semail = d.get('semail', '')
        
    def validate(self):
        v = Validator({
            'sname': [length(max=200, message_template=message.maxlen_msg('Full name', 200))],
            'srace': [length(max=20, message_template=message.maxlen_msg('Race', 20))],
            'sposition': [length(max=50, message_template=message.maxlen_msg('Position', 50))],
            'sphone': [length(max=20, message_template=message.maxlen_msg('Office Phone No', 20))],
            'sfax': [length(max=20, message_template=message.maxlen_msg('Fax No', 20))],
            'smobile': [length(max=20, message_template=message.maxlen_msg('Mobile Phone No', 20))],
            'semail': [length(max=100, message_template=message.maxlen_msg('Email', 100))]
        })
        errors = {}
        b = v.validate(self, results=errors)
        l = message.get_error_list(errors)
        
        return l
        
class UserDetailRemark(JsonModel):
    
    def __init__(self):
        self.index = 0
        self.accountid = None
        self.time = None
        self.login = None
        self.desc = None
        
    def tojson(self):
        m = super(UserDetailRemark, self).tojson()
        m['timestr'] = self.timestr
        return m
        
    @property
    def timestr(self):
        s = None
        
        if self.time is not None:
            s = self.time.strftime('%d/%m/%Y %H:%M:%S')
            
        return s
    
    def setfromdic(self, d):
        self.accountid = d['accountid']
        self.desc = d['remark']
        self.login = d['login']
    
    def validate(self):
        v = Validator({
            'desc': [required(message_template=message.required_msg('Remark'))]
        })
        errors = {}
        b = v.validate(self, results=errors)
        l = message.get_error_list(errors)
        
        return l
        
class vUserDetailDevice(JsonModel):
    
    def __init__(self):
        self.idx = 0
        self.accountid = None
        self.deviceid = 0
        self.units = 0
        self.remarks = None
        self.loginid = None
        self.devicename = None
        
    def setfromdic(self, d):
        self.idx = d.get('idx', 0)
        self.accountid = d.get('accountid', '')
        self.deviceid = d.get('deviceid', 1)
        self.units = d.get('units', 0)
        self.remarks = d.get('remarks', '')
        
class Wholesaler(JsonModel):
    
    def __init__(self):
        self.wholesalerkey = 0
        self.wholesalername = None

class WholesalerLogin(JsonModel):
    
    def __init__(self):
        self.sloginname = None
        self.wholesalerkey = None

class RTCDRUser(JsonModel):
    
    def __init__(self):
        self.loginid = None
        self.wholesalerid = None
        
class WsCountries(JsonModel):
    
    def __init__(self):
        self.custid = None
        self.allowtocall = None
        self.country = None
        self.username = None
        
    def tojson(self):
        m = super(WsCountries, self).tojson()
        m['isenabled'] = self.isenabled
        m['iscountryallow'] = self.iscountryallow
        return m
        
    @property
    def isenabled(self):
        return True if self.allowtocall == 0 or self.allowtocall == 1 else False
    
    @property
    def iscountryallow(self):
        return True if self.allowtocall == 1 else False
    
    @property
    def enabled(self):
        return self._enabled
    
    @enabled.setter
    def enabled(self, val):
        self._enabled = 1 if val == True else 9
    
    @property
    def allow(self):
        return self._allow
    
    @allow.setter
    def allow(self, val):
        self._allow = 1 if val == True else 0
        self.allowtocall = self.enabled if self.enabled == 9 else self.allow
    
    @property
    def isvalidcountrycodes(self):
        a = True
        if self.country is None:
            self.country = ''
            
        ls = self.country.strip().split('|')
        for s in ls:
            r = s.replace('X', '')
            if r is not None and r != '' and r.isdigit() == False:
                a = False
                break
            
        return a
    
class UserDetailFax(JsonModel):
    
    def __init__(self):
        self.guseridx = 0
        self.parent_guseridx = 0
        self.username = None
        self.ddi = None
        self.status = 0
        self.lastlogin = None
        self.fax_useridx = 0
        
class FaxDetail(JsonModel):
    
    def __init__(self):
        self.in_enabled = None
        self.in_notify_num = None
        self.in_format = None
        self.in_primaryemail = None
        self.out_enabled = None
        self.out_dailylimit = None
        self.out_notify = None
        self.email = None
        self.status = None
        self.tsi = None
        self.custom_header = None
        self.password_retry = None
        self.last_used = None
        self.registered = None
        self.ddi = None
        self.fax_useridx = None
        
    def tojson(self):
        m = super(FaxDetail, self).tojson()
        m['disable_ifax'] = self.disable_ifax
        m['disable_out_fax'] = self.disable_out_fax
        m['out_notify_email'] = self.out_notify_email
        m['disable_in_fax'] = self.disable_in_fax
        m['fwdemail'] = self.fwdemail
        return m
    
    def setfromdic(self, d):
        self.in_enabled = 0 if d['disable_in_fax'] == True else 1
        self.in_notify_num = d['in_notify_num']
        self.in_format = d['in_format']
        self.in_primaryemail = 1 if d['fwdemail'] == True else 0
        self.out_enabled = 0 if d['disable_out_fax'] == True else 1
        self.out_dailylimit = d['out_dailylimit']
        self.out_notify = 1 if d['out_notify_email'] == True else 0
        self.email = d['email'].strip()
        self.status = 0 if d['disable_ifax'] == True else 1
        self.tsi = d['tsi'].strip()
        self.custom_header = d['custom_header'].strip()
        self.password_retry = d['password_retry']
        
    @property
    def disable_ifax(self):
        return False if self.status == 1 else True
    
    @property
    def disable_out_fax(self):
        return False if self.out_enabled == 1 else True
    
    @property
    def out_notify_email(self):
        return True if self.out_notify == 1 else False
    
    @property
    def disable_in_fax(self):
        return False if self.in_enabled == 1 else True
    
    @property
    def fwdemail(self):
        return True if self.in_primaryemail == 1 else False
    
class PostpaidFreeNumber(JsonModel):
    
    def __init__(self):
        self.numidx = 0
        self.faxnum = None
        self.numberfee = 0
        self.activationfee = 0
        self.monthlyfee = 0
        self.quarterlyfee = 0
        self.halfyearlyfee = 0
        self.yearlyfee = 0
        
class TLogin(JsonModel):
    
    def __init__(self):
        self.sloginname = None
        self.sloginpassword = None
        self.iaccesslevel = None
        self.ip = None
        self.itopupaccesslevel = None
        self.twholesaler = None
        self.featureflag = None
        self.functionflag = None
        self.department = None
        self.admin = None
        self.expiry = None
        
class Authority(JsonModel):
    
    def __init__(self):
        self.accountid = None
        self.accountname = None
        self.amount = 0
        self.topuptype = None
        self.remark = None
        self.ip = None
        
    def setfromdic(self, d):
        self.accountid = d['accountid']
        self.accountname = d['accountname']
        self.amount = d['amount']
        self.topuptype = d['topuptype']
        self.remark = d['remark']
        self.ip = d['ip']
        
    def validate(self):
        v = Validator({
            'remark': [required(message_template=message.required_msg('Remark'))]
        })
        errors = {}
        b = v.validate(self, results=errors)
        l = message.get_error_list(errors)
        
        return l
    
class AuthoritySubmit(JsonModel):
    
    def __init__(self):
        self.supervisor = None
        self.psw = None
        self.remark = None
        
    def setfromdic(self, d):
        self.supervisor = d['supervisor']
        self.psw = d['psw']
        self.remark = d['remark']
        
    def validate(self):
        v = Validator({
            'supervisor': [required(message_template=message.required_msg('Supervisor'))],
            'psw': [required(message_template=message.required_msg('Password'))],
            'remark': [required(message_template=message.required_msg('Remark'))]
        })
        errors = {}
        b = v.validate(self, results=errors)
        l = message.get_error_list(errors)
        
        return l
    
class VkNotification(JsonModel):
    
    def __init__(self):
        self.accountid = None
        self.callerid = None
        self.surchargetype = 0
        self.smsno = None
        self.faxno = None
        self.phoneno = None

class WSLogin(JsonModel):
    
    def __init__(self):
        self.wsid = None
        self.pattern = None
        self.loginid = None
        self.pwd = None
        self.wsname = None

    def setfromdic(self, d):
        self.wsid = d['wsid']
        self.pattern = d['pattern']
        self.loginid = d['loginid']
        self.pwd = d['pwd']
        self.wsname = d.get('wsname', '')

    def validate(self):
        v = Validator({
            'wsid': [required(message_template=message.required_msg('Wholesaler ID'))],
            'pattern': [required(message_template=message.required_msg('Customer ID Pattern'))],
            'loginid': [required(message_template=message.required_msg('Login ID'))],
            'pwd': [required(message_template=message.required_msg('Password')),
                    length(min=6, message_template=message.minlen_msg('Password', 6))]
        })
        errors = {}
        b = v.validate(self, results=errors)
        l = message.get_error_list(errors)

        return l

class State(JsonModel):
    codearea = models.CharField(max_length=100)
    statearea = models.CharField(max_length=100)

    def __unicode__(self):
        return u'{0} - {1}'.format(self.codearea, self.statearea)
        #return self.name.decode('utf8')
        #return self.name
    def __str__(self):
        return self.statearea

class Manager(JsonModel):
    
    def __init__(self):
        self.id = None

        self.name = None
        self.position = None
        self.company = None

    def setfromdic(self, d):
        self.id = d.get('id', '')

        self.name = d.get('name', '')
        self.position = d.get('position', '')
        self.company = d.get('company', '')


class Codearea(JsonModel):
    
    def __init__(self):
        self.codearea = 0
        self.statearea = None

    def setfromdic(self, d):
        self.codearea = d.get('codearea', '')
        self.statearea = d.get('statearea', '')


class statearea(JsonModel):
    
    def __init__(self):
        self.id = 0

        self.codearea = 0
        self.charearea = None
    
    def setfromdic(self, d):
        self.id = d.get('id', '')
        self.codearea = d.get('codearea', '')
        self.charearea = d.get('charearea', '')

class batchID(JsonModel):
    batch_id = models.CharField(max_length=100)
    batch_qty = models.CharField(max_length=100)

    def __unicode__(self):
        return u'{0} - {1}'.format(self.batch_id, self.batch_qty)
        #return self.name.decode('utf8')
        #return self.name
    def __str__(self):
        return self.batch_id

      




        