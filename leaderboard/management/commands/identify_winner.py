from django.core.management.base import BaseCommand
from leaderboard.models import User, Winner
from django.db import transaction
from django.utils import timezone

class Command(BaseCommand):
    help = 'Identify the user with the highest points and record them as a winner.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Identifying the winner...")
        try:

            highest_points_users = User.objects.all().order_by('-points')
            if not highest_points_users:
                return

            top_user = highest_points_users.first()
            if highest_points_users.count() > 1 and highest_points_users[1].points == top_user.points:
                # If there's a tie, do not declare a winner
                return

            Winner.objects.create(user=top_user, points=top_user.points, timestamp=timezone.now())

        except Exception as e:
            self.stderr.write(f"Error: {str(e)}")
            raise
