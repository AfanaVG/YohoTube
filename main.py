import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pytube import YouTube
from threading import Thread
import os


class DownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Youtube Downloader")
        self.root.geometry("600x300")

        self.setup_ui()

    def setup_ui(self):
        # URL entry
        self.url_label = tk.Label(self.root, text="Ingresa la URL del video:")
        self.url_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.url_entry = tk.Entry(self.root, width=40)
        self.url_entry.grid(row=0, column=1, padx=10, pady=5)

        # Folder selection
        self.select_folder_button = tk.Button(self.root, text="Seleccionar carpeta", command=self.select_folder)
        self.select_folder_button.grid(row=0, column=2, padx=10, pady=5)
        self.path_label = tk.Label(self.root, text=default_download_path)
        self.path_label.grid(row=1, column=0, columnspan=3, padx=10, pady=0, sticky='w')

        # Download options
        self.download_type = tk.StringVar(value='Video')
        self.video_button = tk.Radiobutton(self.root, text="Video", variable=self.download_type, value='Video')
        self.audio_button = tk.Radiobutton(self.root, text="Audio", variable=self.download_type, value='Audio')
        self.video_button.grid(row=2, column=1, padx=10, pady=5, sticky='w')
        self.audio_button.grid(row=3, column=1, padx=10, pady=5, sticky='w')

        # Download button
        self.download_button = tk.Button(self.root, text="Descargar", command=self.start_download_thread)
        self.download_button.grid(row=4, column=1, pady=10)

        # Download status label
        self.status_label = tk.Label(self.root, text="", font=('Helvetica', 12))
        self.status_label.grid(row=5, column=1, pady=20)

    def select_folder(self):
        directory = filedialog.askdirectory()
        if directory:
            self.path_label.config(text=directory)
        else:
            self.path_label.config(text="No se ha seleccionado ningún directorio")

    def start_download_thread(self):
        url = self.url_entry.get()
        folder_path = self.path_label.cget("text")
        download_choice = self.download_type.get()

        if not url:
            messagebox.showerror("Error", "Por favor, introduce una URL válida.")
            return

        if not folder_path or folder_path == "No se ha seleccionado ningún directorio":
            folder_path = os.path.join(os.path.expanduser('~'), 'Downloads')

        Thread(target=self.descargar_video, args=(url, folder_path, download_choice)).start()

    def descargar_video(self, url, folder_path, download_choice):
        try:
            self.disable_widgets()
            self.status_label.config(text="Descargando...", fg="green")

            yt = YouTube(url)
            if download_choice == 'Video':
                stream = yt.streams.get_highest_resolution()
                file_extension = stream.mime_type.split('/')[-1]
            else:
                stream = yt.streams.get_audio_only()
                file_extension = 'mp3'

            output_file = stream.default_filename.replace(stream.default_filename.split('.')[-1], file_extension)
            final_path = os.path.join(folder_path, output_file)

            if os.path.exists(final_path):
                base, extension = os.path.splitext(final_path)
                i = 1
                while os.path.exists(f"{base}({i}){extension}"):
                    i += 1
                final_path = f"{base}({i}){extension}"

            stream.download(output_path=folder_path, filename=os.path.basename(final_path))
            messagebox.showinfo("Éxito", f"Descarga completada: {os.path.basename(final_path)}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.status_label.config(text="", fg="black")
            self.enable_widgets()

    def disable_widgets(self):
        self.url_entry.config(state="disabled")
        self.select_folder_button.config(state="disabled")
        self.video_button.config(state="disabled")
        self.audio_button.config(state="disabled")
        self.download_button.config(state="disabled")

    def enable_widgets(self):
        self.url_entry.config(state="normal")
        self.select_folder_button.config(state="normal")
        self.video_button.config(state="normal")
        self.audio_button.config(state="normal")
        self.download_button.config(state="normal")


if __name__ == "__main__":
    # Configuración de la carpeta de descargas por defecto
    default_download_path = os.path.join(os.path.expanduser('~'), 'Downloads')

    # Creación de la ventana principal
    root = tk.Tk()
    app = DownloaderApp(root)
    root.mainloop()
