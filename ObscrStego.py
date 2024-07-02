import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk
import os
from datetime import datetime
import numpy as np

class TAsimilaritas(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ObscuraStego | Obfuscated Steganography Application")

        # Membuat frame container utama
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)
        
        # Membuat sidebar kiri lebih lebar
        left_sidebar = tk.Frame(self.main_frame, width=900)
        left_sidebar.pack(side="left", padx=5, pady=5, fill="both")

        # Frame untuk informasi file
        file_info_frame = tk.Frame(left_sidebar, bd=1, relief=tk.SOLID)
        file_info_frame.pack(fill="x", padx=5, pady=5)

        # Label "FILE INFORMATION" di tengah
        file_info_label = tk.Label(file_info_frame, text="FILE INFORMATION", font=("Arial", 12, "bold"))
        file_info_label.pack(anchor="center", padx=5, pady=5)

        # Deskripsi aplikasi
        app_description = "ObscuraStego adalah aplikasi digital forensics yang dirancang untuk analisis gambar dan deteksi steganografi. Aplikasi ini menggunakan berbagai alat seperti zsteg, steghide, outguess, exiftool, binwalk, foremost, dan strings untuk analisis yang mendalam. ObscuraStego mendukung berbagai format gambar termasuk .png, .jpg, .gif, .bmp, .jpeg, .jfif, .jpe, dan .tiff. | Created By Nuno Zildjian"
        description_label = tk.Label(file_info_frame, text=app_description, wraplength=700, font=("Arial", 12, "bold"), justify="left", anchor="w")
        description_label.pack(padx=5, pady=5, anchor="w")

        # Frame untuk konten file info
        content_frame = tk.Frame(file_info_frame)
        content_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Canvas untuk gambar
        self.image_canvas = tk.Canvas(content_frame, width=300, height=250, bg="gray")
        self.image_canvas.pack(side="left", padx=5, pady=5)

        # Frame untuk informasi file
        info_frame = tk.Frame(content_frame)
        info_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Informasi file
        self.name_label = tk.Label(info_frame, text="[+] Name(s):", anchor="w", font=("Arial", 12, "bold"))
        self.name_label.pack(fill="x", pady=2)
        self.size_label = tk.Label(info_frame, text="[+] Size:", anchor="w", font=("Arial", 12, "bold"))
        self.size_label.pack(fill="x", pady=2)
        self.date_label = tk.Label(info_frame, text="[+] Date Upload:", anchor="w", font=("Arial", 12, "bold"))
        self.date_label.pack(fill="x", pady=2)
        self.extension_label = tk.Label(info_frame, text="[+] Extension:", anchor="w", font=("Arial", 12, "bold"))
        self.extension_label.pack(fill="x", pady=2)
        self.strings_label = tk.Label(info_frame, text="[+] Strings Count:", anchor="w", font=("Arial", 12, "bold"))
        self.strings_label.pack(fill="x", pady=2)
        self.extraction_label = tk.Label(info_frame, text="[+] Extraction Status:", anchor="w", font=("Arial", 12, "bold"))
        self.extraction_label.pack(fill="x", pady=2)

        # Frame untuk tombol
        button_frame = tk.Frame(file_info_frame)
        button_frame.pack(fill="x", padx=5, pady=5)

        # Frame tambahan untuk mengatur tombol di tengah
        center_button_frame = tk.Frame(button_frame)
        center_button_frame.pack(expand=True)

        # Tombol UPLOAD
        upload_button = tk.Button(center_button_frame, text="UPLOAD", width=14, height=2, command=self.upload_image)
        upload_button.pack(side="left", padx=5)

        # Tombol ANALYZE IMAGE
        analyze_button = tk.Button(center_button_frame, text="ANALYZE IMAGE", width=14, height=2, command=self.analyze_image)
        analyze_button.pack(side="left", padx=5)

        # Frame untuk ExifTool INFORMATION
        exif_frame = tk.Frame(left_sidebar, bd=1, relief=tk.SOLID)
        exif_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Label "ExifTool INFORMATION"
        exif_label = tk.Label(exif_frame, text="RGBA VALUES INFORMATION", font=("Arial", 12, "bold"))
        exif_label.pack(anchor="center", padx=5, pady=5)

        # Frame untuk text widget dan scrollbar
        text_scroll_frame = tk.Frame(exif_frame)
        text_scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Text widget untuk informasi ExifTool
        self.exif_text = tk.Text(text_scroll_frame, wrap=tk.WORD)
        self.exif_text.pack(side="left", fill="both", expand=True)

        # Scrollbar untuk text widget
        text_scrollbar = tk.Scrollbar(text_scroll_frame, command=self.exif_text.yview)
        text_scrollbar.pack(side="right", fill="y")

        # Menghubungkan scrollbar dengan text widget
        self.exif_text.config(yscrollcommand=text_scrollbar.set)

        # Frame untuk elemen-elemen di bagian bawah
        bottom_frame = tk.Frame(left_sidebar)
        bottom_frame.pack(fill="x", padx=5, pady=5)

        # Text di bawah kanvas untuk grafik matplotlib, di pojok kiri bawah
        label_text_below_canvas = tk.Label(bottom_frame, text="ObscuraStego | Obfuscated Steganography V.1.0", font=("Arial", 13, "bold"))
        label_text_below_canvas.pack(side="left", padx=5, pady=5)

        # Frame untuk tombol di sebelah kanan teks "Below Canvas"
        button_frame_below_canvas = tk.Frame(bottom_frame, bg="white")
        button_frame_below_canvas.pack(side="right", padx=5, pady=5)

        # Button save hasil graph
        button1_below_canvas = tk.Button(button_frame_below_canvas, text="SHOW RGBA VALUES", width=16, height=2)
        button1_below_canvas.pack(side="left", padx=(0, 5))

        # Button untuk Show Preprocessing
        button2_below_canvas = tk.Button(button_frame_below_canvas, text="CLEAR ALL", width=15, height=2, command=self.clear_all)
        button2_below_canvas.pack(side="left", padx=(0, 0))

        # Membuat sidebar kanan dengan scrollbar
        self.sidebar_right = tk.Frame(self.main_frame)
        self.sidebar_right.pack(side="right", fill="both", expand=True)

        # Membuat canvas untuk scrolling
        self.canvas_right = tk.Canvas(self.sidebar_right)
        self.canvas_right.pack(side="left", fill="both", expand=True)

        # Scrollbar untuk canvas
        self.scrollbar_right = tk.Scrollbar(self.sidebar_right, orient="vertical", command=self.canvas_right.yview)
        self.scrollbar_right.pack(side="right", fill="y")

        # Konfigurasi canvas
        self.canvas_right.configure(yscrollcommand=self.scrollbar_right.set)
        self.canvas_right.bind('<Configure>', lambda e: self.canvas_right.configure(scrollregion=self.canvas_right.bbox("all")))

        # Frame di dalam canvas untuk konten
        self.frame_right_content = tk.Frame(self.canvas_right)
        self.canvas_right.create_window((0, 0), window=self.frame_right_content, anchor="nw")

        def create_section(title, row, color):
            # Hanya menambahkan judul di atas bagian "[+] SUPER IMPOSED"
            if row == 0:
                title_label = tk.Label(self.frame_right_content, text="VIEW BIT PLANES COLOR", font=("Arial", 16, "bold"), fg="black", anchor="center")
                title_label.grid(row=row, column=0, padx=5, pady=5, columnspan=4, sticky="ew")

            # Label untuk bagian "[+] SUPER IMPOSED"
            label = tk.Label(self.frame_right_content, text=title, font=("Arial", 15, "bold"), fg=color, anchor="center")
            label.grid(row=row + 1, column=0, padx=5, pady=5, columnspan=4, sticky="ew")
            for i in range(8):
                canvas = tk.Canvas(self.frame_right_content, bg="gray", width=275, height=250)
                canvas.grid(row=row + 2 + i//4, column=i%4, padx=5, pady=5)

        # Creating sections with appropriate colors and larger text
        create_section("[+] SUPER IMPOSED", 0, "orange")
        create_section("[+] RED", 3, "red")
        create_section("[+] GREEN", 6, "green")
        create_section("[+] BLUE", 9, "blue")

        # Frame for Strings, PNG Check, and InfoSteg (below all other sections)
        info_frame = tk.Frame(self.frame_right_content, bd=1, relief=tk.SOLID)
        info_frame.grid(row=13, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

        # Frame for Strings and PNG Check (horizontal layout)
        horizontal_frame = tk.Frame(info_frame)
        horizontal_frame.pack(fill="x", padx=5, pady=5)

        # Strings section (left side)
        strings_frame = tk.Frame(horizontal_frame)
        strings_frame.pack(side="left", fill="both", expand=True)
        tk.Label(strings_frame, text="STRINGS", font=("Arial", 12, "bold")).pack(anchor="w", padx=5, pady=5)
        self.strings_text = tk.Text(strings_frame, height=5, wrap=tk.WORD)
        self.strings_text.pack(fill="both", expand=True, padx=5, pady=5)
        tk.Scrollbar(self.strings_text).pack(side="right", fill="y")

        # PNG Check section (right side)
        png_frame = tk.Frame(horizontal_frame)
        png_frame.pack(side="right", fill="both", expand=True)
        tk.Label(png_frame, text="PNG CHECK", font=("Arial", 12, "bold")).pack(anchor="w", padx=5, pady=5)
        self.png_check_text = tk.Text(png_frame, height=5, wrap=tk.WORD)
        self.png_check_text.pack(fill="both", expand=True, padx=5, pady=5)
        tk.Scrollbar(self.png_check_text).pack(side="right", fill="y")

        # InfoSteg section (below Strings and PNG Check)
        tk.Label(info_frame, text="INFOSTEG", font=("Arial", 12, "bold")).pack(anchor="w", padx=5, pady=5)
        self.infosteg_text = tk.Text(info_frame, height=10, wrap=tk.WORD)
        self.infosteg_text.pack(fill="both", expand=True, padx=5, pady=5)
        tk.Scrollbar(self.infosteg_text).pack(side="right", fill="y")
                
        # Fungsi untuk mengatur ukuran canvas
        def configure_scroll_region(event):
            self.canvas_right.configure(scrollregion=self.canvas_right.bbox("all"))

        # Bind fungsi ke event konfigurasi frame
        self.frame_right_content.bind("<Configure>", configure_scroll_region)

        self.uploaded_image = None
        self.uploaded_image_path = None


    def upload_image(self):
        file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")])
        if file_path:
            self.uploaded_image_path = file_path
            self.uploaded_image = Image.open(file_path)
            
            # Display image on canvas
            img = self.uploaded_image.copy()
            img.thumbnail((300, 250))
            photo = ImageTk.PhotoImage(img)
            self.image_canvas.create_image(0, 0, anchor="nw", image=photo)
            self.image_canvas.image = photo

            # Update file information
            file_info = os.stat(file_path)
            self.name_label.config(text=f"[+] Name(s): {os.path.basename(file_path)}")
            self.size_label.config(text=f"[+] Size: {file_info.st_size} bytes")
            self.date_label.config(text=f"[+] Date Upload: {datetime.fromtimestamp(file_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
            self.extension_label.config(text=f"[+] Extension: {os.path.splitext(file_path)[1]}")
            
            # Extract strings and update strings count
            extracted_strings = self.get_strings(file_path)
            string_count = len(extracted_strings.split('\n'))
            self.strings_label.config(text=f"[+] Strings Count: {string_count}")
            
            # Update extraction status
            self.extraction_label.config(text=f"[+] Extraction Status: File uploaded successfully")
            
            # Populate new text boxes
            self.strings_text.delete('1.0', tk.END)
            self.strings_text.insert(tk.END, self.get_strings(file_path))

            self.png_check_text.delete('1.0', tk.END)
            self.png_check_text.insert(tk.END, self.get_png_info(file_path))

            self.infosteg_text.delete('1.0', tk.END)
            self.infosteg_text.insert(tk.END, self.get_infosteg(file_path))
            

    def analyze_image(self):
        if self.uploaded_image is None:
            messagebox.showerror("Error", "Please upload an image first.")
            return

        # Get RGBA values
        rgba_values = self.get_rgba_values()
        self.display_rgba_values(rgba_values)

        # Generate and display bit planes
        self.generate_bit_planes()

    def get_rgba_values(self):
        img_array = np.array(self.uploaded_image)
        if img_array.shape[2] == 3:  # RGB image
            r, g, b = img_array[:,:,0], img_array[:,:,1], img_array[:,:,2]
            a = np.full(r.shape, 255)  # Add alpha channel with full opacity
        else:  # RGBA image
            r, g, b, a = img_array[:,:,0], img_array[:,:,1], img_array[:,:,2], img_array[:,:,3]
        
        return r, g, b, a

    def display_rgba_values(self, rgba_values):
        r, g, b, a = rgba_values
        
        # Flatten the arrays and take the first 100 values (or less if the image is smaller)
        flat_r = r.flatten()[:100]
        flat_g = g.flatten()[:100]
        flat_b = b.flatten()[:100]
        flat_a = a.flatten()[:100]
        
        # Combine the values into the desired format
        rgba_str = ", ".join([f"{r}, {g}, {b}, {a}" for r, g, b, a in zip(flat_r, flat_g, flat_b, flat_a)])
        
        # Display the RGBA values
        self.exif_text.delete(1.0, tk.END)
        self.exif_text.insert(tk.END, rgba_str)
        
        # Add scrollbar if needed
        if len(rgba_str) > 1000:  # Arbitrary threshold, adjust as needed
            scrollbar = tk.Scrollbar(self.exif_text.master, command=self.exif_text.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.exif_text.config(yscrollcommand=scrollbar.set)

        # Display additional statistics
        stats = f"\n\nRed channel:   Min: {r.min()}, Max: {r.max()}, Mean: {r.mean():.2f}\n"
        stats += f"Green channel: Min: {g.min()}, Max: {g.max()}, Mean: {g.mean():.2f}\n"
        stats += f"Blue channel:  Min: {b.min()}, Max: {b.max()}, Mean: {b.mean():.2f}\n"
        stats += f"Alpha channel: Min: {a.min()}, Max: {a.max()}, Mean: {a.mean():.2f}"
        
        self.exif_text.insert(tk.END, stats)

    def generate_bit_planes(self):
        r, g, b, _ = self.get_rgba_values()
        
        def get_bit_planes(channel):
            return [(channel & (1 << i)) for i in range(8)]
        
        r_planes = get_bit_planes(r)
        g_planes = get_bit_planes(g)
        b_planes = get_bit_planes(b)
        
        # Display superimposed bit planes
        for i in range(8):
            img = Image.fromarray(np.uint8(r_planes[i] | g_planes[i] | b_planes[i]) * 255)
            self.display_on_canvas(img, i, 0)
        
        # Display red bit planes
        for i in range(8):
            img = Image.fromarray(np.uint8(r_planes[i]) * 255)
            self.display_on_canvas(img, i, 3)
        
        # Display green bit planes
        for i in range(8):
            img = Image.fromarray(np.uint8(g_planes[i]) * 255)
            self.display_on_canvas(img, i, 6)
        
        # Display blue bit planes
        for i in range(8):
            img = Image.fromarray(np.uint8(b_planes[i]) * 255)
            self.display_on_canvas(img, i, 9)

    def display_on_canvas(self, img, index, row_offset):
        img.thumbnail((275, 250))
        photo = ImageTk.PhotoImage(img)
        canvas = self.frame_right_content.grid_slaves(row=row_offset + 2 + index//4, column=index%4)[0]
        canvas.create_image(0, 0, anchor="nw", image=photo)
        canvas.image = photo

    def show_preprocessing(self):
        # Placeholder for preprocessing function
        pass

    def clear_all(self):
        self.image_canvas.delete("all")
        self.exif_text.delete(1.0, tk.END)
        for widget in self.frame_right_content.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.delete("all")
        
        # Reset file information labels
        self.name_label.config(text="[+] Name(s):")
        self.size_label.config(text="[+] Size:")
        self.date_label.config(text="[+] Date Upload:")
        self.extension_label.config(text="[+] Extension:")
        self.strings_label.config(text="[+] Strings Count:")
        self.extraction_label.config(text="[+] Extraction Status:")

        self.uploaded_image = None
        self.uploaded_image_path = None
        
        
    def get_strings(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            strings = []
            current_string = b''
            for byte in content:
                if 32 <= byte <= 126:  # printable ASCII characters
                    current_string += bytes([byte])
                elif current_string:
                    if len(current_string) >= 4:  # minimum string length
                        strings.append(current_string.decode('ascii', errors='ignore'))
                    current_string = b''
            if current_string and len(current_string) >= 4:
                strings.append(current_string.decode('ascii', errors='ignore'))
            return '\n'.join(strings)
        except Exception as e:
            return f"Error extracting strings: {str(e)}"

    def get_png_info(self, file_path):
        try:
            with Image.open(file_path) as img:
                info = f"Header File:\n"
                info += f"Dimensions: {img.size[0]}x{img.size[1]}\n"
                info += f"Color Depth: {img.mode}\n"
                info += f"Compression: {img.info.get('compression', 'Unknown')}\n"
                info += f"Color Info: {img.info.get('icc_profile', 'Not available')}\n\n"
                
                info += "Metadata:\n"
                for k, v in img.info.items():
                    info += f"{k}: {v}\n"
                
                # Add IHDR chunk information
                with open(file_path, 'rb') as f:
                    f.seek(12)
                    ihdr = f.read(13)
                    width, height = int.from_bytes(ihdr[0:4], 'big'), int.from_bytes(ihdr[4:8], 'big')
                    bit_depth, color_type, compression, filter_method, interlace = ihdr[8:]
                    info += f"\nIHDR Chunk:\n"
                    info += f"Width: {width}\n"
                    info += f"Height: {height}\n"
                    info += f"Bit Depth: {bit_depth}\n"
                    info += f"Color Type: {color_type}\n"
                    info += f"Compression: {compression}\n"
                    info += f"Filter Method: {filter_method}\n"
                    info += f"Interlace: {interlace}\n"
                
                return info
        except Exception as e:
            return f"Error extracting PNG info: {str(e)}"
        
    def get_infosteg(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                img = Image.open(f)
                width, height = img.size

                info = "File Analysis:\n"
                info += f"File size: {self.get_file_size(file_path)} bytes\n"
                info += f"File type: {self.get_file_type(img)}\n\n"

                info += "Steganography Detection:\n"
                info += self.analyze_byte_swapped(img)
                info += self.analyze_lsb(img, 'rgb')
                info += self.analyze_msb(img, 'bgr')
                info += self.analyze_mpeg(img)
                info += self.analyze_lsb(img, 'r')
                info += self.analyze_lsb(img, 'g')
                info += self.analyze_lsb(img, 'b')
                info += self.analyze_msb(img, 'b')

                return info

        except Exception as e:
            return f"Error analyzing file: {str(e)}"

    def analyze_byte_swapped(self, img):
        try:
            img_data = img.tobytes()
            if img_data.startswith(b'\x42\x65\x72\x6B\x65\x6C\x65\x79'):  # Example byte-swapped pattern
                return "imagedata .. file: byte-swapped Berkeley vfont data"
            return ""
        except Exception as e:
            return f"Error analyzing byte-swapped data: {str(e)}"

    def analyze_lsb(self, img, channel):
        try:
            image_array = np.array(img)
            height, width, _ = image_array.shape
            lsb_data = []

            if channel == 'rgb':
                for y in range(height):
                    for x in range(width):
                        pixel = image_array[y, x]
                        lsb_data.extend([pixel[0] & 1, pixel[1] & 1, pixel[2] & 1])
            else:
                channel_index = {'r': 0, 'g': 1, 'b': 2}[channel]
                for y in range(height):
                    for x in range(width):
                        pixel = image_array[y, x]
                        lsb_data.append(pixel[channel_index] & 1)

            binary_string = ''.join(map(str, lsb_data))
            text = self.binary_to_text(binary_string)
            if text:
                return f'b1,{channel},lsb,xy .. text: "{text}"'
            return ""
        
        except Exception as e:
            return f"Error analyzing LSB data: {str(e)}"

    def analyze_msb(self, img, channel):
        try:
            image_array = np.array(img)
            height, width, _ = image_array.shape
            msb_data = []

            if channel == 'rgb':
                for y in range(height):
                    for x in range(width):
                        pixel = image_array[y, x]
                        msb_data.extend([pixel[0] >> 7, pixel[1] >> 7, pixel[2] >> 7])
            else:
                channel_index = {'r': 0, 'g': 1, 'b': 2}[channel]
                for y in range(height):
                    for x in range(width):
                        pixel = image_array[y, x]
                        msb_data.append(pixel[channel_index] >> 7)

            binary_string = ''.join(map(str, msb_data))
            text = self.binary_to_text(binary_string)
            if text:
                return f'b1,{channel},msb,xy .. text: "{text}"'
            return ""
        
        except Exception as e:
            return f"Error analyzing MSB data: {str(e)}"

    def analyze_mpeg(self, img):
        # Mock implementation: In a real implementation, you would detect MPEG data
        try:
            img_data = img.tobytes()
            if img_data.startswith(b'\x00\x00\x00\x01\xBA'):
                return 'b3,g,lsb,xy .. file: MPEG ADTS, layer III, v1, 40 kbps, 48 kHz, 2x Monaural'
            return ""
        except Exception as e:
            return f"Error analyzing MPEG data: {str(e)}"

    def binary_to_text(self, binary_data):
        try:
            binary_chunks = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
            text = ''.join([chr(int(b, 2)) for b in binary_chunks if int(b, 2) != 0])
            return text
        except Exception as e:
            return f"Error converting binary to text: {str(e)}"

    def get_file_size(self, file_path):
        try:
            return os.path.getsize(file_path)
        except Exception as e:
            return f"Error getting file size: {str(e)}"

    def get_file_type(self, img):
        try:
            file_signatures = {
                b'\x89PNG\r\n\x1a\n': 'PNG',
                b'\xff\xd8\xff': 'JPEG',
                b'GIF87a': 'GIF',
                b'GIF89a': 'GIF',
                b'BM': 'BMP',
            }
            for sig, ftype in file_signatures.items():
                if img.tobytes().startswith(sig):
                    return ftype
            return 'Unknown'
        except Exception as e:
            return f"Error detecting file type: {str(e)}"

if __name__ == "__main__":
    app = TAsimilaritas()
    app.mainloop()