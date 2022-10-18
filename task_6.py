"""
Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
Далее забыть о том, что мы сами только что создали этот файл и исходить из того, что перед нами файл в неизвестной
кодировке. Задача: открыть этот файл БЕЗ ОШИБОК вне зависимости от того, в какой кодировке он был создан.
"""
import chardet as chardet

with open('test_file.txt', 'rb') as f:
    line = f.read()
    code = chardet.detect(line)
    print(line.decode(code['encoding']))