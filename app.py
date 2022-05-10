import tkinter as tk

# 
# 
# from camtrapml.image.utils import load_image
from PIL import ImageTk, Image
# import tensorflow


def donothing():
    print("I won't")

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()

        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=donothing)
        filemenu.add_command(label="Open", command=self.pick_image, accelerator="Command+O")
        filemenu.add_command(label="Save", command=donothing)
        filemenu.add_command(label="Save as...", command=donothing)
        filemenu.add_command(label="Close", command=self.destroy, accelerator="Command+Q")
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)

        



        self.title("CamTrap Workbench")
        self.geometry("900x900")
        
        self.bind("<Command-o>", lambda _: self.pick_image())
        self.bind("<Command-q>", lambda _: self.destroy())
        # self.resizable(False, False)



        # self.label = tk.Label(self, text="Hello World")
        # self.label.pack()

        # # Image Picker
        # self.image_picker = tk.Button(self, text="Pick Image", command=self.pick_image)
        # self.image_picker.pack()

        # Image Viewer
        # render = ImageTk.PhotoImage(Image.open("/Users/ben/Datasets/ENA24/ena24/3502.jpg"))
        self.image_viewer = tk.Canvas(self)
        self.image_viewer.place(x=0, y=0, relheight=100, relwidth=100)
        # self.image_viewer.image = render
        # self.image_viewer.pack()

        self.statusbar = tk.Label(self, text="", bd=10, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.statusbar.config(text=f"Loading MegaDetector v4.1")
        self.update()
        from camtrapml.detection.models.megadetector import MegaDetectorV4_1
        self.detector = MegaDetectorV4_1()
        self.detector.load_model()
        self.statusbar.config(text=f"Complete")
        self.update()
        



        
    
    def pick_image(self):
        
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(
          title="Select an image",
          initialdir="/Users/ben/Datasets/ENA24/ena24",
          filetypes=(("Image Files", ("*.jpg", "*.jpeg","*.png")), ("jpeg files", "*.jpeg"), ("All Files", "*.*"))
        )

        # User's canceleds the file selection
        if len(file_path) == 0:
            return

        self.statusbar.config(text=f"Loading {file_path}")
        self.update()

        from camtrapml.image.utils import load_image

        image = load_image(file_path)
        image.thumbnail((700, 700))
        image_render = ImageTk.PhotoImage(image)

        self.image_viewer.create_image(0, 0, image=image_render, anchor="nw")
        self.image_viewer.image = image_render
        self.update()

        
        from camtrapml.detection.utils import render_detections
        
        self.statusbar.config(text=f"Running MegaDetector v4.1")
        self.update()
        boxes = self.detector.detect(image)
            
        detection_image = render_detections(image, [box for box in boxes if box['conf'] >= .5], class_map=self.detector.class_map)
        detection_image.thumbnail((700, 700))
        detection_image_render = ImageTk.PhotoImage(detection_image)

        self.image_viewer.delete('all')
        self.image_viewer.create_image(0, 0, image=detection_image_render, anchor="nw")
        self.image_viewer.image = detection_image_render
        print(boxes)

        self.statusbar.config(text=f"Complete")
        self.update()

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()

