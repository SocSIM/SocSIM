import logging

log = logging

def initialize_logging():
    #creation of logger
    rootLogger = logging.getLogger()
    rootLogger.name = 'SOC'
    rootLogger.setLevel(logging.INFO)
    
    #creation of formatter
    logFormatter = logging.Formatter("%(asctime)s - %(name)-7.7s- %(levelname)-9.9s- %(message)s")
    
    #console handler
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
    
    #console handler
    fileHandler = logging.FileHandler("socsim.log")
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    logging.info("Logging Initialization")

if __name__ == 'common':
    initialize_logging()