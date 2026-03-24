from django.contrib.auth.models import AbstractUser
from django.db.models import Model, CharField, TextField, EmailField, DateTimeField
from django.db.models.fields import BooleanField


class User(AbstractUser):
    is_worker = BooleanField(default=False)


class Footer(Model):
    instagram_link = CharField(max_length=255)
    facebook_link = CharField(max_length=255)
    twitter_link = CharField(max_length=255)
    linkedin_link = CharField(max_length=255)


class TelegramGroup(Model):
    group_name = CharField(max_length=255)
    group_id = CharField(max_length=255)
    bot_token = CharField(max_length=255)

    def __str__(self):
        return f"Telegram group {self.group_id}"


class Contact(Model):
    name = CharField(max_length=100)
    surname = CharField(max_length=100)
    email = EmailField()
    phone = CharField(max_length=20)
    message = TextField()
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.surname} - {self.email}"
