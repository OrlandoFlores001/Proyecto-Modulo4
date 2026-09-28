# main.py
import tkinter as tk
from tkinter import messagebox, ttk
from models import ClienteRegular, ClientePremium, ClienteCorporativo, AdminMain
from basededatos import GestorPersistencia
from excepciones import ErrorGestionCliente

class VentanaLogin:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MachaTech - Iniciar Sesión")
        self.root.geometry("320x280")

        tk.Label(self.root, text="Gestión de Clientes", font=("Arial", 12, "bold")).pack(pady=10)
        
        tk.Label(self.root, text="RUT / Usuario:").pack()
        self.ent_rut = tk.Entry(self.root)
        self.ent_rut.pack(pady=5)

        tk.Label(self.root, text="Contraseña:").pack()
        self.ent_pass = tk.Entry(self.root, show="*")
        self.ent_pass.pack(pady=5)

        tk.Button(self.root, text="Ingresar", command=self.verificar_login, bg="lightblue", width=15).pack(pady=15)
        self.root.mainloop()

    def verificar_login(self):
        rut_ingresado = self.ent_rut.get().strip().replace(".", "").replace("-", "").upper()
        pass_ingresada = self.ent_pass.get().strip()

        if rut_ingresado == "12345678K" and pass_ingresada == "admin":
            usuario_actual = AdminMain("12345678K", "Admin Master", "admin@tech.com", "911111111", "admin")
            self.root.destroy()
            AppPrincipal(usuario_actual)
            return

        lista_clientes = GestorPersistencia.cargar_clientes()
        for cliente in lista_clientes:
            if cliente.rut == rut_ingresado and cliente.password == pass_ingresada:
                self.root.destroy()
                AppPrincipal(cliente)
                return

        messagebox.showerror("Error", "Credenciales incorrectas o usuario no registrado.")

