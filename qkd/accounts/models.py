from django.db import models

# Create your models here.
class secret_keys(models.Model):
	sender_key = models.CharField(max_length=1000)
	receiver_key = models.CharField(max_length=1000)


