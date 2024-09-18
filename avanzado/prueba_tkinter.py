import RCAC
import tkinter as tk
from tkinter import messagebox
import threading
import time
import entrenamiento  
import pymysql
def iniciar_captura():
    nombre_carpeta = codigo_est_entry.get()
    if not nombre_carpeta:
        messagebox.showerror("Error", "Debe ingresar un código de usuario.")
        return
    RCAC.ejecutar(nombre_carpeta)
    print("Captura de fotos iniciada...")

def mostrar_ventana_carga():
    carga_window = tk.Toplevel(root)
    carga_window.geometry("400x200")
    carga_window.title("Cargando...")
    carga_window.config(bg="#2C2C34")
    
    carga_label = tk.Label(
        carga_window,
        text="Entrenando, por favor espere...",
        bg="#2C2C34",
        fg="#FFFFFF",
        font=("Garamond", 16)
    )
    carga_label.pack(pady=20)
    
    carga_barra = tk.Canvas(carga_window, width=300, height=20, bg="#3A3A42", bd=0, highlightthickness=0)
    carga_barra.pack(pady=10)
    
    carga_progreso = carga_barra.create_rectangle(0, 0, 0, 20, fill="#6D28D9")
    
    carga_window.update()
    
    return carga_window, carga_barra, carga_progreso

def actualizar_barra_progreso(carga_window, carga_barra, carga_progreso):
    for i in range(100):
        carga_barra.coords(carga_progreso, 0, 0, 3 * i, 20)
        carga_window.update()
        time.sleep(0.05)

def finalizar_entrenamiento(carga_window):
    carga_window.destroy()
    messagebox.showinfo("Entrenamiento Completo", "El entrenamiento se ha completado exitosamente.")

def iniciar_entrenamiento():
    carga_window, carga_barra, carga_progreso = mostrar_ventana_carga()
    
    def entrenamiento_thread():
        try:
            actualizar_barra_progreso(carga_window, carga_barra, carga_progreso)  
            entrenamiento.ejecutar_entrenamiento()
            root.after(0, finalizar_entrenamiento, carga_window)
        except Exception as e:
            print(f"Error en entrenamiento: {str(e)}")
    
    threading.Thread(target=entrenamiento_thread).start()

def on_enter(event, button):
    button.config(bg="#B257F4", fg="#2C2C34")

def on_leave(event, button):
    button.config(bg="#6D28D9", fg="#FFFFFF")
 
def crear_boton(root, text, command):
    button = tk.Button(
        root, 
        text=text, 
        command=command, 
        font=("Garamond", 18), 
        bg="#6D28D9",  
        fg="#FFFFFF",
        activebackground="#B257F4", 
        activeforeground="#2C2C34", 
        bd=0, 
        padx=20, 
        pady=10,
        relief="flat",
        highlightthickness=0,
        cursor="hand2"
    )
    button.bind("<Enter>", lambda event: on_enter(event, button))
    button.bind("<Leave>", lambda event: on_leave(event, button))
    button.pack(pady=10)  
    
    return button

