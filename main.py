from automation import Automation
from robocorp.tasks import task

@task
def main():
    bot = Automation()
    bot.run('Test', 1)

main()
