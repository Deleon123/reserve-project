from django.db import models
from hashlib import md5
from django.core.validators import MinValueValidator

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    auth_token = models.UUIDField()

    def save(self, *args, **kwargs):
        # Generates new hashed value for token
        self.auth_token = md5(self.email.encode()).hexdigest()
        super().save(*args, **kwargs)

class Room(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])  
    location = models.CharField(max_length=255)


class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reservations")
    user_name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_time__lt=models.F('end_time')),
                name="start_time_before_end_time"
            )
        ]