# Función para abrir la ventana principal de captura de datos y entrenamiento
def abrir_ventana_principal():
    global root
    root = tk.Toplevel(ventana_bienvenida)
    root.geometry("1200x650")
    root.resizable(True , True)
    root.config(bg="#2C2C34")
    root.title("Eye System")

    title_label = tk.Label(
        root, 
        text="Bienvenido a Eye System", 
        bg="#2C2C34", 
        fg="#E8E8E8",  
        font=("Garamond", 36, "italic")
    )
    title_label.pack(pady=20)

    subtitle_label = tk.Label(
        root, 
        text="Estás en el mejor reconocedor facial del colegio, optimizado para ofrecerte la mejor experiencia.",
        bg="#2C2C34",
        fg="#C0C0C0",
        font=("Garamond", 18),
        wraplength=800
    )
    subtitle_label.pack(pady=10)


    main_frame = tk.Frame(root, bg="#2C2C34")
    main_frame.pack(fill="both", expand=True, padx=20, pady=10)

    student_info_frame = tk.Frame(main_frame, bg="#3A3A42", highlightbackground="#2C2C34", highlightthickness=1)
    student_info_frame.pack(fill="x", pady=10)

    tk.Label(student_info_frame, text="Información del Estudiante:", bg="#3A3A42", fg="#FFFFFF", font=("Garamond", 16)).pack()
    
    codigo_est_label = tk.Label(student_info_frame, text="Código del Estudiante:", bg="#3A3A42", fg="#FFFFFF", font=("Garamond", 14))
    codigo_est_label.pack(side=tk.LEFT, expand=True, padx=5, pady=5)

    global codigo_est_entry
    codigo_est_entry = tk.Entry(student_info_frame, font=("Garamond", 14), width=6, bg="#4F4F4F", fg="#FFFFFF", bd=0, insertbackground="#FFFFFF")
    codigo_est_entry.pack(side=tk.LEFT, expand=True, padx=5, pady=5)

    apellidos_label = tk.Label(student_info_frame, text="Apellidos:", bg="#3A3A42", fg="#FFFFFF", font=("Garamond", 14))
    apellidos_label.pack(side=tk.LEFT, expand=True, padx=5, pady=5)
    
    global apellidos_entry
    apellidos_entry = tk.Entry(student_info_frame, font=("Garamond", 14), width=20, bg="#4F4F4F", fg="#FFFFFF", bd=0, insertbackground="#FFFFFF")
    apellidos_entry.pack(side=tk.LEFT, expand=True, padx=5, pady=5)

    nombres_label = tk.Label(student_info_frame, text="Nombres:", bg="#3A3C44", fg="#FFFFFF", font=("Garamond", 14))
    nombres_label.pack(side=tk.LEFT, expand=True, padx=5, pady=5)
    
    global nombres_entry
    nombres_entry = tk.Entry(student_info_frame, font=("Garamond", 14), width=20, bg="#4F4F4F", fg="#FFFFFF", bd=0, insertbackground="#FFFFFF")
    nombres_entry.pack(side=tk.LEFT, expand=True, padx=5, pady=5)

    grupo_label = tk.Label(student_info_frame, text="Grupo:", bg="#3A3C44", fg="#FFFFFF", font=("Garamond", 14))
    grupo_label.pack(side=tk.LEFT, expand=True, padx=5, pady=5)
    
    global grupo_entry
    grupo_entry = tk.Entry(student_info_frame, font=("Garamond", 14), width=6, bg="#4F4F4F", fg="#FFFFFF", bd=0, insertbackground="#FFFFFF")
    grupo_entry.pack(side=tk.LEFT, expand=True, padx=5, pady=5)

    jornada_label = tk.Label(student_info_frame, text="Jornada:", bg="#3A3C44", fg="#FFFFFF", font=("Garamond", 14))
    jornada_label.pack(side=tk.LEFT, fill="x", expand=True, padx=5, pady=5)
    
    global jornada_var
    jornada_var = tk.StringVar()
    jornada_option = tk.OptionMenu(student_info_frame, jornada_var, "Mañana", "Tarde")
    jornada_option.pack(side=tk.LEFT, fill="x", expand=True, padx=5, pady=5)

    capture_button = crear_boton(root, "Iniciar Captura", iniciar_captura)
    train_button = crear_boton(root, "Iniciar Entrenamiento", iniciar_entrenamiento)

    footer_frame = tk.Frame(root, bg="#2C2C34")
    footer_frame.pack(side="bottom", pady=20)

    footer_label = tk.Label(
        footer_frame, 
        text="Eye System - reconocimiento facial", 
        bg="#2C2C34", 
        fg="#F4F4F4",  
        font=("Garamond", 18, "bold italic"),
        padx=10, pady=5
    )
    footer_label.pack()

    additional_label = tk.Label(
        footer_frame, 
        text="Colegio San José de Guanentá", 
        bg="#2C2C34", 
        fg="#DCDCDC",  
        font=("Garamond", 14, "italic"),
        padx=10, pady=5
    )
    additional_label.pack()
    
    def guardar_datos():
        global codigo_est_entry, apellidos_entry, nombres_entry, grupo_entry, jornada_var
    
        try:
            conn = pymysql.connect(host='localhost', user='root', db='asistencia')
        
            cur = conn.cursor()
        
            sql = "INSERT INTO estudiante (codigo_est, apellidos, nombres, grupo, jornada) VALUES (%s, %s, %s, %s, %s)"
        
            cur.execute(sql, (
                codigo_est_entry.get(),
                apellidos_entry.get(),
                nombres_entry.get(),
                grupo_entry.get(),
                jornada_var.get()
            ))
        
            conn.commit()
            messagebox.showinfo("Datos Guardados", "Los datos del estudiante han sido guardados correctamente.")
        
        except Exception as e:
            print(f"Ocurrió un error al guardar los datos: {str(e)}")
        finally:
            if conn.open:
                cur.close()
                conn.close()
    guardar_button = crear_boton(root, text="Guardar Datos", command=guardar_datos)
    guardar_button.pack()

    root.mainloop()

