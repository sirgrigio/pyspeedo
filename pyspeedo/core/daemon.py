import logging
import time
from playhouse.db_url import connect
from pyspeedtest import SpeedTest
from . import utils
from .models import db_proxy as db
from .models import SpeedtestModel

log = logging.getLogger(__name__)


class SpeedoDaemon(object):

    def __init__(self, host, interval, databaseUrl, server):
        self.host = host
        self.interval = interval
        self.databaseUrl = databaseUrl
        self.server = server

    def run(self):
        log.debug('Starting deamon: {0}'.format(
            dict(host=self.host,
                 server=self.server,
                 interval=self.interval,
                 databaseUrl=self.databaseUrl)))
        st = SpeedTest(host=self.server)
        while(True):
            log.debug('Starting speed test')
            startTime = utils.current_time_millisec()
            stats = dict(server=st.host,
                         ping=st.ping(),
                         download=st.download(),
                         upload=st.upload())
            endTime = utils.current_time_millisec()
            log.debug('Speed test completed: {0}'.format(stats))
            db.initialize(connect(self.databaseUrl))
            db.create_tables([SpeedtestModel], safe=True)
            SpeedtestModel.create(host=self.host,
                                  startTime=startTime,
                                  endTime=endTime,
                                  **stats)
            db.close()
            log.debug('Database updated')
            log.debug('Going to sleep for {:d} seconds'.format(self.interval))
            time.sleep(self.interval)