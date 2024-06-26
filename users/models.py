from django.db import models


class ConfirmationModel(BaseModel):
    VERIFY_TYPS = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE)
    )

    verify_typs = models.CharField(max_length=128, choices=VERIFY_TYPS, default=VIA_EMAIL)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='verification_codes')
    exipiration_time = models.DateField()
