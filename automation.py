from tasks import Tasks
from setup import Setup

class Automation:
    def __init__(self):
        self.setup = Setup()
        self.logger = self.setup.setup_log()
        self.automation = Tasks(self.logger)


    def run(self, search, time_period, item):
        self.setup.clean_screenshots_dir()
        automation = self.automation
        self.logger.info('Testing!')
        self.logger.info('Starting Bot')
        self.logger.info(item)
        try:
            automation.open_browser()
            automation.search(search)
            automation.iterate_news(time_period, search)
            automation.close_browser()
        except Exception as e:
            self.logger.error(e)
            automation.close_browser()
