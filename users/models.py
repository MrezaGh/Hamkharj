from django.contrib.auth.models import AbstractUser


# TODO: Add More Fields


class CustomUser(AbstractUser):
    def __str__(self):
        return self.email

