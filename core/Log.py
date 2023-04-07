import logging
import coloredlogs

class DebugFilter(logging.Filter):

    def __init__(self, name=''):
        super(DebugFilter, self).__init__(name)

        self.last_log = None

    def filter(self, record):

        s = record.getMessage()

        if "INFO" in s:

            if s == self.last_log:
                return False
            else:
                self.last_log = s
                return True
        
        else:

            self.last_log = None
            return True

class log:
    
    def start(self):
        my_filter = DebugFilter()
        self.logger = logging.getLogger('')
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.console = logging.StreamHandler()
        self.console.setLevel(logging.INFO)
        self.console.setFormatter(self.formatter)
        self.console.addFilter(my_filter)
        self.logger.addHandler(self.console)
        coloredlogs.install(level='INFO', logger=self.logger)
        self.logger.info("Logger initialized.")


    def info(self, message):
        self.logger = logging.getLogger('')
        self.logger.info(message)

    def error(self, message):
        self.logger = logging.getLogger('')
        self.logger.error(message)

    def debug(self, message):
        self.logger = logging.getLogger('')
        self.logger.debug(message)

    def warning(self, message):
        self.logger = logging.getLogger('')
        self.logger.warning(message)

    def critical(self, message):
        self.logger = logging.getLogger('')
        self.logger.critical(message)
