from random import uniform, randint
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


class GraphVisualization:

    def __init__(self, matrix):
        self.visual = matrix
        self.color_list = [0 for _ in range(len(matrix))]

        # Алгоритм задания групп цветов для узлов графа | Основная задача
        k = [uniform(0, 1), uniform(0, 1), uniform(0, 1)]
        for i in range(len(matrix)):
            if self.color_list[i] != 0:  # Значит вершина уже покрашена
                continue
            self.color_list[i] = k
            tmp = matrix[i]
            while 0 in tmp:
                j = i + 1
                while j != len(tmp):
                    if tmp[j] == 0 and self.color_list[j] == 0:  # Поиск первого несмежного нераскрашеного элемента
                        self.color_list[j] = k
                        # Ниже происходит дизъюнкция путей обоих вершин, это исключает добавление вершин, которые были несмежны первой, но смежны второй итд
                        tmp = [tmp[index] | self.visual[j][index] for index in range(len(tmp))]
                        break
                    j += 1
                if j == len(tmp):
                    break
            k = [uniform(0, 1), uniform(0, 1), uniform(0, 1)]

        # Создал тут словарь для более удобного вывода принадлежности вершин к общим группам, не относится к основной задаче
        self.color_map = dict()
        for i, node in enumerate(self.color_list):
            if tuple(node) not in self.color_map.keys():
                self.color_map[tuple(node)] = []
            self.color_map[tuple(node)].append(i)

    def visualize(self):
        G = nx.Graph(np.array(self.visual))
        for c, p in enumerate(self.color_map.items()):
            print(f'Группа {c}: {p[1]}')
        nx.draw_networkx(G, node_color=self.color_list, with_labels=True)
        plt.show()


# Генерация графа с size вершинами
size = 6
m = [[0] * size for i in range(size)]
for i in range(size):
    for g in range(size):
        if g == i or m[i].count(1) == 3:
            continue
        m[i][g] = randint(0, 1)
        m[g][i] = m[i][g]
print('\n'.join([str(i) for i in m]))
print()
G = GraphVisualization(m)
G.visualize()
