import tkinter as tk
import threading
import re
import mss
import pyperclip
from PIL import Image, ImageEnhance, ImageTk
import pytesseract

# NOTE: If on Windows, ensure this path points to your Tesseract installation!
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class NumLensSnipper:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("NumLens Snipper")
        self.root.attributes("-topmost", True)
        
        # --- CHANGED: Made the main window significantly wider and taller ---
        self.root.geometry("400x130+100+100") 
        self.root.configure(bg="#1a1a2e")
        self.root.resizable(False, False)

        # UI
        self.status_var = tk.StringVar(value="Ready")
        
        # --- CHANGED: Increased font size to 20 for quick visual confirmation ---
        tk.Label(self.root, textvariable=self.status_var, fg="#00d4aa", bg="#1a1a2e", 
                 font=("Segoe UI", 20, "bold")).pack(pady=(15, 10))
        
        self.btn = tk.Button(self.root, text="✂ SNIP NUMBER", bg="#00875a", fg="white", 
                             font=("Segoe UI", 12, "bold"), relief="flat", command=self.start_snip)
        self.btn.pack(fill="x", padx=20)

        self.root.mainloop()

    def start_snip(self):
        self.root.withdraw() # Hide main menu
        self.root.after(200, self.take_fullscreen_shot) # Wait for menu to vanish

    def take_fullscreen_shot(self):
        # 1. Take a screenshot of the whole screen
        with mss.mss() as sct:
            self.monitor = sct.monitors[1] # Primary monitor
            screenshot = sct.grab(self.monitor)
            # Use safe RGB conversion
            self.full_img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

        # 2. Open fullscreen overlay to draw the box
        self.overlay = tk.Toplevel(self.root)
        self.overlay.attributes('-fullscreen', True)
        self.overlay.attributes('-topmost', True)
        self.overlay.config(cursor="crosshair")

        self.canvas = tk.Canvas(self.overlay, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.tk_img = ImageTk.PhotoImage(self.full_img)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)

        # Variables for drawing
        self.rect = None
        self.start_x = None
        self.start_y = None

        # Bind mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        # Press Escape to cancel
        self.overlay.bind("<Escape>", lambda e: self.cancel_snip())

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, 
                                                 outline="#00d4aa", width=3)

    def on_drag(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_release(self, event):
        end_x, end_y = event.x, event.y
        self.overlay.destroy()
        
        # Calculate correct crop coordinates (handle dragging backwards)
        left = min(self.start_x, end_x)
        top = min(self.start_y, end_y)
        right = max(self.start_x, end_x)
        bottom = max(self.start_y, end_y)

        # Prevent empty crops
        if right - left > 5 and bottom - top > 5:
            cropped_img = self.full_img.crop((left, top, right, bottom))
            self.process_crop(cropped_img)
        else:
            self.cancel_snip()

    def cancel_snip(self):
        try:
            self.overlay.destroy()
        except: pass
        self.root.deiconify()
        self.status_var.set("Snip cancelled")

    def process_crop(self, img):
        self.root.deiconify()
        self.status_var.set("Reading...")
        self.root.update()

        def worker():
            # Very basic cleanup since you cropped it perfectly
            gray = img.convert("L")
            resized = gray.resize((gray.width * 3, gray.height * 3), Image.LANCZOS)
            final_img = ImageEnhance.Contrast(resized).enhance(2.0)
            
            # Use PSM 7 (treat image as a single line of text)
            cfg = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789'
            
            try:
                raw_text = pytesseract.image_to_string(final_img, config=cfg)
                clean_text = "".join(re.findall(r"\d+", raw_text))
                
                if clean_text:
                    pyperclip.copy(clean_text)
                    self.root.after(0, self.success, clean_text)
                else:
                    self.root.after(0, self.fail)
            except Exception as e:
                print(f"Error: {e}")
                self.root.after(0, self.fail)

        threading.Thread(target=worker, daemon=True).start()

    def success(self, text):
        self.status_var.set(f"{text}")
        self.root.configure(bg="#003322") # Flash green
        self.root.after(1000, lambda: self.root.configure(bg="#1a1a2e"))

    def fail(self):
        self.status_var.set("No numbers found!")
        self.root.configure(bg="#330B0B") # Flash red
        self.root.after(1000, lambda: self.root.configure(bg="#1a1a2e"))

if __name__ == "__main__":
    NumLensSnipper()