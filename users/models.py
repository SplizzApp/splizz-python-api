import random

from django.db import models
from django.utils import timezone as tim


class User(models.Model):
    username = models.CharField(max_length=50, unique=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=11)
    color = models.CharField(max_length=8, null=True, blank=True)
    date_joined = models.DateField(auto_now_add=True, editable=True)
    modified_timestamp = models.DateTimeField(default=tim.now, editable=True)
    created_timestamp = models.DateTimeField(default=tim.now, editable=False)

    class Meta:
        db_table = 'user'
        ordering = ['id']

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        if not self.username:
            self._generate_random_username()

        if not self.color:
            random_hex = random.randint(0, 0xFFFFFF)
            self.color = f"FF{random_hex:06X}"

    def __str__(self):
        return self.username

    def _generate_random_username(self):
        random_int = random.randint(0, 999999999)
        username = f"user-{random_int:09}"
        # Check if the generated username already exists
        while User.objects.filter(username=username).exists():
            username = f"user-{random_int:09}"
        self.username = username
