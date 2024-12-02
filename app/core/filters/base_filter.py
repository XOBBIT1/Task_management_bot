from pyrogram import filters


def dynamic_data_filter(data):
    async def func(flt, _, query):
        return flt.data == query.data

    # "data" kwarg is accessed with "flt.data" above
    return filters.create(func, data=data)


def dynamic_data_filter_startswith(prefix):
    async def func(flt, _, query):
        # Проверяем, начинается ли `query.data` с переданного префикса
        return query.data.startswith(flt.prefix)

    # Передаем `prefix` как аргумент в создаваемый фильтр
    return filters.create(func, prefix=prefix)
