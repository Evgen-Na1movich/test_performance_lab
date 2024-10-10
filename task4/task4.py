import sys


def min_moves(path):
    with open(path, 'r') as file:
        numbers = list(map(int, file.readlines()))
        list_moves = []
        for i in range(len(numbers)):
            list_moves.append(sum(list(map(lambda x: abs(x - numbers[i]), numbers))))
        return min(list_moves)


if __name__ == '__main__':
    try:
        print(min_moves(sys.argv[1]))
    except ValueError:
        print("Initial data files are empty")


