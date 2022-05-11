import tkinter as tk
from pathlib import Path
from camtrapml.dataset import ImageDataset
from os import walk
import tensorflow as tf

def enumerate_images(path):
    for root_dir, folders, files in walk(path):
        for file in files:
            if file.endswith('.jpg'):
                yield Path(root_dir) / file

def is_gpu_enabled():
    for dev in tf.config.list_logical_devices():
        if dev.device_type == 'GPU':
            return True
    return False

class MyApp(tk.Tk):

    def pick_folder(self):
        from tkinter import filedialog
        dir_path = filedialog.askdirectory(initialdir=Path('~').expanduser())

        if dir_path == '':
            return

        self.button.destroy()

        self.status = tk.Label(text='Enumerating Dataset\n\n0 images')
        self.status.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.image_paths = []
        for x in enumerate_images(dir_path):
            self.image_paths.append(x)
            
            if len(self.image_paths) % 100 == 0:
                self.status.config(text="Enumerating Dataset\n\n{} images".format(str(len(self.image_paths))))
                self.status.update()
        
        self.status.config(text="Enumerating Dataset\n\n{} images".format(str(len(self.image_paths))))
        self.status.update()

        self.load_detector()


    def load_detector(self):
        from camtrapml.detection.models.megadetector import MegaDetectorV4_1
        self.status.config(text="Loading Model")
        self.status.update()
        self.model = MegaDetectorV4_1()
        self.model.load_model()
        self.status.config(text="Loaded Model")
        self.status.update()

        self.process()

    def process(self):
        
        for i, image_path in enumerate(self.image_paths):
            self.status.config(text=f"Running Detection\n\n{i}/{len(self.image_paths)}")
            self.status.update()
            self.model.detect(image_path)
        


    def __init__(self):
        super().__init__()

        self.title("MegaDetector 4.1 Desktop")
        self.geometry("400x150")
        self.resizable(False, False)

        self.button = tk.Button(text="Choose Folder", command=self.pick_folder)
        self.button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        if is_gpu_enabled():
            self.gpu = tk.Label(text="⚡️ GPU Enabled ⚡️")
            self.gpu.pack(side=tk.BOTTOM)


if __name__ == "__main__":
    app = MyApp()
    app.mainloop()

