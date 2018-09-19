import sqlite3
import logging


class Db(object):
    def __init__(self, db_name):
        self.logger = logging.getLogger()
        self.logger.debug("Opening database: " + db_name)
        self.conn = sqlite3.connect(db_name)
