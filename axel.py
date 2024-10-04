import tkinter as tk
from tkinter import messagebox, PhotoImage
from datetime import datetime
from tkinter import simpledialog
from tkcalendar import Calendar
from tkinter import ttk

# Inicializar la ventana principal
ventana = tk.Tk()
ventana.title("Lista de Tareas")
ventana.geometry("400x500")

# Cargar la imagen de fondo
imagen_fondo = PhotoImage(file="logo Cteisa (2).png")  # Asegúrate de que la ruta sea correcta

# Crear un canvas para poner la imagen de fondo
canvas = tk.Canvas(ventana, width=400, height=500)
canvas.pack(fill="both", expand=True)

# Mostrar la imagen de fondo
canvas.create_image(0, 0, image=imagen_fondo, anchor="nw")

# Lista para almacenar las tareas con fecha de entrega
tareas = []

# Función para abrir el calendario y elegir fecha y hora
def elegir_fecha_hora():
    ventana_calendario = tk.Toplevel(ventana)
    ventana_calendario.title("Seleccionar fecha y hora")
    
    # Crear un widget de calendario
    cal = Calendar(ventana_calendario, selectmode="day", date_pattern="dd-mm-yyyy")
    cal.pack(pady=10)
    
    # Widget para seleccionar la hora
    horas_var = tk.StringVar()
    horas = ttk.Combobox(ventana_calendario, textvariable=horas_var, values=[f"{i:02d}" for i in range(24)], width=3)
    horas.set("00")
    horas.pack(side=tk.LEFT, padx=5)

    minutos_var = tk.StringVar()
    minutos = ttk.Combobox(ventana_calendario, textvariable=minutos_var, values=[f"{i:02d}" for i in range(60)], width=3)
    minutos.set("00")
    minutos.pack(side=tk.LEFT, padx=5)

    def obtener_fecha_hora():
        fecha_seleccionada = cal.get_date()
        hora_seleccionada = horas_var.get()
        minutos_seleccionados = minutos_var.get()
        fecha_hora_completa = f"{fecha_seleccionada} {hora_seleccionada}:{minutos_seleccionados}"
        try:
            fecha_obj = datetime.strptime(fecha_hora_completa, "%d-%m-%Y %H:%M")
            ventana_calendario.destroy()  # Cerrar ventana del calendario
            return fecha_obj
        except ValueError:
            messagebox.showwarning("Advertencia", "Fecha u hora no válida.")
            return None

    # Botón para confirmar la selección
    boton_confirmar = tk.Button(ventana_calendario, text="Confirmar", command=obtener_fecha_hora)
    boton_confirmar.pack(pady=10)

    ventana_calendario.grab_set()
    ventana.wait_window(ventana_calendario)
    return obtener_fecha_hora()

# Función para agregar una tarea
def agregar_tarea():
    tarea = entrada_tarea.get()
    if tarea != "":
        # Pedir la fecha de entrega usando el calendario
        fecha_entrega = elegir_fecha_hora()
        if fecha_entrega:
            tareas.append((tarea, fecha_entrega))
            actualizar_lista()
            entrada_tarea.delete(0, tk.END)
    else:
        messagebox.showwarning("Advertencia", "No puedes agregar una tarea vacía.")
        
# Función para actualizar la lista de tareas en la interfaz
def actualizar_lista():
    lista_tareas.delete(0, tk.END)
    for tarea, fecha in tareas:
        lista_tareas.insert(tk.END, f"{tarea} (Entrega: {fecha.strftime('%d-%m-%Y %H:%M')})")
    actualizar_barra_estado()

# Función para eliminar la tarea seleccionada
def eliminar_tarea():
    try:
        indice = lista_tareas.curselection()[0]
        del tareas[indice]
        actualizar_lista()
    except IndexError:
        messagebox.showwarning("Advertencia", "Por favor selecciona una tarea para eliminar.")
        
