from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, fullname, phone, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
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
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            fullname,
            phone,
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
