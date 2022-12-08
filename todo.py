from datetime import datetime
import pickle
import argparse
from tabulate import tabulate

# Declaring global null date variable
# This will help use due_date for sorting and operations (like printing)
# If due_date is chosen as null then it can't be used for sorting
global null_date

#Assigning value to global variable
null_date = datetime.min 

class Task:
    """Representation of a task

    Attributes:
                - created - date
                - completed - date
                - name - string
                - unique id - number
                - priority - int value of 1, 2, or 3; 1 is default
                - due date - date, this is optional
                - age - string
    """

    def __init__(self, name, unique_id, priority=1, due_date = null_date):
        """Default Constructor for Task Class"""
        self.created = datetime.now()
        self.completed = None
        self.name = name
        self.unique_id = unique_id
        self.priority = priority
        self.age = "0d"

        try:
            self.due_date = datetime.strptime(due_date,"%m/%d/%Y")
        
        except TypeError:
            self.due_date = due_date

    
    def returnList(self):
        """Method that returns a list of the task for list and query presentation"""

        list_due_date = self.due_date.strftime("%m/%d/%Y") if self.due_date != null_date else "-"

        list_data = [self.unique_id, self.age, list_due_date, self.priority, self.name]
        return list_data
    
    def returnReport(self):
        """Method that returns a list of the task for report presentation"""

        report_due_date = self.due_date.strftime("%m/%d/%Y") if self.due_date != null_date else "-"
        report_completed_date = self.completed.strftime("%a %b %d %H:%M:%S %Z %Y") if self.completed != None else "-"

        report_data = [self.unique_id, self.age, report_due_date, self.priority, self.name, self.created.strftime("%a %b %d %H:%M:%S %Z %Y"), report_completed_date]
        
        return report_data    


class Tasks:
    """A list of `Task` objects."""


    def __init__(self):
        """Read pickled tasks file into a list"""
        
        #To keep track of uid count for add
        self.uid_count = 1
        
        #reading data from pickle file
        try:
            with open(".todo.pickle",'rb') as f:
                self.tasks = pickle.load(f)
        
        except FileNotFoundError:
            #For the very first time file is being created
            default_task_list = []
            default_task_1 = Task("Default Task_1",1)
            default_task_2 = Task("Default Task_2",2)
            default_task_list.extend([default_task_1,default_task_2])
            with open(".todo.pickle",'wb') as f:
                pickle.dump(default_task_list,f)
            
            with open(".todo.pickle",'rb') as f:
                self.tasks = pickle.load(f)

        #Updating values for every task
        for task in self.tasks:
            age = datetime.now() - task.created
            task.age = str(age.days) + "d"
            if task.unique_id >= self.uid_count:
                self.uid_count = task.unique_id + 1
                

    def pickle_tasks(self):
        """Picle your task list to a file"""
        
        with open(".todo.pickle",'wb') as f:
            pickle.dump(self.tasks, f)

    def list(self):
        """Method to display a list of all the uncompleted tasks"""

        task_list = []

        self.tasks.sort(key= lambda x: x.due_date, reverse= True)

        for task in self.tasks:
            if task.completed == None:
                list_data = task.returnList()
                task_list.append(list_data)

        list_headings = ["ID", "Age", "Due Date", "Priority", "Task"]

        print(tabulate(task_list, headers= list_headings))


    def report(self):
        """Method to display a list of all the tasks"""

        task_report = []

        self.tasks.sort(key= lambda x: x.created, reverse= True)

        for task in self.tasks:
            report_data = task.returnReport()
            task_report.append(report_data)
        
        report_headings = ["ID", "Age", "Due Date", "Priority", "Task", "Created", "Completed"]

        print(tabulate(task_report, headers= report_headings))

    def done(self, uid):
        """Method to mark a task as completed"""

        for task in self.tasks:
            if task.unique_id == uid:
                task.completed = datetime.now()
                print("Completed Task:", uid)
                break

    def query(self, queries):
        """Method to print all the uncompleted tasks with words in the queries"""
        
        query_list = []

        for query in queries:
            for task in self.tasks:
                if task.completed == None:
                    if task.name.find(query) > -1:
                        query_data = task.returnList()
                        query_list.append(query_data)

        query_headings = ["ID", "Age", "Due Date", "Priority", "Task"] 

        print(tabulate(query_list, headers= query_headings))               

    def add(self, name, priority = 1, due_date = null_date):
        """Method to add a task in the list"""
        
        task_add = Task(name, self.uid_count, priority, due_date)
        self.tasks.append(task_add)
        print("Created Task:",task_add.unique_id)
        self.uid_count += 1
    
    def delete(self, uid):
        """Method to delete a task based on its unique id"""

        for task in self.tasks:
            if task.unique_id == uid:
                self.tasks.remove(task)
                print("Deleted Task:",uid)
                break

def main():
    """Main function of todo.py"""
    tasks = Tasks()

    parser = argparse.ArgumentParser()

    #parsers for adding tasks
    parser.add_argument("--add", type=str)
    parser.add_argument("--priority", type=int, default=1)
    parser.add_argument("--due", type=str, default= null_date)

    #parsers for tasks that prints tables
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--query",type=str, required=False, nargs="+")

    #parsers that perform operation on unique_id
    parser.add_argument("--delete", type= int)
    parser.add_argument("--done", type= int)

    argument = parser.parse_args()

    #If argument is for adding tasks
    if argument.add:
        
        if argument.due:
            due_date = argument.due

        if argument.priority:
            priority = argument.priority
        
        tasks.add(argument.add, priority, due_date)

    #If argument is for printing tables
    if argument.list:
        tasks.list()
    
    if argument.report:
        tasks.report()

    if argument.query:
        tasks.query(argument.query)

    #If argument perform operation on unique_id
    if argument.delete:
        tasks.delete(argument.delete)
    
    if argument.done:
        tasks.done(argument.done)
    
    tasks.pickle_tasks()

if __name__ == "__main__":
    main()
