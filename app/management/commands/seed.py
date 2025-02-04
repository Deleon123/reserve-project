import random
from django.core.management.base import BaseCommand
from faker import Faker
from app.models import User, Room, Reservation
from datetime import timedelta
from django.utils import timezone

fake = Faker()

class Command(BaseCommand):
    help = "Seed the database with fake data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding database...")

        # Create Users
        users = []
        for _ in range(100):
            user = User.objects.create(
                name=fake.name(),
                email=fake.unique.email(),
            )
            users.append(user)

        # Create Rooms
        rooms = []
        for _ in range(50):
            room = Room.objects.create(
                name=fake.company(),
                capacity=random.randint(5, 50),
                location=fake.address(),
            )
            rooms.append(room)

        # Create Reservations
        for _ in range(200):
            start_time = timezone.now()
            end_time = start_time + timedelta(hours=random.randint(1, 4))

            Reservation.objects.create(
                room=random.choice(rooms),
                user_name=random.choice(users).name,
                start_time=start_time,
                end_time=end_time
            )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
