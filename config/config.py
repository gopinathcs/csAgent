"""

 * Copyright (c) ConverSight.ai - All Rights Reserved

 * This material is proprietary to ConverSight.ai.

 * The methods and techniques described herein are considered trade secrets and/or confidential.

 * Reproduction or distribution, in whole or in part, is forbidden except by express written permission of ConverSight.ai.

"""

import os
import yaml
import inspect
from models.config import Config
from tracing.tracing import Tracing
from service.logger.logger import Log
from datastore.datastore import Datastore
from service.templates.queries import Queries
from service.utils.utils import _printException


filePath = os.path.relpath(__file__)


def initialize() -> Config():

    func = inspect.currentframe()

    try:

        config = Config()

        configFile = open('./config/config.yml')
        configYML = yaml.load(configFile, Loader=yaml.FullLoader)

        # Env
        config.env = config.envValues['env'] = os.getenv("ENV", configYML['ENV'])

        # Initialize logger
        config.envValues['log']['level'] = os.getenv("LOG_LEVEL", configYML['LOG_LEVEL'])

        # Fetch Server Details
        config.server.host = config.envValues['server']['HOST'] = os.getenv("SERVER_HOST", configYML['SERVER_HOST'])
        config.server.port = config.envValues['server']['PORT'] = os.getenv("SERVER_PORT", configYML['SERVER_PORT'])
        config.server.envValues = config.envValues['server']['ENV'] = os.getenv("ENV", configYML['ENV'])
        config.staticToken = config.envValues['STATIC_TOKEN'] = os.getenv('STATIC_TOKEN', configYML['STATIC_TOKEN'])
        config.datasetId = config.envValues['DATASET_ID'] = os.getenv('DATASET_ID', configYML['DATASET_ID'])

        # Fetch Arango Server Details
        config.arango.server = config.envValues['arango']['server'] = os.getenv("ARANGO_SERVER", configYML['ARANGO_SERVER'])
        config.arango.adminDB = config.envValues['arango']['adminDB'] = os.getenv("ARANGO_DB_AUTH", configYML['ARANGO_DB_AUTH'])
        config.arango.userName = config.envValues['arango']['username'] = os.getenv("ARANGO_USER", configYML['ARANGO_USER'])
        config.arango.password = config.envValues['arango']['password'] = os.getenv("ARANGO_PASSWORD", configYML['ARANGO_PASSWORD'])

        # Fetch Redis Details
        config.redis.client = config.envValues['redis']['REDIS_SERVER'] = os.getenv("REDIS_SERVER", configYML['REDIS_SERVER'])
        config.redis.port = config.envValues['redis']['PORT'] = os.getenv("REDIS_PORT", configYML['REDIS_PORT'])
        config.redis.db = config.envValues['redis']['REDIS_DB'] = os.getenv("REDIS_DB", configYML['REDIS_DB'])

        # Fetch Elastic Server Details
        config.es.server = config.envValues['elastic']['ES_SERVER'] = os.getenv("ES_SERVER", configYML['ES_SERVER'])

        # Fetch Jaeger Details
        config.jaeger.host = config.envValues['jaeger']['HOST'] = os.getenv("JAEGER_AGENT_HOST", configYML['JAEGER_AGENT_HOST'])
        config.jaeger.port = config.envValues['server']['PORT'] = os.getenv("JAEGER_AGENT_PORT", configYML['JAEGER_AGENT_PORT'])
        config.jaeger.span = config.envValues['server']['LOG_SPAN'] = os.getenv("JAEGER_LOG_SPANS", configYML['JAEGER_LOG_SPANS'])
        config.jaeger.samplerParam = config.envValues['server']['SAMPLER_PARAM'] = os.getenv("JAEGER_SAMPLER_PARAM", configYML['JAEGER_SAMPLER_PARAM'])
        config.jaeger.samplerType = config.envValues['server']['SAMPLER_TYPE'] = os.getenv("JAEGER_SAMPLER_TYPE", configYML['JAEGER_SAMPLER_TYPE'])

        # Endpoints
        config.endpoints.agentEngine = config.envValues['endpoints']['AGENT_ENGINE'] = os.getenv("AGENT_ENGINE", configYML['AGENT_ENGINE'])

        # Sentry Config
        config.sentry.dsn = config.envValues['sentry']['SENTRY_DSN'] = os.getenv("SENTRY_DSN", configYML['SENTRY_DSN'])

        config.log = Log(config)

        config.log.info(filePath, func, 'Env config details has been loaded -> {} '.format(config.envValues))

        config.queries = Queries()

        config = Datastore(config).initialize()

        config = Tracing(config).initialize()
        
        return config

    except Exception as err:
        _printException()
        raise SystemExit()
