from peewee import Model, DatabaseProxy, CompositeKey, CharField, IntegerField, DateField


db_proxy = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = db_proxy

    @property
    def dict(self):
        return self.__dict__['__data__']


class WeatherStats(BaseModel):
    class Meta:
        primary_key = CompositeKey('city', 'date')

    city = CharField()
    date = DateField()
    temp_day = IntegerField()
    temp_night = IntegerField()
    descr = CharField(max_length=20)
    press = IntegerField()
    humidity = IntegerField()
    wind_speed = IntegerField()
    wind_dir = CharField(max_length=20)
