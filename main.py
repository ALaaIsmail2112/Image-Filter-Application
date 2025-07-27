import tkinter as tk
from tkinter import filedialog ,messagebox
from PIL import Image, ImageTk
import os

from filters import(diagonal_Filter, increase_brightness, decrease_brightness, 
 negative_Filter, PowerLow_Filter,logTransformation_Filter , 
 PowerLow_Log , Average_Filter , Maxmimun_Filter , Minmium_Filter , 
 Median_Filter ,Sobel_Filter , Prewitt_Filter , Histogram_Equalization , histogram_matching_algorithm)

class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Filter Application")  

        #  upload original image
        self.image_path = None
        self.original_image = None
        self.current_image = None

        # Title
        self.title_label = tk.Label(self.root, text="Image Filter Editor", font=("Arial", 24, "bold"), fg="#800080")
        self.title_label.grid(row=0, column=0, columnspan=5, pady=20)  # وضع العنوان في أعلى الشاشة

        # make frame for origianl image
        self.frame_before = tk.Frame(self.root)
        self.frame_before.grid(row=1, column=0, padx=20, pady=10)

        self.canvas_before = tk.Canvas(self.frame_before, width=300, height=400)
        self.canvas_before.pack()

        # make frame for filtered image
        self.frame_after = tk.Frame(self.root)
        self.frame_after.grid(row=1, column=1, padx=20, pady=10)

        self.canvas_after = tk.Canvas(self.frame_after, width=300, height=400)
        self.canvas_after.pack()

        #make border for images Canvas_before و canvas_after
        self.canvas_before.create_rectangle(5, 5, 295, 395, outline="#800080", width=4) 
        self.canvas_after.create_rectangle(5, 5, 295, 395, outline="#800080", width=4)  

        # Buttons
        self.frame_buttons = tk.Frame(self.root)
        self.frame_buttons.grid(row=2, column=0, columnspan=2, pady=10, padx=10)

        self.filter_button_brightness = tk.Button(self.frame_buttons, text="Increasing Brightness", command=self.increase_brightness, bg="#800080", fg="white", relief="flat", borderwidth=2, width=18, height=2)
        self.filter_button_brightness.grid(row=0, column=0, padx=10, pady=5)

        self.filter_button_gray = tk.Button(self.frame_buttons, text="Decrease Brightness", command=self.decrease_brightness, bg="#800080", fg="white", relief="flat", borderwidth=2, width=18, height=2)
        self.filter_button_gray.grid(row=0, column=1, padx=10, pady=5)

        self.filter_button_sepia = tk.Button(self.frame_buttons, text="Negative Filter", command=self.negative_Filter, bg="#800080", fg="white", relief="flat", borderwidth=2, width=18, height=2)
        self.filter_button_sepia.grid(row=0, column=2, padx=10, pady=5)

        self.filter_button_negative = tk.Button(self.frame_buttons, text="Power Low Filter", command=self.PowerLow_Filter, bg="#800080", fg="white", relief="flat", borderwidth=2, width=18, height=2)
        self.filter_button_negative.grid(row=0, column=3, padx=10, pady=5)

        self.filter_button_powerlow = tk.Button(self.frame_buttons, text="Log Transformation", command=self.logTransformation_Filter, bg="#800080", fg="white", relief="flat", borderwidth=2, width=18, height=2)
        self.filter_button_powerlow.grid(row=0, column=4, padx=10, pady=5)

        # أزرار الفلاتر في الصف الثاني (3 أزرار متمركزة في المنتصف)
        # self.filter_button_log = tk.Button(self.frame_buttons, text="Average Filter", command=self.Average_Filter, bg="#800080", fg="white", relief="flat", borderwidth=2, width=18, height=2)
        # self.filter_button_log.grid(row=1, column=1, padx=10, pady=5)

        self.filter_button_average = tk.Button(self.frame_buttons, text="Average Filter", command=self.Average_Filter, bg="#800080", fg="white", relief="flat", borderwidth=2, width=18, height=2)
        self.filter_button_average.grid(row=1, column=2, padx=10, pady=5)

        self.filter_button_powerlowlog = tk.Button(self.frame_buttons, text="Maxmimun Filter", command=self.Maxmimun_Filter, bg="#800080", fg="white", relief="flat", borderwidth=2, width=18, height=2)
        self.filter_button_powerlowlog.grid(row=1, column=3, padx=10, pady=5)

     
        self.filter_button_custom1 = tk.Button(self.frame_buttons, text="Minimum Filter", command=self.Minmium_Filter, bg="#800080", fg="white", relief="flat", borderwidth=2, width=18, height=2)
        self.filter_button_custom1.grid(row=2, column=0, padx=10, pady=5)

        self.filter_button_custom2 = tk.Button(self.frame_buttons, text="Histogram Matching", command=self.histogram_matching_m, bg="#800080", fg="white", relief="flat", borderwidth=2, width=18, height=2)
        self.filter_button_custom2.grid(row=2, column=1, padx=10, pady=5)

        self.matching_button = tk.Button(self.frame_buttons, text="Median Filter", command=self.Median_Filter, bg="#800080", fg="white", width=20, height=2)
        self.matching_button.grid(row=1, column=1, padx=10, pady=5)

        self.filter_button_custom3 = tk.Button(self.frame_buttons, text="Histogram Equalizationr", command=self.Histogram_Equalization, bg="#800080", fg="white", relief="flat", borderwidth=2, width=18, height=2)
        self.filter_button_custom3.grid(row=2, column=2, padx=10, pady=5)

        self.filter_button_custom4 = tk.Button(self.frame_buttons, text="Sobel Filter", command=self.Sobel_Filter, bg="#800080", fg="white", relief="flat", borderwidth=2, width=18, height=2)
        self.filter_button_custom4.grid(row=2, column=3, padx=10, pady=5)

        self.filter_button_custom5 = tk.Button(self.frame_buttons, text="Prewitt Filter", command=self.Prewitt_Filter, bg="#800080", fg="white", relief="flat", borderwidth=2, width=18, height=2)
        self.filter_button_custom5.grid(row=2, column=4, padx=10, pady=5)

        # button for upload image
        self.load_button = tk.Button(self.frame_buttons, text="Load Image", command=self.load_image, bg="#808080", fg="white", relief="flat", borderwidth=2, width=20, height=2)
        self.load_button.grid(row=3, column=0, padx=10, pady=20)  # الصف الرابع، أول عمود

        self.reset_button = tk.Button(
         self.frame_buttons, 
        text="Reset Image", 
        command=self.reset_image, 
        bg="#FFFF00", 
        fg="black",    
        relief="flat", 
        borderwidth=2, 
        width=18, 
        height=2
        )
        self.reset_button.grid(row=3, column=1, padx=10, pady=20)


        self.launch_filter_window_button = tk.Button(self.frame_buttons, text="Launch Filter on DataSet", command=self.launch_filter_window, bg="#000000", fg="white", relief="flat", borderwidth=2, width=18, height=2)
        self.launch_filter_window_button.grid(row=3, column=3, padx=10, pady=20) 

        # button for save image
        self.save_button = tk.Button(self.frame_buttons, text="Save Image", command=self.save_image, bg="#808080", fg="white", relief="flat", borderwidth=2, width=20, height=2)
        self.save_button.grid(row=3, column=4, padx=10, pady=20)  # الصف الرابع، آخر عمود

        self.frame_buttons.grid_rowconfigure(0, weight=1)
        self.frame_buttons.grid_columnconfigure(0, weight=1)

    def load_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if self.image_path:
            self.original_image = Image.open(self.image_path).convert("L") 
            self.current_image = self.original_image
            self.display_images()  

    def reset_image(self):
            if self.original_image:
                self.current_image = self.original_image 
                self.display_images() 
    def display_images(self):
        # Display the original image in the first window
        original_image_resized = self.original_image.resize((300, 400), Image.LANCZOS)  # Change here
        original_image_tk = ImageTk.PhotoImage(original_image_resized)
        self.canvas_before.create_image(0, 0, anchor=tk.NW, image=original_image_tk)
        self.canvas_before.image = original_image_tk
        
        # Display the modified image in the second window
        current_image_resized = self.current_image.resize((300, 400), Image.LANCZOS)
        current_image_tk = ImageTk.PhotoImage(current_image_resized)
        self.canvas_after.create_image(0, 0, anchor=tk.NW, image=current_image_tk)
        self.canvas_after.image = current_image_tk
    
    def launch_filter_window(self):
        self.folder_path = tk.StringVar()

       
        self.filter_window = tk.Toplevel(self.root)
        self.filter_window.title("Filter Application")
        self.filter_window.geometry("500x400")
        self.filter_window.configure(bg="#f0f0f0")  
       
        tk.Label(self.filter_window, text="Filter Application", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333333").pack(pady=15)

        
        folder_frame = tk.Frame(self.filter_window, bg="#f0f0f0")
        folder_frame.pack(pady=10)

        tk.Label(folder_frame, text="Select Folder:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(folder_frame, textvariable=self.folder_path, width=30, font=("Arial", 10), state="readonly").grid(row=0, column=1, padx=10)
        tk.Button(folder_frame, text="Browse", command=self.browse_folder, bg="#808080", fg="white", width=15).grid(row=0, column=2, padx=10)

       
        filter_frame = tk.Frame(self.filter_window, bg="#f0f0f0")
        filter_frame.pack(pady=20)

        tk.Label(filter_frame, text="Choose Filter:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, columnspan=2, pady=5)

        self.selected_filter = tk.StringVar(value="None")
        filters = [
                ("Sobel Filter", "sobel"), 
                ("Increase Brightness", "brightness"),
                ("Histogram Equalization", "histogram_equalization")
            ]


        for idx, (filter_name, filter_value) in enumerate(filters):
            tk.Radiobutton(filter_frame, text=filter_name, variable=self.selected_filter, value=filter_value, 
                        bg="#f0f0f0", fg="#333333", font=("Arial", 10)).grid(row=idx + 1, column=0, sticky="w", padx=20, pady=5)

       
        button_frame = tk.Frame(self.filter_window, bg="#f0f0f0")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Apply Now", command=self.apply_selected_filter, bg="green", fg="white", width=15, height=1).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Save Image", command=self.save_image, bg="blue", fg="white", width=15, height=1).grid(row=0, column=1, padx=10)

   
        tk.Label(self.filter_window, text="", bg="#f0f0f0").pack(pady=10)

       
        tk.Label(self.filter_window, text="", bg="#f0f0f0").pack(pady=10)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)
            messagebox.showinfo("Folder Selected", f"Selected Folder: {folder_selected}")

    def apply_selected_filter(self):
        folder = self.folder_path.get()
        chosen_filter = self.selected_filter.get()

        if not folder:
            messagebox.showwarning("Warning", "Please select a folder!")
            return

        if chosen_filter not in ["sobel", "brightness", "histogram_equalization"]:
            messagebox.showwarning("Warning", "Please choose a filter!")
            return

        for filename in os.listdir(folder):
            if filename.endswith((".png", ".jpg", ".jpeg", ".bmp")):
                file_path = os.path.join(folder, filename)
                image = Image.open(file_path).convert("L")  # Convert to grayscale

                # Apply the selected filter
                if chosen_filter == "sobel":
                    image = Sobel_Filter(image)
                elif chosen_filter == "brightness":
                    image = increase_brightness(image)
                elif chosen_filter == "histogram_equalization":
                    image = Histogram_Equalization(image)  # Apply the Histogram Equalization filter

                # Save the modified image
                save_path = os.path.join(folder, f"filtered_{filename}")
                image.save(save_path)

        messagebox.showinfo("Success", "Filter applied to all images in the folder!")

    def diagonal_Filter(self):
        if self.current_image:
            self.current_image = diagonal_Filter(self.current_image) 
            self.display_images()
    
    def increase_brightness(self):
        if self.current_image:
            self.current_image = increase_brightness(self.current_image) 
            self.display_images()
    
    def decrease_brightness(self):
        if self.current_image:
            self.current_image = decrease_brightness(self.current_image)  
            self.display_images()

    def negative_Filter(self):
        if self.current_image:
            self.current_image = negative_Filter(self.current_image)  
            self.display_images()
    
    def PowerLow_Filter(self):
        if self.current_image:
            self.current_image = PowerLow_Filter(self.current_image) 
            self.display_images()
    
    def PowerLow_Log(self):
        if self.current_image:
            self.current_image = PowerLow_Log(self.current_image) 
            self.display_images()
    
    def logTransformation_Filter(self):
        if self.current_image:
            self.current_image = logTransformation_Filter(self.current_image)  
            self.display_images()

    def Average_Filter(self):
        if self.current_image:
            self.current_image = Average_Filter(self.current_image)  
            self.display_images()

    def Maxmimun_Filter(self):
        if self.current_image:
            self.current_image = Maxmimun_Filter(self.current_image)  
            self.display_images()

    def Minmium_Filter(self):
        if self.current_image:
            self.current_image =Minmium_Filter(self.current_image)  
            self.display_images()
    
    def Median_Filter(self):
        if self.current_image:
            self.current_image =Median_Filter(self.current_image)  
            self.display_images()
    
    def Histogram_Equalization(self):
        if self.current_image:
            self.current_image =Histogram_Equalization(self.current_image)  
            self.display_images()

    def histogram_matching_m(self):
        if self.current_image:
            reference_image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
            if reference_image_path:
                reference_image = Image.open(reference_image_path).convert('L')
                self.current_image = histogram_matching_algorithm(self.current_image, reference_image)  # Use the reference image
                self.display_images()

    def Sobel_Filter(self):
        if self.current_image:
            self.current_image =Sobel_Filter(self.current_image) 
            self.display_images()

    def Prewitt_Filter(self):
        if self.current_image:
            self.current_image =Prewitt_Filter(self.current_image)  
            self.display_images()

    def save_image(self):
        if self.current_image:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
            if save_path:
                self.current_image.save(save_path)
                print(f"Image saved at {save_path}")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    editor = ImageEditor(root)
    root.mainloop()
