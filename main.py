from automation import Automation
from robocorp.tasks import task
from robocorp import workitems

@task
def main():
    item = workitems.Inputs
    print(item)
    bot = Automation()
    bot.run('Test', 1, item)

if __name__ == "__main__":
    main()
