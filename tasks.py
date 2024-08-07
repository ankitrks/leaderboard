from celery_app import app
from django.utils import timezone

@app.task
def check_highest_points_user():
    from leaderboard.models import User, Winner

    # Get the user with the highest points
    highest_points_user = User.objects.order_by('-points').first()

    # Check if there's a tie (multiple users with the same highest points)
    if highest_points_user:
        tie_users = User.objects.filter(points=highest_points_user.points)
        if tie_users.count() > 1:
            # If tie, do not declare a winner
            return None

    # Create a winner record
    if highest_points_user:
        Winner.objects.create(
            user=highest_points_user,
            points=highest_points_user.points,
            timestamp=timezone.now()
        )
        return highest_points_user
    return None