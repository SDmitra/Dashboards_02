import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random

# Чтение данных из CSV файла
data = pd.read_csv('source.csv', encoding='cp1251', sep=';')

# Преобразование данных в список кортежей для бизнес-процессов
process_data = list(zip(data['export_source'], data['import_source']))

# Создание пустого графа
G = nx.DiGraph()



# Добавление рёбер в граф на основе данных о бизнес-процессах
for source, target in process_data:
    G.add_edge(source, target)

# Вычисление степеней узлов (количество входящих и исходящих связей)
node_sizes = [len(list(G.successors(node))) + len(list(G.predecessors(node))) for node in G.nodes()]

# Рисование графа с изменённым размещением узлов, размерами узлов и цветами линий
pos = nx.spring_layout(G, k=0.9, iterations=50)

# Создание случайных цветов для линий (для примера)
edge_colors = [random.choice(['red', 'green', 'blue', 'black', 'pink', 'purple']) for _ in range(len(G.edges()))]

nx.draw(G, pos, with_labels=True, node_size=[200 * size for size in node_sizes], node_color='skyblue', font_weight='bold', arrows=True, edge_color=edge_colors)

# Создание пустого словаря для подписей
edge_labels = {}

# Заполнение словаря количеством взаимосвязей для каждой связи
for source, target in G.edges():
    num_relations = len(list(G.successors(target))) + len(list(G.predecessors(source)))
    edge_labels[(source, target)] = str(num_relations)

# Добавление подписей к рёбрам
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black')

plt.show()
