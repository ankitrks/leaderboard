from django.core.management.base import BaseCommand
from leaderboard.factories import UserFactory

class Command(BaseCommand):
    help = 'Populate the database with initial users'

    def handle(self, *args, **kwargs):
        for _ in range(10):  # Number of users to create
            UserFactory.create()

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with initial users'))
