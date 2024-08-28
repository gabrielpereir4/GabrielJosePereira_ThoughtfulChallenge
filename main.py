from automation import Automation
from robocorp.tasks import task
from robocorp import workitems
@task
def main():
    item = workitems.inputs.current
    print(item.payload)
    bot = Automation()
    bot.run('Test', 1, item.payload)

if __name__ == "__main__":
    main()
