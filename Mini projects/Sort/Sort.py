import tkinter as tk
from tkinter import ttk, messagebox
import time
import copy
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Algoritmos de ordenamiento
def bubble_sort(arr):
    n = len(arr)
    for i in range(n-1):
        for j in range(n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def selection_sort(arr):
    n = len(arr)
    for i in range(n-1):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + equal + quick_sort(right)

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def heap_sort(arr):
    def heapify(n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and arr[l] > arr[largest]:
            largest = l
        if r < n and arr[r] > arr[largest]:
            largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(n, largest)
    
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)
    for i in range(n-1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(i, 0)
    return arr

def hash_sort(arr):
    if not arr:
        return arr
    min_val = min(arr)
    max_val = max(arr)
    range_val = max_val - min_val + 1
    count = [0] * range_val
    for num in arr:
        count[num - min_val] += 1
    idx = 0
    for i in range(range_val):
        while count[i] > 0:
            arr[idx] = i + min_val
            idx += 1
            count[i] -= 1
    return arr

def bucket_sort(arr):
    if not arr:
        return arr
    min_val = min(arr)
    max_val = max(arr)
    bucket_count = int(len(arr) ** 0.5) or 1
    range_val = (max_val - min_val + 1) / bucket_count
    buckets = [[] for _ in range(bucket_count)]
    for num in arr:
        idx = int((num - min_val) / range_val)
        if idx == bucket_count:
            idx -= 1
        buckets[idx].append(num)
    sorted_arr = []
    for bucket in buckets:
        if bucket:
            sorted_arr.extend(insertion_sort(bucket))
    return sorted_arr

def radix_sort(arr):
    if not arr:
        return arr
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        counting_sort(arr, exp)
        exp *= 10
    return arr

def counting_sort(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    for i in range(n):
        digit = (arr[i] // exp) % 10
        count[digit] += 1
    for i in range(1, 10):
        count[i] += count[i-1]
    for i in range(n-1, -1, -1):
        digit = (arr[i] // exp) % 10
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1
    for i in range(n):
        arr[i] = output[i]

sorting_algorithms = {
    'bubble': {'name': 'Bubble Sort', 'sort': bubble_sort},
    'insertion': {'name': 'Inserción Sort', 'sort': insertion_sort},
    'selection': {'name': 'Selección Sort', 'sort': selection_sort},
    'quick': {'name': 'Quick Sort', 'sort': quick_sort},
    'merge': {'name': 'Merge Sort', 'sort': merge_sort},
    'heap': {'name': 'Heap Sort', 'sort': heap_sort},
    'hash': {'name': 'Hash Sort', 'sort': hash_sort},
    'bucket': {'name': 'Bucket Sort', 'sort': bucket_sort},
    'radix': {'name': 'Radix Sort', 'sort': radix_sort},
}

# Generadores de arrays
def generate_sorted(size):
    return list(range(size))

def generate_partially(size):
    arr = list(range(size))
    for _ in range(size // 10):
        idx1 = random.randint(0, size-1)
        idx2 = random.randint(0, size-1)
        arr[idx1], arr[idx2] = arr[idx2], arr[idx1]
    return arr

def generate_reversed(size):
    return list(range(size-1, -1, -1))

array_generators = {
    'sorted': generate_sorted,
    'partially': generate_partially,
    'reversed': generate_reversed,
}

scenario_names = {
    'sorted': 'Ordenado',
    'partially': 'Mediamente ordenado',
    'reversed': 'Inverso',
}

class SortingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Comparador de Algoritmos de Ordenamiento")
        self.root.geometry("1300x850")

        self.results = {'byMethod': {}, 'byScenario': {}}

        self.create_widgets()
        self.create_chart()

    def create_widgets(self):
        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.pack(fill=tk.X)

        # Algoritmos
        algo_frame = ttk.LabelFrame(control_frame, text="Algoritmos")
        algo_frame.grid(row=0, column=0, padx=10, sticky='nw')
        self.algo_vars = {}
        for key, algo in sorting_algorithms.items():
            var = tk.BooleanVar(value=True)
            cb = ttk.Checkbutton(algo_frame, text=algo['name'], variable=var)
            cb.pack(anchor='w')
            self.algo_vars[key] = var

        # Tamaños (hasta 100,000)
        size_frame = ttk.LabelFrame(control_frame, text="Tamaños de array")
        size_frame.grid(row=0, column=1, padx=10, sticky='nw')
        self.size_vars = {}
        sizes = [100, 500, 1000, 5000, 10000, 50000, 100000]
        for size in sizes:
            var = tk.BooleanVar(value=True if size <= 1000 else False)
            cb = ttk.Checkbutton(size_frame, text=f"{size:,}", variable=var)
            cb.pack(anchor='w')
            self.size_vars[size] = var

        # Escenarios
        scen_frame = ttk.LabelFrame(control_frame, text="Escenarios")
        scen_frame.grid(row=0, column=2, padx=10, sticky='nw')
        self.scen_vars = {}
        for key in array_generators.keys():
            var = tk.BooleanVar(value=True)
            cb = ttk.Checkbutton(scen_frame, text=scenario_names[key], variable=var)
            cb.pack(anchor='w')
            self.scen_vars[key] = var

        # Botones
        btn_frame = ttk.Frame(control_frame)
        btn_frame.grid(row=0, column=3, padx=10)
        ttk.Button(btn_frame, text="Ejecutar Pruebas", command=self.run_tests).pack(pady=5)
        ttk.Button(btn_frame, text="Limpiar Resultados", command=self.reset_results).pack(pady=5)

        self.loading_label = ttk.Label(control_frame, text="", foreground="blue")
        self.loading_label.grid(row=1, column=0, columnspan=4, pady=5)

        # Notebook
        nb = ttk.Notebook(self.root)
        nb.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tabla por método
        method_tab = ttk.Frame(nb)
        nb.add(method_tab, text="Por Algoritmo")
        self.method_tree = ttk.Treeview(method_tab, columns=('Name', 'Avg', 'Best', 'Worst'), show='headings')
        self.method_tree.heading('Name', text='Algoritmo')
        self.method_tree.heading('Avg', text='Promedio (ms)')
        self.method_tree.heading('Best', text='Mejor (ms)')
        self.method_tree.heading('Worst', text='Peor (ms)')
        self.method_tree.pack(fill=tk.BOTH, expand=True)

        # Tabla por escenario
        scen_tab = ttk.Frame(nb)
        nb.add(scen_tab, text="Por Escenario")
        self.scen_tree = ttk.Treeview(scen_tab, columns=('Scenario', 'BestAlgo', 'WorstAlgo', 'Diff'), show='headings')
        self.scen_tree.heading('Scenario', text='Escenario (tamaño)')
        self.scen_tree.heading('BestAlgo', text='Mejor Algoritmo')
        self.scen_tree.heading('WorstAlgo', text='Peor Algoritmo')
        self.scen_tree.heading('Diff', text='Diferencia (ms)')
        self.scen_tree.pack(fill=tk.BOTH, expand=True)

        # Gráfico
        chart_tab = ttk.Frame(nb)
        nb.add(chart_tab, text="Gráfico")
        self.chart_frame = ttk.Frame(chart_tab)
        self.chart_frame.pack(fill=tk.BOTH, expand=True)

    def create_chart(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def get_selected(self):
        algos = [k for k, v in self.algo_vars.items() if v.get()]
        sizes = [k for k, v in self.size_vars.items() if v.get()]
        scenarios = [k for k, v in self.scen_vars.items() if v.get()]
        if not algos or not sizes or not scenarios:
            messagebox.showwarning("Selección", "Selecciona al menos un algoritmo, tamaño y escenario.")
            return None, None, None
        return algos, sizes, scenarios

    def run_tests(self):
        algos, sizes, scenarios = self.get_selected()
        if not algos:
            return

        self.loading_label.config(text="Ejecutando pruebas... Por favor espera.")
        self.root.update_idletasks()

        try:
            self.results = {'byMethod': {}, 'byScenario': {}}

            for algo in algos:
                self.results['byMethod'][algo] = {
                    'name': sorting_algorithms[algo]['name'],
                    'times': [],
                    'totalTime': 0
                }

            for scen in scenarios:
                self.results['byScenario'][scen] = {}
                for size in sizes:
                    self.results['byScenario'][scen][size] = {}

            for scen in scenarios:
                for size in sizes:
                    test_arr = array_generators[scen](size)
                    for algo in algos:
                        arr_copy = copy.deepcopy(test_arr)
                        start = time.perf_counter()
                        sorting_algorithms[algo]['sort'](arr_copy)
                        end = time.perf_counter()
                        exec_time = (end - start) * 1000
                        self.results['byMethod'][algo]['times'].append(exec_time)
                        self.results['byMethod'][algo]['totalTime'] += exec_time
                        self.results['byScenario'][scen][size][algo] = exec_time

            self.process_results()
            self.update_tables()
            self.update_chart()

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
        finally:
            self.loading_label.config(text="Pruebas completadas.")
            self.root.after(2000, lambda: self.loading_label.config(text=""))

    def process_results(self):
        for algo, data in self.results['byMethod'].items():
            times = data['times']
            if times:
                data['averageTime'] = data['totalTime'] / len(times)
                data['bestTime'] = min(times)
                data['worstTime'] = max(times)

        for scen in self.results['byScenario']:
            for size in self.results['byScenario'][scen]:
                sdata = self.results['byScenario'][scen][size]
                if not sdata:
                    continue
                best_algo = min(sdata.keys(), key=lambda k: sdata[k])
                worst_algo = max(sdata.keys(), key=lambda k: sdata[k])
                sdata['bestAlgo'] = best_algo
                sdata['worstAlgo'] = worst_algo
                sdata['difference'] = sdata[worst_algo] - sdata[best_algo]

    def update_tables(self):
        for item in self.method_tree.get_children():
            self.method_tree.delete(item)
        method_list = []
        for algo, data in self.results['byMethod'].items():
            if 'averageTime' in data:
                method_list.append((algo, data))
        method_list.sort(key=lambda x: x[1]['averageTime'])
        for algo, data in method_list:
            self.method_tree.insert('', 'end', values=(
                data['name'],
                f"{data['averageTime']:.4f}",
                f"{data['bestTime']:.4f}",
                f"{data['worstTime']:.4f}"
            ))

        for item in self.scen_tree.get_children():
            self.scen_tree.delete(item)
        for scen in self.results['byScenario']:
            for size in self.results['byScenario'][scen]:
                sdata = self.results['byScenario'][scen][size]
                if 'bestAlgo' in sdata:
                    self.scen_tree.insert('', 'end', values=(
                        f"{scenario_names[scen]} ({size:,} elementos)",
                        sorting_algorithms[sdata['bestAlgo']]['name'],
                        sorting_algorithms[sdata['worstAlgo']]['name'],
                        f"{sdata['difference']:.4f}"
                    ))

    def update_chart(self):
        algos, _, scenarios = self.get_selected()
        if not algos or not scenarios:
            return

        self.ax.clear()

        labels = [sorting_algorithms[a]['name'] for a in algos]
        scenario_colors = {
            'sorted': '#369AEB',
            'partially': '#FFCE56',
            'reversed': '#FF6384',
        }

        n_algos = len(algos)
        n_scen = len(scenarios)
        bar_width = 0.25
        total_width = bar_width * n_scen
        index = list(range(n_algos))
        offset = -total_width / 2 + bar_width / 2

        for i, scen in enumerate(scenarios):
            avg_times = []
            for algo in algos:
                total = 0
                count = 0
                for size in self.results['byScenario'][scen]:
                    if algo in self.results['byScenario'][scen][size]:
                        total += self.results['byScenario'][scen][size][algo]
                        count += 1
                avg_times.append(total / count if count else 0)

            positions = [x + offset + i * bar_width for x in index]
            self.ax.bar(
                positions, avg_times, bar_width,
                label=scenario_names[scen],
                color=scenario_colors.get(scen, '#CCCCCC'),
                edgecolor='black', linewidth=0.5
            )

        self.ax.set_xlabel('Algoritmos')
        self.ax.set_ylabel('Tiempo promedio (ms)')
        self.ax.set_title('Tiempo de Ejecución por Algoritmo y Escenario')
        self.ax.set_xticks(index)
        self.ax.set_xticklabels(labels, rotation=45, ha='right')
        self.ax.legend(title="Escenario")
        self.ax.grid(True, axis='y', alpha=0.3)

        self.fig.tight_layout()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def reset_results(self):
        self.results = {'byMethod': {}, 'byScenario': {}}
        for item in self.method_tree.get_children():
            self.method_tree.delete(item)
        for item in self.scen_tree.get_children():
            self.scen_tree.delete(item)
        self.ax.clear()
        self.fig.canvas.draw()
        self.loading_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingApp(root)
    root.mainloop()