import math


# генерируем коды длины max_len
def gen_bin(max_len: int, codes: list[str], bin_str: str = '') -> list[str]:
    if len(bin_str) == max_len: # проверка на длину кодового слова на заданном слое
        codes.append(bin_str) # добавление кодового слова в список
    else:
        gen_bin(max_len, codes, bin_str + '0') # генерация левого дочернего кодового слова
        gen_bin(max_len, codes, bin_str + '1') # генерация правого дочернего кодового слова
    return codes


# удаление дочерних элементов
def del_post(i_elem: int, i_layer: int, left_end: int, bin_list_new: list[str], T: int):
    bin_list_new[i_elem] = '' # вычеркиваем текущий элемент
    if i_layer == T: # проверка на последний слой
        return
    i_elem_child = left_end + 2 ** i_layer + 2 * (i_elem - left_end) # левый дочерний элемент

    del_post(i_elem_child, i_layer + 1, left_end + 2 ** i_layer, bin_list_new, T) # вычеркивание дочерних элементов левого дочернего элемента
    del_post(i_elem_child + 1, i_layer + 1, left_end + 2 ** i_layer, bin_list_new, T) # вычеркивание дочерних элементов правого дочернего элемента
    return


# удаление родительских элементов
def del_pre(i_elem: int, i_layer: int, left_end: int, bin_list_new: list[str]):
    for i_layer_parent in range(i_layer - 1, 0, -1):
        distance = (i_elem - left_end) // 2 # расстояние между левой границей родительского слоя и родительским элементом
        left_end -= 2 ** i_layer_parent # левая граница родительского слоя
        i_elem = left_end + distance # родительский элемент
        bin_list_new[i_elem] = '' # вычеркиваем родительский элемент
    return


# подсчет количества вычеркнутых родителей у всех элеметов рассматриваемого слоя
def count_pre(i_layer: int, left_end: int, right_end: int, bin_list_new: list[str]):
    res_list = [] # список из кол-ва вычеркнутых родительских элементов для каждого элемента слоя i_layer
    for i_elem in range(left_end, right_end + 1): # цикл по элементам слоя
        del_parent = 0 # кол-во вычеркнутых родительских элементов
        left_end_new = left_end
        for i_layer_parent in range(i_layer - 1, 0, -1): # цикл по родительским слоям
            distance = (i_elem - left_end_new) // 2 # расстояние между левой границей родительского слоя и родительским элементом
            left_end_new -= 2 ** i_layer_parent # левая граница родительского слоя
            i_elem = left_end_new + distance # родительский элемент
            if bin_list_new[i_elem] == '': # проверка на вычеркнутость
                del_parent += 1
        res_list.append(del_parent) # добавление кол-ва вычеркнутых родительских элементов в список
    return res_list


# рекуррентная функция для нахождения P и L
def recur(bin_list: list[str], N: int, T: int, step: int = 0, code_words_list: list[str] = [],
          flag_list: list[int] = [], code_len: float = 0, code_cnt: int = 0):

    # проверка случая, когда подходящих элементов осталось меньше, чем нужно выбрать
    if len(list(filter(None, bin_list))) < N:
        return 0, code_len, code_cnt

    # проверка случая, когда все элементы выбраны
    if N == 0:
        return 1, code_len, code_cnt

    left_end = 0  # индекс начального элемента слоя дерева
    bin_list_new = bin_list.copy()  # список подходящих элементов, учитывающих выбор без возвращения
    final_prob = 0  # итоговая вероятность на рассматриваемом шаге
    flag = 1  # флаг для идентичных случаев

    for i_layer in range(1, T + 1):  # цикл по слоям

        right_end = left_end + (2 ** i_layer) - 1 # правая граница слоя

        # для каждого элемента слоя вычисляем количество неподходящих элементов-предков для выявления идентичных случаев
        count_pre_list = count_pre(i_layer, left_end, right_end, bin_list_new.copy())
        done_list = []  # список учтенных идентичных элементов

        for i_elem in range(left_end, right_end + 1):  # цикл по элементам конкретного слоя

            # не рассматриваем неподходящие элементы или уже учтенные идентичные
            if bin_list[i_elem] == '' or i_elem in done_list:
                continue

            # поиск идентичных элементов
            for i_right_elem in range(i_elem + 1, right_end + 1):  # цикл по элементам слоя, которые правее рассматриваемого

                # условие идентичности элементов
                if bin_list[i_right_elem] != '' and count_pre_list[i_elem - left_end] == count_pre_list[i_right_elem - left_end]:
                    flag += 1                 # увеличиваем флаг в случае нахождения идентичного элемента
                    done_list.append(i_right_elem)    # и добавляем элемент в список учтенных элементов

            code_words_list.append(bin_list[i_elem])  # добавляем в код выбранное кодовое слово
            flag_list.append(flag)  # добавляем кол-во идентичных элементов

            # проверяем на префиксность и отмечаем неподходящие элементы
            del_pre(i_elem, i_layer, left_end, bin_list_new) # удаляем родительские элементы
            del_post(i_elem, i_layer, left_end, bin_list_new, T) # удаляем текущий и дочерние элементы

            # условная вероятность следующих шагов, сумма средних длин идентичных кодов, кол-во кодовых слов
            temp_prob, code_len, code_cnt = recur(bin_list_new, N - 1, T, step + 1, code_words_list, flag_list, code_len, code_cnt)
            if temp_prob == 1: # проверка на успешность получения префиксного кода
                code_len += sum([len(i) for i in code_words_list]) * math.prod(flag_list) / len(code_words_list) # сумма средних длин идентичных кодов
                code_cnt += math.prod(flag_list) # общее кол-во кодов

            final_prob += temp_prob * flag / num_choice_list[step]  # итоговая вероятность текущего шага

            flag_list.pop()  # удаляем из списка последнее кол-во идентичных кодовых слов
            code_words_list.pop()  # удаляем из списка последнее выбранное кодовое слово
            flag = 1  # сбрасываем флаг для идентичных случаев
            bin_list_new = bin_list.copy()  # возвращаемся к прежнему списку

        left_end = right_end + 1 # сдвигаем границу для рассмотрения следующего слоя

    return final_prob, code_len, code_cnt


if __name__ == "__main__":
    N = 7
    T = 3
    bin_list = []  # список кодовых слов

    # генерируем коды длины <= T
    for i_layer in range(1, T + 1):
        bin_list.extend(gen_bin(i_layer, []))

    # удаление некоторых начальных элементов bin_list
    for i_layer in range(T - 1, 0, -1): # цикл по слоям кроме последнего
        if 2 ** T - 2 ** i_layer < N - 1: # проверка достаточности элементов на последнем слое при выборе элемента на T - i слое
            if i_layer == T - 1: # проверка на первый слой
                bin_list[:2] = ['', ''] # вычеркивание элементов с первого слоя
            else:
                # вычеркивание элементов с T - i слоя
                for i_elem in range(sum([2 ** i_layer_new for i_layer_new in range(1, T - i_layer)]), sum([2 ** i_layer_new for i_layer_new in range(1, T - i_layer + 1)])):
                    bin_list[i_elem] = ''

    list_len = len(list(filter(lambda i_elem: i_elem != '', bin_list))) # удаляем вычеркнутые слои
    num_choice_list = [(list_len - step) for step in range(N)] # кол-во возможных кодовых слов для выбора на каждом шаге

    final_prob, final_sum, final_cnt = recur(bin_list, N, T)
    # вывод T, N, P, 1/P, L
    print(T, N, final_prob, 1/final_prob if final_prob > 0 else 0, final_sum / final_cnt if final_cnt > 0 else 0)
