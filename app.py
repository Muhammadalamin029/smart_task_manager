from classes import User, Task
import json

users = {}
logged_in_user = {}

with open("users.json", "r") as file:
    users.update(json.load(file))


def start_manager():
    while True:

        print("\nWelcome to Smart Task Manager")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        try:
            prompt = int(input("\nChoose Your prompt? "))
        except ValueError:
            print("Only numbers are accepted!!!")
            continue

        if prompt == 1:
            register_user()
        elif prompt == 2:
            login_user()
        elif prompt == 3:
            print("Goodbye!!!")
            break
        else:
            print("Enter numbers between 1 - 3")
            continue


def register_user():

    while True:
        username = input("Enter your preferred username: ").lower().title()

        if username in users:
            print("Username exists")
            continue

        else:
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            confirm_password = input("Confirm your entered: ")

            if password == confirm_password:

                user = User(name=username, password=password, email=email)

                users.update({username: user.to_dict()})

            else:
                print("\n Password doesn't match!!!")
                continue

        with open("users.json", "w") as file:
            json.dump(users, file, indent=4)
            print("\nUser registered")
            break


def login_user():
    while True:
        print("\nLogin into your account")
        print("1. Login with username")
        print("2. Login with email")
        print("3. Go back")

        try:
            prompt = int(input("\nChoose Your prompt? "))
        except ValueError:
            print("Only numbers are accepted!!!")
            continue

        if prompt == 1:
            username = input("Enter your preferred username: ").title()

            if username in users:
                password = input("Enter your password: ")

                if users[username]["password"] == password:
                    logged_in_user.update(users[username])
                    logged_in(username=username)
            else:
                print(f"No user with the username {username} registered")
                continue
        elif prompt == 2:
            print("Not available yet")
        elif prompt == 3:
            break
        else:
            print("Enter numbers between 1 - 3")
            continue


def logged_in(username):
    while True:
        print(f"\nHello, {users[username]["username"]}!")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. View Stats")
        print("6. Logout")

        try:
            prompt = int(input("\nChoose Your prompt? "))
        except ValueError:
            print("Only numbers are accepted!!!")
            continue

        if prompt == 1:
            AddTask(username)
        elif prompt == 2:
            ViewTask()
        elif prompt == 3:
            UpdateTask()
        elif prompt == 4:
            DeleteTask()
        elif prompt == 5:
            ViewStats()
        elif prompt == 6:
            logged_in_user.clear()
            print("Goodbye!!!")
            break
        else:
            print("Enter numbers between 1 - 6")
            continue


def AddTask(username):
    old_tasks = []
    for task in logged_in_user["tasks"]:
        old_tasks.append(task)
    title = input("Enter task title: ").lower().title()
    category = input(
        "Enter task category: (Work, Personal or Study)").lower().title()
    description = input("Enter task description: ").lower().title()
    due_date = input("Enter task due date: ").lower().title()
    priority = input(
        "Enter task priority: (High, Normal or Low)").lower().title()

    new_task = Task(title=title, category=category,
                    description=description, due_date=due_date, priority=priority)

    old_tasks.append(new_task.to_dict())
    print(old_tasks)

    logged_in_user.update({"tasks": old_tasks})
    users[username].update(logged_in_user)

    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

    print(f"Task successfully added with an id of {new_task.id}")


def ViewTask():
    tasks = logged_in_user["tasks"]

    print(f"\n{logged_in_user["username"]}'s Tasks:\n")

    for i, task in enumerate(tasks, 1):
        print(f"Task {i}")
        print(f"  ID         : {task['id']}")
        print(f"  Title      : {task['title']}")
        print(f"  Description: {task['description']}")
        print(f"  Category   : {task['category']}")
        print(f"  Priority   : {task['priority']}")
        print(f"  Due Date   : {task['due_date']}")
        print(f"  Status     : {task['status']}")
        print(f"  Created At : {task['created_at']}\n")


def UpdateTask():
    tasks = logged_in_user["tasks"]

    ViewTask()
    task_title = input("Enter the task title: ").lower().title()

    while True:
        print("\nChoose status update: ")
        print("1. Completed")
        print("2. In Progress")

        try:
            new_status = int(input("Enter the new status: "))
        except ValueError:
            print("Only numbers are accepted!!!")
            continue

        for i, task in enumerate(tasks):
            if task_title == task["title"]:
                task["status"] = "Completed" if new_status == 1 else "In Progress"
                tasks[i] = task

        users[logged_in_user["username"]].update(logged_in_user)

        with open("users.json", "w") as file:
            json.dump(users, file, indent=4)

        print(f"Task has been successfully updated")
        break


def DeleteTask():
    tasks = []
    for task in logged_in_user["tasks"]:
        tasks.append(task)

    ViewTask()
    task_title = input("Enter the task title: ").lower().title()
    tasks_by_title = {task["title"]: task for task in logged_in_user["tasks"]}
    new_task = []

    while True:
        if task_title in tasks_by_title:
            print(f"\nAre you sure you want to delete task {task_title}: ")
            print("1. Yes")
            print("2. No")

            try:
                prompt = int(input("Choose your option: "))
            except ValueError:
                print("Only numbers are accepted!!!")
                continue

            if prompt == 1:
                for task in tasks:
                    if task["title"] != task_title:
                        new_task.append(task)

                logged_in_user["tasks"] = new_task
                users[logged_in_user["username"]].update(logged_in_user)

            else:
                break

            with open("users.json", "w") as file:
                json.dump(users, file, indent=4)
            print(
                f"Task {task_title} has been deleted succesfully!!!\n")
            break

        else:
            print(f"Task with the title {task_title} doesn`t exist!!!")
            continue


def ViewStats():
    tasks = []
    for task in logged_in_user["tasks"]:
        tasks.append(task)

    total_tasks = len(tasks)

    pending_tasks = [item for item in tasks if item["status"] == "Pending"]
    completed_tasks = [item for item in tasks if item["status"] == "Completed"]
    progress_tasks = [
        item for item in tasks if item["status"] == "In Progress"]

    high_priority = [
        item for item in tasks if item["priority"] == "High"]
    normal_priority = [
        item for item in tasks if item["priority"] == "Normal"]
    low_priority = [
        item for item in tasks if item["priority"] == "Low"]

    work_category = [
        item for item in tasks if item["category"] == "Work"]
    personal_category = [
        item for item in tasks if item["category"] == "Personal"]
    study_category = [
        item for item in tasks if item["category"] == "Study"]

    print(f"""========= Your Task Stats =========

Total Tasks: {total_tasks}

By Status:
  - Pending      : {len(pending_tasks)}
  - In Progress    : {len(progress_tasks)}
  - Completed    : {len(completed_tasks)}

By Priority:
  - High         : {len(high_priority)}
  - Normal       : {len(normal_priority)}
  - Low          : {len(low_priority)}

By Category:
  - Work         : {len(work_category)}
  - Personal     : {len(personal_category)}
  - Study        : {len(study_category)}

Overdue Tasks: 2

===================================""")


start_manager()
