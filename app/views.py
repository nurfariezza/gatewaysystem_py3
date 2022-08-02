from django.shortcuts import render, redirect
from django.http.response import JsonResponse, HttpResponseRedirect
# from django.http.response import HttpResponseServerError, JsonResponse, HttpResponse, HttpResponseRedirect

from django.template.loader import render_to_string
from django.core.exceptions import SuspiciousOperation
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings 
from django.contrib import messages

from datetime import datetime
from gatewaynum import helpers, utils, make_json_serializable, constants, models
from gatewaynum.utils import UIException, sendfile, sendfileinline
from app.models import Account, AccountRenew
from app import decorators
import logging, traceback, socket, select, uuid, requests, pdfkit, json

from gatewaynum.auth_helper import get_sign_in_url, get_token_from_code, store_token, store_user, remove_user_and_token, get_token
from gatewaynum.graph_helper import get_user


logger = logging.getLogger(__name__)

# Create your views here.
@login_required
def index(request):
    user, pw = getdbauth(request)
    da = utils.checkaccesslevel(request.user.iaccesslevel)
    edit = False if request.user.iaccesslevel >= 5 else True
    flag = request.user.functionflag
    features = {
        'new': utils.isnewvisible(flag),
        'update': utils.isupdatevisible(flag),
        'topupreport': utils.istopupreportvisible(flag),
        'contactlist': utils.iscontactlistvisible(flag),
        'delete': utils.isdeletevisible(flag),
        'other': utils.isothervisible(flag),
        'techinfo': utils.istechinfovisible(flag),
        'resetiddusage': utils.isresetiddusagevisible(flag),
        'show015pwd': utils.is015pwdvisible(flag),
        'syncbal': utils.isallowsyncbalance(request.user.iaccesslevel)
    }
    ctx = {
        'title': 'Gateway Numbering System | Home',
        'access': da,
        'features': features,
        'edit': edit,
        'ver': constants.VER
    }
    return render(request, 'app/index.html', context=ctx)

def loginview(req):
    try:
        print("ok tak tu 1")
        logout(req)

    except:
        print("ok tak tuc2")
        pass

    print("ok tak tuc3")
    return login_(req)

@login_required
def loginrenew(req):
    return loginrenew_(req)
@login_required
def dwld_report(req):
    ctx = {
           'title': 'Gateway Numbering System | Search By State'
    }
    return render(req, 'app/report.html', context=ctx)
def login_(req, error=None):

    print("oh kt sini")
    # q = ('https://accounts.google.com/o/oauth2/auth'
    #     '?response_type=code'
    #     '&client_id={0}'
    #     '&redirect_uri={1}'
    #     '&scope=openid%20profile%20email'
    #     '&login_hint=email'
    #     '&hd=redtone.com')
    # url = q.format(settings.CLIENT_ID, settings.REDIRECT_URI)
    # ctx = {
    #     'title': 'Golden Key System | Login',
    #     'url': url
    # }
    # if error is not None:
    #     ctx['error'] = error

    # # return render(req, 'app/login.html', context=ctx)
    # # url = q.format(settings.CLIENT_ID, settings.REDIRECT_URI)
    # sign_in_url, state = get_sign_in_url()
    # # print(sign_in_url)
    # q = sign_in_url
    # req.session['auth_state'] = state

    # nexturl = req.GET.get('next', 'home')
    # print(nexturl)
    # url = q.format(nexturl)
    ctx = {
        'title': 'Gateway Numbering System | Login'
        # 'url': url
    }
    # if error is not None:
    #     ctx['error'] = error
    # return redirect ('index')
    return render(req, 'app/login.html', context=ctx)


def loginrenew_(req, error=None):
    ctx = {
        'title': 'Gateway Numbering System | Change Password'
    }
    if error is not None:
        ctx['error'] = error

    x = req.GET.get('id', '')
    if x is not None:
        ctx['username'] = x

    return render(req, 'app/loginrenew.html', context=ctx)

@login_required
def changepwd(req):
    try:
        o = AccountRenew()
        o.username = req.user.username
        o.password = req.POST.get('pwd', '')
        o.newpassword = req.POST.get('newpwd', '')
        o.confirmpassword = req.POST.get('newpwd2', '')
        le = o.validate()

        if len(le) > 0:
            return loginrenew_(req, render_to_string('app/_errorlist.html', { 'errorlist': le }))

        if o.newpassword.strip() != o.confirmpassword.strip():
            raise UIException('New Password does not match! please try again')

        helpers.changepassword(o)
        req.session['pwd'] = o.newpassword
        return redirect('index')

    except UIException as e:
        return loginrenew_(req, str(e))

    except Exception as e:
        logger.exception(e)
        return loginrenew_(req, str(e))

    logout(req)
    return loginrenew_(req, 'Unable to change password, please contact Administrator')

    
# def search_n(req):
#     batch_id = req.POST.get('batch_id')
#     print(batch_id)
#     try:
#         o = models.BatchDetail()
#         o.batch_id = batch_id
#         x = helpers.userdetail_getbatch(batch_id)
#         ctx = {
#             'listed': x
#         }

#         return render(req, 'personal/_form_customer_info.html', context=ctx)

        
#     except Exception as e:
#         logger.exception(e)


def search_n(req):
    batch_id = req.POST.get('batch_id')
    # print(batch_id)
    o = helpers.userdetail_getbatch(batch_id)
    ctx = {
        'list': o
    }
    # print(o)
    return render(req, 'app/index.html', context=ctx)






def auth(req):
    username = req.POST.get('username')
    print(username)

    try:
        o = Account()
        o.username = username
        o.password = req.POST.get('pwd')
        le = o.validate()

        if len(le) > 0:
            return login_(req, render_to_string('app/_errorlist.html', { 'errorlist': le }))

        user = authenticate(username=o.username, password=o.password)

        if user is not None:
            login(req, user)
            req.session['pwd'] = o.password
            expired = datetime.now() > user.expiry
            if expired == True:
                return redirect('loginrenew')

            else:
                return redirect('index')

    except Exception as e:
        if str(e).find('Login failed for user') >= 0:
            return login_(req, 'Login failed for user {0}'.format(username))

        else:
            return login_(req, str(e))

    return login_(req, 'Invalid login')

def oauthcallback(req):
    # code = req.GET.get('code')
    # url = 'https://accounts.google.com/o/oauth2/token'
    # k = {
    #     'code': code,
    #     'client_id': settings.CLIENT_ID,
    #     'client_secret': settings.CLIENT_SECRET,
    #     'redirect_uri': settings.REDIRECT_URI,
    #     'grant_type': 'authorization_code'
    # }
    # r = requests.post(url, data=k)
    # d = r.json()

      expected_state = req.session.pop('auth_state', '')
      token = get_token_from_code(req.get_full_path(), expected_state)

  # Get the user's profile
      user_m = get_user(token)
      print(user_m)

  # Save token and user
      store_token(req, token)
      store_user(req, user_m)



    # url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    # k = {
    #     'access_token': d.get('access_token')
    # }
    # r = requests.get(url, params=k)
    # m = r.json()

    # if 'email' in m:
      email = user_m['mail']

    #     try:
    #         user = authenticate(email=email)

    #         if user is not None:
    #             login(req, user)
    #             req.session['pwd'] = helpers.tlogin_password_get(user.username)
    #             req.session['googleuser'] = m
    #             return redirect('index')

    #     except Exception as e:
    #         return login_(req, str(e))

    # return login_(req, 'Invalid login')

      try:
            user = authenticate(email=email)

            if user is not None:
                login(req, user)
                req.session['pwd'] = helpers.tlogin_password_get(user.username)
                req.session['email'] = user_m
                return redirect('index')

      except Exception as e:
            return login_(req, str(e))

      return login_(req, 'Invalid login')



# @login_required
def loginemail(req, pid):
    print(pid)
    email = pid
    try:
        user = authenticate(email=email)

        if user is not None:
            login(req, user)
            pwd = helpers.tlogin_password_get(user.username)
            email = pid

            user = authenticate(username=user.username, password=pwd)

        if user is not None:

            return redirect('index')

        else:
            return login_(req, 'Invalid login')

    except Exception as e:
        print("error")
        return login_(req, str(e))

    return login_(req, 'Invalid login')


def logoff(req):
    logout(req)
    return redirect('loginview')

@login_required
def aninewreg(req):
    ctx = {
           'title': 'Gateway Numbering System | Search By State'
    }
    return render(req, 'app/searchbystate.html', context=ctx)

@login_required
@decorators.hasfeature_topupreport
def topupreport(req):
    ctx = {
        'title': 'Gateway Numbering System | Topup Report'
    }
    return render(req, 'app/topupreport.html', context=ctx)

@login_required
def topupstatus(req):
    ctx = {
        'title': 'Gateway Numbering System | Upload Batch'
    }
    return render(req, 'app/uploadnumber.html', context=ctx)

@login_required
def view015number(req):
    ctx = {
        'title': 'Gateway Numbering System | Check By Wholesaler',
        'ver': constants.VER
    }
    return render(req, 'app/searchbyws.html', context=ctx)

@login_required
def view015numberbatchid(req):
    l = []

    l = helpers.batchidlist()
    
    ctx = {
        'title': 'Gateway Numbering System | Check By Batch ID',
        'ver': constants.VER,
        'batchidlist': l
    }
    return render(req, 'app/searchbybatchid.html', context=ctx)


