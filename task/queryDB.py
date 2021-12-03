

def getData(query,data,filePath):
    pass

class QueryDB():
    def __init__(self,queries,dbType):
        self.queries = queries
        self.dbType = dbType
    def run(self,connectionString):
       for query in self.queries:
           Database(self.dbType).connect(connectionString)

