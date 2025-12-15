import tkinter as tk
# <--- MODIFICADO: Añadido simpledialog
from tkinter import messagebox, filedialog, simpledialog
import json
import random

class SudokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("SudokuProAña")
       
        self.root.geometry("780x780") 
        self.root.resizable(False, False)

        self.size_map = {
            'very-easy': {'size': 4, 'box_shape': (2, 2), 'name': 'Muy Fácil'},
            'easy':      {'size': 6, 'box_shape': (2, 3), 'name': 'Fácil'},
            'normal':    {'size': 6, 'box_shape': (3, 2), 'name': 'Normal'},
            'hard':      {'size': 9, 'box_shape': (3, 3), 'name': 'Difícil'},
            'expert':    {'size': 9, 'box_shape': (3, 3), 'name': 'Experto'}
        }
        
        self.xp_map = {
            'very-easy': 100,
            'easy': 200,
            'normal': 300,
            'hard': 500,
            'expert': 1500
        }

        self.game_state = {
            "level": 1,
            "xp": 0,
            "xp_needed": 500,
            "lives": 5,
            "currentDifficulty": None, 
            "selectedCell": None,
            "grid": [],
            "solution": [],
            "initialGrid": []
        }
        
        # <--- AÑADIDO: Archivo para guardar puntuaciones
        self.leaderboard_file = "sudoku_leaderboard.json"

        self.cells = {}
        self.diff_var = tk.StringVar(value='very-easy')
        self.size = 4
        self.box_rows = 2
        self.box_cols = 2

        self.create_interface()
        self.change_difficulty('very-easy')

    def create_interface(self):
        tk.Label(self.root, text="SUDOKU MATADOR", font=("Arial", 28, "bold"), fg="#2c3e50").pack(pady=15)

        stats_frame = tk.Frame(self.root)
        stats_frame.pack(pady=5)
        self.level_label = tk.Label(stats_frame, text="Nivel: 1", font=("Arial", 14))
        self.level_label.pack(side=tk.LEFT, padx=40)
        self.xp_label = tk.Label(stats_frame, text="XP: 0 / 500", font=("Arial", 14))
        self.xp_label.pack(side=tk.LEFT, padx=40)

        self.lives_frame = tk.Frame(self.root)
        self.lives_frame.pack(pady=5)
        self.update_lives_display()

        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(pady=15)

        self.numpad_frame = tk.Frame(self.root)
        self.numpad_frame.pack(pady=10)

        ctrl_frame = tk.Frame(self.root)
        ctrl_frame.pack(pady=10)
        tk.Button(ctrl_frame, text="Nuevo", width=10, bg="#3498db", fg="white", command=self.generate_new_puzzle).pack(side=tk.LEFT, padx=8)
        tk.Button(ctrl_frame, text="Comprobar", width=10, bg="#f39c12", fg="white", command=self.check_solution).pack(side=tk.LEFT, padx=8)
        
        # <--- AÑADIDO: Botón de Leaderboard
        tk.Button(ctrl_frame, text="Leaderboard", width=10, bg="#2ecc71", fg="white", command=self.show_leaderboard).pack(side=tk.LEFT, padx=8)
        
        tk.Button(ctrl_frame, text="Guardar", width=10, bg="#9b59b6", fg="white", command=self.save_game).pack(side=tk.LEFT, padx=8)
        tk.Button(ctrl_frame, text="Cargar", width=10, bg="#34495e", fg="white", command=self.load_game).pack(side=tk.LEFT, padx=8)

        diff_frame = tk.Frame(self.root)
        diff_frame.pack(pady=15)
        for diff in self.size_map:
            rb = tk.Radiobutton(diff_frame, text=self.size_map[diff]['name'], variable=self.diff_var, value=diff, font=("Arial", 11), command=lambda d=diff: self.change_difficulty(d))
            rb.pack(side=tk.LEFT, padx=12)

        self.message_label = tk.Label(self.root, text="", fg="green", font=("Arial", 12))
        self.message_label.pack(pady=5)

        self.modal = tk.Toplevel(self.root)
        self.modal.withdraw()
        self.modal.title("¡Subiste de nivel!")
        self.modal.geometry("320x160")
        tk.Label(self.modal, text="¡Nivel completado!", font=("Arial", 16, "bold")).pack(pady=20)
        self.modal_level_label = tk.Label(self.modal, text="", font=("Arial", 14))
        self.modal_level_label.pack(pady=5)
        tk.Button(self.modal, text="Continuar", bg="#27ae60", fg="white", command=self.continue_to_next_level).pack(pady=10)

    # --- (Las funciones de create_numpad a is_puzzle_complete no cambian) ---
    def create_numpad(self):
        for widget in self.numpad_frame.winfo_children():
            widget.destroy()
        num_per_row = self.size
        if self.size > 6: num_per_row = (self.size + 1) // 2 
        current_frame = tk.Frame(self.numpad_frame)
        current_frame.pack()
        for num in range(1, self.size + 1):
            if num == num_per_row + 1: 
                current_frame = tk.Frame(self.numpad_frame)
                current_frame.pack()
            btn = tk.Button(current_frame, text=str(num), font=("Arial", 14, "bold"), width=3, height=1, command=lambda n=num: self.fill_cell(n))
            btn.pack(side=tk.LEFT, padx=5, pady=2)
        clear_btn = tk.Button(self.numpad_frame.winfo_children()[0], text="Borrar", font=("Arial", 12), width=5, bg="#e74c3c", fg="white", command=self.clear_cell)
        clear_btn.pack(side=tk.LEFT, padx=15)

    def update_lives_display(self):
        for widget in self.lives_frame.winfo_children():
            widget.destroy()
        for i in range(5):
            emoji = "❤️" if i < self.game_state["lives"] else "💔" 
            label = tk.Label(self.lives_frame, text=emoji, font=("Arial", 18))
            label.pack(side=tk.LEFT, padx=4)

    def change_difficulty(self, diff):
        if self.game_state["currentDifficulty"] == diff:
            return
        self.game_state["currentDifficulty"] = diff
        config = self.size_map[diff]
        self.size = config['size']
        self.box_rows, self.box_cols = config['box_shape']
        self.create_numpad()
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        self.cells.clear()
        self.generate_new_puzzle()
        self.update_ui()

    def generate_grid_display(self):
        cell_width = 3 if self.size <= 6 else 2
        font_size = 16 if self.size <= 6 else 14
        for i in range(self.size):
            for j in range(self.size):
                thick_left = 3 if j % self.box_cols == 0 and j != 0 else 1
                thick_right = 3 if j == self.size - 1 or (j + 1) % self.box_cols == 0 else 1
                thick_top = 3 if i % self.box_rows == 0 and i != 0 else 1
                thick_bottom = 3 if i == self.size - 1 or (i + 1) % self.box_rows == 0 else 1
                cell = tk.Entry(self.grid_frame, width=cell_width, font=("Arial", font_size), justify="center", bd=0, highlightthickness=2, highlightcolor="#3498db")
                cell.grid(row=i, column=j, padx=(thick_left, thick_right), pady=(thick_top, thick_bottom), ipady=5)
                cell.bind("<FocusIn>", lambda e, r=i, c=j: self.select_cell(r, c))
                self.cells[(i, j)] = cell

    def select_cell(self, row, col):
        if self.game_state["initialGrid"][row][col] != 0:
             self.game_state["selectedCell"] = None
             self.root.focus()
             return
        if self.game_state["selectedCell"]:
            r, c = self.game_state["selectedCell"]
            if (r, c) in self.cells:
                self.cells[(r, c)].config(highlightbackground="white")
        self.game_state["selectedCell"] = (row, col)
        self.highlight_related(row, col)

    def highlight_related(self, row, col):
        for i in range(self.size):
            for j in range(self.size):
                self.cells[(i, j)].config(highlightbackground="white", highlightcolor="#3498db")
        for i in range(self.size):
            self.cells[(row, i)].config(highlightbackground="#dfe6e9")
            self.cells[(i, col)].config(highlightbackground="#dfe6e9")
        br, bc = (row // self.box_rows) * self.box_rows, (col // self.box_cols) * self.box_cols
        for i in range(self.box_rows):
            for j in range(self.box_cols):
                self.cells[(br + i, bc + j)].config(highlightbackground="#b2bec3")
        if self.game_state["initialGrid"][row][col] == 0:
            self.cells[(row, col)].config(highlightbackground="#74b9ff", highlightcolor="#0984e3")

    def fill_cell(self, num):
        if not self.game_state["selectedCell"]: return
        row, col = self.game_state["selectedCell"]
        if self.game_state["initialGrid"][row][col] != 0:
            return
        self.game_state["grid"][row][col] = num
        if not self.is_valid_move(row, col, num):
            self.game_state["lives"] -= 1
            self.update_lives_display()
            self.show_message("¡Error! Pierdes una vida.", "error")
            if self.game_state["lives"] <= 0:
                self.game_over()
        self.update_grid_display()
        if self.is_puzzle_complete():
            self.handle_completion()

    def clear_cell(self):
        if not self.game_state["selectedCell"]: return
        row, col = self.game_state["selectedCell"]
        if self.game_state["initialGrid"][row][col] != 0:
            return
        self.game_state["grid"][row][col] = 0
        self.update_grid_display()

    def is_valid_move(self, row, col, num):
        for i in range(self.size):
            if self.game_state["grid"][row][i] == num and i != col: 
                return False
        for i in range(self.size):
            if self.game_state["grid"][i][col] == num and i != row: 
                return False
        br, bc = (row // self.box_rows) * self.box_rows, (col // self.box_cols) * self.box_cols
        for i in range(self.box_rows):
            for j in range(self.box_cols):
                if self.game_state["grid"][br + i][bc + j] == num and (br + i != row or bc + j != col):
                    return False
        return True
        
    def is_puzzle_complete(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.game_state["grid"][i][j] == 0:
                    return False
        for r in range(self.size):
            if len(set(self.game_state["grid"][r])) != self.size:
                return False
        for c in range(self.size):
            col = [self.game_state["grid"][r][c] for r in range(self.size)]
            if len(set(col)) != self.size:
                return False
        for br_start in range(0, self.size, self.box_rows):
            for bc_start in range(0, self.size, self.box_cols):
                box = []
                for r in range(self.box_rows):
                    for c in range(self.box_cols):
                        box.append(self.game_state["grid"][br_start + r][bc_start + c])
                if len(set(box)) != self.size:
                    return False
        return True

    def handle_completion(self):
        difficulty = self.game_state["currentDifficulty"]
        xp_gain = self.xp_map.get(difficulty, 100)
        self.game_state["xp"] += xp_gain
        self.show_message(f"¡Completado! +{xp_gain} XP", "success")

        if self.game_state["xp"] >= self.game_state["xp_needed"]:
            self.level_up()
        else:
            self.update_ui()
            self.root.after(2000, self.generate_new_puzzle)

    def level_up(self):
        self.game_state["level"] += 1
        self.game_state["xp"] -= self.game_state["xp_needed"]
        self.modal_level_label.config(text=f"Nivel {self.game_state['level']-1} → {self.game_state['level']}")
        self.modal.deiconify()
        self.update_ui()

    def continue_to_next_level(self):
        self.modal.withdraw()
        self.generate_new_puzzle()

    # <--- MODIFICADO: game_over ahora guarda la puntuación
    def game_over(self):
        self.show_message("¡Game Over!", "error")
        
        # Guardar puntuación ANTES de preguntar si quiere reiniciar
        self.check_and_save_highscore()
        
        if messagebox.askyesno("Fin nub", "¿Jugar de nuevo?"):
            self.reset_game()

    def reset_game(self):
        self.game_state.update({
            "level": 1, 
            "xp": 0, 
            "lives": 5, 
            "xp_needed": 500
        })
        self.change_difficulty('very-easy')

    # --- (Funciones de generación de puzzle no cambian) ---
    def generate_new_puzzle(self):
        config = self.size_map[self.game_state["currentDifficulty"]]
        self.size = config['size']
        self.box_rows, self.box_cols = config['box_shape']
        self.game_state["solution"] = self.generate_solved()
        self.game_state["grid"] = [row[:] for row in self.game_state["solution"]]
        self.game_state["initialGrid"] = [row[:] for row in self.game_state["solution"]]
        cells_to_remove = self.get_remove_count()
        self.remove_numbers(cells_to_remove)
        self.game_state["selectedCell"] = None 
        self.show_message("", "")             
        self.generate_grid_display() 
        self.update_grid_display()

    def generate_solved(self):
        grid = [[0] * self.size for _ in range(self.size)]
        self.fill_diagonal(grid)
        self.solve_sudoku(grid)
        return grid

    def fill_diagonal(self, grid):
        for i in range(0, self.size, self.box_rows):
            nums = list(range(1, self.size + 1))
            random.shuffle(nums)
            idx = 0
            col_start = (i // self.box_rows) * self.box_cols
            for x in range(self.box_rows):
                for y in range(self.box_cols):
                    if i + x < self.size and col_start + y < self.size:
                        grid[i + x][col_start + y] = nums[idx]
                        idx += 1

    def solve_sudoku(self, grid):
        empty = self.find_empty(grid)
        if not empty: return True
        row, col = empty
        for num in random.sample(range(1, self.size + 1), self.size):
            if self.is_safe(grid, row, col, num):
                grid[row][col] = num
                if self.solve_sudoku(grid): return True
                grid[row][col] = 0
        return False

    def find_empty(self, grid):
        for i in range(self.size):
            for j in range(self.size):
                if grid[i][j] == 0:
                    return i, j
        return None

    def is_safe(self, grid, row, col, num):
        for i in range(self.size):
            if grid[row][i] == num or grid[i][col] == num:
                return False
        br, bc = (row // self.box_rows) * self.box_rows, (col // self.box_cols) * self.box_cols
        for i in range(self.box_rows):
            for j in range(self.box_cols):
                if grid[br + i][bc + j] == num:
                    return False
        return True

    def get_remove_count(self):
        diff = self.game_state["currentDifficulty"]
        if diff == 'very-easy': return random.randint(3, 4) 
        if diff == 'easy': return random.randint(12, 16)
        if diff == 'normal': return random.randint(18, 22)
        if diff == 'hard': return random.randint(35, 40)
        return random.randint(42, 48)

    def remove_numbers(self, count):
        removed = 0
        while removed < count:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            if self.game_state["grid"][row][col] != 0:
                self.game_state["grid"][row][col] = 0
                self.game_state["initialGrid"][row][col] = 0
                removed += 1

    def update_grid_display(self):
        for i in range(self.size):
            for j in range(self.size):
                cell = self.cells[(i, j)]
                cell.config(state="normal")
                cell.delete(0, tk.END)
                val = self.game_state["grid"][i][j]
                fg_color = "black"
                if val != 0:
                    cell.insert(0, str(val))
                    if self.game_state["initialGrid"][i][j] == 0:
                        if not self.is_valid_move(i, j, val):
                            fg_color = "red"
                        else:
                            fg_color = "black"
                    else:
                        fg_color = "blue"
                if self.game_state["initialGrid"][i][j] != 0:
                    cell.config(state="readonly", fg="blue", readonlybackground="#f0f0f0")
                else:
                    cell.config(state="readonly", fg=fg_color, readonlybackground="white")

    def check_solution(self):
        for r in range(self.size):
            for c in range(self.size):
                val = self.game_state["grid"][r][c]
                if val != 0 and self.game_state["initialGrid"][r][c] == 0:
                    if not self.is_valid_move(r, c, val):
                         self.show_message("Ey, esta mal en algo.", "error")
                         return
        if self.is_puzzle_complete():
            self.show_message("¡Perfecto!", "success")
        else:
            self.show_message("Todo bien :b.", "success")


    def save_game(self):
        data = {
            "level": self.game_state["level"],
            "xp": self.game_state["xp"],
            "xp_needed": self.game_state["xp_needed"],
            "lives": self.game_state["lives"],
            "currentDifficulty": self.game_state["currentDifficulty"],
            "grid": self.game_state["grid"],
            "solution": self.game_state["solution"],
            "initialGrid": self.game_state["initialGrid"],
            "size": self.size,
            "box_rows": self.box_rows,
            "box_cols": self.box_cols
        }
        file = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if file:
            with open(file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            self.show_message("Guardado.", "success")

    def load_game(self):
        file = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if file:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
            diff = data.get("currentDifficulty", 'very-easy')
            config = self.size_map[diff]
            self.game_state.update({
                "level": data.get("level", 1),
                "xp": data.get("xp", 0),
                "xp_needed": data.get("xp_needed", 500),
                "lives": data.get("lives", 5),
                "currentDifficulty": diff,
                "grid": data.get("grid", []),
                "solution": data.get("solution", []), 
                "initialGrid": data.get("initialGrid", [])
            })
            self.size = data.get("size", config['size'])
            self.box_rows = data.get("box_rows", config['box_shape'][0])
            self.box_cols = data.get("box_cols", config['box_shape'][1])
            self.diff_var.set(self.game_state["currentDifficulty"])
            for widget in self.grid_frame.winfo_children():
                widget.destroy()
            self.cells.clear()
            self.create_numpad()
            self.generate_grid_display()
            self.update_grid_display()
            self.update_ui()
            self.show_message("Cargado.", "success")

    def update_ui(self):
        self.level_label.config(text=f"Nivel: {self.game_state['level']}")
        self.xp_label.config(text=f"XP: {self.game_state['xp']} / {self.game_state['xp_needed']}")
        self.update_lives_display()

    def show_message(self, text, type_):
        colors = {"success": "green", "error": "red"}
        self.message_label.config(text=text, fg=colors.get(type_, "black"))
        if text:
            self.root.after(3000, lambda: self.message_label.config(text="") if self.message_label.cget("text") == text else None)

    # <--- AÑADIDO: Nuevas funciones para el Leaderboard ---

    def load_leaderboard(self):
        """Carga las puntuaciones desde el archivo JSON."""
        try:
            with open(self.leaderboard_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return [] # Devuelve lista vacía si no existe o está corrupto

    def save_leaderboard(self, scores):
        """Guarda la lista de puntuaciones en el archivo JSON."""
        with open(self.leaderboard_file, "w") as f:
            json.dump(scores, f, indent=2)

    def check_and_save_highscore(self):
        """Comprueba si la puntuación actual entra en el Top 10."""
        scores = self.load_leaderboard()
        current_level = self.game_state["level"]
        current_xp = self.game_state["xp"]

        # Comprobar si es un high score (Top 10)
        # Es un high score si hay menos de 10 puntuaciones,
        # o si es mayor que la puntuación más baja en el Top 10
        if len(scores) < 10 or current_level > scores[-1]['level'] or \
           (current_level == scores[-1]['level'] and current_xp > scores[-1]['xp']):
            
            # Pedir nombre al jugador
            name = simpledialog.askstring("¡High Score!", "¡Entraste al Leaderboard!\nIngresa tu nombre:", parent=self.root)
            if not name:
                name = "Jugador Anónimo" # Nombre por defecto
            
            # Añadir la nueva puntuación
            scores.append({"name": name, "level": current_level, "xp": current_xp})
            
            # Ordenar: primero por Nivel (desc), luego por XP (desc)
            scores.sort(key=lambda s: (s['level'], s['xp']), reverse=True)
            
            # Mantener solo el Top 10
            scores = scores[:10]
            
            # Guardar la nueva lista
            self.save_leaderboard(scores)
            
            # Mostrar el leaderboard actualizado
            self.show_leaderboard()

    def show_leaderboard(self):
        """Muestra una ventana Toplevel con las puntuaciones."""
        lb_window = tk.Toplevel(self.root)
        lb_window.title("Leaderboard")
        lb_window.geometry("350x400")
        lb_window.resizable(False, False)
        
        # Hacer la ventana modal (bloquea la principal)
        lb_window.grab_set()
        lb_window.transient(self.root)

        tk.Label(lb_window, text="🏆 Mejores Puntuaciones 🏆", font=("Arial", 18, "bold")).pack(pady=10)
        
        scores_frame = tk.Frame(lb_window)
        scores_frame.pack(pady=10, fill="both", expand=True)

        scores = self.load_leaderboard()

        if not scores:
            tk.Label(scores_frame, text="No hay puntuaciones guardadas.", font=("Arial", 12)).pack(pady=20)
        else:
            for i, score in enumerate(scores):
                rank = i + 1
                name = score.get('name', 'N/A')
                level = score.get('level', 0)
                xp = score.get('xp', 0)
                
                text = f"{rank}. {name} - Nivel: {level} (XP: {xp})"
                font_weight = "bold" if rank <= 3 else "normal"
                
                tk.Label(scores_frame, text=text, font=("Arial", 12, font_weight)).pack(pady=3)
        
        tk.Button(lb_window, text="Cerrar", width=10, command=lb_window.destroy).pack(pady=10)


# === INICIAR JUEGO ===
if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGame(root)
    root.mainloop()