@login_required
def available015number(req):
    ctx = {
        'title': 'Gateway Numbering System | Check Available 015/03 Number',
        'ver': constants.VER
    }
    return render(req, 'app/available015number.html', context=ctx)

@login_required
@decorators.hasfeature_assign015number
def assign015number(req):
    l = []

    l = helpers.list_wholesaler()

    ctx = {
        'title': 'Gateway Numbering System | Assign 015/03 Number',
        'ver': constants.VER,
        'wslist': l,

    }
    return render(req, 'app/assign015number.html', context=ctx)


def reserve015number(req):
    l = []

    l = helpers.manager_list()

    ctx = {
        'title': 'Gateway Numbering System | Assign 015/03 Number',
        'ver': constants.VER,
        'mgrlist': l,

    }

    # print(l)
    return render(req, 'app/reserve015number.html', context=ctx)


@login_required
def createlogin(req):
    ctx = {
        'title': 'Gateway Numbering System | Create Login',
        'ver': constants.VER
    }
    return render(req, 'app/createlogin.html', context=ctx)


@login_required
def upload_batch(req):
    ctx = {
        'title': 'Gateway Numbering System | Upload New Batch',
        'ver': constants.VER
    }
    return render(req, 'app/uploadnumber.html', context=ctx)

@login_required
def cust_detail(req, pid):
    print(pid)

    res = {}
    try:
        if pid is None:
            print(req.user.twholesaler)
            raise UIException('Record not found')

        res = helpers.userdetail_load(pid,req.user.twholesaler)
        # print(res)
        res['success'] = 1

    except UIException as e:
        res['error'] = 1
        res['message'] = str(e)

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)

def batch_detail(req, pid):
    res = {}

    try:
        if pid is None:
            raise UIException('Record not found')

        res = helpers.userdetail_load(pid, req.user.twholesaler)
        # print(res)
        res['success'] = 1

    except UIException as e:
        res['error'] = 1
        res['message'] = str(e)

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)



@login_required
def cust_find(req):
    res = {}
    searchby = 0
    keyword = ''

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            searchby = dic.get('searchby', 0)
            keyword = dic.get('keyword', '')
            page = int(dic.get('page', 1))
            print("run here")
            pagesize = constants.PAGE_SIZE
            l = helpers.userdetail_list(searchby, keyword)
            p = Paginator(l, pagesize)
            px = p.page(page)
            lx = px.object_list

            pager = models.Pager(p.count, page, pagesize)

            res['success'] = 1
            res['list'] = lx
            res['pager'] = pager

        except Exception as e:
            logger.exception('searchby = {0}, keyword = {0}'.format(searchby, keyword))
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    raise SuspiciousOperation()

@login_required
@decorators.hasfeature_other
def cust_copy(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)

            o = models.UserDetail()
            x = models.UserDetailExt()
            o.setfromdic(dic)
            x.setfromdic(dic)

            helpers.userdetail_copy(dic['srcaccountid'], o, x, req.user) #TODO

            res['success'] = 1
            res['message'] = 'Customer account has been successfully copied'

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
@decorators.hasfeature_new
def cust_create(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)

            ex = UIException('Data not Complete (Customer Name or Customer AccountID)...')
            accountid = dic.get('accountid', '').strip()
            name = dic.get('name', '').strip()

            if dic['wholesalerkey'] is None:
                raise UIException('Please select a Agent Group for this account')

            if accountid == '' or name == '' or dic['imaintype'] is None or dic['isubtype'] is None or \
                dic['iratetype'] is None or dic['igatetype'] is None or dic['ilang'] is None or dic['ilcrtype'] is None:
                raise ex

            o = models.UserDetail()
            x = models.UserDetailExt()
            #y = models.MaxCallAppearanceDN()
            o.setfromdic(dic)
            x.setfromdic(dic)
            #y.setfromdic(dic)

            helpers.userdetail_create(o, x, req.user) #TODO

            res['success'] = 1
            res['message'] = 'Customer account has been successfully created'

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
@decorators.hasfeature_update
def cust_update(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            o = models.UserDetail()
            x = models.UserDetailExt()
            y = models.MaxCallAppearanceDN()
            o.setfromdic(dic)
            x.setfromdic(dic)
            y.setfromdic(dic)
            
            confirm = bool(dic.get('confirm', False))

            #TODO
            user, pwd = getdbauth(req)
            prompt = helpers.userdetail_update(o, x, y, dic, req.user, pwd, confirm)
            if prompt is not None:
                res['success'] = 0
                res['prompt'] = prompt

            else:
                res['success'] = 1
                res['message'] = 'Customer account has been successfully updated'

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
@decorators.hasfeature_delete
def cust_delete(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            accountid = dic['accountid']
            user, pwd = getdbauth(req)
            le = helpers.userdetail_delete(accountid, user, pwd)

            if len(le) > 0:
                logger.exception('\n'.join(le))
                raise UIException(render_to_string('app/_errorlist.html', { 'errorlist': le }))

            else:
                res['success'] = 1
                res['message'] = 'Customer account has been successfully deleted'

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
def cust_loadmobusage(req, pid):
    res = {}

    try:
        x = helpers.userdetail_loadmobusage(pid)
        res['success'] = 1
        res['data'] = x

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)

@login_required
def cust_loadstdusage(req, pid):
    res = {}

    try:
        x = helpers.userdetail_loadstdusage(pid)
        res['success'] = 1
        res['data'] = x

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)

@login_required
def cust_loadiddusage(req, pid):
    res = {}

    try:
        x = helpers.userdetail_loadiddusage(pid)
        res['success'] = 1
        res['data'] = x

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)

@login_required
def cust_resetmobusage(req, pid):
    res = {}

    try:
        helpers.userdetail_resetmobusage(pid)

        res['success'] = 1
        res['message'] = 'MOB Usage has been reset'

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)

@login_required
def cust_resetstdusage(req, pid):
    res = {}

    try:
        helpers.userdetail_resetstdusage(pid)

        res['success'] = 1
        res['message'] = 'STD Usage has been reset'

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)

@login_required
@decorators.hasfeature_resetiddusage
def cust_resetiddusage(req, pid):
    res = {}

    try:
        helpers.userdetail_resetiddusage(pid)

        res['success'] = 1
        res['message'] = 'IDD Usage has been reset'

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)

@login_required
def cust_lookup(req):
    res = []

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            accountid = dic.get('a', '')
            res = helpers.userdetail_list_by_accountid(accountid, req.user.twholesaler)

        except Exception as e:
            logger.exception(e)

        return JsonResponse(res, safe=False)

    return SuspiciousOperation()

@login_required
def wscountries_update(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            o = models.WsCountries()
            o.custid = dic['custid']
            o.enabled = dic['enabled']
            o.allow = dic['allow']
            o.country = dic['country']
            o.username = req.user.username #TODO

            helpers.wscountries_update(o)

            res['success'] = 1
            res['message'] = 'Country code has been successfully updated'

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    raise SuspiciousOperation()

@login_required
def gateway_lookup(req):
    res = {}

    try:
        res = helpers.load_gatewaylookup(req.user.twholesaler)
        res['success'] = 1

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)

@login_required
def gateway_type(req, pid):
    res = {}

    try:
        res = helpers.load_type(int(pid))
        res['success'] = 1

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)

@login_required
def gateway_ratetpe(req):
    res = {}

    try:
        res['list'] = helpers.list_ratetype(0)
        res['success'] = 1

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)

