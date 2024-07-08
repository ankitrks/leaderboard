from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils import timezone
from leaderboard.models import User, Winner
from unittest.mock import patch
from datetime import timedelta

class UserTests(APITestCase):

    def setUp(self):
        self.user_data = {
            "name": "John Doe",
            "age": 30,
            "address": "123 Main St",
        }

    def test_create_user(self):
        url = reverse('user-list')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().name, "John Doe")

    def test_get_user(self):
        user = User.objects.create(**self.user_data)
        url = reverse('user-detail', kwargs={'pk': user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "John Doe")

    def test_add_points(self):
        user = User.objects.create(**self.user_data)
        url = reverse('add-points', kwargs={'pk': user.pk})
        response = self.client.post(url, {"points": 10}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.points, 10)

    def test_subtract_points(self):
        user = User.objects.create(**self.user_data)
        url = reverse('subtract-points', kwargs={'pk': user.pk})
        response = self.client.post(url, {"points": 5}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.points, -5)

class ScheduledJobTests(APITestCase):

    def setUp(self):
        self.user_data1 = {
            "name": "John Doe",
            "age": 30,
            "address": "123 Main St",
            "points": 10
        }
        self.user_data2 = {
            "name": "Jane Smith",
            "age": 25,
            "address": "456 Elm St",
            "points": 20
        }
        self.user1 = User.objects.create(**self.user_data1)
        self.user2 = User.objects.create(**self.user_data2)

    @patch('tasks.check_highest_points_user')
    def test_scheduled_job(self, mock_check_highest_points_user):
        mock_check_highest_points_user.return_value = None
        # Simulate running the task
        from tasks import check_highest_points_user
        check_highest_points_user()
        mock_check_highest_points_user.assert_called_once()

    def test_winner_creation(self):
        from tasks import check_highest_points_user
        check_highest_points_user()
        self.assertEqual(Winner.objects.count(), 1)
        winner = Winner.objects.first()
        self.assertEqual(winner.user, self.user2)
        self.assertEqual(winner.points, 20)

    def test_no_winner_on_tie(self):
        self.user1.points = 20
        self.user1.save()
        from tasks import check_highest_points_user
        check_highest_points_user()
        self.assertEqual(Winner.objects.count(), 0)

    def test_winner_has_timestamp(self):
        from tasks import check_highest_points_user
        check_highest_points_user()
        winner = Winner.objects.first()
        self.assertIsNotNone(winner.timestamp)
        self.assertAlmostEqual(winner.timestamp, timezone.now(), delta=timedelta(seconds=10))
