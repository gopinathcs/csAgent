"""

 * Copyright (c) ConverSight.ai - All Rights Reserved

 * This material is proprietary to ConverSight.ai.

 * The methods and techniques described herein are considered trade secrets and/or confidential.

 * Reproduction or distribution, in whole or in part, is forbidden except by express written permission of ConverSight.ai.

"""

import os
import logging
import inspect
from models.config import Config
from pylogrus import TextFormatter, PyLogrus

filePath = os.path.relpath(__file__)


class Log:

    def __init__(self, config=Config()):
        self.config = config
        self.log = self.initialize()
        pass

    def initialize(self) -> Config():

        func = inspect.currentframe()

        try:

            logging.setLoggerClass(PyLogrus)

            level = logging.getLevelName(self.config.envValues['log']['level'])

            logger = logging.getLogger(__name__)
            logger.setLevel(level)

            self.config.log = logger

            ch = logging.StreamHandler()
            ch.setLevel(level)

            formatter = TextFormatter(fmt='[%(asctime)s] [%(levelname)s] %(message)s', datefmt='Z', colorize=True)
            ch.setFormatter(formatter)

            logger.addHandler(ch)
            logger.propagate = False

            self.log = logger

            return logger

        except Exception as err:
            print("[{}][{}][{}] Exception while initializing logger -> {} ".format(filePath, func.f_code.co_name, func.f_lineno, err))
            raise SystemExit()

    def info(self, processFilePath: str, frame, message: str):
        self.log.info("[{}][{}][{}] {}".format(processFilePath, frame.f_code.co_name, frame.f_lineno, message))
        
    def debug(self, processFilePath: str, frame, message: str):
        self.log.debug("[{}][{}][{}] {}".format(processFilePath, frame.f_code.co_name, frame.f_lineno, message))

    def error(self, processFilePath: str, frame, message: str):
        self.log.error("[{}][{}][{}] {}".format(processFilePath, frame.f_code.co_name, frame.f_lineno, message))
