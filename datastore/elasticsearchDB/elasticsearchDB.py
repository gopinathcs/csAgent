"""

 * Copyright (c) ConverSight.ai - All Rights Reserved

 * This material is proprietary to ConverSight.ai.

 * The methods and techniques described herein are considered trade secrets and/or confidential.

 * Reproduction or distribution, in whole or in part, is forbidden except by express written permission of ConverSight.ai.

"""

import os
import inspect
from models.config import Config
from elasticsearch import Elasticsearch

filePath = os.path.relpath(__file__)


class ElasticSearch:
    def __init__(self, config=Config()):
        self.config = config
        pass

    def initialize(self):
        self.config.es.client = self.connectES()
        return self.config

    def connectES(self):

        func = inspect.currentframe()

        try:
            self.config.es.client = Elasticsearch([{'host': self.config.es.server.split("//")[1].split(":")[0], 'port': 9200}])
            if self.config.es.client.ping():
                self.config.log.info(filePath, func, "Elasticsearch Connected Successfully -> {} " .format(self.config.es.server))
            else:
                self.config.log.info(filePath, func, "Elasticsearch Connection failed -> {} " .format(self.config.es.server))
                raise SystemExit()
        except Exception as err:
            self.config.log.error(filePath, func, "Elasticsearch Connection failed -> {} -> {} " .format(self.config.es.server, err))
            raise SystemExit()
