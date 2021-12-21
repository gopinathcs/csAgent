"""

 * Copyright (c) ConverSight.ai - All Rights Reserved

 * This material is proprietary to ConverSight.ai.

 * The methods and techniques described herein are considered trade secrets and/or confidential.

 * Reproduction or distribution, in whole or in part, is forbidden except by express written permission of ConverSight.ai.

"""


class EndPoints:
    def __init__(self):
        self.agentEngine = ""


class Config:
    def __init__(self):
        self.serviceName = "CS-Agent"
        self.staticToken = ""
        self.envValues = {"log": {}, "endpoints": {}}
        self.endpoints = EndPoints()
        self.queries = None
        self.templates = None
        self.log = None

