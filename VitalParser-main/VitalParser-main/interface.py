import matplotlib
matplotlib.use('TkAgg')

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Selector de Modo")
        self.geometry("1650x850")  # Ajustar a menor tamaño para evitar recortes

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (StartPage, RealTimePage, OfflinePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Button(self, text="Real Time", command=lambda: controller.show_frame(RealTimePage)).pack(pady=20)
        ttk.Button(self, text="Offline", command=lambda: controller.show_frame(OfflinePage)).pack()

class OfflinePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="Funcionalidad Offline aquí").pack(pady=30)
        ttk.Button(self, text="Volver", command=lambda: controller.show_frame(StartPage)).pack()

class RealTimePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="Visualización en Tiempo Real").pack(pady=2)

        selector_frame = tk.Frame(self)
        selector_frame.pack(pady=1)

        self.variable_options = ['Variable 1', 'Variable 2', 'Variable 3', 'Variable 4']
        self.selected_vars = []
        for i in range(4):
            label = ttk.Label(selector_frame, text=f"Variable gráfica {i+1}:")
            label.grid(row=0, column=i, padx=2)
            combo = ttk.Combobox(selector_frame, values=self.variable_options, state="readonly", width=14)
            combo.grid(row=1, column=i, padx=2)
            combo.current(i % len(self.variable_options))
            self.selected_vars.append(combo)
        for combo in self.selected_vars:
            combo.bind("<<ComboboxSelected>>", lambda e: self.draw_plots())

        # Botón Retrospective a la derecha del último combobox
        btn_retro = ttk.Button(selector_frame, text="Retrospective")
        btn_retro.grid(row=1, column=4, padx=15)

        plot_frame = tk.Frame(self)
        plot_frame.pack(fill="both", expand=True)

        # Tamaño compacto de subplots
        self.fig, self.axs = plt.subplots(2, 2, figsize=(12, 6.5), constrained_layout=True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.canvas.mpl_connect("button_press_event", self.on_graph_click)
        self.draw_plots()

    def draw_plots(self):
        for i in range(2):
            for j in range(2):
                ax = self.axs[i, j]
                ax.clear()
                var_name = self.selected_vars[i*2 + j].get()
                x = [1, 2, 3, 4, 5]
                y = [(i+1)*(j+1)*val for val in range(1, 6)]
                ax.plot(x, y)
                ax.set_title(var_name)
        self.canvas.draw()

    def on_graph_click(self, event):
        if event.inaxes:
            for i in range(2):
                for j in range(2):
                    if event.inaxes == self.axs[i, j]:
                        self.maximize_plot((i, j))

    def maximize_plot(self, idx):
        new_win = tk.Toplevel(self)
        new_win.title(f"Gráfica {idx[0]*2 + idx[1] + 1} - Ampliada")
        fig, ax = plt.subplots(figsize=(10, 8))
        var_name = self.selected_vars[idx[0]*2 + idx[1]].get()
        x = [1, 2, 3, 4, 5]
        y = [(idx[0]+1)*(idx[1]+1)*val for val in range(1, 6)]
        ax.plot(x, y)
        ax.set_title(var_name)
        canvas = FigureCanvasTkAgg(fig, master=new_win)
        canvas.get_tk_widget().pack()
        canvas.draw()

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
