"""

 * Copyright (c) ConverSight.ai - All Rights Reserved

 * This material is proprietary to ConverSight.ai.

 * The methods and techniques described herein are considered trade secrets and/or confidential.

 * Reproduction or distribution, in whole or in part, is forbidden except by express written permission of ConverSight.ai.

"""

import os
import redis
import inspect
from models.config import Config


filePath = os.path.relpath(__file__)


class Redis:
    def __init__(self, config=Config()):
        self.config = config
        pass

    def initialize(self):
        self.config.redis.client = self.connectRedis()
        return self.config

    def connectRedis(self):

        func = inspect.currentframe()

        try:
            self.config.redis.client = redis.StrictRedis(host=self.config.redis.server, port=self.config.redis.port, db=int(self.config.redis.db))
            self.config.log.info(filePath, func, "Redis connected successfully -> {} " .format(self.config.redis.server))
        except Exception as err:
            self.config.log.error(filePath, func, "Redis connection failed -> {} -> {} " .format(self.config.redis.server, err))
            raise SystemExit()
