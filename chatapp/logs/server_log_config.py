import logging.handlers
import datetime

logger = logging.getLogger('chatapp.server')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - server.py - %(message)s ")

file_hand = logging.handlers.TimedRotatingFileHandler(f'{datetime.date.today()}-chatapp.server.log',
                                                      when='D', interval=1, encoding='utf-8')
console_hand = logging.StreamHandler()
file_hand.setFormatter(formatter)
console_hand.setFormatter(formatter)

logger.addHandler(file_hand)
logger.addHandler(console_hand)

if __name__ == '__main__':
    logger.debug('Тестовый запуск логирования сервера')
