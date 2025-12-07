import tkinter as tk
from datetime import datetime
from zoneinfo import ZoneInfo
import os
from tkinter import ttk
import vitaldb

BOXES_ROOT = "./Front/Boxes" #Ruta archivos de ejemplo

print("Ruta absoluta:", os.path.abspath(BOXES_ROOT))
if not os.path.isdir(BOXES_ROOT):
    print("NO existe ese directorio.")
else:
    print("Contenido de BOXES_ROOT:")
    for name in os.listdir(BOXES_ROOT):
        full = os.path.join(BOXES_ROOT, name)
        print("  ", name, "->", "dir" if os.path.isdir(full) else "file")


# 1) Ventana box + paciente
class BoxPatientWindow(tk.Toplevel):
    def __init__(self, master=None, boxes_root="./Boxes"):
        """
        boxes_root: directorio donde están las carpetas Box_1, Box_2, ...
        Dentro de cada Box_X hay subcarpetas de pacientes tipo UID1234, UIDXXXX, etc.
        """
        super().__init__(master)
        self.title("Selección de box y paciente")
        self.resizable(False, False)
        self.result = None

        self.boxes_root = boxes_root

        frame = tk.LabelFrame(self, text="Box y paciente")
        frame.pack(padx=20, pady=20)

        # --------- Selector de BOX ----------
        tk.Label(frame, text="Box:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.var_box = tk.StringVar()
        self.combo_box = ttk.Combobox(
            frame,
            textvariable=self.var_box,
            state="readonly",
            width=20,
        )
        self.combo_box.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Cargar boxes desde el sistema de archivos
        boxes = []
        if os.path.isdir(self.boxes_root):
            for name in os.listdir(self.boxes_root):
                full = os.path.join(self.boxes_root, name)
                if os.path.isdir(full) and name.startswith("Box_"):
                    boxes.append(name)
        boxes.sort()
        self.combo_box["values"] = boxes

        # --------- Selector de PACIENTE (UID...) ----------
        tk.Label(frame, text="Paciente (UID):").grid(
            row=1, column=0, padx=5, pady=5, sticky="e"
        )

        self.var_patient = tk.StringVar()
        self.combo_patient = ttk.Combobox(
            frame,
            textvariable=self.var_patient,
            state="readonly",
            width=20,
        )
        self.combo_patient.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Ahora que combo_patient existe, podemos cargar pacientes del primer box
        if boxes:
            self.combo_box.current(0)
            self.load_patients_for_box(boxes[0])

        # Cambiar pacientes cuando cambie el box
        self.combo_box.bind("<<ComboboxSelected>>", self.on_box_changed)

        # --------- Botones ----------
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Aceptar", width=10,
                  command=self.on_ok).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Cancelar", width=10,
                  command=self.on_cancel).pack(side="left", padx=5)

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.grab_set()
        self.focus_set()

    # --------- Helpers ---------
    def load_patients_for_box(self, box_name: str):
        """
        Lista subcarpetas de pacientes (UID...) dentro de boxes_root/box_name
        y las carga en el combobox de pacientes.
        """
        patients = []
        box_path = os.path.join(self.boxes_root, box_name)
        if os.path.isdir(box_path):
            for name in os.listdir(box_path):
                full = os.path.join(box_path, name)
                # Asumimos que cualquier carpeta que empieza por UID es un paciente
                if os.path.isdir(full) and name.startswith("UID"):
                    patients.append(name)
        patients.sort()
        self.combo_patient["values"] = patients
        if patients:
            self.combo_patient.current(0)
        else:
            self.combo_patient.set("")

    def on_box_changed(self, event=None):
        box_name = self.var_box.get()
        if box_name:
            self.load_patients_for_box(box_name)

    # --------- Callbacks OK / Cancel ---------
    def on_ok(self):
        box_id = self.var_box.get().strip()
        patient_id = self.var_patient.get().strip()

        if not box_id or not patient_id:
            # Aquí podrías añadir un messagebox.showerror si quieres obligar a elegir ambos
            return

        self.result = {
            "box_id": box_id,
            "patient_id": patient_id,
        }
        self.destroy()

    def on_cancel(self):
        self.result = None
        self.destroy()

# 2) Ventana selección archivo.vital

class SelectVitalWindow(tk.Toplevel):
    def __init__(self, master, boxes_root: str, box_id: str, patient_id: str):
        """
        Ventana para elegir qué archivo .vital analizar dentro de
        boxes_root/box_id/patient_id
        """
        super().__init__(master)
        self.title("Seleccionar archivo .vital")
        self.resizable(False, False)
        self.result = None

        self.boxes_root = boxes_root
        self.box_id = box_id
        self.patient_id = patient_id

        frame = tk.LabelFrame(self, text=f"Box: {box_id}  |  Paciente: {patient_id}")
        frame.pack(padx=20, pady=20)

        tk.Label(frame, text="Archivo .vital:").grid(
            row=0, column=0, padx=5, pady=5, sticky="e"
        )

        self.var_vital = tk.StringVar()
        self.combo_vital = ttk.Combobox(
            frame,
            textvariable=self.var_vital,
            state="readonly",
            width=40,
        )
        self.combo_vital.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Listar .vital en la carpeta Box_x/UIDxxxx
        vitals = []
        patient_path = os.path.join(self.boxes_root, box_id, patient_id)
        if os.path.isdir(patient_path):
            for name in os.listdir(patient_path):
                full = os.path.join(patient_path, name)
                if os.path.isfile(full) and name.lower().endswith(".vital"):
                    vitals.append(name)

        vitals.sort()
        self.combo_vital["values"] = vitals
        if vitals:
            self.combo_vital.current(0)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Aceptar", width=10,
                  command=self.on_ok).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Cancelar", width=10,
                  command=self.on_cancel).pack(side="left", padx=5)

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.grab_set()
        self.focus_set()

    def on_ok(self):
        vital_name = self.var_vital.get().strip()
        if not vital_name:
            return

        # ruta completa al .vital seleccionado
        vital_path = os.path.join(self.boxes_root, self.box_id, self.patient_id, vital_name)
        self.result = {
            "vital_name": vital_name,
            "vital_path": vital_path,
        }
        self.destroy()

    def on_cancel(self):
        self.result = None
        self.destroy()


