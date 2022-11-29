import platform
from subprocess import Popen, PIPE
from tabulate import tabulate


def host_ping(address):
    url_list = []
    for url in address:
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        # Popen не проглатывает объект типа IPv4Address
        args = ['ping', param, '1', url]
        reply = Popen(args, stdout=PIPE)
        code = reply.wait()
        if code == 0:
            url_list.append(['Узел доступен', url])
        else:
            url_list.append(['Узел недоступен', url])
    host_range_ping_tab([{i[0]: i[1]} for i in url_list])


def host_range_ping():
    while True:
        first_address = input('Введите первый адрес: ')
        num = int(input('Сколько адресов необходимо проверить: '))
        last_oct = int(first_address.split('.')[3])
        if last_oct + num > 256:
            print('Необходим диапазон одного октета.')
            break
        else:
            hosts = (['.'.join(first_address.split('.')[:3]) + '.' + str(last_oct + i) for i in range(num)])
            host_ping(hosts)


def host_range_ping_tab(dicts_list):
    print(tabulate(dicts_list, headers='keys'))


if __name__ == '__main__':
    host_range_ping()
