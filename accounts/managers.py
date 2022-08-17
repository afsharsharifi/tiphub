from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, fullname, phone, email, password=None):
        if not phone:
            raise ValueError('Users must have a phone number')

        user = self.model(
            fullname=fullname,
            phone=phone,
            email=email
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, fullname, phone, email, password=None):
        user = self.create_user(
            fullname,
            phone,
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
