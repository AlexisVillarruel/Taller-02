import sys
import os
from PyQt6.QtWidgets import   QMessageBox, QApplication, QMainWindow, QListWidget, QListWidgetItem, QVBoxLayout, QPushButton, QWidget, QLabel, QMessageBox, QFileDialog
from PyQt6.QtGui import QPixmap,QIcon,QAction
from PIL import Image




def duplicate_frames(gif_path):
    if not os.path.exists(gif_path):
        print("El archivo GIF no existe.")
        return

    try:
        gif = Image.open(gif_path)
        frames = []

        # Obtener todos los frames del GIF
        while True:
            try:
                frame = gif.copy()
                frames.append(frame)
                gif.seek(gif.tell() + 1)
            except EOFError:
                break

        # Duplicar los frames
        duplicated_frames = []
        for frame in frames:
            for _ in range(2):  # Duplicar cada frame dos veces
                duplicated_frames.append(frame.copy())

        # Guardar el GIF duplicado
        duplicated_gif_path = gif_path.replace('.gif', '_duplicated.gif')

        # Obtener la duración del frame del GIF original
        duration = gif.info.get('duration', 100)  # Si no se puede obtener, usar 100 ms como valor predeterminado

        duplicated_frames[0].save(duplicated_gif_path, save_all=True, append_images=duplicated_frames[1:], loop=0, duration=duration)

        print(f"GIF duplicado guardado como: {duplicated_gif_path}")
        return duplicated_gif_path  # Devolver la ruta del GIF duplicado

    except Exception as e:
        print(f"Error al duplicar los frames del GIF: {e}")

# Clase para la ventana principal
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Crear gifS")
        self.resize(400, 200)  # Tamaño de la ventana principal (ancho x alto)
        self.setWindowIcon(QIcon("ico.png"))
        
        # Crear la cinta de opciones (menú)
        menu_bar = self.menuBar()
        help_menu=menu_bar.addMenu("Help")

        # Opción "Help" en la cinta de opciones
        about_action = QAction(QIcon("about.png"), "About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        create_gif_action = QAction(QIcon("info.png"), "Crear GIFs", self)
        create_gif_action.triggered.connect(self.show_help)
        help_menu.addAction(create_gif_action)

        # Botón para ordenar imágenes
        self.order_button = QPushButton("Ordenar Imágenes", self)
        self.order_button.setObjectName("orderButton")
        self.order_button.clicked.connect(self.order_images)
        self.order_button.resize(200, 50)
        self.order_button.move(20, 30)

        # Botón para duplicar frames de un GIF
        self.duplicate_button = QPushButton("Duplicar Frames de GIF", self)
        self.duplicate_button.setObjectName("duplicatebutton")
        self.duplicate_button.clicked.connect(self.duplicate_frames_wrapper)
        self.duplicate_button.move(20, 80)
        self.duplicate_button.resize(200, 50)

    def show_about(self):
        message="desarrollado por: asdasfasf"
        QMessageBox.about(self,"Acerca de",message)

    def show_help(self):
        message="Ayuda a ususario"
        QMessageBox.information(self,"Ayuda",message)

    def order_images(self):
        self.image_viewer = ImageViewer()
        self.image_viewer.resize(800, 600)  # Ajustar el tamaño inicial de la ventana principal
        self.image_viewer.show()

    def duplicate_frames_wrapper(self):
        gif_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar GIF", "", "GIF Files (*.gif)")
        if gif_path:
            try:
                duplicated_gif_path = duplicate_frames(gif_path)
                if duplicated_gif_path:
                    QMessageBox.information(self, "Éxito", "El GIF duplicado se guardó exitosamente")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al duplicar y guardar el GIF: {e}")

# Clase para la ventana de visualización de imágenes
class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Organizer")
        self.setWindowIcon(QIcon("ico.png"))

        self.image_paths = []

        self.layout = QVBoxLayout(self)

        self.image_list = QListWidget()
        self.image_list.setObjectName("lista")

        self.image_list.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.layout.addWidget(self.image_list)

        self.open_button = QPushButton("Abrir Imágenes", self)
        self.open_button.setObjectName("abrir")
        self.open_button.clicked.connect(self.open_images)
        self.layout.addWidget(self.open_button)

        self.save_button = QPushButton("Guardar Imágenes como GIF", self)
        self.save_button.setObjectName("guardar")
        self.save_button.clicked.connect(self.save_images)
        self.layout.addWidget(self.save_button)

        self.image_width = 400  # Ancho predefinido para las imágenes
        self.image_height = 300  # Alto predefinido para las imágenes



    def open_images(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Abrir Imágenes", "", "Images (*.jpg *.png *.jpeg)")

        for file_path in files:
            if os.path.exists(file_path):
                item = QListWidgetItem()

                # Crear QLabel para mostrar la imagen
                label = QLabel()
                pixmap = QPixmap(file_path)

                # Escalar la imagen al tamaño predefinido
                pixmap_scaled = pixmap.scaled(self.image_width, self.image_height)

                label.setPixmap(pixmap_scaled)

                # Configurar el widget personalizado como elemento del QListWidgetItem
                item.setSizeHint(label.sizeHint())  # Establecer el tamaño del ítem según el tamaño del QLabel
                self.image_list.addItem(item)
                self.image_list.setItemWidget(item, label)  # Asignar el QLabel como widget del ítem

                self.image_paths.append(file_path)
            else:
                print(f"Failed to load image: {file_path}")

    def save_images(self):
        if not self.image_paths:
            print("No hay imágenes para guardar.")
            return

        # Redimensionar todas las imágenes al mismo tamaño
        images = [Image.open(image_path).resize((self.image_width, self.image_height)) for image_path in self.image_paths]

        # Abrir y guardar las imágenes en un archivo .gif
        gif_path, _ = QFileDialog.getSaveFileName(self, "Guardar GIF", "", "GIF Files (*.gif)")
        if gif_path:
            images[0].save(gif_path, save_all=True, append_images=images[1:], loop=0, duration=500)
            print(f"Imágenes guardadas como {gif_path}")

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()

    style_sheet_file = "styles.css"
    with open(style_sheet_file, "r") as f:
        app.setStyleSheet(f.read())

    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
