import tkinter as tk
from pathlib import Path
from camtrapml.dataset import ImageDataset
from os import walk
from platform import system, machine
from warnings import warn
import tensorflow as tf

# Disable the GPU on M1 Macs as there appears to be a bug where the outputs are
# not the same as the reference implementation.
if system() == "Darwin" and machine() == "arm64":
    warn("Disabling GPU on M1 Macs")
    tf.config.set_visible_devices([], "GPU")

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

        self.dir_path = Path(dir_path)

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

        output_images = []
        
        for i, image_path in enumerate(self.image_paths):
            self.status.config(text=f"Running Detection\n\n{i}/{len(self.image_paths)}")
            self.status.update()

            detections = self.model.detect(image_path)
            for detection in detections:
                detection['conf'] = float(detection['conf'])
                for coord in detection['bbox']:
                    coord = float(coord)

            output_images.append({
                'file': str(image_path.relative_to(self.dir_path)),
                'detections': detections
            })
        
        self.status.config(text="Saving Output")
        self.status.update()

        from json import dump
        with open(self.dir_path / 'md.4.1.0.json', 'w') as f:
            dump(output_images, f)
        
        self.status.config(text="Saved Output")
        self.status.update()

        self.status.config(text="Done")
        self.status.update()

        from time import sleep
        sleep(4)

        self.destroy()


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

