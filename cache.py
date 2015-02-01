""""

DBCache Class

Definition: Creates class to operate on a persistent cache for JSON Messages

"""
import sys
import logging
import time
import json
from tinydb import TinyDB, where
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware

log = logging.getLogger("web_poll")

#######################################################
#
# Persistent Cache Operations
#
######################################################
class Singleton(object):
    """
    Singleton base class for creating singleton classes
    """

    __single = None

    def __new__(classtype, *args, **kwargs):
        #
        # Check to see if __single already exists already for this class
        #
        if classtype !=  type(classtype.__single):
            classtype.__single = object.__new__(classtype, *args, **kwargs)
        return classtype.__single

    def __init__(self,name=None):
        self.name = name

    def display(self):
        print self.name, id(self), type(self)

#####################################################
#
# DBCache
#
#####################################################
class DBCache(Singleton):

    _status = False

    def __init__(self,dbFile= None):
        if not self._status:
            self._status = True
            Singleton.__init__(self,"DBache")

            if (dbFile == None):
                dbFile = 'db_cache.json'
            
            self._dbHandle = TinyDB(dbFile)
            self._tableHandle = self._dbHandle.table("questions_table")
            self._dbfile = dbFile
            self._dbHandle.purge()
            print "INSERT DB"
            quizzes = json.loads(open('quizzes/sample_qns').read())
            self._tableHandle.insert(quizzes)


    @property
    def dbHandle(self):
        return self._dbHandle

    @property
    def tableHandle(self):
        return self._tableHandle

    @property
    def dbFile(self):
        return self._dbFile



    
