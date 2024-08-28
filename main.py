from automation import Automation
from robocorp.tasks import task
from robocorp import workitems

@task
def main():
    item = workitems.inputs.current
    print(item)
    bot = Automation()
    bot.run('Test', 1)

if __name__ == "__main__":
    main()
