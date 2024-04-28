"""
Напишите программу, которая выводит путь, по которому, двигаясь интервалом длины
m по заданному массиву, концом будет являться первый элемент.
Началом одного интервала является конец предыдущего.
"""
import sys


def find_path(len_array, step):
    circle_array = [i for i in range(1, len_array + 1)]
    first_elem = circle_array[0]
    path = [first_elem]
    while first_elem != circle_array[step - 1]:
        path.append(circle_array[step - 1])
        circle_array = circle_array[step - 1:] + circle_array[:step - 1]
    return print(*path, sep='')


if __name__ == '__main__':
    n, m = int(sys.argv[1]), int(sys.argv[2])
    find_path(n, m)
