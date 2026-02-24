import gi
try:
    # Esto evita que la documentación falle si no encuentra GTK
    gi.require_version('Gtk', '3.0')
except (AttributeError, NameError, ValueError):
    pass

from gi.repository import Gtk, Pango
import os
from libreria_CabbaGG.conexionBD import ConexionBD

class BibliotecaApp(Gtk.Window):
    """
    Clase que define la ventana principal de la aplicación de gestión de biblioteca.

    Esta clase hereda de Gtk.Window y se encarga de gestionar la interfaz de usuario
    y la interacción directa con la base de datos de libros.
    """

    def __init__(self):
        """
        Inicializa la ventana principal, configura el diseño y establece la conexión
        inicial con la base de datos, asegurando la existencia de las tablas.
        """
        super().__init__(title="Gestión de Biblioteca Municipal")

        self.connect("destroy", Gtk.main_quit)

        self.set_default_size(800, 600)
        self.set_border_width(10)

        # Ruta de la base de datos
        print(f"Directorio actual: {os.getcwd()}")

        ruta_directorio = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(ruta_directorio, "biblioteca.db")
        self.db = ConexionBD(self.db_path)

        # CREAMOS LA TABLA SI NO EXISTE
        conn = self.db.conectaBD()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS libros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                autor TEXT NOT NULL,
                xenero TEXT,
                disponible INTEGER
            )
        """)
        conn.commit()
        # -----------------------------------------------

        # Layout Principal
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

        # --- SECCIÓN SUPERIOR: FORMULARIO (Gtk.Frame) ---
        frame_engadir = Gtk.Frame(label="Añadir Nuevo Libro")
        grid = Gtk.Grid(column_spacing=10, row_spacing=10, margin=10)
        frame_engadir.add(grid)

        self.entry_titulo = Gtk.Entry(placeholder_text="Título del libro")
        self.entry_autor = Gtk.Entry(placeholder_text="Autor")

        # ComboBox para Género
        self.combo_xenero = Gtk.ComboBoxText()
        for g in ["Narrativa", "Poesía", "Ensayo", "Ciencia Ficción"]:
            self.combo_xenero.append_text(g)
        self.combo_xenero.set_active(0)

        # RadioButtons para estado
        self.radio_si = Gtk.RadioButton.new_with_label(None, "Sí")
        self.radio_no = Gtk.RadioButton.new_with_label_from_widget(self.radio_si, "No")
        box_radio = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        box_radio.pack_start(self.radio_si, False, False, 0)
        box_radio.pack_start(self.radio_no, False, False, 0)

        grid.attach(Gtk.Label(label="Título:"), 0, 0, 1, 1)
        grid.attach(self.entry_titulo, 1, 0, 1, 1)
        grid.attach(Gtk.Label(label="Autor:"), 0, 1, 1, 1)
        grid.attach(self.entry_autor, 1, 1, 1, 1)
        grid.attach(Gtk.Label(label="Género:"), 2, 0, 1, 1)
        grid.attach(self.combo_xenero, 3, 0, 1, 1)
        grid.attach(Gtk.Label(label="Disponible:"), 2, 1, 1, 1)
        grid.attach(box_radio, 3, 1, 1, 1)

        btn_engadir = Gtk.Button(label="Guardar Libro")
        btn_engadir.connect("clicked", self.on_btn_engadir_clicked)
        grid.attach(btn_engadir, 4, 0, 1, 2)

        vbox.pack_start(frame_engadir, False, False, 0)

        # --- SECCIÓN CENTRAL: TREEVIEW (LISTA) ---
        self.model = Gtk.ListStore(int, str, str, str, bool)
        self.treeview = Gtk.TreeView(model=self.model)

        for i, title in enumerate(["ID", "Título", "Autor", "Género", "Disp."]):
            renderer = Gtk.CellRendererText()
            if i == 4:  # Renderizado especial para booleano
                renderer = Gtk.CellRendererToggle()
                col = Gtk.TreeViewColumn(title, renderer, active=i)
            else:
                col = Gtk.TreeViewColumn(title, renderer, text=i)
            self.treeview.append_column(col)

        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        scroll.add(self.treeview)
        vbox.pack_start(scroll, True, True, 0)

        # --- SECCIÓN INFERIOR: BOTONES CRUD ---
        hbox_btns = Gtk.Box(spacing=10)
        btn_editar = Gtk.Button(label="Editar Seleccionado")
        btn_editar.connect("clicked", self.on_btn_editar_clicked)
        btn_borrar = Gtk.Button(label="Eliminar Libro")
        btn_borrar.connect("clicked", self.on_btn_borrar_clicked)

        hbox_btns.pack_start(btn_editar, True, True, 0)
        hbox_btns.pack_start(btn_borrar, True, True, 0)
        vbox.pack_start(hbox_btns, False, False, 0)

        self.actualizar_lista()
        self.show_all()

    def amosar_dialogo(self, tipo, mensaxe):
        """
        Muestra un diálogo de información o error al usuario.

        :param tipo: El tipo de mensaje de GTK (Info, Error, Warning).
        :type tipo: Gtk.MessageType
        :param mensaxe: El texto del mensaje que se mostrará.
        :type mensaxe: str
        """
        dialogo = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=tipo,
            buttons=Gtk.ButtonsType.OK,
            text=mensaxe,
        )
        dialogo.run()
        dialogo.destroy()

    def actualizar_lista(self):
        """
        Consulta todos los registros de la tabla 'libros' y refresca el TreeView.
        Limpia el modelo de datos y lo vuelve a cargar desde la base de datos.
        """
        self.model.clear()
        conn = self.db.conectaBD()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM libros")
        for fila in cursor.fetchall():
            lista_fila = list(fila)
            if len(lista_fila) > 4:
                lista_fila[4] = bool(lista_fila[4])
            self.model.append(lista_fila)

    def on_btn_engadir_clicked(self, widget):
        """
        Manejador del evento de clic en el botón guardar. Inserta un nuevo libro en la base de datos.

        :param widget: El componente que dispara el evento.
        :type widget: Gtk.Button
        """
        titulo = self.entry_titulo.get_text()
        autor = self.entry_autor.get_text()
        xenero = self.combo_xenero.get_active_text()
        disp = 1 if self.radio_si.get_active() else 0

        if not titulo or not autor:
            self.amosar_dialogo(Gtk.MessageType.ERROR, "El título y el autor son obligatorios.")
            return

        conn = self.db.conectaBD()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO libros (titulo, autor, xenero, disponible) VALUES (?, ?, ?, ?)",
                       (titulo, autor, xenero, disp))
        conn.commit()
        self.actualizar_lista()
        self.amosar_dialogo(Gtk.MessageType.INFO, "Libro añadido con éxito.")

    def on_btn_borrar_clicked(self, widget):
        """
        Elimina el libro seleccionado en el TreeView previa confirmación del usuario.

        :param widget: El componente que dispara el evento.
        :type widget: Gtk.Button
        """
        selection = self.treeview.get_selection()
        model, treeiter = selection.get_selected()

        if treeiter is not None:
            id_libro = model[treeiter][0]

            confirm = Gtk.MessageDialog(transient_for=self, flags=0, message_type=Gtk.MessageType.QUESTION,
                                        buttons=Gtk.ButtonsType.YES_NO,
                                        text=f"¿Seguro que quieres borrar el ID {id_libro}?")
            res = confirm.run()
            confirm.destroy()

            if res == Gtk.ResponseType.YES:
                conn = self.db.conectaBD()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM libros WHERE id=?", (id_libro,))
                conn.commit()
                self.actualizar_lista()
        else:
            self.amosar_dialogo(Gtk.MessageType.WARNING, "Selecciona un libro primero.")

    def on_btn_editar_clicked(self, widget):
        """
        Obtiene los datos del libro seleccionado y abre el diálogo de edición.

        :param widget: El componente que dispara el evento.
        :type widget: Gtk.Button
        """
        selection = self.treeview.get_selection()
        model, treeiter = selection.get_selected()

        if treeiter is not None:
            datos = list(model[treeiter])
            dialogo = EdicionDialog(self, datos)
            # Iniciamos un bucle para validar antes de cerrar definitivamente
            while True:
                res = dialogo.run()

                if res == Gtk.ResponseType.OK:
                    novos_datos = dialogo.get_datos()

                    # Validación de campos vacíos
                    if not novos_datos[0].strip() or not novos_datos[1].strip():
                        error_dialog = Gtk.MessageDialog(
                            transient_for=dialogo,  # Importante: el padre es el diálogo de edición
                            modal=True,
                            message_type=Gtk.MessageType.ERROR,
                            buttons=Gtk.ButtonsType.OK,
                            text="Error de validación",
                            secondary_text="El título y el autor no pueden estar vacíos."
                        )
                        error_dialog.run()
                        error_dialog.destroy()
                        # No salimos del bucle, por lo que dialogo.run() se ejecutará de nuevo
                        continue

                        # Si pasa la validación, guardamos en BD
                    try:
                        conn = self.db.conectaBD()
                        cursor = conn.cursor()
                        cursor.execute("UPDATE libros SET titulo=?, autor=?, xenero=? WHERE id=?",
                                       (novos_datos[0], novos_datos[1], novos_datos[2], datos[0]))
                        conn.commit()
                        self.actualizar_lista()
                        break  # Salimos del bucle while porque todo salió bien
                    except Exception as e:
                        print(f"Error en la base de datos: {e}")
                        break
                else:
                    # Si el usuario pulsa Cancelar o cierra la ventana
                    break

            dialogo.destroy()


class EdicionDialog(Gtk.Dialog):
    """
    Clase que define un cuadro de diálogo para la edición de registros de libros.
    """

    def __init__(self, parent, datos):
        """
        Constructor del diálogo de edición.

        :param parent: Ventana padre de la que depende el diálogo.
        :type parent: Gtk.Window
        :param datos: Lista con los datos actuales del libro seleccionado.
        :type datos: list
        """
        super().__init__(title="Editar Libro", transient_for=parent, flags=0)
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_button(Gtk.STOCK_SAVE, Gtk.ResponseType.OK)

        # Dimensiones de la ventana de edicion
        self.set_default_size(250, -1)
        box = self.get_content_area()
        box.set_spacing(10)
        box.set_margin_start(15)
        box.set_margin_end(15)
        box.set_margin_top(15)
        box.set_margin_bottom(15)

        box = self.get_content_area()
        self.ent_t = Gtk.Entry(text=datos[1])
        self.ent_a = Gtk.Entry(text=datos[2])

        self.combo_xenero = Gtk.ComboBoxText()
        generos = ["Narrativa", "Poesía", "Ensayo", "Ciencia Ficción"]
        for g in generos:
            self.combo_xenero.append_text(g)

        # Seleccionar el género actual del libro
        if datos[3] in generos:
            self.combo_xenero.set_active(generos.index(datos[3]))
        else:
            self.combo_xenero.set_active(0)

        box.add(Gtk.Label(label="Nuevo Título:", xalign=0))
        box.add(self.ent_t)
        box.add(Gtk.Label(label="Nuevo Autor:", xalign=0))
        box.add(self.ent_a)
        box.add(Gtk.Label(label="Nuevo Género:", xalign=0))
        box.add(self.combo_xenero)
        self.show_all()

    def get_datos(self):
        """
        Recupera los valores introducidos por el usuario en los campos del diálogo.

        :return: Lista con el nuevo título, autor y género.
        :rtype: list
        """
        return [self.ent_t.get_text(), self.ent_a.get_text(), self.combo_xenero.get_active_text()]

def main():
    app = BibliotecaApp()
    Gtk.main()

if __name__ == "__main__":
    main()