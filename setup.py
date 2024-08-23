import logging
import os

class Setup():
    def __init__(self):
        self.log_path = './output/botlog.log'


    def setup_log(self):
        # For cleaning the log file before a new run
        with open(self.log_path, 'w'):
            pass
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_path),
                logging.StreamHandler()
            ]
        )

        logger = logging.getLogger(__name__)
        logger.info("Log setup finished!")
        return logger


    def clean_screenshots_dir(self):
        for file in os.listdir('./output'):
            file_path = os.path.join('./output', file)
            if file.lower().endswith('.png'):
                os.remove(file_path)
