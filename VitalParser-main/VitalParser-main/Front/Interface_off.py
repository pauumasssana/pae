import matplotlib
matplotlib.use('TkAgg')

import tkinter as tk
from tkinter import ttk
from datetime import datetime


class OfflineSelector(tk.Tk):
    """
    Wizard Modo Offline:
      Tab 1: selección de box e ID de paciente
      Tab 2: fecha/hora de INICIO y FIN
      Tab 3: selección de Algoritmos y Constantes

    self.result al cerrar con Aceptar:
      {
        "box": str,
        "patient_id": str,
        "start_datetime": datetime,
        "end_datetime": datetime,
        "algoritmos": [str],
        "constantes": [str],
      }
    """
    def __init__(self,
                 algoritmos=None,
                 constantes=None,
                 initial_start=None,
                 initial_end=None):
        super().__init__()
        self.title("Modo Offline")
        self.geometry("950x450")

        self.result = None

        # ---------------- Datos por defecto ----------------
        if algoritmos is None:
            algoritmos = [
                "ShockIndex",
                "DrivingPressure",
                "DynamicCompliance",
                "ROXIndex",
                "TempTrend",
                "CardiacIndex",
            ]

        if constantes is None:
            constantes = [
                "ABP", "ABP_DIA", "ABP_HR", "ABP_MEAN", "ABP_SYS", "AOP",
                "ART", "ART_DIA", "ART_MEAN", "ART_SYS",
                "AWAY_CO2_ET", "AWAY_CO2_INSP_MIN", "AWP_WAV",
                "BP_DIA", "BP_MEAN", "BP_SYS",
                "BT_BLD", "BT_CORE", "BT_SKIN",
                "CARD_FUNC_INDEX", "CI", "CI_CTS",
                "CO", "CO2", "CO_CTS",
                "CVP", "CVP_DIA", "CVP_MEAN", "CVP_SYS",
                "ECG_AI_WAV", "ECG_AS_WAV", "ECG_AVF", "ECG_AVL", "ECG_AVR",
                "ECG_AVR_WAV", "ECG_ES_WAV", "ECG_HR",
                "ECG_I", "ECG_II", "ECG_III",
                "ECG_III_WAV", "ECG_II_WAV", "ECG_I_WAV",
                "ECG_MCL", "ECG_V", "ECG_VPC_CNT", "ECG_V_WAV",
                "EEG", "EEG_BIS", "EEG_BIS_ASYM", "EEG_BIS_SQI",
                "EEG_RATIO_SUPPRN", "EMG_ELEC_POTL_MUSCL",
                "FIO2", "FLOW_WAV", "FRACT_EJECT", "HR",
                "ICP", "ICP_MEAN", "LAP_MEAN",
                "MV_EXP", "MV_INSP",
                "NIBP_DIA", "NIBP_HR", "NIBP_MEAN", "NIBP_SYS",
                "PAP_DIA", "PAP_MEAN", "PAP_SYS",
                "PEEP_CMH2O", "PIP_CMH2O",
                "PLETH", "PLETH_HR", "PLETH_PERF_REL", "PLETH_SAT_O2",
                "PPLAT_CMH2O", "PPV",
                "PRESS_CEREB_PERF", "PTC_CNT",
                "RESP", "RR",
                "ST_AVF", "ST_AVL", "ST_AVR",
                "ST_I", "ST_II", "ST_III", "ST_INDEX",
                "ST_MCL", "ST_V", "ST_V1", "ST_V2", "ST_V3", "ST_V4", "ST_V5", "ST_V6",
                "TEMP",
                "TOF1", "TOF2", "TOF3", "TOF4", "TOF_CNT", "TOF_RATIO",
                "TV_EXP", "TV_INSP",
                "VENT_RR", "VENT_RR_SPONT",
                "VOL_BLD_INTRA_THOR", "VOL_BLD_INTRA_THOR_INDEX",
                "VOL_BLD_STROKE", "VOL_BLD_STROKE_INDEX", "VOL_BLD_STROKE_VAR",
                "VOL_GLOBAL_END_DIA", "VOL_GLOBAL_END_DIA_INDEX",
                "VOL_LUNG_WATER_EXTRA_VASC", "VOL_LUNG_WATER_EXTRA_VASC_INDEX",
            ]

        now = datetime.now()
        if initial_start is None:
            initial_start = now
        if initial_end is None:
            initial_end = now

        # ---------------- Notebook con 3 pestañas ----------------
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=5, pady=5)

        tab_box = ttk.Frame(notebook)
        tab_time = ttk.Frame(notebook)
        tab_signals = ttk.Frame(notebook)

        notebook.add(tab_box, text="1. Box e ID")
        notebook.add(tab_time, text="2. Intervalo tiempo")
        notebook.add(tab_signals, text="3. Señales")

        # =========================================================
        # TAB 1: Box e ID
        # =========================================================
        self.var_box = tk.StringVar()
        self.var_patient_id = tk.StringVar()

        frame_box = tk.LabelFrame(tab_box, text="Selección de box e ID")
        frame_box.pack(padx=20, pady=20, fill="x")

        tk.Label(frame_box, text="Box:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_box = tk.Entry(frame_box, textvariable=self.var_box, width=20)
        self.entry_box.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(frame_box, text="ID paciente:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_patient = tk.Entry(frame_box, textvariable=self.var_patient_id, width=20)
        self.entry_patient.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # =========================================================
        # TAB 2: Fechas inicio / fin
        # =========================================================
        top_time = tk.Frame(tab_time)
        top_time.pack(pady=10)

        # INICIO
        start_frame = tk.LabelFrame(top_time, text="Fecha y hora INICIO")
        start_frame.pack(side="left", padx=10)

        for idx, txt in enumerate(["Año", "Mes", "Día", "Hora", "Min", "Seg"]):
            tk.Label(start_frame, text=txt).grid(row=0, column=idx, padx=2, pady=2)

        self.var_s_year = tk.IntVar(value=2025)
        self.var_s_month = tk.IntVar(value=10)
        self.var_s_day = tk.IntVar(value=23)
        self.var_s_hour = tk.IntVar(value=8)
        self.var_s_min = tk.IntVar(value=20)
        self.var_s_sec = tk.IntVar(value=54)

        tk.Spinbox(start_frame, from_=2000, to=2100, width=5,
                   textvariable=self.var_s_year).grid(row=1, column=0, padx=2)
        tk.Spinbox(start_frame, from_=1, to=12, width=3,
                   textvariable=self.var_s_month).grid(row=1, column=1, padx=2)
        tk.Spinbox(start_frame, from_=1, to=31, width=3,
                   textvariable=self.var_s_day).grid(row=1, column=2, padx=2)
        tk.Spinbox(start_frame, from_=0, to=23, width=3,
                   textvariable=self.var_s_hour).grid(row=1, column=3, padx=2)
        tk.Spinbox(start_frame, from_=0, to=59, width=3,
                   textvariable=self.var_s_min).grid(row=1, column=4, padx=2)
        tk.Spinbox(start_frame, from_=0, to=59, width=3,
                   textvariable=self.var_s_sec).grid(row=1, column=5, padx=2)

        # FIN
        end_frame = tk.LabelFrame(top_time, text="Fecha y hora FIN")
        end_frame.pack(side="left", padx=10)

        for idx, txt in enumerate(["Año", "Mes", "Día", "Hora", "Min", "Seg"]):
            tk.Label(end_frame, text=txt).grid(row=0, column=idx, padx=2, pady=2)

        self.var_e_year = tk.IntVar(value=2025)
        self.var_e_month = tk.IntVar(value=10)
        self.var_e_day = tk.IntVar(value=23)
        self.var_e_hour = tk.IntVar(value=8)
        self.var_e_min = tk.IntVar(value=20)
        self.var_e_sec = tk.IntVar(value=58)

        tk.Spinbox(end_frame, from_=2000, to=2100, width=5,
                   textvariable=self.var_e_year).grid(row=1, column=0, padx=2)
        tk.Spinbox(end_frame, from_=1, to=12, width=3,
                   textvariable=self.var_e_month).grid(row=1, column=1, padx=2)
        tk.Spinbox(end_frame, from_=1, to=31, width=3,
                   textvariable=self.var_e_day).grid(row=1, column=2, padx=2)
        tk.Spinbox(end_frame, from_=0, to=23, width=3,
                   textvariable=self.var_e_hour).grid(row=1, column=3, padx=2)
        tk.Spinbox(end_frame, from_=0, to=59, width=3,
                   textvariable=self.var_e_min).grid(row=1, column=4, padx=2)
        tk.Spinbox(end_frame, from_=0, to=59, width=3,
                   textvariable=self.var_e_sec).grid(row=1, column=5, padx=2)

        # =========================================================
        # TAB 3: Algoritmos y Constantes
        # =========================================================
        lists_frame = tk.LabelFrame(tab_signals, text="Selección de señales")
        lists_frame.pack(side="top", pady=10, padx=10)

        # Algoritmos
        algo_frame = tk.Frame(lists_frame)
        algo_frame.grid(row=0, column=0, padx=5, pady=5)
        tk.Label(algo_frame, text="Algoritmos").pack(anchor="w")

        self.list_algos = tk.Listbox(
            algo_frame,
            selectmode="multiple",
            exportselection=False,
            height=min(12, len(algoritmos)),
            width=30
        )
        self.list_algos.pack(side="left", fill="y")

        for item in algoritmos:
            self.list_algos.insert(tk.END, item)

        algo_scroll = tk.Scrollbar(algo_frame, orient="vertical",
                                   command=self.list_algos.yview)
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
            width=35
        )
        self.list_consts.pack(side="left", fill="y")

        for item in constantes:
            self.list_consts.insert(tk.END, item)

        const_scroll = tk.Scrollbar(const_frame, orient="vertical",
                                    command=self.list_consts.yview)
        const_scroll.pack(side="right", fill="y")
        self.list_consts.config(yscrollcommand=const_scroll.set)

        # ----------------- Botones globales -----------------
        btn_frame = tk.Frame(self)
        btn_frame.pack(side="bottom", pady=5)

        btn_ok = tk.Button(btn_frame, text="Aceptar", width=12,
                           command=self.on_ok)
        btn_ok.pack(side="left", padx=5)

        btn_back = tk.Button(btn_frame, text="Volver", width=12,
                             command=self.on_cancel)
        btn_back.pack(side="left", padx=5)

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)

    # =======================================================
    # Callbacks
    # =======================================================
    def on_ok(self):
        from datetime import datetime

        try:
            start_dt = datetime(
                year=self.var_s_year.get(),
                month=self.var_s_month.get(),
                day=self.var_s_day.get(),
                hour=self.var_s_hour.get(),
                minute=self.var_s_min.get(),
                second=self.var_s_sec.get(),
            )
            end_dt = datetime(
                year=self.var_e_year.get(),
                month=self.var_e_month.get(),
                day=self.var_e_day.get(),
                hour=self.var_e_hour.get(),
                minute=self.var_e_min.get(),
                second=self.var_e_sec.get(),
            )
        except ValueError:
            return

        sel_algos = [self.list_algos.get(i)
                     for i in self.list_algos.curselection()]
        sel_consts = [self.list_consts.get(i)
                      for i in self.list_consts.curselection()]

        box_id = self.var_box.get().strip()
        patient_id = self.var_patient_id.get().strip()

        self.result = {
            "box_id": box_id,
            "patient_id": patient_id,
            "start_datetime": start_dt,
            "end_datetime": end_dt,
            "algoritmos": sel_algos,
            "constantes": sel_consts,
        }

        self.quit()
        self.destroy()


    def on_cancel(self):
        self.result = None
        self.quit()
        self.destroy()
