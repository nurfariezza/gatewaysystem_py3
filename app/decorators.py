from django.http import HttpResponseForbidden
from gatewaynum import utils, constants

#http://francoisgaudin.com/2013/08/22/decorators-in-django/

def hasaccess_topupreport(a_view):
    def _wrapped_view(request, *args, **kwargs):
        da = utils.checkaccesslevel(request.user.iaccesslevel)
        if constants.ACCESS.TOPUPREPORT in da:
            return a_view(request, *args, **kwargs)

        return HttpResponseForbidden()

    return _wrapped_view

def hasaccess_addremark(a_view):
    def _wrapped_view(request, *args, **kwargs):
        da = utils.checkaccesslevel(request.user.iaccesslevel)
        if constants.ACCESS.ADDREMARK in da:
            return a_view(request, *args, **kwargs)

        return HttpResponseForbidden()

    return _wrapped_view

def hasaccess_edit(a_view):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.iaccesslevel < 5:
            return a_view(request, *args, **kwargs)

        return HttpResponseForbidden()

    return _wrapped_view

def hasaccess_syncbalance(a_view):
    def _wrapped_view(request, *args, **kwargs):
        if utils.isallowsyncbalance(request.user.iaccesslevel):
            return a_view(request, *args, **kwargs)

        return HttpResponseForbidden()

    return _wrapped_view

def hasfeature_new(a_view):
    def _wrapped_view(request, *args, **kwargs):
        if utils.isnewvisible(request.user.functionflag):
            return a_view(request, *args, **kwargs)

        return HttpResponseForbidden()

    return _wrapped_view

def hasfeature_update(a_view):
    def _wrapped_view(request, *args, **kwargs):
        if utils.isupdatevisible(request.user.functionflag):
            return a_view(request, *args, **kwargs)

        return HttpResponseForbidden()

    return _wrapped_view

def hasfeature_topupreport(a_view):
    def _wrapped_view(request, *args, **kwargs):
        if utils.istopupreportvisible(request.user.functionflag):
            return a_view(request, *args, **kwargs)

        return HttpResponseForbidden()

    return _wrapped_view

def hasfeature_contactlist(a_view):
    def _wrapped_view(request, *args, **kwargs):
        if utils.iscontactlistvisible(request.user.functionflag):
            return a_view(request, *args, **kwargs)

        return HttpResponseForbidden()

    return _wrapped_view

def hasfeature_delete(a_view):
    def _wrapped_view(request, *args, **kwargs):
        if utils.isdeletevisible(request.user.functionflag):
            return a_view(request, *args, **kwargs)

        return HttpResponseForbidden()

    return _wrapped_view

def hasfeature_other(a_view):
    def _wrapped_view(request, *args, **kwargs):
        if utils.isothervisible(request.user.functionflag):
            return a_view(request, *args, **kwargs)

        return HttpResponseForbidden()

    return _wrapped_view

def hasfeature_techinfo(a_view):
    def _wrapped_view(request, *args, **kwargs):
        if utils.istechinfovisible(request.user.functionflag):
            return a_view(request, *args, **kwargs)

        return HttpResponseForbidden()

    return _wrapped_view

def hasfeature_resetiddusage(a_view):
    def _wrapped_view(request, *args, **kwargs):
        if utils.isresetiddusagevisible(request.user.functionflag):
            return a_view(request, *args, **kwargs)

        return HttpResponseForbidden()

    return _wrapped_view

def hasfeature_show015pwd(a_view):
    def _wrapped_view(request, *args, **kwargs):
        if utils.is015pwdvisible(request.user.functionflag):
            return a_view(request, *args, **kwargs)

        return HttpResponseForbidden()

    return _wrapped_view

def hasfeature_assign015number(a_view):
    def _wrapped_view(request, *args, **kwargs):
        if utils.is015pwdvisible(request.user.functionflag) or utils.isdeletevisible(request.user.functionflag):
            return a_view(request, *args, **kwargs)

        return HttpResponseForbidden()

    return _wrapped_view
