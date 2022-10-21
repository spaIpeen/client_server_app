"""
2. Каждое из слов «class», «function», «method» записать в байтовом типе. Сделать это необходимо в автоматическом,
а не ручном режиме, с помощью добавления литеры b к текстовому значению, (т.е. ни в коем случае не используя методы
encode, decode или функцию bytes) и определить тип, содержимое и длину соответствующих переменных.
"""

class_word, function_word, method_word = 'class', 'function', 'method'
words = [class_word, function_word, method_word]

for word in words:
    word = eval(f"b'{word}'")
    print(f'Type - {type(word)}\nContent - {word}\nLength - {len(word)}\n')
