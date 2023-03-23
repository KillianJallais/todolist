from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from todolist.models import Task
from django.utils import timezone

import pytz

import datetime


##################### Views that shows the different types of task #####################
def index(request):
    """
    return the home page of the todolist app
    with tasks not completed and not obsolete
    """
    temp = Task.objects.filter(completed=False)
    tasks = [task for task in temp if not task.isExpired()]

    context = {
        "tasks":tasks,
    }
    
    return render(request, "todolist/index.html", context)

def obsoleteTask(request):

    #get all the tasks that are expired and not completed
    temp = Task.objects.filter(completed=False)
    tasks = [task for task in temp if task.isExpired()]

    context = {
        "tasks":tasks,
    }

    return render(request, "todolist/obsoleteTask.html", context)

def completedTask(request):
    """
    return the page that show the completed tasks
    """

    #Get all the task that are completed
    tasks = Task.objects.filter(completed=True)

    context =  {
        "tasks":tasks,
    }

    return render(request, "todolist/completedTask.html", context)



##################### Views that modify the database #####################
def addTask(request):
    """
    Check if the limite date of the task is valid
    and if so, create the task and save it to the database
    then redirect to the home page.
    Else return the page the create tasks.
    """
    annee, mois, jours = request.POST["limiteDate"].split("-")

    date = timezone.datetime(
        int(annee),
        int(mois),
        int(jours),
        tzinfo=pytz.utc
    )
    
    if Task.checkLimitDate(date):
        task = Task(
            name=request.POST["name"],
            description=request.POST["description"],
            limiteDate=date
            )
        task.save()

        return redirect("/todolist/")
    
    else:
        name = request.POST["name"]
        description = request.POST["description"]
        date = request.POST["limiteDate"]

        context = {
            "error" : "La deadline doit être dans le future.",
            "name": name,
            "description":description,
            "limiteDate":date,
        }

        return render(request, "todolist/createTask.html", context)

def delTask(request, taskId):
    """
    get the task associated to the taskId and delete it from the database
    """
    try:
        Task.objects.get(id=taskId).delete()
    except Task.DoesNotExist:
        raise Http404("La tâche n'existe pas.")
    
    return redirect("/todolist/")

def updateTask(request, taskId):
    """
    get the task associated to the taskId and update its
    attribute then redirect to the home page
    """
    try:
        task = Task.objects.get(id=taskId)
    except Task.DoesNotExist:
        raise Http404("La tâche n'existe pas.")
    
    annee, mois, jours = request.POST["limiteDate"].split("-")

    date = timezone.datetime(
        int(annee),
        int(mois),
        int(jours),
        tzinfo=pytz.utc
    )
    
    if Task.checkLimitDate(date):
        task.name = request.POST["name"]
        task.description = request.POST["description"]
        task.limiteDate = date

        task.save()

        return redirect("/todolist/")
    else:
        context = {
            "error":"La deadline ne peut pas être dans le passé",
            "task":task,
        }
        return render(request, "todolist/editTask.html", context)



##################### Views that return pages #####################
def createTask(request):
    """
    return the page for creating tasks
    """

    context = {
        "error":"",
        "name":"",
        "description":"",
        "limiteDate":"",
    }

    return render(request, "todolist/createTask.html", context)

def showTask(request, taskId):
    """
    get the page associated to the taskId and return the page
    which allows to visualize the task
    """

    try:
        task = Task.objects.get(id=taskId)
    except Task.DoesNotExist:
        raise Http404("La tâche n'existe pas.")
    
    print(task.__repr__())
    
    context = {
        "task":task,
    }

    return render(request, "todolist/showTask.html", context)

def editTask(request, taskId):
    """
    get the task associeted to the taskId and return
    the page the modifie this task
    """
    try:
        task = Task.objects.get(id=taskId)
    except Task.DoesNotExist:
        raise Http404("La tâche n'existe pas.")

    context = {
        "error":"",
        "task":task,
    }
    
    return render(request, "todolist/editTask.html", context)

def completeTask(request, taskId):
    """
    get the task associated to the taskId
    and update the completed attribute of the task
    and then redirect to the home page
    """
    try:
        task = Task.objects.get(id=taskId)
    except Task.DoesNotExist:
        raise Http404("La tâche n'existe pas")
    

    """
    check if the task is mark as completed and put the
    value in task.completed. It is done in the form of
    an expression because if the checkbox is not checked,
    it do not appear in request.POST
    """
    task.completed = ("completed" in request.POST.keys())
    task.save()
    
    return redirect("/todolist/")
