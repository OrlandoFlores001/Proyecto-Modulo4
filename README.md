# MACHA-TECH COMPONENTES - Gestor Inteligente de Clientes

Proyecto corregido y desarrollado para el Módulo 4 de Programación Avanzada en Python, enfocado en **Programación Orientada a Objetos (POO)**, arquitectura modular, encapsulación estricta y persistencia de datos.

## 🛠️ Estructura del Código Modularizado
- **'excepciones.py'**: Define la jerarquía de excepciones personalizadas para el control de errores del sistema (`ErrorGestionCliente`, `RutInvalidoError`, `TelefonoInvalidoError`, etc.).
- **'validaciones.py'**: Métodos estáticos de validación de formato para RUT, Correo y Teléfono.
- **'models.py'**: Modelado de dominio con encapsulación estricta (`__rut`, `@property`, `@setter`), herencia (`ClienteRegular`, `ClientePremium`, `ClienteCorporativo`, `AdminMain`), polimorfismo y métodos especiales (`__str__`, `__eq__`).
- **'basededatos.py'**: Gestor de persistencia que opera la lectura, escritura y borrado directo sobre `clientes.txt`.
- **'main.py'**: Interfaz gráfica en Tkinter con control de acceso, jerarquía de permisos por rol e interacción dinámica.

## 🔑 Credenciales de Acceso Maestro
- **RUT / Usuario:** '12345678K'
- **Contraseña:** 'admin'

## 🚀 Cómo ejecutar
`bash`
python main.py