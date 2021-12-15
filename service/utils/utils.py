"""

 * Copyright (c) ConverSight.ai - All Rights Reserved

 * This material is proprietary to ConverSight.ai.

 * The methods and techniques described herein are considered trade secrets and/or confidential.

 * Reproduction or distribution, in whole or in part, is forbidden except by express written permission of ConverSight.ai.

"""
import linecache
import os
import inspect
import sys

import requests
import shortuuid
import datetime as dt
from typing import Any
from models.config import Config


filePath = os.path.relpath(__file__)


# getCurrentTime
def getCurrentTime() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')


# getUUID
def getUUID(length: int = None) -> str:
    if length:
        return shortuuid.ShortUUID(list(str(int((dt.datetime.now() - dt.datetime.utcfromtimestamp(0)).total_seconds() * 1000)) + "abcdefghijkmnopqrstuvwxyz")).random(length=length)
    else:
        return shortuuid.ShortUUID(list(str(int((dt.datetime.now() - dt.datetime.utcfromtimestamp(0)).total_seconds() * 1000)) + "abcdefghijkmnopqrstuvwxyz")).uuid()


# HTTPReq
def HTTPReq(url, method, timeout=None, data=None, config=Config()) -> (Any, Exception):
    func = inspect.currentframe()
    try:

        if method == "POST":
            return (requests.post(url=url, json=data, timeout=timeout) if timeout is not None else requests.post(url=url, json=data)), None
        elif method == "PUT":
            return (requests.put(url=url, json=data, timeout=timeout) if timeout is not None else requests.put(url=url, json=data)), None
        elif method == "GET":
            return (requests.get(url=url, json=data, timeout=timeout) if timeout is not None else requests.get(url=url, json=data)), None
        elif method == "DELETE":
            return (requests.delete(url=url, json=data, timeout=timeout) if timeout is not None else requests.delete(url=url, json=data)), None
        else:
            return None, Exception("invalidMethod")

    except requests.exceptions.ConnectTimeout as err:
        config.log.error(filePath, func, "Timeout [{}] reached -> {}".format(timeout, err))
        return None, Exception("timeoutError")

    except Exception as err:
        config.log.error(filePath, func, "Exception while doing HTTP request -> {}".format(err))
        return None, err

def _printException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineNo = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineNo, f.f_globals)
    resp = 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineNo, line.strip(), exc_obj)
    print(resp)
    return resp