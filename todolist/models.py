from django.db import models
from django.utils import timezone

class Task(models.Model):
    name = models.CharField(max_length=200, default="")
    description = models.CharField(max_length=200, default="")
    completed = models.BooleanField(default=False)
    limiteDate = models.DateTimeField() #deadline for the task
    pubDate = models.DateTimeField(default=timezone.now) #publication date

    """
    There are 3 types of tasks:
        -the "valid" task:
            It's a task that is not completed and not expired
        -the "completed" task:
            It's simply a task that is completed weither it's expired or not
        -the "obsolete" task:
            It's a task that is expired and not completed
    """

    def isExpired(self) -> bool:
        """
        return True if the limite date is passed,
        that means that the task is expired.
        """
        return self.limiteDate < timezone.now()
        
    def getDate(self) -> str:
        """
        Return the date in the format DD/MM/YYYY
        """
        return f"{self.limiteDate.day:02d}/{self.limiteDate.month:02d}/{self.limiteDate.year}"
    
    def getHtmlDate(self) -> str:
        """
        return a format that can be used in a html date input (YYYY-MM-DD).
        """
        return f"{self.limiteDate.year}-{self.limiteDate.month:02d}-{self.limiteDate.day:02d}"
    
    def checkLimitDate(date):
        """
        return true if the date that is passed in argument is in the future,
        else return false
        """
        return date > timezone.now()

    def __repr__(self) -> str:
        return f"Task({self.description}, {self.limiteDate}, {self.completed})"
