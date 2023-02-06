import logging
import datetime

logger = logging.getLogger('user_actions')

logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] "%(message)s" %(levelname)s %(name)s', datefmt='%d/%b/%Y %H:%M:%S')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)


def log_request(request):
    current_time = datetime.datetime.now().strftime('%d/%b/%Y %H:%M:%S')
    message = f"{request.method} {request.path}"
    logger.debug(f"[{current_time}] \"{message}\"")