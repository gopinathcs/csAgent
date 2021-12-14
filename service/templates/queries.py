"""

 * Copyright (c) ConverSight.ai - All Rights Reserved

 * This material is proprietary to ConverSight.ai.

 * The methods and techniques described herein are considered trade secrets and/or confidential.

 * Reproduction or distribution, in whole or in part, is forbidden except by express written permission of ConverSight.ai.

"""


class Queries:
    def __init__(self):
        self.insert = "INSERT {} IN {}"
        self.insertNewReturn = "INSERT {} INTO {} RETURN UNSET(NEW, '_key', '_rev', '_id')"
        self.get = "FOR doc IN {} FILTER doc.{} == '{}' RETURN UNSET(doc, '_key', '_rev', '_id')"
        self.getCustom = "FOR doc IN {} FILTER {} RETURN UNSET(doc, '_key', '_rev', '_id')"
        self.getCustomSort = "FOR doc IN {} FILTER {} SORT doc.{} DESC RETURN UNSET(doc, '_key', '_rev', '_id')"
        self.update = "FOR doc IN {} FILTER doc.{} == '{}' UPDATE doc WITH {} IN {}"
        self.updateNewReturn = "FOR doc IN {} FILTER doc.{} == '{}' UPDATE doc WITH {} IN {} RETURN UNSET(NEW, '_key', '_rev', '_id')"
        self.updateALL = "FOR doc IN {} FILTER doc.{} == '{}' UPDATE doc WITH {} IN {} OPTIONS {mergeObjects: false} RETURN doc"
        self.updateReturn = "FOR doc IN {} FILTER doc.{} == '{}' UPDATE doc WITH {} IN {} RETURN doc"
        self.updateALLReturn = "FOR doc IN {} FILTER doc.{} == '{}' UPDATE doc WITH {} IN {} OPTIONS {mergeObjects: false} RETURN doc"
        self.updateCustom = "FOR doc IN {} FILTER {} UPDATE doc WITH {} IN {}"
        self.updateCustomNewReturn = "FOR doc IN {} FILTER {} UPDATE doc WITH {} IN {} RETURN UNSET(NEW, '_key', '_rev', '_id')"
        self.delete = "FOR doc IN {} FILTER doc.{} == '{}' REMOVE doc IN {}"
        self.deleteCustom = "FOR doc IN {} FILTER {} REMOVE doc IN {}"
        self.deleteCustomReturn = "FOR doc IN {} FILTER {} REMOVE doc IN {} RETURN doc"
        self.deleteReturn = "FOR doc IN {} FILTER doc.{} == '{}' REMOVE doc IN {} RETURN doc"
        self.deleteReturnOld = "FOR doc IN {} FILTER doc.{} == '{}' REMOVE doc IN {} RETURN UNSET(OLD, '_key', '_rev', '_id')"
        self.bulkDelete = "FOR doc IN {} FILTER doc.{} IN {} REMOVE doc IN {}"
        self.getALL = "FOR doc IN {} RETURN UNSET(doc, '_key', '_rev', '_id')"
        self.getIn = "FOR doc IN {} FILTER doc.{} IN {} RETURN UNSET(doc, '_key', '_rev', '_id')"
        self.getCustomReturn = "FOR doc IN {} FILTER {} RETURN {}"
        self.upsert = "UPSERT {{}:'{}'} INSERT {} UPDATE {{}} in {}"
