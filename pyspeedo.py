import logging
import time
from playhouse.db_url import connect
from pyspeedtest import SpeedTest
from models import db_proxy as db
from models import SpeedtestModel

log = logging.getLogger('pyspeedo')


def current_time_millisec():
    return int(round(time.time() * 10**3))


def daemon(host, interval, databaseUrl, server):
    log.debug('Starting deamon: {0}'.format(
        dict(host=host,
             server=server,
             interval=interval,
             databaseUrl=databaseUrl)))
    st = SpeedTest(host=server)
    while(True):
        log.debug('Starting speed test')
        startTime = current_time_millisec()
        stats = dict(server=st.host,
                     ping=st.ping(),
                     download=st.download(),
                     upload=st.upload())
        endTime = current_time_millisec()
        log.debug('Speed test completed: {0}'.format(stats))
        db.initialize(connect(databaseUrl))
        db.create_tables([SpeedtestModel], safe=True)
        SpeedtestModel.create(host=host, startTime=startTime, endTime=endTime, **stats)
        db.close()
        log.debug('Database updated')
        log.debug('Going to sleep for {:d} seconds'.format(interval))
        time.sleep(interval)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    daemon('ciccio', 1, 'sqlite:////tmp/ciccio.db', None)
