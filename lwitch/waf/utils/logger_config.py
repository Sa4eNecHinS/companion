import logging
from pathlib import Path


def setup_file_logger(name: str):
    log_dir = Path("logs")  # для корректный путей в разных ОС
    log_dir.mkdir(exist_ok=True)  # exist_ok - не выдавать ошибку если есть папка

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # handlers - список текущих обработчиков (файлы, консоль и т.п)
    # чтобы избежать дублирования обработчикво
    if not logger.handlers:
        formatter = logging.Formatter(
            "[%(asctime)s] %(name)s %(levelname)s: %(message)s",
            datefmt="%H:%M:%S",
        )

        # FileHandler - отправляет логи в файл
        file_handler = logging.FileHandler(log_dir / "robot.log", encoding="utf-8")
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger
