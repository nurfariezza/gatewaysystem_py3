from app import models
from gatewaynum import helpers

#http://blackglasses.me/2013/09/17/custom-django-user-model/
#http://blog.mathandpencil.com/replacing-django-custom-user-models-in-an-existing-application/

class ClientAuthBackend(object):
    
    def authenticate(self, username=None, password=None, email=None):
        user = None
        
        try:
            if email is not None:
                user = models.User.objects.get(email=email)
                user.save()
            
            else:
                o = helpers.tlogin_get(username, password)
                
                if o is None:
                    raise Exception('User {0} not found'.format(username))
                
                try:
                    user = models.User.objects.get(username=o.sloginname)
                    user.iaccesslevel = o.iaccesslevel
                    user.ip = o.ip
                    user.itopupaccesslevel = o.itopupaccesslevel
                    user.twholesaler = o.twholesaler
                    user.featureflag = o.featureflag
                    user.functionflag = o.functionflag
                    user.department = o.department
                    user.admin = o.admin
                    user.expiry = o.expiry
                    user.save()
                    
                except models.User.DoesNotExist:
                    user = models.User(username=o.sloginname, iaccesslevel=o.iaccesslevel, ip=o.ip,
                                       itopupaccesslevel=o.itopupaccesslevel, twholesaler=o.twholesaler,
                                       featureflag=o.featureflag, functionflag=o.functionflag,
                                       department=o.department, admin=o.admin, expiry=o.expiry)
                    user.save()
            
        except Exception:
            raise

        return user
        
    def get_user(self, user_id):
        try:
            return models.User.objects.get(pk=user_id)
        
        except models.User.DoesNotExist:
            return None