def mostrar_ventana_error():
    def volver_a_intentar():
        error_window.destroy()
        abrir_ventana_password() 

    error_window = tk.Toplevel(ventana_bienvenida)
    error_window.geometry("400x200")
    error_window.title("Error")
    error_window.config(bg="#2C2C34")
    
    error_label = tk.Label(
        error_window,
        text="Contraseña incorrecta. Inténtelo de nuevo.",
        bg="#2C2C34",
        fg="#FFFFFF",
        font=("Garamond", 16)
    )
    error_label.pack(pady=20)
    
    retry_button = tk.Button(
        error_window,
        text="Volver a Intentar",
        command=volver_a_intentar,
        font=("Garamond", 14),
        bg="#6D28D9",
        fg="#FFFFFF",
        activebackground="#B257F4",
        activeforeground="#2C2C34",
        bd=0,
        padx=10,
        pady=5,
        relief="flat"
    )
    retry_button.pack(pady=20)
    
    error_window.mainloop()

def abrir_ventana_password():
    password_window = tk.Toplevel(ventana_bienvenida)
    password_window.geometry("400x200")
    password_window.title("Ingrese la contraseña")
    password_window.config(bg="#2C2C34")

    label = tk.Label(
        password_window, 
        text="Ingrese la contraseña:", 
        bg="#2C2C34", 
        fg="#FFFFFF",  
        font=("Garamond", 16)
    )
    label.pack(pady=20)

    password_entry = tk.Entry(
        password_window, 
        show="*", 
        font=("Garamond", 16), 
        justify="center", 
        width=20, 
        bg="#3A3A42", 
        fg="#FFFFFF", 
        bd=0,
        insertbackground="#FFFFFF"  
    )
    password_entry.pack(pady=10)

    def verificar_contraseña():
        if password_entry.get() == "sis2021":
            password_window.destroy()
            abrir_ventana_principal()
        else:
            password_window.destroy()
            mostrar_ventana_error()  

    btn_verificar = crear_boton(password_window, "Verificar", verificar_contraseña)
    password_window.mainloop()

def abrir_ventana_crear_cuenta():
    crear_cuenta_window = tk.Toplevel(ventana_bienvenida)
    crear_cuenta_window.geometry("400x350")
    crear_cuenta_window.title("Crear Cuenta")
    crear_cuenta_window.config(bg="#2C2C34")

    tk.Label(
        crear_cuenta_window,
        text="Crear Cuenta",
        bg="#2C2C34",
        fg="#E8E8E8",
        font=("Garamond", 20, "bold")
    ).pack(pady=10)

    tk.Label(
        crear_cuenta_window,
        text="Correo Electrónico:",
        bg="#2C2C34",
        fg="#FFFFFF",
        font=("Garamond", 14)
    ).pack(pady=5)
    
    correo_entry = tk.Entry(
        crear_cuenta_window,
        font=("Garamond", 14),
        bg="#3A3A42",
        fg="#FFFFFF",
        bd=0,
        insertbackground="#FFFFFF"
    )
    correo_entry.pack(pady=5)

    tk.Label(
        crear_cuenta_window,
        text="Contraseña:",
        bg="#2C2C34",
        fg="#FFFFFF",
        font=("Garamond", 14)
    ).pack(pady=5)
    
    contraseña_entry = tk.Entry(
        crear_cuenta_window,
        show="*",
        font=("Garamond", 14),
        bg="#3A3A42",
        fg="#FFFFFF",
        bd=0,
        insertbackground="#FFFFFF"
    )
    contraseña_entry.pack(pady=5)
    
    def guardar_info():
        correo = correo_entry.get()
        contraseña = contraseña_entry.get()
        
        try:
             conn = pymysql.connect(host='localhost', user='root', db='asistencia')
        
             cur = conn.cursor()
        
             sql = "INSERT INTO usuario (correo, password) VALUES (%s, %s)"
           
             cur.execute(sql, (correo, contraseña))
        
             conn.commit()
        
             messagebox.showinfo("Cuenta Creada", "Cuenta creada exitosamente.")
             
             crear_cuenta_window.destroy()
        
        except Exception as e:
             print(f"Ocurrió un error: {e}")
        finally:
             if conn.open:
                 cur.close()
                 conn.close()

    crear_cuenta_btn = crear_boton(crear_cuenta_window, text="Crear Cuenta", command=guardar_info)
    crear_cuenta_btn.pack(pady=10)

    cancelar_btn = crear_boton(crear_cuenta_window, text="Cancelar", command=crear_cuenta_window.destroy)
    cancelar_btn.pack(pady=10)