class AppPrincipal:
    def __init__(self, usuario):
        self.usuario = usuario
        self.root = tk.Tk()
        self.root.title("MACHA-TECH COMPONENTES")
        self.root.geometry("720x680")

        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10, fill=tk.X, padx=20)
        tk.Label(top_frame, text=f"Usuario: {usuario.nombre} ({usuario.rol})", font=("Arial", 11, "bold")).pack(side=tk.LEFT)
        tk.Button(top_frame, text="Cerrar Sesión", command=self.cerrar_sesion, bg="#ffcccc").pack(side=tk.RIGHT)

        form_frame = tk.LabelFrame(self.root, text=" Formulario de Cliente ", padx=10, pady=10)
        form_frame.pack(pady=5, padx=20, fill=tk.X)

        tk.Label(form_frame, text="RUT:").grid(row=0, column=0, sticky="w")
        self.ent_rut = tk.Entry(form_frame, width=30)
        self.ent_rut.grid(row=0, column=1, pady=2)

        tk.Label(form_frame, text="Nombre:").grid(row=1, column=0, sticky="w")
        self.ent_nom = tk.Entry(form_frame, width=30)
        self.ent_nom.grid(row=1, column=1, pady=2)

        tk.Label(form_frame, text="Correo:").grid(row=2, column=0, sticky="w")
        self.ent_cor = tk.Entry(form_frame, width=30)
        self.ent_cor.grid(row=2, column=1, pady=2)

        tk.Label(form_frame, text="Teléfono:").grid(row=3, column=0, sticky="w")
        self.ent_tel = tk.Entry(form_frame, width=30)
        self.ent_tel.grid(row=3, column=1, pady=2)

        tk.Label(form_frame, text="Contraseña:").grid(row=4, column=0, sticky="w")
        self.ent_pwd = tk.Entry(form_frame, width=30, show="*")
        self.ent_pwd.grid(row=4, column=1, pady=2)

        tk.Label(form_frame, text="Tipo Cliente:").grid(row=5, column=0, sticky="w")
        self.rol_var = tk.StringVar(value="Regular")
        tk.OptionMenu(form_frame, self.rol_var, "Regular", "Premium", "Corporativo", "AdminMain").grid(row=5, column=1, sticky="w", pady=2)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        # Botón Guardar
        tk.Button(btn_frame, text="Guardar / Crear", command=self.guardar, bg="#d4edda", width=15).pack(side=tk.LEFT, padx=5)
        
        # Botón Eliminar (Deshabilitado si no tiene permiso)
        btn_eliminar = tk.Button(btn_frame, text="Eliminar", command=self.eliminar, bg="#f8d7da", width=15)
        if not usuario.puede_eliminar(): 
            btn_eliminar.config(state=tk.DISABLED)
        btn_eliminar.pack(side=tk.LEFT, padx=5)

        btn_vaciar = tk.Button(btn_frame, text="Vaciar BD", command=self.vaciar_base_datos, bg="#f5c6cb", width=15)
        if not getattr(usuario, 'puede_vaciar', lambda: False)():
            btn_vaciar.config(state=tk.DISABLED)
        btn_vaciar.pack(side=tk.LEFT, padx=5)

        columnas = ("rut", "nombre", "correo", "telefono", "rol")
        self.tabla = ttk.Treeview(self.root, columns=columnas, show="headings", height=10)
        for columna in columnas:
            self.tabla.heading(columna, text=columna.capitalize())
            self.tabla.column(columna, width=130)
        self.tabla.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        self.actualizar_lista()
        self.root.mainloop()

    def cerrar_sesion(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Desea salir del sistema?"):
            self.root.destroy()
            VentanaLogin()

    def limpiar_formulario(self):
        self.ent_rut.delete(0, tk.END)
        self.ent_nom.delete(0, tk.END)
        self.ent_cor.delete(0, tk.END)
        self.ent_tel.delete(0, tk.END)
        self.ent_pwd.delete(0, tk.END)
        self.rol_var.set("Regular")

    def guardar(self):
        try:
            rut = self.ent_rut.get()
            nombre = self.ent_nom.get()
            correo = self.ent_cor.get()
            telefono = self.ent_tel.get()
            password = self.ent_pwd.get()
            tipo_rol = self.rol_var.get()

            rol_actual = self.usuario.rol
            if rol_actual == "Regular" and tipo_rol != "Regular":
                raise ErrorGestionCliente("Un cliente Regular solo puede crear cuentas de tipo Regular.")
            elif rol_actual == "Premium" and tipo_rol not in ["Regular", "Premium"]:
                raise ErrorGestionCliente("Un cliente Premium no puede crear cuentas Corporativas o Admin.")
            elif rol_actual == "Corporativo" and tipo_rol == "AdminMain":
                raise ErrorGestionCliente("Un cliente Corporativo no puede crear cuentas de tipo AdminMain.")

            if tipo_rol == "Premium":
                cliente_nuevo = ClientePremium(rut, nombre, correo, telefono, password)
            elif tipo_rol == "Corporativo":
                cliente_nuevo = ClienteCorporativo(rut, nombre, correo, telefono, password)
            elif tipo_rol == "AdminMain":
                cliente_nuevo = AdminMain(rut, nombre, correo, telefono, password)
            else:
                cliente_nuevo = ClienteRegular(rut, nombre, correo, telefono, password)

            GestorPersistencia.agregar_cliente(cliente_nuevo)
            messagebox.showinfo("Éxito", "Cliente guardado correctamente.")
            self.limpiar_formulario()
            self.actualizar_lista()

        except ErrorGestionCliente as e:
            messagebox.showerror("Error de Permisos / Validación", str(e))
        except Exception as e:
            messagebox.showerror("Error Inesperado", str(e))

    def eliminar(self):
        try:
            seleccion = self.tabla.selection()
            if not seleccion:
                raise ErrorGestionCliente("Seleccione un registro de la tabla para eliminar.")
                
            valores_fila = self.tabla.item(seleccion[0])['values']
            rut_a_eliminar = str(valores_fila[0])
            rol_a_eliminar = str(valores_fila[4])

            rol_actual = self.usuario.rol

            if rol_a_eliminar == "AdminMain" and rol_actual != "AdminMain":
                raise ErrorGestionCliente("No tiene permisos para eliminar a un Administrador del sistema.")

            if rol_actual == "Premium" and rol_a_eliminar in ["Premium", "Corporativo", "AdminMain"]:
                raise ErrorGestionCliente("Una cuenta Premium solo puede eliminar cuentas de tipo Regular.")

            if rol_actual == "Corporativo" and rol_a_eliminar in ["Corporativo", "AdminMain"]:
                raise ErrorGestionCliente("Una cuenta Corporativa no puede eliminar administradores ni otros clientes corporativos.")

            if messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar al cliente con RUT {rut_a_eliminar}?"):
                GestorPersistencia.eliminar_cliente(rut_a_eliminar)
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
                self.actualizar_lista()

        except ErrorGestionCliente as e:
            messagebox.showerror("Permisos Insuficientes", str(e))
        except Exception as e:
            messagebox.showerror("Error Inesperado", f"No se pudo eliminar: {str(e)}")

    def vaciar_base_datos(self):
        confirmacion = messagebox.askokcancel(
            "¡ATENCIÓN!", 
            "¿Está completamente seguro de vaciar TODA la base de datos?\nEsta acción no se puede deshacer."
        )
        if confirmacion:
            GestorPersistencia.vaciar_bd()
            messagebox.showinfo("Éxito", "Base de datos vaciada correctamente.")
            self.actualizar_lista()

    def actualizar_lista(self):
        for elemento in self.tabla.get_children():
            self.tabla.delete(elemento)
            
        lista_clientes = GestorPersistencia.cargar_clientes()
        for cliente in lista_clientes:
            self.tabla.insert("", tk.END, values=(cliente.rut, cliente.nombre, cliente.correo, cliente.telefono, cliente.rol))

if __name__ == "__main__":
    VentanaLogin()