import logging
import sys

# Настройки логгера

logger = logging.getLogger("LOG")
logger.setLevel(logging.INFO)

# Настройки обработчика потока
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s %(message)s", "%H:%M:%S")

# Применение настроек
handler.setFormatter(formatter)
logger.addHandler(handler)


def logged_request_response(function):
    """Декоратор, логирующий request и response"""

    def wrapper(*args, **kwargs):
        res = function(*args, **kwargs)

        logger.info("")

        logger.info("--- REQUEST ---")
        logger.info(f"method: {res.request.method}")
        logger.info(f"url: {res.request.url}")
        logger.info(f"headers: {res.request.headers}")
        logger.info(f"body: {res.request.body}")

        logger.info("--- RESPONSE ---")
        logger.info(f"status code: {res.status_code}")
        logger.info(f"headers: {res.headers}")
        logger.info(f"body: {res.text}")

        return res

    return wrapper