def mostrar_ventana_inicio_sesion():
    inicio_sesion_window = tk.Toplevel(ventana_bienvenida)
    inicio_sesion_window.geometry("400x300")
    inicio_sesion_window.title("Iniciar Sesión")
    inicio_sesion_window.config(bg="#2C2C34")

    tk.Label(
        inicio_sesion_window,
        text="Iniciar Sesión",
        bg="#2C2C34",
        fg="#E8E8E8",
        font=("Garamond", 20, "bold")
    ).pack(pady=10)

    tk.Label(
        inicio_sesion_window,
        text="Correo Electrónico:",
        bg="#2C2C34",
        fg="#FFFFFF",
        font=("Garamond", 14)
    ).pack(pady=5)
    
    id_entry = tk.Entry(
        inicio_sesion_window,
        font=("Garamond", 14),
        bg="#3A3A42",
        fg="#FFFFFF",
        bd=0,
        insertbackground="#FFFFFF"
    )
    id_entry.pack(pady=5)

    tk.Label(
        inicio_sesion_window,
        text="Contraseña:",
        bg="#2C2C34",
        fg="#FFFFFF",
        font=("Garamond", 14)
    ).pack(pady=5)
    
    contraseña_entry = tk.Entry(
        inicio_sesion_window,
        show="*",
        font=("Garamond", 14),
        bg="#3A3A42",
        fg="#FFFFFF",
        bd=0,
        insertbackground="#FFFFFF"
    )
    contraseña_entry.pack(pady=5)

    def iniciar_sesion():
        email_docente = id_entry.get()
        contraseña = contraseña_entry.get()

        try:
            # Establecer la conexión a la base de datos
            conn = pymysql.connect(host='localhost', user='root', db='asistencia')
            
            # Crear un objeto cursor
            cur = conn.cursor()
            
            # Preparar la consulta SQL para verificar los datos de inicio de sesión
            sql = "SELECT * FROM usuario WHERE correo = %s AND password = %s"
            
            # Ejecutar la consulta SQL con los valores obtenidos de los campos de entrada
            cur.execute(sql, (email_docente, contraseña))
            
            # Obtener el resultado de la consulta
            resultado = cur.fetchone()
            
            # Verificar si se obtuvo algún resultado
            if resultado:
                messagebox.showinfo("Inicio de Sesión", "Sesión iniciada exitosamente.")
                
                nueva_ventana = tk.Toplevel(ventana_bienvenida)
                nueva_ventana.title("Ventana nueva")
                nueva_ventana.geometry("750x300")
                tk.Label(
        nueva_ventana,
        text="ESTA EN PROCESO... AGRADECEMOS SU COMPRENSIÓN",
        bg="#8A09E6",
        fg="#E8E8E8",
        font=("Garamond", 20, "bold")
    ).pack(pady=10)
                
                inicio_sesion_window.destroy()
            else:
                messagebox.showerror("Error", "Correo electrónico o contraseña incorrectos.")
                
        except Exception as e:
            print(f"Ocurrió un error: {e}")
        finally:
            # Cerrar la conexión a la base de datos
            if conn.open:
                cur.close()
                conn.close()

    iniciar_sesion_btn = crear_boton(inicio_sesion_window, text="Iniciar Sesión", command=iniciar_sesion)
    iniciar_sesion_btn.pack(pady=10)



ventana_bienvenida = tk.Tk()
ventana_bienvenida.geometry("1200x650")
ventana_bienvenida.resizable(True, True)
ventana_bienvenida.config(bg="#2C2C34")
ventana_bienvenida.title("Eye System")

tk.Label(
    ventana_bienvenida,
    text="¡Bienvenido a Eye System!",
    bg="#2C2C34",
    fg="#E8E8E8",
    font=("Garamond", 36, "italic")
).pack(pady=10)

tk.Label(
    ventana_bienvenida,
    text="Estás en el mejor reconocedor facial del colegio, optimizado para ofrecerte la mejor experiencia.",
    bg="#2C2C34",
    fg="#C0C0C0",
    font=("Garamond", 18),
    wraplength=800
).pack(pady=10)

crear_boton(ventana_bienvenida, "Iniciar Sesión",mostrar_ventana_inicio_sesion)
crear_boton(ventana_bienvenida, "Crear Cuenta", abrir_ventana_crear_cuenta)
crear_boton(ventana_bienvenida, "Tomar Datos", abrir_ventana_password)

footer_frame = tk.Frame(ventana_bienvenida, bg="#2C2C34")
footer_frame.pack(side="bottom", pady=20)

footer_label = tk.Label(
    footer_frame,
    text="Eye System - reconocimiento facial",
    bg="#2C2C34",
    fg="#F4F4F4",
    font=("Garamond", 18, "bold italic"),
    padx=10, pady=5
)
footer_label.pack()

additional_label = tk.Label(
    footer_frame,
    text="Colegio San José de Guanentá",
    bg="#2C2C34",
    fg="#DCDCDC",
    font=("Garamond", 14, "italic"),
    padx=10, pady=5
)
additional_label.pack()

ventana_bienvenida.mainloop()