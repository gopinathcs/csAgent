"""

 * Copyright (c) ConverSight.ai - All Rights Reserved

 * This material is proprietary to ConverSight.ai.

 * The methods and techniques described herein are considered trade secrets and/or confidential.

 * Reproduction or distribution, in whole or in part, is forbidden except by express written permission of ConverSight.ai.

"""

from arango.database import StandardDatabase


class Collections:
    def __init__(self):
        self.envConfig = ""
        self.resource = ""


class Arango:
    def __init__(self):
        self.server = ""
        self.userName = ""
        self.password = ""
        self.client = None
        self.adminDBClient = StandardDatabase
        self.collections = Collections()
        self.collectionSchema = {}


class Elasticsearch:
    def __init__(self):
        self.server = ""
        self.client = None


class Redis:
    def __init__(self):
        self.server = ""
        self.port = 6379
        self.db = 0
        self.client = None


class Sentry:
    def __init__(self):
        self.dsn = ""


class Jaeger:
    def __init__(self):
        self.host = ""
        self.port = ""
        self.span = False
        self.samplerParam = "1"
        self.samplerType = "const"


class EndPoints:
    def __init__(self):
        self.apiserver = ""
        self.agentEngine = ""


class Server:
    def __init__(self):
        self.host = "localhost",
        self.port = 8082
        self.env = "dev"
        self.clusterMode = True
        self.staticToken = ""


class Config:
    def __init__(self):
        self.serviceName = "CS-Agent"
        self.env = "local"
        self.staticToken = ""
        self.datasetId = []
        self.envValues = {"log": {}, "server": {}, "redis": {}, "arango": {}, "elastic": {}, "endpoints": {}, "rabbitmq": {}, 'sentry': {}, 'jaeger': {}}
        self.server = Server()
        self.arango = Arango()
        self.es = Elasticsearch()
        self.redis = Redis()
        self.sentry = Sentry()
        self.jaeger = Jaeger()
        self.endpoints = EndPoints()
        self.queries = None
        self.templates = None
        self.log = None
        self.tracer = None


