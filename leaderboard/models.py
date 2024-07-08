from django.db import models

class User(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    points = models.IntegerField(default=0)
    address = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)

    def __str__(self):
        return self.name

class Winner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField()

    def __str__(self):
        return f'{self.user.name} - {self.timestamp}'
