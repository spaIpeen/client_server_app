"""
1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и проверить тип и содержание
соответствующих переменных. Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode
и также проверить тип и содержимое переменных.
"""

import re

development, socket, decorator = 'разработка', 'сокет', 'декоратор'
words = [development, socket, decorator]

for item in words:
    print(f'String\nType - {type(item)}\nContent - {item}\n')
    unicode_item = re.sub('.', lambda x: r'\u%04X' % ord(x.group()), item)
    print(f'Unicode String\nType - {type(unicode_item)}\nContent - {unicode_item}\n')
