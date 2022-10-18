"""
5. Написать код, который выполняет пинг веб-ресурсов yandex.ru, youtube.com и преобразовывает
результат из байтовового типа данных в строковый без ошибок для любой кодировки операционной системы.
"""

import subprocess
import chardet


def ping(host):
    sub_ping = subprocess.Popen(['ping', host], stdout=subprocess.PIPE)

    for line in sub_ping.stdout:
        code = chardet.detect(line)
        print(line.decode(code['encoding']))


ping('yandex.ru')
ping('youtube.com')
