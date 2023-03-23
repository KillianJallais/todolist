from django.test import TestCase
from django.utils import timezone

import datetime

from todolist.models import Task
from . import views

class TaskTest(TestCase):
    
    def setUp(self):
        self.futureDate = timezone.now() + datetime.timedelta(days=10)
        self.name = "tast"

    def test_if_is_expired_when_expired(self):
        """
        test if task.expired() return true when she is expired
        """

        date = timezone.now() - datetime.timedelta(seconds=1)
        task = Task(name=self.name, limiteDate=date)

        self.assertIs(task.isExpired(), True)

    def test_if_completed_is_set_to_false_when_created(self):
        """
        Test if the attribute completed is set to False
        when an object task is created
        """

        task = Task(name=self.name, limiteDate=self.futureDate)

        self.assertIs(task.completed, False)
    
    def test_if_pubDate_is_correct(self):
        """
        test if the attribut pubDate who is create automaticaly
        is valid (pubDate is the publication date of a task)
        """

        passedDate = timezone.now() - datetime.timedelta(seconds=10) #date 10 seconds in the past
        incomingDate = timezone.now() + datetime.timedelta(seconds=10) #date 10 seconds in the future

        task = Task(name=self.name, limiteDate=self.futureDate)

        expression = task.pubDate > passedDate and task.pubDate < incomingDate

        self.assertIs(expression, True)

    def test_checkLimitDate_when_date_is_in_the_future(self):
        """
        test if the class method Task.checkLimitDate(date) return True
        when the date that is passed in argument is in the future.
        """

        date = timezone.now() + datetime.timedelta(days=10)
        self.assertIs(Task.checkLimitDate(date), True)
    
    def test_checkLimitDate_when_date_is_in_the_past(self):
        """
        test if the class method Task.checkLimitDate(date) return False
        when the date that is passed in argument is in the past
        """

        date = timezone.now() - datetime.timedelta(10)
        self.assertIs(Task.checkLimitDate(date), False)
    
   