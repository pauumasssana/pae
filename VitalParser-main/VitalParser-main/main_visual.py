import tkinter as tk
from Front.Interface import RealTimeApp
from Front.offline_windows import run_offline_wizard
from Front.offline_pipeline import run_offline_pipeline  # tu pipeline de .vital

# from Streaming import monitorizar_actualizacion_recurso
# from Algorithms import ejecutar_algoritmos


def seleccionar_modo_gui():
    try:
        import tkinter as tk
    except Exception:
        # Fallback a consola si no hay Tk
        try:
            return input("Selecciona modo (online/offline): ")
        except Exception:
            return None

    selection = {'mode': None}
    root = tk.Tk()
    root.title('Seleccionar modo')
    root.resizable(False, False)

    width = 300
    height = 120
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    root.geometry(f"{width}x{height}+{x}+{y}")

    def set_mode(m):
        selection['mode'] = m
        root.quit()

    lbl = tk.Label(root, text='Selecciona modo:')
    lbl.pack(pady=(12, 6))

    frm = tk.Frame(root)
    frm.pack(pady=(0, 8))

    btn_off = tk.Button(frm, text='Offline', width=10,
                        command=lambda: set_mode('offline'))
    btn_off.pack(side='left', padx=10)

    btn_on = tk.Button(frm, text='Online', width=10,
                       command=lambda: set_mode('online'))
    btn_on.pack(side='left', padx=10)

    root.protocol('WM_DELETE_WINDOW', lambda: set_mode(None))

    root.mainloop()
    try:
        root.destroy()
    except Exception:
        pass

    return selection['mode']


def main():
    # Bucle principal: mostrar selector repetidamente. Cuando la ventana
    # de la interfaz (modo online) se cierre, volvemos a mostrar el selector.
    while True:
        modo = seleccionar_modo_gui()

        if modo is None:
            print("No se seleccionó modo. Saliendo.")
            break

        if modo == "offline":
            print("Modo offline activado. Iniciando wizard offline...")

            root = tk.Tk()
            root.withdraw()

            result = run_offline_wizard(root)
            root.destroy()

            if result is None:
                print("Wizard cancelado. Volviendo al selector de modo.")
                continue

            box_id = result["box_id"]
            patient_id = result["patient_id"]
            vital_path = result["vital_path"]
            algos = result["algoritmos"]
            consts = result["constantes"]

            # Aquí lanzas el pipeline offline con todos los datos
            res = run_offline_pipeline(
                vital_path=vital_path,
                algoritmos=algos,
                constantes=consts,
            )

            print("Box:", box_id)
            print("Paciente:", patient_id)
            print("Vital seleccionado:", vital_path)
            print("Algoritmos .vital:", res["alg_vital_path"])
            print("Constantes .vital:", res["const_vital_path"])

            #Ejecutar VitalRecorder

            continue



        elif modo == "online":
            print("Modo online activado. Iniciando interfaz gráfica...")
            from Front.Interface import RealTimeApp
            app = RealTimeApp()
            # `app.mainloop()` bloqueará hasta que la ventana sea destruida;
            # al volver, el bucle repetirá y se mostrará el selector de modo.
            app.mainloop()
            print("Interfaz cerrada. Volviendo al selector de modo.")
            continue

        else:
            print("Modo no reconocido. Saliendo.")
            break


if __name__ == '__main__':
    main()
