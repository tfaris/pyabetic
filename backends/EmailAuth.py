from django.contrib.auth.models import User
from django.core.validators import email_re
            
class EmailBackend(object):
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
            
    def authenticate(self,username=None,password=None):
        if email_re.search(username):
            try:
                user = User.objects.get(email__iexact=username)
            except User.DoesNotExist:
                return None
        if user.check_password(password):
            return user
        else:
            return None            