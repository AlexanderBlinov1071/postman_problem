import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
from networkx.algorithms import matching
import matplotlib.pyplot as plt


app = tk.Tk()
app.title("Задача китайского почтальона")
app.geometry("1000x600")
app.configure(bg='chocolate')
my_font = ("Times New Roman", 28)


vertex_label = ttk.Label(app, text = "Вершины (через запятую):", font = my_font, background='yellow')
vertex_entry = ttk.Entry(app, font = my_font)
vertex_entry.config(width=45)


edges_label = ttk.Label(app, text = "Рёбра (через запятую):", font = my_font, background='yellow')
edges_entry = ttk.Entry(app, font = my_font)
edges_entry.config(width=45)


weights_label = ttk.Label(app, text = "Веса рёбер (через запятую):", font = my_font, background='yellow')
weights_entry = ttk.Entry(app, font = my_font)
weights_entry.config(width=45)


result_label = ttk.Label(app, text = "Маршрут почтальона:", font = my_font, background='yellow')
result_entry = ttk.Entry(app, font = my_font)
result_entry.config(width=45)


length_label = ttk.Label(app, text = "Длина маршрута:", font = my_font, background='yellow')
length_entry = ttk.Entry(app, font = my_font)
length_entry.config(width=45)


solve_button = ttk.Button(app, text = "Решить")
solve_button.pack(ipadx = 15, ipady = 15)


info_button = ttk.Button(app, text = "Справка")
info_button.pack(ipadx = 15, ipady = 15)


def show_info_window():
    window = tk.Toplevel(app)
    window.title("Справка")
    info = "Задача китайского почтальона (англ. Chinese postman problem, CPP), маршрут почтальона или задача инспекции дорог заключается \n в поиске кратчайшего замкнутого пути или цикла, который проходит через каждое ребро (связного) взвешенного неориентированного графа.\n Если граф имеет эйлеров цикл (замкнутый маршрут, который проходит любое ребро ровно один раз),\n тогда этот цикл служит оптимальным решением. В противном случае задачей\n оптимизации является поиск наименьшего\n числа рёбер графа с повторными проходами (или подмножество рёбер с минимальным возможным общим весом), так что\n получающийся мультиграф имеет эйлеров цикл. Эта задача может быть решена за полиномиальное время."
    text = "\nПрограммная реализация решения задачи китайского почтальона. Вершины графа необходимо вводить через запятую, например: a,b,c...\n и т.д. Аналогично ребра и их веса, без пробелов, через запятую, например: a-b,b-c,c-a... и т.д.\n Сплошной линией на рисунке изображаются реальные рёбра исходного графа, пунктиром - искусственные рёбра мультиграфа (имеет тот же вес, что ребро, отображаемое сплошной линией)."
    label = tk.Label(window, text=info + text, font=26)
    label.pack()
    close_button = tk.Button(window, text="Закрыть", command=window.destroy, font=18)
    close_button.pack()


def solve():
    try:
        vertices = vertex_entry.get().split(',')
        edges = edges_entry.get().split(',')
        weights = weights_entry.get().split(',')

        G = nx.Graph()
        labels = {}  
        e_label = {}

        for vertex in vertices:
            G.add_node(vertex)

        for edge, weight in zip(edges, weights):
            u, v = edge.split('-')
            G.add_edge(u, v)
            labels[(u, v)] = weight  
            e_label[(u, v)] = weight
            labels[(v, u)] = weight  

        pos = nx.spring_layout(G)

        if nx.is_eulerian(G):
            messagebox.showinfo("Внимание!","Исходный граф имеет эйлеров цикл!")
            eulerian_tour = list(nx.eulerian_circuit(G)) 
            nx.draw(G, pos, with_labels=True, node_color='yellow', node_size=600, edge_color="brown")
            nx.draw_networkx_edge_labels(G, pos, edge_labels=e_label, label_pos=0.18, font_color='red', font_size=12)

            result_entry.delete(0, 'end') 
            result_entry.insert(0, str(eulerian_tour))

            route_length = int(sum(float(labels.get((u, v), 0)) for u, v in eulerian_tour))
            
            length_entry.delete(0, 'end')  
            length_entry.insert(0, str(route_length))

            plt.show()

        else:
            messagebox.showinfo("Внимание!","Исходный граф будет преобразован к мультиграфу, поскольку не является эйлеровым.")
            odd_vertices = [v for v, degree in G.degree() if degree % 2 != 0]
            odd_subgraph = G.subgraph(odd_vertices)
            matching_edges = list(matching.min_weight_matching(odd_subgraph))
            multigraph = nx.MultiGraph(G)
            multigraph.add_edges_from(matching_edges)
            eulerian_tour = list(nx.eulerian_circuit(multigraph))

            
            nx.draw(multigraph, pos, with_labels=True, node_color='yellow', node_size=600, edge_color="brown")
            nx.draw_networkx_edges(multigraph, pos, edgelist=matching_edges, edge_color='brown', width=1.5, style='dashed', connectionstyle='arc3, rad=0.085', arrows=True)
            nx.draw_networkx_edge_labels(multigraph, pos, edge_labels=e_label, label_pos=0.2, font_color='red', font_size=12)

            result_entry.delete(0, 'end') 
            result_entry.insert(0, str(eulerian_tour))

            route_length = int(sum(float(labels.get((u, v), 0)) for u, v in eulerian_tour))
            
            length_entry.delete(0, 'end')  
            length_entry.insert(0, str(route_length))

            plt.show()

    except Exception as exc:
        messagebox.showerror("Ошибка!", str(exc))


solve_button.config(command=solve)
info_button.config(command=show_info_window)


vertex_label.pack()
vertex_entry.pack()
edges_label.pack()
edges_entry.pack()
weights_label.pack()
weights_entry.pack()
result_label.pack()
result_entry.pack()
length_label.pack()
length_entry.pack()
solve_button.pack()
info_button.pack()


app.mainloop()
