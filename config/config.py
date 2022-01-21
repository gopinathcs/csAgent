"""

 * Copyright (c) ConverSight.ai - All Rights Reserved

 * This material is proprietary to ConverSight.ai.

 * The methods and techniques described herein are considered trade secrets and/or confidential.

 * Reproduction or distribution, in whole or in part, is forbidden except by express written permission of ConverSight.ai.

"""

import inspect
import os

import yaml

from models.config import Config
from service.logger.logger import Log
from service.templates.queries import Queries
from service.utils.utils import _printException

filePath = os.path.relpath(__file__)


def initialize() -> Config():

    func = inspect.currentframe()

    try:

        config = Config()

        configFile = open('./config/config.yml')
        configYML = yaml.load(configFile, Loader=yaml.FullLoader)

        # Initialize logger
        config.envValues['log']['level'] = os.getenv("LOG_LEVEL", configYML['LOG_LEVEL'])

        # Fetch Static Token
        config.staticToken = config.envValues['STATIC_TOKEN'] = os.getenv('STATIC_TOKEN', configYML['STATIC_TOKEN'])

        # Endpoints
        config.endpoints.agentEngine = config.envValues['endpoints']['AGENT_ENGINE'] = os.getenv("AGENT_ENGINE", configYML['AGENT_ENGINE'])

        config.dbDetails.mySQL = configYML['mySQL']

        config.log = Log(config)

        # config.log.info(filePath, func, 'Env config details has been loaded -> {} '.format(config.envValues))

        config.queries = Queries()

        return config

    except Exception as err:
        _printException()
        raise SystemExit()
