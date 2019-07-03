from django.db import models
from django_random_queryset import RandomManager

class Question(models.Model):
    text = models.TextField(max_length=500)
    weight = models.IntegerField(choices=[(x, x) for x in range(5, 21)])
    randoms = RandomManager()
    objects = models.Manager()

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(max_length=250)
    right = models.BooleanField()
    objects = models.Manager()
    def __str__(self):
        return self.text

class GameRecord(models.Model):
    user_name = models.CharField(max_length=100)
    user_surname = models.CharField(max_length=100)
    score = models.IntegerField(default=0)
