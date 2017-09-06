from django.db import models


class Booking(models.Model):
    resnr = models.IntegerField()
    relation = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()
    activities = models.CharField(max_length=255)

    def __str__(self):
        return str(self.start) + self.relation


class Activity(models.Model):
    name = models.CharField(max_length=255)
    bookings = models.ManyToManyField(Booking, blank=True)

    def __str__(self):
        return self.name


class Instructor(models.Model):
    name = models.CharField(max_length=255)
    bookings = models.ManyToManyField(Booking, blank=True)

    def __str__(self):
        return self.name
