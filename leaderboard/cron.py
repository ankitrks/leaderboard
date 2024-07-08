from django_cron import CronJobBase, Schedule
from .models import User, Winner

class IdentifyWinnerJob(CronJobBase):
    RUN_EVERY_MINS = 5  # every 5 minutes

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'leaderboard.identify_winner'

    def do(self):
        top_users = User.objects.order_by('-points')
        if top_users.exists():
            top_user = top_users.first()
            # Check if there's a tie
            if top_users.filter(points=top_user.points).count() == 1:
                Winner.objects.create(user=top_user, points=top_user.points)
