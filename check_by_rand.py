import random
from time import time

# генерируем коды длины n
def genbin(n, a, bs=''):
    if len(bs) == n:
        a.append(bs)
    else:
        genbin(n, a, bs + '0')
        genbin(n, a, bs + '1')
    return a

N = 7 # мощность алфавита источника
T = 3 # максимальная длина кодовых слов
minus = 0 # кол-во не префиксных
total = 100000 # общее число попыток

bin_list = [] # список рассматриваемых кодовых слов
for i in range(1, T + 1):
    bin_list.extend(genbin(i, []))

# обрезаем список с начала
for i in range(T - 1, 0, -1):
    if 2**T - 2**i < N - 1:
        if i == T - 1:
            bin_list[:2] = ['','']
        else:
            for j in range(sum([2**k for k in range(1, T - i)]), sum([2**k for k in range(1, T - i + 1)])):
                bin_list[j] = ''
bin_list = list(filter(lambda q: q != '', bin_list))

# вычисление вероятности, средней длины, времени
t1 = time()
code_len_temp = 0
for s in range(total):
    flag = True
    # случайно выбираем N кодов
    c = random.sample(bin_list, N)
    # проверяем на префиксность
    for i in range(N - 1):
        for j in range(i + 1, N):
            m = len(min(c[i], c[j], key=len))
            if c[i][:m] == c[j][:m]:
                flag = False
                break
        if (flag == False):
            minus += 1
            break
    else:
        code_len_temp += sum([len(i) for i in c]) / len(c)
t2 = time()

print('N =', N, 'T =', T)
print('P =', 1 - minus / total)
print('L =', code_len_temp / (total - minus))
print("время:", t2 - t1)
