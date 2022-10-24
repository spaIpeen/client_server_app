"""
4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в
байтовое и выполнить обратное преобразование (используя методы encode и decode)..
"""

development_word, administration_word, protocol_word, standard_word = 'разработка', 'администрирование',\
                                                                      'protocol', 'standard'
words = [development_word, administration_word, protocol_word, standard_word]

for word in words:
    bytes_word = word.encode("utf-8")
    str_word = bytes_word.decode("utf-8")
    print(f'Bytes - {bytes_word}\nString - {str_word}\n')
