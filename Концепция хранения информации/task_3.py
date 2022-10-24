"""
3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.
Важно: решение должно быть универсальным, т.е. не зависеть от того, какие конкретно слова мы исследуем.
"""

attribute_word, class_word, function_word, type_word = 'attribute', 'класс', 'функция', 'type'
words = [attribute_word, class_word, function_word, type_word]

for word in words:
    try:
        word = bytes(word, 'ascii')
    except UnicodeEncodeError:
        print(word)
