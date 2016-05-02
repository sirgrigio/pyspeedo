from peewee import *

db_proxy = Proxy()


class BaseModel(Model):
    class Meta:
        database = db_proxy


class SpeedtestModel(BaseModel):
    host = CharField()
    startTime = BigIntegerField()
    endTime = BigIntegerField()
    server = CharField()
    ping = IntegerField()
    download = IntegerField()
    upload = IntegerField()

    class Meta:
        indexes = ((('host', 'timestamp'), True))
