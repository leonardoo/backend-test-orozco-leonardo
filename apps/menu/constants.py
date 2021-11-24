from django.db.models import TextChoices


class MenuStatus(TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    SEND = "send", "Send"
    RESEND = "resend", "Resend"
