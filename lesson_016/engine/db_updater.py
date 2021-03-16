from playhouse.db_url import connect

from .db_models import WeatherStats, db_proxy


class DatabaseUpdater:
    """ Класс для работы с БД """
    def __init__(self, db_url):
        """
        :param db_url: str Путь к бд.
                           См. https://peewee.readthedocs.io/en/latest/peewee/playhouse.html#db-url
        """
        db = connect(db_url)
        db_proxy.initialize(db)
        WeatherStats.create_table()

    def add_stats(self, stats):
        """
        Добавляет прогноз в базу данных

        :param stats: [Stats, ] список прогнозов погоды
        """
        stats = [stats, ] if not isinstance(stats, list) else stats
        for stat in stats:
            _ = (WeatherStats
                 .insert(**stat.dict)
                 .on_conflict('replace')
                 .execute())

    def get_stats(self, city, start_date, end_date=None):
        """
        Тащит из бд прогноз погоды для выбранного города за выбранный диапазон дат

        :param city: str Город
        :param start_date: datetime.date Первый день диапазона
        :param end_date: datetime.date Последний день диапазона

        :return: [WeatherStats, ] список прогнозов погоды
        """
        if end_date:
            stats = WeatherStats.select().where(
                (WeatherStats.city == city) &
                (WeatherStats.date >= start_date) &
                (WeatherStats.date <= end_date)
            )
        else:
            stats = WeatherStats.get(
                (WeatherStats.city == city) &
                (start_date == WeatherStats.date)
            )
        return stats
