from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from shared.models import BaseModel

VIA_EMAIL, VIA_PHONE = "VIA_EMAIL", "VIA_PHONE"
ORDINARY_USER, MANAGER, ADMIN = "ORDINARY_USER", "MANAGER", "ADMIN"
NEW, CODE_VERIFIED, DONE, PHOTO = "NEW", "CODE_VERIFIED", "DONE", "PHOTO"


class UserModel(AbstractUser, BaseModel):
    AUTH_TYPES = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE)
    )

    AUTH_STATUSES = (
        (NEW, NEW),
        (CODE_VERIFIED, CODE_VERIFIED),
        (DONE, DONE),
        (PHOTO, PHOTO)
    )

    USER_ROLES = (
        (ADMIN, ADMIN),
        (MANAGER, MANAGER),
        (ORDINARY_USER, ORDINARY_USER)
    )

    auth_type = models.CharField(max_length=128, choices=AUTH_TYPES, default=VIA_EMAIL)
    auth_status = models.CharField(max_length=128, choices=AUTH_STATUSES, default=NEW)
    user_role = models.CharField(max_length=128, choices=USER_ROLES, default=ORDINARY_USER)

    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=13, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)

    def __str__(self):
        return self.get_full_name()


EMAIL_EXPIRATION_TIME = 4
PHONE_EXPIRATION_TIME = 2


class ConfirmationModel(BaseModel):
    VERIFY_TYPS = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE)
    )

    verify_typs = models.CharField(max_length=128, choices=VERIFY_TYPS, default=VIA_EMAIL)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='verification_codes')
    expiration_time = models.DateField()
    is_confirmed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.verify_typs == VIA_EMAIL:
                self.expiration_time = timezone.now() + timedelta(minutes=EMAIL_EXPIRATION_TIME)
            else:
                self.expiration_time = timezone.now() + timedelta(minutes=PHONE_EXPIRATION_TIME)
        super(ConfirmationModel, self).save(*args, **kwargs)
        
