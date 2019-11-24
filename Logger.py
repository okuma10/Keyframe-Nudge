import logging

class Log:
    def __init__(self,file):
        self.file = file
        self.logger = logging.getLogger(__file__)
        self.logger.setLevel(logging.INFO)
        self.file_handler = logging.FileHandler(self.file,encoding='utf-8')
        self.formatter = logging.Formatter('%(levelname)s: %(name)s:\n\t%(message)s')
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)
        self.handlers = []

    def setLevel(self,level=int):
        if level   == 0:
            self.formatter = logging.Formatter('%(levelname)s: %(name)s:\n%(message)s')
        elif level == 1:
            self.formatter = logging.Formatter('\tl1 %(message)s')
        elif level == 2:
            self.formatter = logging.Formatter('\t\tl2 %(message)s')
        elif level == 3:
            self.formatter = logging.Formatter('\t\t\tl3 %(message)s')
        elif level == 4:
            self.formatter = logging.Formatter('\t\t\tl4 %(message)s')

        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

    def print(self,message):
        self.logger.info(message)

    def debug(self):
        self.logger.debug('debug')

    def clearFile(self):
         open(self.file,'w').close()

    def addHandler(self,file):
        self.file_handler = logging.FileHandler(file , encoding='utf-8')
        self.logger.addHandler(self.file_handler)
        self.handlers.append(self.file_handler)
        self.file = file

    def removeHandler(self):
        self.file_handler.close()
        self.logger.removeHandler(self.file_handler)

    def removeAllHandlers(self):
        for handler in self.handlers:
            handler.close()
            self.logger.removeHandler(handler)