# 3) Ventana algoritmos / constantes
from Algorithms.check_availability import check_availability

class SignalsWindow(tk.Toplevel):
    def __init__(self, master=None, vital_path: str | None = None):
        """
        vital_path: ruta al .vital seleccionado en la ventana anterior.
                    Se usa para obtener los algoritmos disponibles.
        """
        super().__init__(master)
        self.title("Selección de algoritmos y constantes")
        self.resizable(False, False)
        self.result = None

        # ---------------- Algoritmos según .vital ----------------
        if vital_path is not None:
            try:
                vf = vitaldb.VitalFile(vital_path)
                tracks = vf.get_track_names()
                algoritmos = check_availability(tracks)
            except Exception as e:
                print(f"Error obteniendo algoritmos de {vital_path}: {e}")
                algoritmos = []
        else:
            algoritmos = []

        if not algoritmos:
            algoritmos = ["No algorithms available in this file"]

        # ---------------- Constantes (como antes) ----------------

        tracks_sin_prefijo = [t.removeprefix("Intellivue/") for t in tracks]

        constantes = tracks_sin_prefijo

        # ---------------- UI listas ----------------
        lists_frame = tk.LabelFrame(self, text="Selección de señales")
        lists_frame.pack(side="top", pady=10, padx=10)

        # Algoritmos
        algo_frame = tk.Frame(lists_frame)
        algo_frame.grid(row=0, column=0, padx=5, pady=5)
        tk.Label(algo_frame, text="Algoritmos disponibles").pack(anchor="w")

        self.list_algos = tk.Listbox(
            algo_frame,
            selectmode="multiple",
            exportselection=False,
            height=min(12, len(algoritmos)),
            width=35,
        )
        self.list_algos.pack(side="left", fill="y")
        for item in algoritmos:
            self.list_algos.insert(tk.END, item)

        algo_scroll = tk.Scrollbar(
            algo_frame,
            orient="vertical",
            command=self.list_algos.yview,
        )
        algo_scroll.pack(side="right", fill="y")
        self.list_algos.config(yscrollcommand=algo_scroll.set)

        # Constantes
        const_frame = tk.Frame(lists_frame)
        const_frame.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(const_frame, text="Constantes").pack(anchor="w")

        self.list_consts = tk.Listbox(
            const_frame,
            selectmode="multiple",
            exportselection=False,
            height=min(12, len(constantes)),
            width=35,
        )
        self.list_consts.pack(side="left", fill="y")
        for item in constantes:
            self.list_consts.insert(tk.END, item)

        const_scroll = tk.Scrollbar(
            const_frame,
            orient="vertical",
            command=self.list_consts.yview,
        )
        const_scroll.pack(side="right", fill="y")
        self.list_consts.config(yscrollcommand=const_scroll.set)

        # Botones
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Seleccionar todo", width=15,
            command=self.select_all).pack(side="left", padx=5)

        tk.Button(btn_frame, text="Aceptar", width=10,
                  command=self.on_ok).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Cancelar", width=10,
                  command=self.on_cancel).pack(side="left", padx=5)

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.grab_set()
        self.focus_set()

    def select_all(self):
        """Selecciona todos los algoritmos y todas las constantes."""
        # Algoritmos
        self.list_algos.selection_set(0, tk.END)
        # Constantes
        self.list_consts.selection_set(0, tk.END)


    def on_ok(self):
        sel_algos = [self.list_algos.get(i) for i in self.list_algos.curselection()]
        sel_consts = [self.list_consts.get(i) for i in self.list_consts.curselection()]

        self.result = {
            "algoritmos": sel_algos,
            "constantes": sel_consts,
        }
        self.destroy()

    def on_cancel(self):
        self.result = None
        self.destroy()



# 4) Orquestador del wizard
def run_offline_wizard(root):
    # 1) Box + paciente
    win1 = BoxPatientWindow(master=root, boxes_root=BOXES_ROOT)
    root.wait_window(win1)
    if not win1.result:
        return None

    box_id = win1.result["box_id"]
    patient_id = win1.result["patient_id"]

    # 2) Archivo .vital
    win2 = SelectVitalWindow(
        master=root,
        boxes_root=BOXES_ROOT,
        box_id=box_id,
        patient_id=patient_id,
    )
    root.wait_window(win2)
    if not win2.result:
        return None

    vital_path = win2.result["vital_path"]
    print("Selected vital path:", vital_path)

    # 3) Algoritmos/Constantes DEPENDIENDO DEL .VITAL
    win3 = SignalsWindow(master=root, vital_path=vital_path)
    root.wait_window(win3)
    if not win3.result:
        return None

    data = {}
    data.update(win1.result)
    data.update(win2.result)
    data.update(win3.result)
    return data