@login_required
def gateway_ratetype_create(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            o = models.RateType()
            o.setfromdic(dic)
            le = o.validate()

            if len(le) > 0:
                raise UIException(render_to_string('app/_errorlist.html', { 'errorlist': le }))

            helpers.ratetype_create(o)

            res['success'] = 1
            res['message'] = 'Rate Type has been successfully created'

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
def gateway_ratetype_update(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            o = models.RateType()
            o.setfromdic(dic)
            le = o.validate()

            if len(le) > 0:
                raise UIException(render_to_string('app/_errorlist.html', { 'errorlist': le }))

            helpers.ratetype_update(o)

            res['success'] = 1
            res['message'] = 'Rate Type has been successfully updated'

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
def callerid_list(req, pid):
    res = {}

    try:
        res['list'] = helpers.authentication_list(pid)
        res['success'] = 1

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)

@login_required
def callerid_list_view(request, pid):
    l = helpers.authentication_list(pid)
    ctx = {
        'list': l
    }
    return render(request, 'app/callerid.html', context=ctx)

@login_required
def callerid_list_pdf(request, pid):
    try:
        l = helpers.authentication_list(pid)
        ctx = {
            'list': l
        }
        opt = {
            'page-size': 'A4',
            'margin-top': 20,
            'margin-bottom': 20,
            'quiet': '',
            'footer-center': '[page] of [topage]'
        }
        s = render_to_string('app/callerid.html', ctx)
        h = pdfkit.from_string(s, False, options=opt)
        r = sendfileinline(h, 'callerid_{0}.pdf'.format(pid), 'application/pdf')
        return r

    except Exception as e:
        logger.exception(e)

    return SuspiciousOperation()
    
@login_required
@decorators.hasfeature_update
def callerid_delete(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            idxlist = dic['idxlist']
            user, pwd = getdbauth(req)
            helpers.authentication_delete(idxlist, user, pwd)

            res['success'] = 1
            res['message'] = 'Callerids have been successfully deleted'

        except UIException as e:
            res['error'] = 1
            res['message'] = e

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
@decorators.hasfeature_update
def callerid_suspend(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            idxlist = dic['idxlist']
            accountid = dic['accountid']
            status = dic['status']
            user, pwd = getdbauth(req)
            helpers.authentication_suspend(idxlist, accountid, status, user, pwd)

            res['success'] = 1
            res['message'] = 'Callerids have been successfully updated'

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
@decorators.hasfeature_update
def callerid_suspendall(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            accountid = dic['accountid']
            status = dic['status']
            user, pwd = getdbauth(req)
            helpers.authentication_suspendall(accountid, status, user, pwd)

            res['success'] = 1
            res['message'] = 'Callerids have been successfully updated'

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
@decorators.hasfeature_update
def callerid_create(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            o = models.Authentication()
            o.setfromdic(dic)
            le = o.validate()

            if len(le) > 0:
                raise UIException(render_to_string('app/_errorlist.html', { 'errorlist': le }))

            user, pwd = getdbauth(req)
            helpers.authentication_add(o, user, pwd)

            res['success'] = 1
            res['message'] = 'Caller ID has been successfully created'

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
@decorators.hasfeature_update
def callerid_update(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            o = models.Authentication()
            o.setfromdic(dic)
            le = o.validate()

            if len(le) > 0:
                raise UIException(render_to_string('app/_errorlist.html', { 'errorlist': le }))

            user, pwd = getdbauth(req)
            helpers.authentication_update(dic['oldcallerid'], o, user, pwd)

            res['success'] = 1
            res['message'] = 'Caller ID {0} have been successfully updated'.format(o.callerid)

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
@decorators.hasfeature_update
def callerid_bulkcreate(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            res['list'] = helpers.authentication_bulkcreate(dic['startcallerid'], dic['qty'])
            res['success'] = 1

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
@decorators.hasfeature_update
def callerid_bulksave(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            data = dic['list']
            accountid = dic['accountid']
            user, pwd = getdbauth(req)
            b, x = helpers.authentication_bulksave(data, accountid, user, pwd)

            if b:
                res['success'] = 1
                res['message'] = '{0} callerid{1} has been successfully added'.format(x, 's' if x > 1 else '')

            else:
                raise UIException('Failed to add callerid')

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
def callerid_search(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            data = dic['list']
            res['list'] = helpers.authentication_search(data)
            res['success'] = 1

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
def bbcallerid_list(req, pid):
    res = {}

    try:
        res['list'] = helpers.bbauthentication_list(pid)
        res['success'] = 1

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)

# @login_required
# def bbcallerid_delete(req):
#     res = {}

#     if req.method == 'POST':
#         try:
#             dic = utils.fromjson(req)
#             idxlist = dic['idxlist']
#             user, pwd = getdbauth(req)
#             o = models.callerid_detail()
#             o.setfromdic(dic)
#             callerid=o.callerid
#             print(callerid)

#             le = helpers.bbauthentication_delete_number(idxlist,callerid, user, pwd)

#             if len(le) > 0:
#                 logger.exception('\n'.join(le))
#                 raise UIException(render_to_string('app/_errorlist.html', { 'errorlist': le }))

#             else:
#                 res['success'] = 1
#                 res['message'] = '{0} Numbers have been successfully deleted'.format(len(idxlist))

#         except UIException as e:
#             res['error'] = 1
#             res['message'] = str(e)

#         except Exception as e:
#             logger.exception(e)
#             res['error'] = 1
#             res['message'] = traceback.format_exc()

#         return JsonResponse(res)

#     return SuspiciousOperation()

# @login_required
# def bbcallerid_suspend(req):
#     res = {}

#     if req.method == 'POST':
#         try:
#             dic = utils.fromjson(req)
#             idxlist = dic['idxlist']
#             suspend = dic['suspend']
#             print(suspend)
#             o = models.callerid_detail()
#             o.setfromdic(dic)
#             callerid=o.callerid
#             print(callerid)


#             user, pwd = getdbauth(req)
#             le = helpers.bbauthentication_delete(idxlist, callerid, user, pwd)

#             if len(le) > 0:
#                 logger.exception('\n'.join(le))
#                 raise UIException(render_to_string('app/_errorlist.html', { 'errorlist': le }))

#             else:
#                 res['success'] = 1
#                 res['message'] = '{0} 015/03 numbers have been successfully suspended'.format(len(idxlist))

#         except UIException as e:
#             res['error'] = 1
#             res['message'] = str(e)

#         except Exception as e:
#             logger.exception(e)
#             res['error'] = 1
#             res['message'] = traceback.format_exc()

#         return JsonResponse(res)

#     return SuspiciousOperation()
@login_required
def bbcallerid_delete(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            idxlist = dic['idxlist']
            # callerid = dic['callerid']
            o = models.callerid_detail()
            o.setfromdic(dic)
            callerid=o.callerid

            user, pwd = getdbauth(req)
            le = helpers.bbauthentication_delete_number(idxlist, callerid, user, pwd)

            if len(le) > 0:
                logger.exception('\n'.join(le))
                raise UIException(render_to_string('app/_errorlist.html', { 'errorlist': le }))

            else:
                res['success'] = 1
                res['message'] = '{0} Successfully Deleted'.format(len(idxlist))

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()


@login_required
def bbcallerid_suspend(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            idxlist = dic['idxlist']
            # callerid = dic['callerid']
            o = models.callerid_detail()
            o.setfromdic(dic)
            callerid=o.callerid

            user, pwd = getdbauth(req)
            le = helpers.bbauthentication_block(idxlist, callerid, user, pwd)

            if len(le) > 0:
                logger.exception('\n'.join(le))
                raise UIException(render_to_string('app/_errorlist.html', { 'errorlist': le }))

            else:
                res['success'] = 1
                res['message'] = '{0} Number Successfully Blocked'.format(len(idxlist))

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
def bbcallerid_suspend_testnum(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            idxlist = dic['idxlist']
            # callerid = dic['callerid']
            o = models.callerid_detail()
            o.setfromdic(dic)
            callerid=o.callerid

            user, pwd = getdbauth(req)
            le = helpers.bbauthentication_block(idxlist, callerid, user, pwd)

            if len(le) > 0:
                logger.exception('\n'.join(le))
                raise UIException(render_to_string('app/_errorlist.html', { 'errorlist': le }))

            else:
                res['success'] = 1
                res['message'] = '{0} Number Successfully Blocked'.format(len(idxlist))

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
def bbcallerid_suspend_used(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            idxlist = dic['idxlist']
            # callerid = dic['callerid']
            o = models.callerid_detail()
            o.setfromdic(dic)
            callerid=o.callerid

            user, pwd = getdbauth(req)
            le = helpers.bbauthentication_block(idxlist, callerid, user, pwd)

            if len(le) > 0:
                logger.exception('\n'.join(le))
                raise UIException(render_to_string('app/_errorlist.html', { 'errorlist': le }))

            else:
                res['success'] = 1
                res['message'] = '{0} Number Successfully Blocked'.format(len(idxlist))

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()



@login_required
def bbcallerid_resume(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            idxlist = dic['idxlist']
            # callerid = dic['callerid']
            o = models.callerid_detail()
            o.setfromdic(dic)
            callerid=o.callerid

            user, pwd = getdbauth(req)
            le = helpers.bbauthentication_resume(idxlist, callerid, user, pwd)

            if len(le) > 0:
                logger.exception('\n'.join(le))
                raise UIException(render_to_string('app/_errorlist.html', { 'errorlist': le }))

            else:
                res['success'] = 1
                res['message'] = '{0} Successfully Release Selected number'.format(len(idxlist))

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()


@login_required
def bbcallerid_resumetestnum(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            idxlist = dic['idxlist']
            # callerid = dic['callerid']
            o = models.callerid_detail()
            o.setfromdic(dic)
            callerid=o.callerid

            user, pwd = getdbauth(req)
            le = helpers.bbauthentication_resume(idxlist, callerid, user, pwd)

            if len(le) > 0:
                logger.exception('\n'.join(le))
                raise UIException(render_to_string('app/_errorlist.html', { 'errorlist': le }))

            else:
                res['success'] = 1
                res['message'] = '{0} Successfully Release Selected number'.format(len(idxlist))

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
def releasenumber(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            idxlist = dic['idxlist']
            # callerid = dic['callerid']
            o = models.callerid_detail()
            o.setfromdic(dic)
            callerid=o.callerid

            user, pwd = getdbauth(req)
            le = helpers.bbauthentication_resume(idxlist, callerid, user, pwd)

            if len(le) > 0:
                logger.exception('\n'.join(le))
                raise UIException(render_to_string('app/_errorlist.html', { 'errorlist': le }))

            else:
                res['success'] = 1
                res['message'] = '{0} Successfully Release Selected number'.format(len(idxlist))

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()


@login_required
def extendblocknum(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            idxlist = dic['idxlist']
            # callerid = dic['callerid']
            o = models.callerid_detail()
            o.setfromdic(dic)
            callerid=o.callerid

            user, pwd = getdbauth(req)
            le = helpers.bbauthentication_extend(idxlist, callerid, user, pwd)

            if len(le) > 0:
                logger.exception('\n'.join(le))
                raise UIException(render_to_string('app/_errorlist.html', { 'errorlist': le }))

            else:
                res['success'] = 1
                res['message'] = '{0} Successfully Extend Block Period Selected number'.format(len(idxlist))

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()


@login_required
def bbcallerid_settestnumber(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            idxlist = dic['idxlist']
            # callerid = dic['callerid']
            o = models.callerid_detail()
            o.setfromdic(dic)
            callerid=o.callerid

            user, pwd = getdbauth(req)
            le = helpers.bbauthentication_settestnum(idxlist, callerid, user, pwd)

            if len(le) > 0:
                logger.exception('\n'.join(le))
                raise UIException(render_to_string('app/_errorlist.html', { 'errorlist': le }))

            else:
                res['success'] = 1
                res['message'] = '{0}  Successfully Set As Test Number'.format(len(idxlist))

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
def bbcallerid_unreservednumber(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            idxlist = dic['idxlist']
            # callerid = dic['callerid']
            o = models.callerid_detail()
            o.setfromdic(dic)
            callerid=o.callerid

            user, pwd = getdbauth(req)
            le = helpers.bbauthentication_setusednum(idxlist, callerid, user, pwd)

            if len(le) > 0:
                logger.exception('\n'.join(le))
                raise UIException(render_to_string('app/_errorlist.html', { 'errorlist': le }))

            else:
                res['success'] = 1
                res['message'] = '{0}  Successfully Set As Used Number'.format(len(idxlist))

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()



@login_required
def bbcallerid_changepwd(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            idxlist = dic['idxlist']
            accountid = dic['accountid']
            username = req.user.username
            le = helpers.bbauthentication_changepwd(idxlist, accountid, username)

            if len(le) > 0:
                logger.exception('\n'.join(le))
                raise UIException(render_to_string('app/_errorlist.html', { 'errorlist': le }))

            else:
                res['success'] = 1
                res['message'] = '{0} passwords have been successfully changed'.format(len(idxlist))

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
def bbcallerid_listws(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            batch_id = req.GET.get('batch_id', '')
            print(batch_id)

            # wholesalerkey = dic['wholesalerkey']
            # search = dic.get('search', None)
            # nicenum = dic.get('nicenum', False)
            page = dic.get('page', 1)

            pagesize = constants.PAGE_SIZE
            l = helpers.bbauthentication_list_add(batch_id)
            p = Paginator(l, pagesize)
            px = p.page(page)
            lx = px.object_list

            pager = models.Pager(p.count, page, pagesize)

            res['success'] = 1
            res['list'] = lx
            res['pager'] = pager

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    raise SuspiciousOperation()

@login_required
def bbcallerid_listws_download(req):
    try:
        id = req.GET.get('id', '')
        dic = req.session[id]
        wholesalerkey = dic['wholesalerkey']
        search = dic.get('search', None)
        nicenum = dic.get('nicenum', False)
        b = helpers.bbauthentication_listws_excel_list(wholesalerkey, nicenum, search)
        r = sendfile(b, 'rt015_03_{0}_list.xlsx'.format(wholesalerkey), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        return r

    except Exception as e:
        logger.exception(e)

    return SuspiciousOperation()

@login_required
def bbcallerid_listws_downloadtemp(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            k = uuid.uuid4()
            s = str(k)
            req.session[s] = dic
            res['success'] = 1
            res['data'] = s

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
def bbcallerid_pstntoggle(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            idxlist = dic['idxlist']
            user, pwd = getdbauth(req)
            helpers.bbauthentication_pstntoggle(idxlist, user, pwd)

            res['success'] = 1
            res['message'] = 'PSTN has been successfully updated'

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
def bbcallerid_pstnset(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            idxlist = dic['idxlist']
            pstn = dic['pstn']
            user, pwd = getdbauth(req)
            helpers.bbauthentication_pstnset(idxlist, pstn, user, pwd)

            res['success'] = 1
            res['message'] = 'PSTN has been successfully updated'

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
def bbcallerid_nicenumtoggle(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            idxlist = dic['idxlist']
            user, pwd = getdbauth(req)
            helpers.bbauthentication_nicenumtoggle(idxlist, user, pwd)

            res['success'] = 1
            res['message'] = 'Nice number has been successfully updated'

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
def bbcallerid_nicenumset(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            idxlist = dic['idxlist']
            nicenum = dic['nicenum']
            user, pwd = getdbauth(req)
            helpers.bbauthentication_nicenumset(idxlist, nicenum, user, pwd)

            res['success'] = 1
            res['message'] = 'Nice number has been successfully updated'

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
def bbcallerid_addtoacc(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            idxlist = dic['idxlist']
            accountid = dic['accountid']
            user, pwd = getdbauth(req)
            dept = req.user.department
            dept = dept.lower() if dept is not None else ''

            if dept in ('tecnical', 'technical'):
                wskey = helpers.wholesaler_get(accountid)
                if wskey not in constants.REDTONE_WHOLESALER:
                    raise UIException('Invalid Wholesaler for Technical Department')

            le = helpers.bbauthentication_resume(idxlist, accountid, user, pwd, True)

            if len(le) > 0:
                logger.exception('\n'.join(le))
                raise UIException(render_to_string('app/_errorlist.html', { 'errorlist': le }))

            else:
                res['success'] = 1
                res['message'] = '{0} 015/03 numbers have been successfully registered'.format(len(idxlist))

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
def bbcallerid_generatepwd(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            idxlist = dic['idxlist']
            user, pwd = getdbauth(req)
            helpers.bbauthentication_generatepwd(idxlist, user, pwd)

            res['success'] = 1
            res['message'] = '{0} passwords have been successfully generated'.format(len(idxlist))

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
@decorators.hasaccess_edit
def bbcallerid_displayname_update(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            user, pwd = getdbauth(req)
            helpers.bbauthentication_update_displayname(dic['name'], dic['callerid'], user, pwd)

            res['success'] = 1
            res['message'] = 'Display name has been successfully updated'

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
@decorators.hasaccess_edit
def bbcallerid_mca_update(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            mca = dic['MaxCallAppearance']
            user, pwd = getdbauth(req)
          
            helpers.bbauthentication_update_MCA(mca, dic['callerid'], user, pwd)

            res['success'] = 1
            res['message'] = 'Max Call Appearance has been successfully updated'

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()


@login_required
@decorators.hasaccess_edit
def bbcallerid_callfwd_update(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            callfwd = dic.get('callfwd', '')
            username = req.user.username

            if callfwd == '':
                helpers.bbauthentication_removecallforward(dic['callerid'], dic['accountid'], username)

            else:
                helpers.bbauthentication_setcallforward(dic['callerid'], callfwd, dic['accountid'], username)

            res['success'] = 1
            res['message'] = 'Call forwarding has been successfully updated'

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
@decorators.hasaccess_edit
def bbcallerid_password_update(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            ex = helpers.bbauthentication_changepwd_callerid(None, dic['callerid'], dic['pwd'], dic['accountid'], req.user.username)

            if ex is not None:
                logger.exception(ex)
                raise UIException(ex)

            else:
                res['success'] = 1
                res['message'] = 'Password has been successfully updated'

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
@decorators.hasaccess_edit
def bbcallerid_subnetmaskset(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            helpers.bbauthentication_update_subnetmask(dic['callerid'], dic['subnetmask'])

            res['success'] = 1
            res['message'] = 'Subnetmask setting has been successfully updated'

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
@decorators.hasaccess_edit
def bbcallerid_sippstnset(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            helpers.bbauthentication_update_sippstn(dic['callerid'], dic['pstn'], req.user.username)

            res['success'] = 1
            res['message'] = 'AllowPSTN setting has been successfully updated'

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
@decorators.hasaccess_edit
def bbcallerid_sipprepaidset(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            helpers.bbauthentication_update_sipprepaid(dic['callerid'], dic['prepaid'], dic['accountid'], req.user.username)

            res['success'] = 1
            res['message'] = 'Prepaid setting has been successfully updated'

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
def pin_list(req, pid):
    res = {}

    try:
        res['list'] = helpers.pinuserid_list(pid)
        res['success'] = 1

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)

@login_required
@decorators.hasaccess_edit
def pin_create(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            o = models.PinUserID()
            o.setfromdic(dic)
            le = o.validate()

            if len(le) > 0:
                raise UIException(render_to_string('app/_errorlist.html', { 'errorlist': le }))

            user, pwd = getdbauth(req)
            helpers.pinuserid_add(o, user, pwd)

            res['success'] = 1
            res['message'] = 'Pin has been successfully created'

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
@decorators.hasaccess_edit
def pin_update(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            o = models.PinUserID()
            o.setfromdic(dic)
            le = o.validate()

            if len(le) > 0:
                raise UIException(render_to_string('app/_errorlist.html', { 'errorlist': le }))

            user, pwd = getdbauth(req)
            helpers.pinuserid_update(dic['oldpin'], o, user, pwd)

            res['success'] = 1
            res['message'] = 'Pin has been successfully updated'

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
def pin_list_view(request, pid):
    l = helpers.pinuserid_list(pid)
    ctx = {
        'list': l
    }
    if request.GET.get('d') == '1':
        ctx['d'] = 1
        return render(request, 'app/pin.html', context=ctx)

    else:
        return render(request, 'app/pin.html', context=ctx)

@login_required
def pin_importsave(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            pinlength = dic.get('pinlength', 6)
            data = dic['list']
            accountid = dic['accountid']
            withdesc = dic.get('withdesc', False)
            user, pwd = getdbauth(req)
            b, x = helpers.pinuserid_importsave(pinlength, data, accountid, user, pwd, withdesc)

            if b:
                res['success'] = 1
                res['message'] = '{0} pin{1} has been successfully added'.format(x, 's' if x > 1 else '')

            else:
                raise UIException('Failed to add pin')

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
def pin_userid_update(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            user, pwd = getdbauth(req)
            helpers.pinuserid_userid_update(dic['accountid'], dic['pin'], dic['userid'], dic['newuserid'], user, pwd)

            res['success'] = 1
            res['message'] = 'UserID have been successfully updated'

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
def pin_delete(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            idxlist = dic['idxlist']
            accountid = dic['accountid']
            user, pwd = getdbauth(req)
            helpers.pinuserid_delete(idxlist, accountid, user, pwd)

            res['success'] = 1
            res['message'] = 'Pins have been successfully deleted'

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
def pin_deleteall(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            accountid = dic['accountid']
            user, pwd = getdbauth(req)
            helpers.pinuserid_deleteall(accountid, user, pwd)

            res['success'] = 1
            res['message'] = 'Pins have been successfully deleted'

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
def topuprequest_list(pid):
    res = {}

    try:
        res['list'] = helpers.topuprequest_list(pid)
        res['success'] = 1

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)

@login_required
def topupreqest_delete(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            idxlist = dic['idxlist']
            helpers.topuprequest_delete(idxlist)

            res['success'] = 1
            res['message'] = 'Topup Request have been successfully deleted'

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    raise SuspiciousOperation()

@login_required
@decorators.hasaccess_edit
def topuprequest_add(req):
    res = {}

    try:
        res['list'] = helpers.list_topuptype()
        res['success'] = 1

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)

@login_required
@decorators.hasaccess_edit
def topuprequest_check(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            o = models.Topup()
            o.setfromdic(dic)

            res = helpers.postnonepaymenttopup_check(o)
            res['success'] = 1

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
@decorators.hasaccess_edit
def topuprequest_create(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            o = models.Topup()
            o.setfromdic(dic)

            if o.topuptype == constants.CREDIT_TRANSFER:
                raise UIException('You cannot select Credit Transfer topup type')

            if helpers.allowperformtopup(o.topuptype, req.user.iaccesslevel) == False: #TODO
                return JsonResponse(res)

            le = o.validate()

            if len(le) > 0:
                raise UIException(render_to_string('app/_errorlist.html', { 'errorlist': le }))

            ex, lqs = helpers.postnonepaymenttopup(o)
            if len(lqs) > 0:
                for qs in lqs:
                    logger.info(qs)

            if ex is not None:
                raise Exception(ex)

            res['success'] = 1
            res['message'] = 'Topup Request has been successfully created'

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
@decorators.hasaccess_edit
def topuprequest_amount_update(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            o = models.Topup()
            o.setfromdic(dic)

            if helpers.ispostedtopuprequest(o.regkey) == True:
                raise UIException('Unable to update this topup request because it just has been posted')

            if constants.ALLOWCALLSHOPTOPUP == 0 and utils.iscallshoptype(dic['subtype']):
                raise UIException('You are not allow to perform CallShop topup')

            if helpers.allowperformtopup(o.topuptype, req.user.iaccesslevel) == False: #TODO
                return JsonResponse(res)

            le = o.validateamount()

            if len(le) > 0:
                raise UIException(render_to_string('app/_errorlist.html', { 'errorlist': le }))

            helpers.topuprequest_amount_update(o)

            res['success'] = 1
            res['message'] = 'Topup Request has been successfully updated'

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
@decorators.hasaccess_edit
def topuprequest_notes_update(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            o = models.Topup()
            o.setfromdic(dic)

            if helpers.ispostedtopuprequest(o.regkey) == True:
                raise UIException('Unable to update this topup request because it just has been posted')

            if constants.ALLOWCALLSHOPTOPUP == 0 and utils.iscallshoptype(dic['subtype']):
                raise UIException('You are not allow to perform CallShop topup')

            if helpers.allowperformtopup(o.topuptype, req.user.iaccesslevel) == False: #TODO
                return JsonResponse(res)

            le = o.validatenotes()

            if len(le) > 0:
                raise UIException(render_to_string('app/_errorlist.html', { 'errorlist': le }))

            helpers.topuprequest_notes_update(o)

            res['success'] = 1
            res['message'] = 'Topup Request has been successfully updated'

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
@decorators.hasaccess_edit
def topuprequest_topuptype_update(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            o = models.Topup()
            o.setfromdic(dic)

            if o.topuptype == constants.CREDIT_TRANSFER:
                raise UIException('You cannot select Credit Transfer topup type')

            if helpers.ispostedtopuprequest(o.regkey) == True:
                raise UIException('Unable to update this topup request because it just has been posted')

            if constants.ALLOWCALLSHOPTOPUP == 0 and utils.iscallshoptype(dic['subtype']):
                raise UIException('You are not allow to perform CallShop topup')

            if helpers.allowperformtopup(o.topuptype, req.user.iaccesslevel) == False: #TODO
                return JsonResponse(res)

            le = o.validate()

            if len(le) > 0:
                raise UIException(render_to_string('app/_errorlist.html', { 'errorlist': le }))

            if o.isnonepaymenttopup:
                ex, lqs = helpers.postnonepaymenttopup(o)
                if len(lqs) > 0:
                    for qs in lqs:
                        logger.info(qs)

                if ex is not None:
                    raise Exception(ex)

                res['success'] = 1
                res['message'] = 'Topup Request has been successfully updated'

            else:
                helpers.topuprequest_topuptype_update(o)

                res['success'] = 1
                res['message'] = 'Topup Request has been successfully updated'

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
@decorators.hasaccess_edit
def topuprequest_sendreq(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            o = models.Authority()
            o.setfromdic(dic)
            le = o.validate()

            if len(le) > 0:
                raise UIException(render_to_string('app/_errorlist.html', { 'errorlist': le }))

            socsend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            socsend.setblocking(0)
            re, se, er = select.select([], [socsend], [])
            if se:
                l = ['TopupNotifier1123']
                l.append('{0} requests for topup authorisation'.format(req.user.username)) #TODO
                l.append(o.accountid)
                l.append(o.accountname)
                l.append(o.amount)
                l.append(o.topuptype)
                l.append(o.remark)
                m = '|'.join(l)
                socsend.sendto(m, (o.ip, 1128))

            socsend.close()

            socrecv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            socrecv.setblocking(0)
            socrecv.bind((o.ip, 1127))
            re = select.select([socrecv], [], [])
            if re:
                data = socrecv.recv(4096)
                res['psw'] = data
                res['success'] = 1

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
@decorators.hasaccess_edit
def topuprequest_authority_submit(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            o = models.AuthoritySubmit()
            o.setfromdic(dic)
            le = o.validate()

            if len(le) > 0:
                raise UIException(render_to_string('app/_errorlist.html', { 'errorlist': le }))

            helpers.authority_submit(o)
            res['success'] = 1

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
def supervisor_list(req):
    res = {}

    try:
        res['list'] = helpers.supervisor_list()
        res['success'] = 1

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)

@login_required
@decorators.hasfeature_contactlist
def contactlist_list(req, pid):
    res = {}

    try:
        res['list'] = helpers.userdetailcontactlist_list(pid)
        res['success'] = 1

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)

@login_required
@decorators.hasaccess_edit
@decorators.hasfeature_contactlist
def contactlist_create(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            o = models.UserDetailContactList()
            o.setfromdic(dic)
            le = o.validate()

            if len(le) > 0:
                raise UIException(render_to_string('app/_errorlist.html', { 'errorlist': le }))

            helpers.userdetailcontactlist_create(o)

            res['success'] = 1
            res['message'] = 'Contact has been successfully created'

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
@decorators.hasaccess_edit
@decorators.hasfeature_contactlist
def contactlist_update(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            o = models.UserDetailContactList()
            o.setfromdic(dic)
            le = o.validate()

            if len(le) > 0:
                raise UIException(render_to_string('app/_errorlist.html', { 'errorlist': le }))

            helpers.userdetailcontactlist_update(o)

            res['success'] = 1
            res['message'] = 'Contact has been successfully updated'

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
@decorators.hasfeature_contactlist
def contactlist_delete(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            idxlist = dic['idxlist']
            helpers.userdetailcontactlist_delete(idxlist)

            res['success'] = 1
            res['message'] = 'Contacts have been successfully deleted'

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    raise SuspiciousOperation()

@login_required
def remark_list(req, pid):
    res = {}

    try:
        res['list'] = helpers.userdetailremark_list(pid)
        res['success'] = 1

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)

@login_required
@decorators.hasaccess_addremark
def remark_create(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            o = models.UserDetailRemark()
            dic['login'] = req.user.username #TODO
            o.setfromdic(dic)
            le = o.validate()

            if len(le) > 0:
                raise UIException(render_to_string('app/_errorlist.html', { 'errorlist': le }))

            helpers.userdetailremark_create(o)

            res['success'] = 1
            res['message'] = 'Remark has been successfully created'

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    raise SuspiciousOperation()

@login_required
def rtsms_detail(req, pid):
    res = {}

    try:
        masterid = int(pid) if pid is not None else 0

        if pid is None:
            raise UIException('Record not found')

        res = helpers.rtsms_get(masterid)
        res['success'] = 1

    except UIException as e:
        res['error'] = 1
        res['message'] = str(e)

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)

@login_required
def rtsms_create(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            m = models.RTSMSMaster()
            u = models.RTSMSUser()
            m.setfromdic(dic)
            u.setfromdic(dic)
            lm = m.validate()
            lu = u.validate()

            le = lm + lu
            if len(le) > 0:
                raise UIException(render_to_string('app/_errorlist.html', { 'errorlist': le }))

            x, smsmasterid = helpers.rtsms_create(dic['accountid'], dic['wholesalerkey'], m, u)
            if x:
                helpers.rtsms_userdetail_update(smsmasterid, dic['accountid'])
                res['success'] = 1
                res['smsmasterid'] = smsmasterid
                res['message'] = 'SMS Detail has been successfully created'

            else:
                raise UIException('Failed to create SMS account')

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
def rtsms_update(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            if len(dic['chg']) < 1:
                raise UIException('No data changed')

            m = models.RTSMSMaster()
            u = models.RTSMSUser()
            m.setfromdic(dic)
            u.setfromdic(dic)
            lm = m.validate()
            lu = u.validate(validate_loginpwd=False)

            le = lm + lu
            if len(le) > 0:
                raise UIException(render_to_string('app/_errorlist.html', { 'errorlist': le }))

            x, qs = helpers.rtsms_update(m, u, dic['chg'])
            if x:
                helpers.insert_into_sql_log(qs, dic['accountid'], req.user.username, -1)
                res['success'] = 1
                res['message'] = 'SMS Detail has been successfully updated'

            else:
                raise UIException('Failed to update SMS account')

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
@decorators.hasfeature_techinfo
def techinfo_lookup(req):
    res = {}

    try:
        res = helpers.load_techinfolookup()
        res['success'] = 1

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)

@login_required
@decorators.hasfeature_techinfo
def techinfo_list(req, pid):
    res = {}

    try:
        res['list'] = helpers.vuserdetaildevice_list(pid)
        res['success'] = 1

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)

@login_required
@decorators.hasfeature_techinfo
def techinfo_create(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            o = models.vUserDetailDevice()
            o.setfromdic(dic)
            o.loginid = req.user.username #TODO

            helpers.vuserdetaildevice_create(o)

            res['success'] = 1
            res['message'] = 'Device has been successfully created'

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
@decorators.hasfeature_techinfo
def techinfo_update(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            o = models.vUserDetailDevice()
            o.setfromdic(dic)

            helpers.vuserdetailldevice_update(o)

            res['success'] = 1
            res['message'] = 'Device has been successfully created'

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
@decorators.hasfeature_techinfo
def techinfo_add(req):
    res = {}

    try:
        res['list'] = helpers.list_devicelist()
        res['success'] = 1

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)

@login_required
@decorators.hasfeature_techinfo
def techinfo_delete(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            idxlist = dic['idxlist']
            helpers.vuserdetaildevice_delete(idxlist)

            res['success'] = 1
            res['message'] = 'Devices have been successfully deleted'

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    raise SuspiciousOperation()

@login_required
def ifaxuser_list(req, pid):
    res = {}

    try:
        res['list'] = helpers.ifaxuser_list(pid, 1)
        res['success'] = 1

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)

@login_required
def ifaxuser_detail(req, pid):
    res = {}

    try:
        if pid is None:
            raise UIException('Record not found')

        res['model'] = helpers.ifaxuser_get(pid)
        res['success'] = 1

    except UIException as e:
        res['error'] = 1
        res['message'] = str(e)

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)

@login_required
def ifax_postpaiduserassignnumber(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            helpers.ifax_postpaiduserassignnumber(dic['guseridx'], dic['ddi'], dic['wholesalerkey'])

            res['success'] = 1
            res['message'] = 'Number has been successfully registered'

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    raise SuspiciousOperation()

@login_required
def ifax_postpaiduserunassignnumber(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            helpers.ifax_postpaiduserunassignnumber(dic['guseridx'], dic['ddi'], dic['wholesalerkey'])

            res['success'] = 1
            res['message'] = 'Number has been successfully deregistered'

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
def ifaxuser_create(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            l = helpers.ifaxuser_create(dic['accountid'], dic['masterid'], dic['username'], dic['loginid'], dic['password'], dic['email'])

            res['success'] = 1
            res['list'] = l
            res['message'] = 'Fax user has been successfully created'

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
def ifaxuser_delete(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            l = helpers.ifaxuser_delete(dic['guseridx'], dic['accountid'])

            res['success'] = 1
            res['list'] = l
            res['message'] = 'Fax user has been successfully deleted'

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    raise SuspiciousOperation()

@login_required
def ifaxuser_update(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            o = models.FaxDetail()
            o.setfromdic(dic)
            helpers.ifaxuser_update(dic['guseridx'], o)

            res['success'] = 1
            res['message'] = 'Data successfully updated'

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    raise SuspiciousOperation()

@login_required
def postpaidfreenumber_list(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            res['list'] = helpers.postpaidfreenumber_list(dic['didprefix'], dic['wholesalerkey'])
            res['success'] = 1

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    raise SuspiciousOperation()

@login_required
@decorators.hasfeature_topupreport
def topupreport_download(req):
    try:
        id = req.GET.get('id', '')
        datefrom = req.GET.get('from', '')
        dateto = req.GET.get('to', '')
        wholesalerkey = int(req.GET.get('ws', 0))
        fmt = int(req.GET.get('fmt', 0))
        custlist = req.session[id] if wholesalerkey != 0 else None

        if fmt == 0:
            b = helpers.topupreport_excel_list(datefrom, dateto, wholesalerkey, custlist)
            r = sendfile(b, 'topupreport.xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            return r

        else:
            b = helpers.topupreport_text_list(datefrom, dateto, wholesalerkey, custlist)
            r = sendfile(b, 'topupreport.txt', 'text/plain')
            return r

    except Exception as e:
        logger.exception(e)

    return SuspiciousOperation()

@login_required
@decorators.hasfeature_topupreport
def topupreport_downloadtemp(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            custlist = dic.get('list', [])
            k = uuid.uuid4()
            s = str(k)
            req.session[s] = custlist
            res['success'] = 1
            res['data'] = s

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
@decorators.hasfeature_topupreport
def topupreport_listws(req):
    res = {}

    try:
        res['list'] = helpers.list_wholesaler()
        res['success'] = 1

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)

@login_required
@decorators.hasfeature_topupreport
def topupreport_listcust(req):
    res = {}

    try:
        accountid = req.GET.get('id', '')
        res['list'] = helpers.topupreport_list_cust(accountid)
        res['success'] = 1

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)

@login_required
@decorators.hasfeature_topupreport
def topupreport_listcust_by_ws(req, pid):
    res = {}

    try:
        res['list'] = helpers.topupreport_list_cust_by_ws(pid)
        res['success'] = 1

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)

@login_required
@decorators.hasfeature_other
def aninewreg_download(req):
    try:
        id = req.GET.get('id', '')
        datefrom = req.GET.get('from', '')
        dateto = req.GET.get('to', '')
        fmt = int(req.GET.get('fmt', 0))
        custlist = None if req.session[id] == [] else req.session[id]

        if fmt == 0:
            b = helpers.aninewreg_excel_list(datefrom, dateto, custlist)
            r = sendfile(b, 'aninewreg.xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            return r

        else:
            b = helpers.aninewreg_text_list(datefrom, dateto, custlist)
            r = sendfile(b, 'aninewreg.txt', 'text/plain')
            return r

    except Exception as e:
        logger.exception(e)

    return SuspiciousOperation()

@login_required
@decorators.hasfeature_other
def aninewreg_downloadtemp(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            custlist = dic.get('list', [])
            k = uuid.uuid4()
            s = str(k)
            req.session[s] = custlist
            res['success'] = 1
            res['data'] = s

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
@decorators.hasfeature_other
def aninewreg_listcust(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            keyword = dic.get('keyword', '')
            page = int(dic.get('page', 1))

            pagesize = constants.PAGE_SIZE
            l = helpers.aninewreg_list_cust(keyword)
            p = Paginator(l, pagesize)
            px = p.page(page)
            lx = px.object_list

            pager = models.Pager(p.count, page, pagesize)

            res['success'] = 1
            res['list'] = lx
            res['pager'] = pager
            # print(lx)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
def topupstatus_list(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            l = helpers.topupstatus_list(dic['wholesalerkey'], dic['from'])

            res['success'] = 1
            res['list'] = l

        except Exception as e:
            logger.exception(e)

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
@decorators.hasfeature_delete
def wholesaler_acstatus_suspend(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            helpers.wholesaler_acstatus_suspend(dic['wholesalerkey'])
            res['success'] = 1
            res['message'] = 'Wholesaler account {0} has been suspended successfully'.format(dic['wholesalerkey'])

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation

@login_required
@decorators.hasfeature_delete
def wholesaler_acstatus_reactivate(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            helpers.wholesaler_acstatus_reactivate(dic['wholesalerkey'])
            res['success'] = 1
            res['message'] = 'Wholesaler account has been reactivated successfully'.format(dic['wholesalerkey'])

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
@decorators.hasaccess_syncbalance
def cust_sync_balance(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            res = helpers.cust_sync_balance(dic['accountid'], dic['igatetype'], dic['creditlimit'])
            res['success'] = 1
            res['message'] = 'Credit balance updated'

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
def view015number_download(req):
    try:
        ws = req.GET.get('ws', '1')
        wskey = int(ws)
        b = helpers.view015numbers_excel_list(wskey)
        r = sendfile(b, 'viewbywskey.xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        return r

    except Exception as e:
        logger.exception(e)

    return SuspiciousOperation()

@login_required
def view015number_download_batchid(req):
    print("here1")
    # l = []

    # l = helpers.batchidlist()
    
    # ctx = {
    #     'title': 'Gateway Numbering System | Check By Batch ID',
    #     'ver': constants.VER,
    #     'batchidlist': l
    # }

    
    # if req.method == 'POST':
    #     try:

    #         o = models.batchID()
    #         o.setfromdic(req.POST)
    #         batchid = o.batchid

    try:
        # o = models.batchID()
        # o.setfromdic(req.GET)
        # batchid = o.batchid
        
        batch_id = req.GET.get('batch_id', '')
        print(batch_id)
        
        b = helpers.view015numbers_excel_list_batchid(batch_id)
        r = sendfile(b, 'viewbybatchid.xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        return r

    except Exception as e:
        logger.exception(e)
    # return render(req,'app/searchbybatchid.html', context=ctx)


    return SuspiciousOperation()

@login_required
def viewprepaidnumber_download(req):
    try:
        b = helpers.prepaid_excel_list()
        r = sendfile(b, 'viewprepaidnumbers.xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        return r

    except Exception as e:
        logger.exception(e)

    return SuspiciousOperation()

@login_required
def usednumber_download(req):
    try:
        b = helpers.download_used_list()
        r = sendfile(b, 'viewusednumbers.xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        return r

    except Exception as e:
        logger.exception(e)

    return SuspiciousOperation()

@login_required
def availnumber_download(req):
    try:
        b = helpers.download_avail_list()
        r = sendfile(b, 'viewavailablenumbers.xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        return r

    except Exception as e:
        logger.exception(e)

    return SuspiciousOperation()



@login_required
def available015number_count(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            x = helpers.available015numbers_count(dic['from'], dic['to'])
            res['success'] = 1
            res['count'] = x
            res['message'] = '{0} number(s) available'.format(x)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
def used015numbers_download(req):
    try:
        sfrom = req.GET.get('f', '')
        sto = req.GET.get('t', '')
        b = helpers.used015numbers_excel_list(sfrom, sto)
        r = sendfile(b, 'used015numbers.xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        return r

    except Exception as e:
        logger.exception(e)

    return SuspiciousOperation()

# @login_required
# @decorators.hasfeature_assign015number
# def assign015number_update(req):
#     res = {}
#     l = []

#     l = helpers.list_wholesaler()

#     ctx = {
#         'wslist': l

#     }
#     if req.method == 'POST':
#         try:

#             o = models.callerid_detail()
#             o.setfromdic(req.POST)
#             # batchid = o.batchid
           
#             wskey = o.wskey
#             tfrom = o.scallerid
#             to = o.tcallerid
#             cnt = o.cnt

#             # dic = utils.fromjson(req)
#             user, pwd = getdbauth(req)
#             x = helpers.assign015(tfrom,to, cnt, wskey, user, pwd)
#             res['success'] = 1
#             res['message'] = '{0} number(s) have been successfully assigned'.format(x)
#             messages.add_message(req, messages.SUCCESS, '{0} number(s) have been successfully assigned'.format(x))
#             # else:
#                 # messages.add_message(req, messages.ERROR,'Please select value for [Code Area] ')


#         except UIException as e:
#             res['error'] = 1
#             res['message'] = str(e)
#             messages.add_message(req, messages.ERROR,str(e))


#         except Exception as e:
#             logger.exception(e)
#             res['error'] = 1
#             res['message'] = traceback.format_exc()
#             messages.add_message(req, messages.ERROR,str(e))


#         # return JsonResponse(res)
#         return render(req,'app/assign015number.html', context=ctx)
#         # return assign015number(req)


    # return SuspiciousOperation()


def assign015number_update(req):
    res = {}

    if req.method == 'POST':
        try:

            dic = utils.fromjson(req)
            user, pwd = getdbauth(req)
            x = helpers.assign015(dic['from'], dic['to'], int(dic['cnt']), dic['wskey'], user, pwd)
            res['success'] = 1
            res['message'] = '{0} number(s) have been successfully assigned'.format(x)

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()


@login_required
@decorators.hasfeature_assign015number
def unassign015number_update(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            user, pwd = getdbauth(req)
            helpers.unassign_wskey(dic['from'], dic['to'], user, pwd)
            res['success'] = 1
            res['message'] = '{0} to {1} have been successfully unassigned'.format(dic['from'], dic['to'])

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()


def reserve015number_update(req):
    res = {}

    if req.method == 'POST':
        try:

            dic = utils.fromjson(req)
            user, pwd = getdbauth(req)
            x = helpers.reserved015(dic['from'], dic['to'], int(dic['cnt']),  dic['id'], dic['remark'],user, pwd)
            print(x)
            res['success'] = 1
            res['message'] = '{0} number(s) have been successfully reserved'.format(x)

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()


@login_required
#@decorators.hasfeature_reserve015number
def unreserve015number_update(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            user, pwd = getdbauth(req)
            helpers.unreserved015(dic['from'], dic['to'], user, pwd)
            res['success'] = 1
            res['message'] = '{0} to {1} have been successfully unreserved'.format(dic['from'], dic['to'])

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()



@login_required
def view015number_listws(req):
    res = {}

    try:
        o = models.Wholesaler()
        o.wholesalerkey = 0
        o.wholesalername = '0-Default'
        l = helpers.list_wholesaler(wskey=req.user.twholesaler)
        l.insert(0, o)
        res['list'] = l
        res['success'] = 1

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)

@login_required
def view015number_listbatch(req):
    res = {}

    try:
        o = models.batchID()
        
        l = helpers.batchidlist(req)
        print(l)
        res['list'] = l
        res['success'] = 1

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)


@login_required
def viewmgr_list(req):
    res = {}

    try:
        o = models.Manager()
        
        l = helpers.manager_list(req)
        print(l)
        res['list'] = l
        res['success'] = 1

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)


@login_required
@decorators.hasfeature_assign015number
def assign015number_listws(req):
    res = {}

    try:
        o = models.Wholesaler()
        o.wholesalerkey = 0
        o.wholesalername = '0-Default'
        l = helpers.list_wholesaler()
        l.insert(0, o)
        res['list'] = l
        res['success'] = 1

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)

@login_required
@decorators.hasfeature_delete
def wslogin_create(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            o = models.WSLogin()
            o.setfromdic(dic)
            le = o.validate()

            if len(le) > 0:
                raise UIException(render_to_string('app/_errorlist.html', { 'errorlist': le }))

            helpers.wslogin_create(o)
            msg = 'Login for wholesaler {0} - {1} has been successfully created.<br />Login ID: {2}<br />Password: {3}'.format(o.wsid, o.wsname, o.loginid, o.pwd)
            res['success'] = 1
            res['message'] = msg

            link = 'https://apps.redtone.com/gatewaynum'

            send_mail(
                'Wholesaler Golden Key Login Created',
                msg.replace('<br />', '\r\n'),
                settings.SERVER_EMAIL,
                [req.user.email],
                fail_silently=True,
                html_message=msg + '<p>You can try to login at <a href="{0}" target="_blank">{0}</a></p>'.format(link)
            )

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
@decorators.hasfeature_delete
def rtcdruser_create(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            o = models.WSLogin()
            o.setfromdic(dic)
            le = o. validate()

            if len(le) > 0:
                raise UIException(render_to_string('app/_errorlist.html', { 'errorlist': le }))

            helpers.rtcdruser_create(o)
            msg = 'Login for wholesaler {0} - {1} has been successfully created.<br />Login ID: {2}<br />Password: {3}'.format(o.wsid, o.wsname, o.loginid, o.pwd)
            res['success'] = 1
            res['message'] = msg

            link = 'https://apps.redtone.com/rtinstantcdr'

            send_mail(
                'REDtone Instant CDR Login Created',
                msg.replace('<br />', '\r\n'),
                settings.SERVER_EMAIL,
                [req.user.email],
                fail_silently=True,
                html_message=msg + '<p>You can try to login at <a href="{0}" target="_blank">{0}</a></p>'.format(link)
            )

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
def setpassword_listwslogin(req):
    res = {}

    try:
        l = helpers.list_wslogin()
        res['list'] = l
        res['success'] = 1

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)

@login_required
def setpassword_listrtcdruser(req):
    res = {}

    try:
        l = helpers.list_rtcdruser()
        res['list'] = l
        res['success'] = 1

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)

@login_required
def setpassword_getwspassword(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            pwd = helpers.wspassword_get(dic['login'], dic['wskey'])
            res['success'] = 1
            res['data'] = pwd

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
def setpassword_getrtcdruserpassword(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            pwd = helpers.rtcdruserpassword_get(dic['login'], dic['wsid'])
            res['success'] = 1
            res['data'] = pwd

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
def setpassword_ws_update(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            helpers.wspassword_update(dic['login'], dic['pwd'])
            res['success'] = 1
            res['message'] = 'Password for {0} has been successfully updated'.format(dic['login'])

        except UIException as e:
            res['error'] = 1
            res['message'] = str(e)

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
def setpassword_rtcdruser_update(req):
    res = {}

    if req.method == 'POST':
        try:
            dic = utils.fromjson(req)
            helpers.rtcdruserpassword_update(dic['login'], dic['pwd'])
            res['success'] = 1
            res['message'] = 'Password for {0} has been successfully updated'.format(dic['login'])

        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        return JsonResponse(res)

    return SuspiciousOperation()

@login_required
@decorators.hasfeature_delete
def custid_pattern_get(req, pid):
    res = {}

    try:
        x = helpers.custid_pattern_get(pid)
        res['success'] = 1
        res['data'] = x

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)

def getdbauth(req):
    user = req.user.username
    if 'pwd' not in req.session:
        req.session['pwd'] = helpers.tlogin_password_get(user)

    pwd = req.session['pwd']
    return user, pwd

def createbatch(req):
    l = []
    ctx = {
        'title': 'REDtone Gateway | Upload batch',
        # 'tab': 1,
        'list': l
    }

    # try:
    #     # custid = req.session.get('custid')
    #     l = helpers.payment_history(req)
    #     ctx['list'] = l

    # except Exception as e:
    #     logger.exception(e)

    return render(req, 'app/createbatch.html', context=ctx)

def createstate(req):
    l = []
    ls = []


    try:
        l = helpers.list_area()
        ls = helpers.list_subarea()

        # print(l)
        ctx = {
            'title': 'REDtone Gateway | createstate',
            'codelist': l
        }



    except Exception as e:
        logger.exception(e)

    return render(req, 'app/createstate.html', context=ctx)

@login_required
def createstate_(req):
    res = {}
    l = []
    # ls = []


    if req.method == 'POST':
        try:
            l = helpers.list_area()
            # ls = helpers.list_subarea()

            # print(l)
            ctx = {
                'title': 'REDtone Gateway | createstate',
                'codelist': l
            }

            
            o = models.statearea()
            o.setfromdic(req.POST)
            codearea = o.codearea
            charearea = o.charearea

            user, pwd = getdbauth(req)

            print(codearea)
            print(charearea)
            if len(codearea) > 1:
                helpers.chargearea_add(codearea, charearea, user)
                res['success'] = 1
                # res['message'] = 'Charge Area for {0} has been successfully updated'.format(codearea)
                messages.add_message(req, messages.SUCCESS, 'Charge Area for {0} has been successfully updated'.format(codearea))
            else:
                messages.add_message(req, messages.ERROR,'Please select value for [Code Area] ')


        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = str(e)
                # res['redirect'] = 'createbatch'
            messages.add_message(req, messages.ERROR,str(e))

        # return JsonResponse(res)
        return render(req,'app/createstate.html', context=ctx)


    return SuspiciousOperation()


def createmanager(req):
    l = []


    try:
        l = helpers.manager_list()

        # print(l)
        ctx = {
            'title': 'REDtone Gateway | Create Accnt Manager',
            'managerlist': l
        }



    except Exception as e:
        logger.exception(e)

    return render(req, 'app/createaccntmgr.html', context=ctx)

@login_required
def createmanager_(req):
    res = {}
    # ls = []


    if req.method == 'POST':
        try:
            
            ctx = {
                'title': 'REDtone Gateway | Create Accnt Manager',
            }

            
            o = models.Manager()
            o.setfromdic(req.POST)
            name = o.name
            position = o.position
            company = o.company

            user, pwd = getdbauth(req)

            
            if len(name) > 1:
                helpers.manager_add(name, position,company)
                res['success'] = 1
                # res['message'] = 'Charge Area for {0} has been successfully updated'.format(codearea)
                messages.add_message(req, messages.SUCCESS, 'New Manager - {0} has been successfully added'.format(name))
            else:
                messages.add_message(req, messages.ERROR,'Name field is required ')


        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = str(e)
            messages.add_message(req, messages.ERROR,str(e))

        return render(req,'app/createaccntmgr.html', context=ctx)


    return SuspiciousOperation()


@login_required
def assignnumberstate_(req):
    res = {}
    l = []
    ls = []


    if req.method == 'POST':
        try:
            l = helpers.list_area()
            ls = helpers.list_subarea()

            # print(l)
            ctx = {
                'title': 'REDtone Gateway | createstate',
                'codelist': l,
                'arealist': ls
            }

            
            # x = models.statearea()
            # x.setfromdic(req.POST)
            # codearea = x.codearea
            # charearea = x.charearea

            o = models.callerid_detail()
            o.setfromdic(req.POST)
            code_area = o.code_area
            state = o.state
            stfrom = o.scallerid
            to = o.tcallerid
            cnt = o.cnt
            print(id)
            print(stfrom)

            user, pwd = getdbauth(req)


            print(code_area)
            print(state)
            if len(code_area) > 0:
                
                x = helpers.assign_state(code_area,state,stfrom, to, cnt, user, pwd)

                res['success'] = 1
                res['message'] = '{0} number(s) have been successfully assigned'.format(cnt)
                messages.add_message(req, messages.SUCCESS, '{0} number(s) have been successfully assigned'.format(cnt))

            
            else:
                messages.add_message(req, messages.ERROR,'Please select value for [Code Area] ')


        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = str(e)
                # res['redirect'] = 'createbatch'
            messages.add_message(req, messages.ERROR,str(e))

        # return JsonResponse(res)
        return render(req,'app/assign015numberstate.html', context=ctx)


    return SuspiciousOperation()


def assignnumberstate(req):
    l = []

    try:
        
        l = helpers.list_area()
        ls = helpers.list_subarea()

        # print(l)
        ctx = {
            'title': 'REDtone Gateway | Assign Number(State)',
            # 'statelist': models.State.objects.all().order_by('codearea'),

            # 'tab': 1,
            'codelist': l,
            'arealist': ls
        }
        # print(ls)
        if req.method == 'POST':
            try:
            
                o = models.callerid_detail()
                o.setfromdic(req.POST)
                # batchid = o.batchid
                statearea = o.state
                charearea = o.code_area
                stfrom = o.scallerid
                to = o.tcallerid
                cnt = o.cnt
                print(statearea)
                print(stfrom)

               
                user, pwd = getdbauth(req)
                x = helpers.assign_state(statearea,charearea,tfrom, to, cnt, user, pwd)

                res['success'] = 1
                res['message'] = '{0} number(s) have been successfully assigned'.format(cnt)
                messages.add_message(req, messages.SUCCESS, '{0} number(s) have been successfully assigned'.format(cnt))
                # messages.add_message(req, messages.SUCCESS, 'Succesfully uploaded!!')  


            except UIException as e:
            
                res['error'] = 1
                res['message'] = str(e)
                # res['redirect'] = 'createbatch'
                messages.add_message(req, messages.ERROR,str(e))


            except Exception as e:
                logger.exception(e)
                res['error'] = 1
                res['message'] = traceback.format_exc()




    except Exception as e:
        logger.exception(e)

    return render(req, 'app/assign015numberstate.html', context=ctx)



@login_required
@decorators.hasfeature_assign015number
def upload_list(req):
    res = {}

    try:
        o = models.Wholesaler()
        o.wholesalerkey = 0
        o.wholesalername = '0-Default'
        l = helpers.list_wholesaler()
        l.insert(0, o)
        res['list'] = l
        res['success'] = 1

    except Exception as e:
        logger.exception(e)
        res['error'] = 1
        res['message'] = traceback.format_exc()

    return JsonResponse(res)


@login_required
@decorators.hasfeature_assign015number
def uploadbatch(req):
    res = {}

    if req.method == 'POST':
        try:
            
            o = models.callerid_detail()
            o.setfromdic(req.POST)
            batchid = o.batchid
            tfrom = o.scallerid
            to = o.tcallerid
            cnt = o.cnt

            print(batchid)
            ctx = {
           'detail': o
            }

            user, pwd = getdbauth(req)
            x = helpers.upload015(batchid, tfrom, to, cnt, user, pwd)

            res['success'] = 1
            res['message'] = '{0} number(s) have been successfully assigned'.format(x)
            messages.add_message(req, messages.SUCCESS, '{0} number(s) have been successfully assigned'.format(x))
            
            y = helpers.batchinfo(batchid, cnt, user)

            # messages.add_message(req, messages.SUCCESS, 'Succesfully uploaded!!')  


        except UIException as e:
           
            res['error'] = 1
            res['message'] = str(e)
            # res['redirect'] = 'createbatch'
            messages.add_message(req, messages.ERROR,str(e))


        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        # return JsonResponse(res)
        return render(req,'app/createbatch.html', context=ctx)

    return SuspiciousOperation()

@login_required
@decorators.hasfeature_assign015number
def assignstate(req):
    l = []
    ls = []

    res = {}

    if req.method == 'POST':
        try:
            
            o = models.callerid_detail()
            o.setfromdic(req.POST)
            # batchid = o.batchid
            statearea = o.state
            chargearea = o.code_area
            stfrom = o.scallerid
            to = o.tcallerid
            cnt = o.cnt
            print(statearea)
            print(stfrom)

            ctx = {
           'detail': o,
           'codelist': l,
           'arealist': ls
 
            }
            
            user, pwd = getdbauth(req)
            x = helpers.assign_state(tfrom, to, cnt, user, pwd)
            # y = helpers.batchinfo(batchid, cnt, user)

            res['success'] = 1
            res['message'] = '{0} number(s) have been successfully assigned'.format(cnt)
            messages.add_message(req, messages.SUCCESS, '{0} number(s) have been successfully assigned'.format(cnt))
            # messages.add_message(req, messages.SUCCESS, 'Succesfully uploaded!!')  


        except UIException as e:
           
            res['error'] = 1
            res['message'] = str(e)
            # res['redirect'] = 'createbatch'
            messages.add_message(req, messages.ERROR,str(e))


        except Exception as e:
            logger.exception(e)
            res['error'] = 1
            res['message'] = traceback.format_exc()

        # return JsonResponse(res)
        return render(req,'app/assign015numberstate.html', context=ctx)

    return SuspiciousOperation()
