
import argparse
import os
import json
import datetime
import tabulate


class TaskCLI:

    """
    Command line tool for managing daily task
    """
    
    def __init__(self) -> None:
        #initiate default file for recording task
        self.default_task_file = "TaskFile.json"
        if not os.path.exists(self.default_task_file):
            taskfile = open(self.default_task_file, mode='x')
            taskfile.close()
            
    
    @staticmethod
    def _get_current_id(current_task_file) -> int:
        if os.path.getsize(current_task_file) == 0:
            current_id = 1
        else:
            with open(current_task_file, mode='r', encoding='utf-8') as file:
                file_data = json.load(file)
            current_id = file_data[-1]["id"] + 1 
        return current_id


    def parse_command(self, argt=None) -> argparse.Namespace:
        """
        command line parsers for tasks

        Returns:
            argument (Namespace): namespace for the arguments parsed from command line
        """
        parser = argparse.ArgumentParser()
        subparser = parser.add_subparsers(dest='command')

        add_task = subparser.add_parser('add')
        add_task.add_argument("taskdescription", help="task decription to be added")

        update_task = subparser.add_parser('update')
        update_task.add_argument("taskid", help="task id to be updated", type=int)
        update_task.add_argument("taskdescription", help="task decription to be updated", type=str)

        delete_task = subparser.add_parser('delete')
        delete_task.add_argument("taskid", help="task id to be deleted", type=int)

        mark_progress = subparser.add_parser('mark-in-progress')
        mark_progress.add_argument("taskid", type=int)

        mark_done = subparser.add_parser('mark-done')
        mark_done.add_argument("taskid", type=int)

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
        add_time = str(datetime.datetime.now())
        task_id = self._get_current_id(self.default_task_file)
        #create List[dict] to create data object and write in JSON format
        task_object = dict(id=task_id, description=p_arg.taskdescription, status='todo', createdAt=add_time, updatedAt=add_time)
        task = list()
        task.append(task_object)
        if os.path.getsize(self.default_task_file) == 0:
            with open(self.default_task_file, 'w', encoding="utf-8") as file:
                json.dump(task, file, indent=4)
        else:
            with open(self.default_task_file, 'r+', encoding='utf-8') as file:
                file_data = json.load(file)
                file_data.append(task_object)
                file.seek(0)
                json.dump(file_data, file, indent=4)
        print("A New Task has been added succesfully!")


    def update_task(self, p_arg):
        """
        Update existing task 

        Args:
            p_arg (argparse.Namespace): parsed argument
        Return:
            None
        """
        update_time = str(datetime.datetime.now())
        with open(self.default_task_file, 'r', encoding='utf-8') as file:
            file_data = json.load(file)
        for task in file_data:
            if task['id'] == p_arg.taskid:
                task['description'] = p_arg.taskdescription
                task['updatedAt'] = update_time
        with open(self.default_task_file, 'w', encoding='utf-8') as file:
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
        with open(self.default_task_file, 'r', encoding='utf-8') as file:
            file_data = json.load(file)

        for task in file_data:
            if task['id'] == p_arg.taskid:
                task_index = file_data.index(task)
                file_data.pop(task_index)
                
        with open(self.default_task_file, 'w', encoding='utf-8') as file:
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
        with open(self.default_task_file, 'r', encoding='utf-8') as file:
            file_data = json.load(file)

        for task in file_data:
            if task['id'] == p_arg.taskid:
                task['status'] = 'In Progress'
                task['updatedAt'] = update_time

        with open(self.default_task_file, 'w', encoding='utf-8') as file:
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
        with open(self.default_task_file, 'r', encoding='utf-8') as file:
            file_data = json.load(file)

        for task in file_data:
            if task['id'] == p_arg.taskid:
                task['status'] = 'Done'
                task['updatedAt'] = update_time

        with open(self.default_task_file, 'w', encoding='utf-8') as file:
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
        try:
            with open(self.default_task_file, 'r', encoding='utf-8') as file:
                file_data = json.load(file)

            match p_arg.status:
                case None:
                    print(tabulate.tabulate(file_data, headers={}, tablefmt="rounded_grid"))
                case 'todo':
                    todo_task = [task for task in file_data if task['status'] == 'todo']
                    print(tabulate.tabulate(todo_task, headers={}, tablefmt="rounded_grid")) if todo_task.__len__() != 0 else print("You dont have any task in progress!")
                case 'in-progress':
                    in_progress_task = [task for task in file_data if task['status'].lower() == 'in progress']
                    print(tabulate.tabulate(in_progress_task, headers={}, tablefmt="rounded_grid")) if in_progress_task.__len__() != 0 else print("You dont have any task in progress!")
                case 'done':
                    done_task = [task for task in file_data if task['status'].lower() == 'done']
                    print(tabulate.tabulate(done_task, headers={}, tablefmt="rounded_grid")) if done_task.__len__() != 0 else print("You haven't completed any task")
        except json.JSONDecodeError:
            print("Hey there! you have no task in your list")


        

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

        
