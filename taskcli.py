
import argparse
import os
import json
from dataclasses import dataclass, field
import datetime
from typing import TextIO


@dataclass
class TaskCLI:
    """
    Command line tool for managing daily task
    """
    
    #initiate name of default file for recording task
    default_file: str = field(default="Default-Task-Tracker.json")

    @staticmethod
    def _create_task_file()->TextIO:
        """
        Create default task file

            Returns: 
                file (TextIO): file for recoding task
        """
        default_filename = "Default-Task-Tracker.json"
        with open(default_filename, 'x', encoding='utf-8') as file:
            return file
    
    def __post_init__(self) -> TextIO | None:
        """
        check if file exist and create if it doesnt exist
        """
        if not os.path.exists(self.default_file):
            self._create_task_file()
   
    def parse_command(self, argt=None) -> argparse.Namespace:
        """
        command line parsers for tasks

        Returns:
            argument (Namespace): namespace for the arguments parsed from command line
        """
        parser = argparse.ArgumentParser()
        subparser = parser.add_subparsers(dest='command')

        add_task = subparser.add_parser('add')
        add_task.add_argument("taskid", help="task id to be added")
        add_task.add_argument("taskdescription", help="task decription to be added")

        update_task = subparser.add_parser('update')
        update_task.add_argument("taskid", help="task id to be updated")
        update_task.add_argument("taskdescription", help="task decription to be updated")

        delete_task = subparser.add_parser('delete')
        delete_task.add_argument("taskid", help="task id to be deleted")

        mark_progress = subparser.add_parser('mark-in-progress')
        mark_progress.add_argument("taskid")

        mark_done = subparser.add_parser('mark-done')
        mark_done.add_argument("taskid")

        list_task = subparser.add_parser('list')
        list_task.add_argument("status", nargs='?', choices=['todo', 'in-progress', 'done'])

        argument = parser.parse_args(argt)

        return argument

    def add_task(self, p_arg)->None:
        """
        Add a new task 

        Args:
            p_arg (argparse.Namespace): parsed argument
        Return:
            None
        """
        added_time = str(datetime.datetime.now())
        task_data = dict(id=p_arg.taskid, description=p_arg.taskdescription, status='todo', createdAt=added_time, updatedAt=added_time)
        task_list = list()
        task_list.append(task_data)
        if os.path.getsize(self.default_file) == 0:
            with open(self.default_file, 'w', encoding="utf-8") as file:
                json.dump(task_list, file, indent=4)
        else:
            with open(self.default_file, 'r+', encoding='utf-8') as file:
                file_data = json.load(file)
                file_data.append(task_data)
                file.seek(0)
                json.dump(file_data, file, indent=4)
        print("New Task added succesfully!")

    def update_task(self, p_arg):
        """
        Update existing task 

        Args:
            p_arg (argparse.Namespace): parsed argument
        Return:
            None
        """
        update_time = str(datetime.datetime.now())
        with open(self.default_file, 'r', encoding='utf-8') as file:
            file_data = json.load(file)

        for task in file_data:
            if task['id'] == p_arg.taskid:
                task['description'] = p_arg.taskdescription
                task['updatedAt'] = update_time

        with open(self.default_file, 'w', encoding='utf-8') as file:
            json.dump(file_data, file, indent=4) 

        print("Task has been updated added succesfully!") 
        
    def delete_task(self, p_arg):
        """
        Delete existing task 

        Args:
            p_arg (argparse.Namespace): parsed argument
        Return:
            None
        """
        with open(self.default_file, 'r', encoding='utf-8') as file:
            file_data = json.load(file)

        for task in file_data:
            if task['id'] == p_arg.taskid:
                task_index = file_data.index(task)
                file_data.pop(task_index)
                
        with open(self.default_file, 'w', encoding='utf-8') as file:
            json.dump(file_data, file, indent=4)

        print("Task has been deleted added succesfully!")

    def mark_progress(self, p_arg):
        """
        Set status of existing task to 'In Progress'

        Args:
            p_arg (argparse.Namespace): parsed argument
        Return:
            None
        """
        update_time = str(datetime.datetime.now())
        with open(self.default_file, 'r', encoding='utf-8') as file:
            file_data = json.load(file)

        for task in file_data:
            if task['id'] == p_arg.taskid:
                task['status'] = 'In Progress'
                task['updatedAt'] = update_time

        with open(self.default_file, 'w', encoding='utf-8') as file:
            json.dump(file_data, file, indent=4)

        print(f"Status of Task {p_arg.taskid} has been set to 'In Progress'.")

    def mark_done(self, p_arg):
        """
        Set status of existing task to 'Done'

        Args:
            p_arg (argparse.Namespace): parsed argument
        Return:
            None
        """
        update_time = str(datetime.datetime.now())
        with open(self.default_file, 'r', encoding='utf-8') as file:
            file_data = json.load(file)

        for task in file_data:
            if task['id'] == p_arg.taskid:
                task['status'] = 'Done'
                task['updatedAt'] = update_time

        with open(self.default_file, 'w', encoding='utf-8') as file:
            json.dump(file_data, file, indent=4)

        print(f"Status of Task {p_arg.taskid} has been set to 'Done'.")

    def list_task(self, p_arg):
        """
        List all the current task, task with 'todo' status, 'in progress' status and 'done' status.

        Args:
            p_arg (argparse.Namespace): parsed argument
        Return:
            None
        """
        with open(self.default_file, 'r', encoding='utf-8') as file:
            file_data = json.load(file)

        match p_arg.status:
            case None:
                for task in file_data:
                    print(f'''Task ID: {task['id']}\n
                              Description: {task['description']}\n
                              Status: {task['status']}\n
                              Created: {task['createdAt']}\n
                              Updated: {task['updatedAt']}\n''')
                    print()
            case 'todo':
                for task in file_data:
                    if task['status'] == 'todo':
                        print(f'''Task ID: {task['id']}\n
                              Description: {task['description']}\n
                              Status: {task['status']}\n
                              Created: {task['createdAt']}\n
                              Updated: {task['updatedAt']}\n''')
                        print()
            case 'in-progress':
                for task in file_data:
                    if task['status'].lower() == 'in progress':
                        print(f'''Task ID: {task['id']}\n
                              Description: {task['description']}\n
                              Status: {task['status']}\n
                              Created: {task['createdAt']}\n
                              Updated: {task['updatedAt']}\n''')
                        print()
            case 'done':
                for task in file_data:
                    if task['status'].lower() == 'done':
                        print(f'''Task ID: {task['id']}\n
                              Description: {task['description']}\n
                              Status: {task['status']}\n
                              Created: {task['createdAt']}\n
                              Updated: {task['updatedAt']}\n''')
                        print()

        


if __name__ == "__main__":
    #initiate TaskCLI class
    my_task: TaskCLI = TaskCLI()

    #return parsed arguments from parse_command function
    parsedCommands = my_task.parse_command()

    #initiate instance of TaskCLI class
    match parsedCommands.command:
        case "add":
            my_task.add_task(parsedCommands)
        case "update":
            my_task.update_task(parsedCommands)
        case "delete":
            my_task.delete_task(parsedCommands)
        case "mark-in-progress":
            my_task.mark_progress(parsedCommands)
        case "mark-done":
            my_task.mark_done(parsedCommands)
        case "list":
            my_task.list_task(parsedCommands)

        
