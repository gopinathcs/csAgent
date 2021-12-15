"""

 * Copyright (c) ConverSight.ai - All Rights Reserved

 * This material is proprietary to ConverSight.ai.

 * The methods and techniques described herein are considered trade secrets and/or confidential.

 * Reproduction or distribution, in whole or in part, is forbidden except by express written permission of ConverSight.ai.

"""

import os
import inspect
from models.config import Config
from datastore.mySQL.mySQL import MYSQL
from datastore.redisDB.redisDB import Redis
from datastore.arangoDB.arangoDB import Arango
from datastore.elasticsearchDB.elasticsearchDB import ElasticSearch

filePath = os.path.relpath(__file__)


class Datastore:
    def __init__(self, config=Config()):
        self.config = config
        pass

    def initialize(self):
        func = inspect.currentframe()
        # self.config = MYSQL(self.config).initialize() currently not initialized due to dynamic connections

        # Currently not needed in CS-Agent
        # self.config = Arango(self.config).initialize()
        # self.config = Redis(self.config).initialize()
        # self.config = ElasticSearch(self.config).initialize

        self.config.log.info(filePath, func, "Datastore initiated successfully.")
        return self.config
