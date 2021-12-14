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
from jaeger_client import Config as JaegerConfig
from opentracing_instrumentation.request_context import span_in_context, get_current_span

filePath = os.path.relpath(__file__)


class Tracing:

    def __init__(self, config=Config()):
        self.config = config
        pass

    def initialize(self):

        func = inspect.currentframe()

        try:

            logging.getLogger('').handlers = []
            logging.basicConfig(format='%(message)s', level=logging.DEBUG)

            config = JaegerConfig(
                config={
                    'sampler': {
                        'type': self.config.jaeger.samplerType,
                        'param': int(self.config.jaeger.samplerParam),
                    },
                    'local_agent': {
                        'reporting_host': self.config.jaeger.host,
                        'reporting_port': int(self.config.jaeger.port),
                    },
                    'logging': self.config.jaeger.span,
                    'reporter_batch_size': 1,
                },
                service_name=self.config.serviceName,
            )

            self.config.tracer = config.initialize_tracer()
            
            self.config.log.info(filePath, func, "Tracing [{}] initiated successfully." .format(self.config.serviceName))

            # this call also sets opentracing.tracer
            return self.config

        except Exception as err:

            self.config.log.info(filePath, func, "Tracing [{}] connection failed -> {}" .format(self.config.serviceName, err))
            raise SystemExit()




