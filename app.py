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
from service.utils.utils import _printException

filePath = os.path.relpath(__file__)


class Initialize:

    def __init__(self):
        self.config = initialize()
        self.mySQL = MYSQL()

    # def runServer(self):
    #     uvicorn.run(app, port=int(self.config.server.port), host=self.config.server.host, debug=True, log_config=None)

    def getQueries(self, datasetId=None):
        func = inspect.currentframe()
        try:
            datasetId = datasetId if datasetId else self.config.datasetId
            if not datasetId:
                self.config.log.error(filePath, func, "No dataset Id to get queries, skipping further process")
                return

            for dIdx, dId in enumerate(datasetId):
                request = "{}/dataset/queries/{}?token={}".format(self.config.endpoints.agentEngine, dId, self.config.staticToken)
                httpResponse, err = HTTPReq(url=request, method="GET", data=None, config=self.config)

                if err is not None:
                    self.config.log.error(filePath, func, "Error Getting queries -> {}".format(err))
                    return

                if httpResponse.status_code != 200:
                    self.config.log.error(filePath, func, "Error from Agent-Engine -> {}".format(httpResponse))
                    return

                response = httpResponse.json()

                if not response or response["status"] != "success":
                    self.config.log.error(filePath, func, "Failed response from Agent-Engine -> {}".format(response))
                    return

                if not response["data"]:
                    self.config.log.error(filePath, func, "Empty response from Agent-Engine -> {}".format(response))
                    return

                self.config.log.info(filePath, func, "Response from Agent-Engine -> {}".format(response))
                fileList = glob.glob(os.path.join(os.getcwd(), "*.parquet"))
                [os.remove(f) for f in fileList]

                objCount = len(response["data"]) - 1
                for idx, obj in enumerate(response["data"]):
                    if obj["properties"]["conn_type"] == "MySQL":
                        myDB = self.mySQL.connect(obj["properties"]["conn_prop"])
                        queriesCount = len(obj["queries"]) - 1
                        for idxq, q in enumerate(obj["queries"]):
                            stage = "close" if idx == objCount and idxq == queriesCount else "start"
                            if q["generate"] == "parquet":
                                pd.read_sql(q["query"], myDB).to_parquet(q["object_name"] + '.parquet')
                                print(pd.read_sql(q["query"], myDB))
                            else:
                                self.config.log.error(filePath, func, "File format [{}] not implemented".format(q["generate"]))
                                continue
                            self.uploadFiles(q["object_name"] + '.parquet', q["object_name"], stage, dId)
                            os.remove(q["object_name"] + '.parquet')
                    else:
                        self.config.log.error(filePath, func, "Connector type [{}] not implemented".format(obj["properties"]["conn_type"]))
        except Exception as e:
            _printException()
            self.config.log.error(filePath, func, "Error in getQueries -> {}".format(e))

    def uploadFiles(self, fileName, objectName, stage, datasetId):
        func = inspect.currentframe()
        try:
            files = {'file': open(fileName, 'rb')}
            httpResponse = requests.post("{}/dataset/upload/?token={}&object_name={}&stage={}&dataset_id={}".format(self.config.endpoints.agentEngine, self.config.staticToken, objectName, stage, datasetId), files=files)
            if httpResponse.status_code != 200:
                self.config.log.error(filePath, func, "Error from Agent-Engine -> {}".format(httpResponse))
                return False

            self.config.log.info(filePath, func, "File [{}] sent to Agent-Engine".format(fileName))
            return True

        except Exception as e:
            _printException()
            self.config.log.error(filePath, func, "Error in uploadFiles -> {}".format(e))
            return False


if __name__ == '__main__':
    Initialize().getQueries()
