"""

 * Copyright (c) ConverSight.ai - All Rights Reserved

 * This material is proprietary to ConverSight.ai.

 * The methods and techniques described herein are considered trade secrets and/or confidential.

 * Reproduction or distribution, in whole or in part, is forbidden except by express written permission of ConverSight.ai.

"""

import os
import inspect
from arango import ArangoClient
from arango.cursor import Cursor
from models.config import Config
from arango.database import StandardDatabase
from arango.exceptions import AQLQueryExecuteError
from opentracing_instrumentation.request_context import get_current_span, span_in_context


filePath = os.path.relpath(__file__)


class Arango:
    def __init__(self, config=Config()):
        self.config = config
        pass

    def initialize(self) -> Config():
        self.config.arango.client = self.connectArango()
        return self.config

    def connectArango(self) -> ArangoClient:

        func = inspect.currentframe()

        try:
            client = ArangoClient(self.config.arango.server)
            self.config.log.info(filePath, func, "Arango server successfully connected -> {} " .format(self.config.arango.server))
            return client
        except Exception as err:
            self.config.log.error(filePath, func, "Arango connection failed -> {} -> {} " .format(self.config.arango.server, err))
            raise SystemExit()

    def connectDB(self, database: str) -> StandardDatabase:

        func = inspect.currentframe()

        try:
            dbClient = self.config.arango.client.db(database, self.config.arango.userName, self.config.arango.password)
            self.config.log.info(filePath, func, "Arango database [{}] is connected successfully" .format(database))
            return dbClient

        except Exception as err:
            self.config.log.error(filePath, func, "Arango database [{}] connection failed -> {}" .format(database, err))
            raise SystemExit()

    def executeQuery(self, dbClient: StandardDatabase, query: str) -> (Cursor, Exception):
        with self.config.tracer.start_span('Execute_Query', child_of=get_current_span()) as span:
            with span_in_context(span):
                func = inspect.currentframe()
                try:

                    self.config.log.debug(filePath, func, "Query to execute -> {}" .format(query))
                    self.config.log.debug(filePath, func, "Database to query -> [{}]" .format(dbClient.name))

                    cursor = dbClient.aql.execute(query)

                    return cursor, None

                except AQLQueryExecuteError as err:
                    if err.error_code is not None and err.error_code == 1620:
                        self.config.log.error(filePath, func, "Schema validation failed in arango -> {}" .format(err))
                    else:
                        self.config.log.error(filePath, func, "Exception while executing query -> {}" .format(err))
                    return None, Exception(err.error_message)

                except Exception as err:
                    self.config.log.error(filePath, func, "Exception while running query -> {}" .format(err))
                    return None, err

