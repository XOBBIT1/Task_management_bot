import logging


def setup_logger():
    """
    Настроить логгер для приложения.

    Эта функция конфигурирует глобальный логгер для записи логов как в файл, так и в терминал.
    Устанавливается уровень логирования `DEBUG`, что позволяет записывать все сообщения от уровня `DEBUG` и выше.
    Логи будут записываться в файл `app.log`, а также выводиться в терминал.

    Логгер использует следующий формат:
    - Время события: `%(asctime)s`
    - Уровень логирования: `%(levelname)s`
    - Сообщение: `%(message)s`

    Пример записи:
    ```
    2024-12-03 12:34:56,789 - DEBUG - Sample debug message
    ```

    Логгер записывает сообщения в файл `app.log` и выводит их на экран в реальном времени.
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),  # Write logs to a file
            logging.StreamHandler()  # Print logs to the terminal
        ]
    )
