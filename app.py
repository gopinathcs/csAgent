"""
Copyright 2021 ConverSight.ai, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import glob
import inspect
import os
import pandas as pd
import requests

__author__ = "Gopinath Jaganmohan"
__copyright__ = "Copyright 2021, ConverSight.ai"
__license__ = "Apache License 2.0"
__maintainer__ = "developer"
__status__ = "Production"
__version__ = "0.1.0"

from config.config import initialize
from service.utils.utils import HTTPReq
from datastore.mySQL.mySQL import MYSQL
from service.utils.utils import _printException, validate

import service.templates.templates as templates

filePath = os.path.relpath(__file__)


class Initialize:

    def __init__(self):
        self.config = initialize()
        self.mySQL = MYSQL(self.config)
        self.notification = templates.notification

    def getQueries(self):
        func = inspect.currentframe()
        try:
            self.config.log.info(filePath, func, "Getting list of queries from Agent Engine")
            request = "{}/dataset/queries?token={}".format(self.config.endpoints.agentEngine, self.config.staticToken)
            httpResponse, err = HTTPReq(url=request, method="GET", timeout=5, data=None, config=self.config)

            if err:
                self.notification["message"] = "Error fetching queries: {}".format(err)
                self.slackNotification()
                return

            if httpResponse.status_code != 200:
                self.notification["message"] = "Error fetching queries from Agent Engine: {}".format(httpResponse.reason)
                self.slackNotification()
                return

            response = httpResponse.json()

            if not response or response["status"] != "success":
                self.notification["message"] = "Error response from Agent Engine. Reason [{}]".format(response)
                self.slackNotification()
                return

            if not response["data"]:
                self.notification["message"] = "Empty response from Agent Engine. Reason [{}]".format(response)
                self.slackNotification()
                return

            self.config.log.info(filePath, func, "Received queries from Agent Engine")
            fileList = glob.glob(os.path.join(os.getcwd(), "*.parquet"))
            [os.remove(f) for f in fileList]

            myDB = None
            objCount = len(response["data"]) - 1
            for idx, obj in enumerate(response["data"]):
                if obj["properties"]["conn_type"] == "MySQL":

                    '''check mySQL credentials from yaml first and persist it'''
                    yamlCredentials = False

                    if not yamlCredentials:
                        self.config.log.info(filePath, func, "Checking mySQL credentials from the yaml file...")
                        if validate(self.config.dbDetails.mySQL) is not None:
                            self.config.log.info(filePath, func, "No/partial details from yaml, checking credentials from the agent response...")
                            if validate(obj["properties"]["conn_prop"]):
                                self.notification["message"] = "Aborting mySQL connection due to insufficient credentials"
                                self.slackNotification()
                                return
                            else:
                                myDB, err = self.mySQL.connect(obj["properties"]["conn_prop"])
                                if err:
                                    self.notification["message"] = "Error from mySQL connection: {}".format(err)
                                    self.slackNotification()
                                    return
                        else:
                            connDetails = {
                                "url": self.config.dbDetails.mySQL["host"] + ":" + self.config.dbDetails.mySQL["port"],
                                "username": self.config.dbDetails.mySQL["username"],
                                "password": self.config.dbDetails.mySQL["password"],
                                "database": self.config.dbDetails.mySQL["database"]}
                            myDB, err = self.mySQL.connect(connDetails)
                            if err:
                                self.notification["message"] = "Error from mySQL connection: {}".format(err)
                                self.slackNotification()
                                return
                            yamlCredentials = True

                    queriesCount = len(obj["queries"]) - 1
                    for idxq, q in enumerate(obj["queries"]):
                        stage = "close" if idx == objCount and idxq == queriesCount else "start"
                        if q["generate"] == "parquet":
                            pd.read_sql(q["query"], myDB).to_parquet(q["object_name"] + '.parquet')
                        else:
                            self.config.log.error(filePath, func, "File format [{}] not implemented".format(q["generate"]))
                            continue
                        self.uploadFiles(q["object_name"] + '.parquet', q["object_name"], stage)
                        os.remove(q["object_name"] + '.parquet')
                else:
                    self.notification["message"] = "Connector type [{}] not implemented".format(obj["properties"]["conn_type"])
                    self.slackNotification()
                    return

        except Exception as e:
            self.notification["message"] = "Error in getQueries: {}".format(_printException())
            self.slackNotification()
            return

    def uploadFiles(self, fileName, objectName, stage):
        func = inspect.currentframe()
        try:
            self.config.log.info(filePath, func, "Sending file [{}] to Agent Engine".format(fileName))
            files = {'file': open(fileName, 'rb')}
            httpResponse = requests.post("{}/dataset/upload?token={}&object_name={}&stage={}".format(self.config.endpoints.agentEngine, self.config.staticToken, objectName, stage), files=files)
            files["file"].close()
            if httpResponse.status_code != 200:
                self.notification["message"] = "Error from Agent Engine -> {}".format(httpResponse.reason)
                self.slackNotification()
                return False

            self.config.log.info(filePath, func, "File [{}] sent to Agent Engine".format(fileName))
            return True

        except Exception as e:
            self.notification["message"] = "Error uploading file to Agent Engine: {}".format(_printException())
            self.slackNotification()
            return False

    def slackNotification(self):
        func = inspect.currentframe()
        try:
            self.config.log.info(filePath, func, "{}".format(self.notification["message"]))
            request = "{}/slack/notification?token={}".format(self.config.endpoints.agentEngine, self.config.staticToken)
            httpResponse, err = HTTPReq(url=request, method="POST", timeout=5, data=self.notification, config=self.config)
            if err:
                self.config.log.error(filePath, func, "Slack Notification failed -> {}".format(err))
            elif httpResponse.status_code != 200:
                self.config.log.error(filePath, func, "Error from agent engine: Slack Notification failed: {}".format(httpResponse.reason))
                return
            self.config.log.error(filePath, func, "Slack Notification Sent !!:")
            return
        except Exception as e:
            self.config.log.error(filePath, func, "Error sending slack notification: {}".format(_printException()))
            return


if __name__ == '__main__':
    Initialize().getQueries()