# Función para marcar una tarea como completada
def marcar_completada():
    try:
        indice = lista_tareas.curselection()[0]
        tarea, fecha_entrega = tareas[indice]
        
        # Verificar si la tarea ha caducado
        ahora = datetime.now()
        if ahora > fecha_entrega:
            messagebox.showwarning("Advertencia", f"La tarea '{tarea}' ha caducado. Su fecha de entrega era {fecha_entrega.strftime('%d-%m-%Y %H:%M')}.")
        
        tareas[indice] = (tarea + " (Completada)", fecha_entrega)
        actualizar_lista()
    except IndexError:
        messagebox.showwarning("Advertencia", "Por favor selecciona una tarea para marcar como completada.")
        
# Función para limpiar todas las tareas
def limpiar_tareas():
    global tareas
    confirmacion = messagebox.askyesno("Confirmación", "¿Estás seguro de que deseas eliminar todas las tareas?")
    if confirmacion:
        tareas = []
        actualizar_lista()

# Crear los elementos de la interfaz sobre el canvas
etiqueta_tarea = tk.Label(ventana, text="Nueva tarea:")
canvas.create_window(200, 100, window=etiqueta_tarea)

entrada_tarea = tk.Entry(ventana, width=40)
canvas.create_window(200, 130, window=entrada_tarea)

boton_agregar = tk.Button(ventana, text="Agregar tarea", command=agregar_tarea)
canvas.create_window(200, 160, window=boton_agregar)

lista_tareas = tk.Listbox(ventana, width=50, height=10)
canvas.create_window(200, 260, window=lista_tareas)

boton_eliminar = tk.Button(ventana, text="Eliminar tarea", command=eliminar_tarea)
canvas.create_window(200, 320, window=boton_eliminar)

boton_completar = tk.Button(ventana, text="Marcar como completada", command=marcar_completada)
canvas.create_window(200, 350, window=boton_completar)

boton_limpiar = tk.Button(ventana, text="Eliminar todas las tareas", command=limpiar_tareas)
canvas.create_window(200, 380, window=boton_limpiar)

# Agregar una barra de estado para mostrar el total de tareas
barra_estado = tk.Label(ventana, text="Total de tareas: 0", bd=1, relief=tk.SUNKEN, anchor=tk.W)
barra_estado.pack(side=tk.BOTTOM, fill=tk.X)

# Función para actualizar la barra de estado
def actualizar_barra_estado():
    barra_estado.config(text=f"Total de tareas: {len(tareas)}")

# Función para cerrar el programa con confirmación
def cerrar_programa():
    confirmacion = messagebox.askyesno("Confirmación", "¿Estás seguro de que deseas salir?")
    if confirmacion:
        ventana.destroy()

# Configurar el botón de cerrar ventana con confirmación
ventana.protocol("WM_DELETE_WINDOW", cerrar_programa)

# Función para guardar las tareas en un archivo
def guardar_tareas():
    with open("tareas.txt", "w") as archivo:
        for tarea, fecha_entrega in tareas:
            archivo.write(f"{tarea},{fecha_entrega.strftime('%d-%m-%Y %H:%M')}\n")
    messagebox.showinfo("Información", "Las tareas han sido guardadas en 'tareas.txt'.")

# Función para cargar tareas desde un archivo
def cargar_tareas():
    try:
        with open("tareas.txt", "r") as archivo:
            for linea in archivo:
                tarea, fecha_entrega = linea.strip().split(",")
                fecha_obj = datetime.strptime(fecha_entrega, "%d-%m-%Y %H:%M")
                tareas.append((tarea, fecha_obj))
        actualizar_lista()
    except FileNotFoundError:
        messagebox.showwarning("Advertencia", "No se encontró un archivo de tareas.")

# Crear menú para guardar y cargar tareas
menu_barra = tk.Menu(ventana)
ventana.config(menu=menu_barra)

menu_archivo = tk.Menu(menu_barra, tearoff=0)
menu_barra.add_cascade(label="Archivo", menu=menu_archivo)
menu_archivo.add_command(label="Guardar tareas", command=guardar_tareas)
menu_archivo.add_command(label="Cargar tareas", command=cargar_tareas)
menu_archivo.add_separator()
menu_archivo.add_command(label="Salir", command=cerrar_programa)

# Iniciar la ventana principal
ventana.mainloop()