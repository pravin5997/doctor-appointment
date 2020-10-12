from django.contrib.auth.models import BaseUserManager
from django.utils.translation import ugettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, mobile, user_type, referral_code, password=None,):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            user_type = user_type,
            mobile = mobile,
            referral_code = referral_code,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, mobile, user_type, referral_code, password):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
            user_type = user_type,
            referral_code = referral_code,
            password=password,

        )
        user.is_active = True
        user.is_admin = True
        user.save(using=self._db)
        return user