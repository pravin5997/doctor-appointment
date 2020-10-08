from django.contrib.auth.models import BaseUserManager
from django.utils.translation import ugettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, email, username, mobile, referral_code, password=None,):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            mobile = mobile,
            referral_code = referral_code,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, mobile, referral_code):
        user = self.create_user(
            email = email,
            password=password,
            username=username,
            mobile=mobile,
            referral_code = referral_code,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user