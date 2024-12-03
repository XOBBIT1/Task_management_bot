from pyrogram import filters


def dynamic_data_filter(data):
    """
    Создает фильтр, который проверяет, равны ли данные в запросе и фильтре.

    Аргументы:
        data (any): Данные, которые будут использованы для фильтрации.

    Возвращает:
        Функцию фильтрации, которая сравнивает `query.data` с переданным значением `data`.
    """
    async def func(flt, _, query):
        return flt.data == query.data

    # "data" kwarg is accessed with "flt.data" above
    return filters.create(func, data=data)


def dynamic_data_filter_startswith(prefix):
    """
   Создает фильтр, который проверяет, начинается ли `query.data` с заданного префикса.

   Аргументы:
       prefix (str): Префикс, с которым нужно сравнить начало строки `query.data`.

   Возвращает:
       Функцию фильтрации, которая проверяет, начинается ли `query.data` с переданного префикса.
   """
    async def func(flt, _, query):
        # Проверяем, начинается ли `query.data` с переданного префикса
        return query.data.startswith(flt.prefix)

    # Передаем `prefix` как аргумент в создаваемый фильтр
    return filters.create(func, prefix=prefix)
