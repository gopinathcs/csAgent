from  mysql import MYSQL

class DataBase(object):
    def __init__(self,type):
        if type == "mysql":
            return MYSQL()
