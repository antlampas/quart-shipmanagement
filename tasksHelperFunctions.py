#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-06-24

from tasksClasses import Task
from tasksClasses import Tasks
from loaders      import load

def isTaskPresent(task=Task()):
    """
    Checks if the single task is in datastore
    """
    if task.Name:
        taskDB = load('task',task.Name)
        if taskDB:
            return True
        else:
            return False
    else:
        return False

def tasksMatchDatastore(tasks=Tasks()):
    """
    Checks if the list of tasks is in datastore
    """
    tasksDB = load('tasks')
    if tasksDB:
        tasksList = Tasks(tasksDB)
        if tasksList == tasks:
            return True
        else:
            return False
    else:
        return False