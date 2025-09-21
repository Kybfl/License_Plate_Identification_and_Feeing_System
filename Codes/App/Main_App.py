import tkinter as tk
import cv2
import numpy as np
import pytesseract
import os
from datetime import datetime

from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from ultralytics import YOLO


class PlateRecognitionApp:
    def __init__(self, root):
        self.root = root
        pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract\tesseract.exe'
        self.root.title("Araç Plaka Tanıma Sistemi")
        self.root.geometry("1600x950")
        
        # Koyu tema renk paleti
        self.colors = {
            'primary_bg': '#0D0D0D',          
            'secondary_bg': '#1A1A1A',        
            'tertiary_bg': '#222222',         
            'text_primary': "#FFFFFF",        
            'text_secondary': "#FFFFFF",     
            'accent_button': '#F59E0B',       
            'button_hover': '#FBBF24',     
            'success': '#22C55E',             
            'success_hover': '#4ADE80',      
            'warning': '#DC2626',             
            'warning_hover': '#EF4444',      
            'input_bg': '#141414',            
            'placeholder': '#6B7280',         
            'border': '#2E2E2E',             
            'active_highlight': '#FACC15'     
        }
        
        # Ana pencere stili
        self.root.configure(bg=self.colors['primary_bg'])
        
        # Model 
        self.model = None

        # Değişkenler
        self.original_image = None
        self.cropped_plate = None
        
        # Ücretlendirme tablosu
        self.billing_data = []
        
        # Ücret tarifeleri
        self.pricing = {
            "0-1 saat": 130,
            "1-2 saat": 180,
            "2-3 saat": 230,
            "3-4 saat": 280,
            "4-5 saat": 330,
            "5-6 saat": 380,
            "Aylık": 6910
        }
        
        self.setup_styles()
        self.setup_ui()
        
    def setup_styles(self):
        """TTK stillerini yapılandır"""
        style = ttk.Style()
        
        # Ana stil teması
        style.theme_use('clam')
        
        # LabelFrame stilleri
        style.configure('Custom.TLabelframe', 
                       background=self.colors['secondary_bg'],
                       borderwidth=2,
                       relief='groove',
                       bordercolor=self.colors['border'])
        style.configure('Custom.TLabelframe.Label', 
                       background=self.colors['secondary_bg'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 12, 'bold'))
        
        # Primary Button stilleri (Amber Orange)
        style.configure('Primary.TButton',
                       background=self.colors['accent_button'],
                       foreground=self.colors['primary_bg'],
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 11, 'bold'),
                       padding=(18, 10))
        
        style.map('Primary.TButton',
                 background=[('active', self.colors['button_hover'])])
        
        # Secondary Button stilleri (Koyu gri)
        style.configure('Secondary.TButton',
                       background=self.colors['tertiary_bg'],
                       foreground=self.colors['text_primary'],
                       borderwidth=1,
                       bordercolor=self.colors['border'],
                       focuscolor='none',
                       font=('Segoe UI', 10),
                       padding=(15, 8))
        
        style.map('Secondary.TButton',
                 background=[('active', self.colors['border'])])
        
        # Success Button stilleri (Yeşil)
        style.configure('Success.TButton',
                       background=self.colors['success'],
                       foreground=self.colors['primary_bg'],
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(12, 8))
        
        style.map('Success.TButton',
                 background=[('active', self.colors['success_hover'])])
        
        # Entry stilleri
        style.configure('Custom.TEntry',
                       fieldbackground=self.colors['input_bg'],
                       borderwidth=2,
                       relief='solid',
                       bordercolor=self.colors['border'],
                       foreground=self.colors['text_primary'],
                       insertcolor=self.colors['text_primary'],
                       font=('Segoe UI', 11))
        
        style.map('Custom.TEntry',
                 bordercolor=[('focus', self.colors['active_highlight'])])
        
        # Label stilleri
        style.configure('Title.TLabel',
                       background=self.colors['secondary_bg'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 14, 'bold'))
        
        style.configure('Subtitle.TLabel',
                       background=self.colors['secondary_bg'],
                       foreground=self.colors['text_secondary'],
                       font=('Segoe UI', 11))
        
        style.configure('Status.TLabel',
                       background=self.colors['secondary_bg'],
                       font=('Segoe UI', 10))
        
        # Combobox stilleri
        style.configure('Custom.TCombobox',
                       fieldbackground=self.colors['input_bg'],
                       borderwidth=2,
                       relief='solid',
                       bordercolor=self.colors['border'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 11))
        
        # Treeview stilleri
        style.configure('Custom.Treeview',
                       background=self.colors['input_bg'],
                       foreground=self.colors['text_primary'],
                       fieldbackground=self.colors['input_bg'],
                       borderwidth=1,
                       relief='solid')
        
        style.configure('Custom.Treeview.Heading',
                       background=self.colors['tertiary_bg'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 10, 'bold'))
        
    def setup_ui(self):
        # Başlık
        header_frame = tk.Frame(self.root, bg=self.colors['tertiary_bg'], height=90)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text="🚗 ARAÇ PLAKA TANIMA SİSTEMİ",
                              bg=self.colors['tertiary_bg'],
                              fg=self.colors['text_primary'],
                              font=('Segoe UI', 20, 'bold'))
        title_label.pack(expand=True)
        
        # Ana container
        main_container = tk.Frame(self.root, bg=self.colors['primary_bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=(0, 25))
        
        # Sol panel - Kontroller
        left_panel = tk.Frame(main_container, bg=self.colors['primary_bg'], width=380)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        left_panel.pack_propagate(False)
        
        # Orta panel - Görüntüler
        middle_panel = tk.Frame(main_container, bg=self.colors['primary_bg'], width=600)
        middle_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        # Sağ panel - Ücretlendirme
        right_panel = tk.Frame(main_container, bg=self.colors['primary_bg'], width=430)
        right_panel.pack(side=tk.LEFT, fill=tk.Y)
        right_panel.pack_propagate(False)
        
        self.setup_left_panel(left_panel)
        self.setup_middle_panel(middle_panel)
        self.setup_right_panel(right_panel)
        
    def setup_left_panel(self, parent):
        # Model ayarları
        model_frame = ttk.LabelFrame(parent, text="⚙️ Model Ayarları", 
                                   style='Custom.TLabelframe', padding=20)
        model_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(model_frame, text="Model Dosyası:", 
                 style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 8))
        
        path_frame = tk.Frame(model_frame, bg=self.colors['secondary_bg'])
        path_frame.pack(fill=tk.X, pady=(0, 12))
        
        self.model_path_var = tk.StringVar()
        path_entry = ttk.Entry(path_frame, textvariable=self.model_path_var, 
                              style='Custom.TEntry', width=20)
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(path_frame, text="📁 Seç", command=self.load_model,
                  style='Secondary.TButton').pack(side=tk.RIGHT, padx=(8, 0))
        
        self.model_status_label = ttk.Label(model_frame, text="❌ Model yüklenmedi", 
                                           style='Status.TLabel', 
                                           foreground=self.colors['warning'])
        self.model_status_label.pack(anchor=tk.W)
        
        # İşlem butonları
        process_frame = ttk.LabelFrame(parent, text="🔧 İşlemler", 
                                     style='Custom.TLabelframe', padding=20)
        process_frame.pack(fill=tk.X, pady=(0, 20))
        
        buttons = [
            ("📷 Fotoğraf Seç", self.select_image, 'Primary.TButton'),
            ("🔍 Plaka Tespit Et", self.detect_plate, 'Primary.TButton'),
            ("📝 OCR Çalıştır", self.run_ocr, 'Primary.TButton'),
            ("🗑️ Temizle", self.clear_all, 'Secondary.TButton')
        ]
        
        for text, command, style in buttons:
            btn = ttk.Button(process_frame, text=text, command=command, style=style)
            btn.pack(fill=tk.X, pady=3)
        
        # Sonuç alanı
        result_frame = ttk.LabelFrame(parent, text="📋 Sonuç", 
                                    style='Custom.TLabelframe', padding=20)
        result_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(result_frame, text="Tespit Edilen Plaka:", 
                 style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 8))
        
        result_container = tk.Frame(result_frame, bg=self.colors['secondary_bg'])
        result_container.pack(fill=tk.X, pady=(0, 12))
        
        self.result_var = tk.StringVar()
        result_entry = ttk.Entry(result_container, textvariable=self.result_var, 
                               style='Custom.TEntry', font=('Consolas', 14, 'bold'))
        result_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(result_container, text="📋", command=self.copy_result,
                  style='Success.TButton').pack(side=tk.RIGHT, padx=(8, 0))
        
        # Güven skorları
        self.confidence_label = tk.Label(result_frame, text="", 
                                       bg=self.colors['secondary_bg'],
                                       fg=self.colors['text_secondary'],
                                       font=('Segoe UI', 10),
                                       wraplength=320,
                                       justify=tk.LEFT)
        self.confidence_label.pack(anchor=tk.W, pady=(8, 0))
        
    def setup_middle_panel(self, parent):
        # Görüntü başlığı
        image_title = tk.Label(parent, text="🖼️ Görüntü Analizi", 
                              bg=self.colors['primary_bg'],
                              fg=self.colors['text_primary'],
                              font=('Segoe UI', 16, 'bold'))
        image_title.pack(pady=(0, 20))
        
        # Görüntü container
        image_container = tk.Frame(parent, bg=self.colors['primary_bg'])
        image_container.pack(fill=tk.BOTH, expand=True)
        
        # Orijinal görüntü
        original_frame = self.create_image_frame(image_container, "📸 Orijinal Görüntü")
        original_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 12))
        
        self.original_canvas = tk.Canvas(original_frame, bg=self.colors['input_bg'],
                                       highlightbackground=self.colors['border'],
                                       highlightthickness=2)
        self.original_canvas.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
        
        # Kırpılmış görüntü
        cropped_frame = self.create_image_frame(image_container, "✂️ Tespit Edilen Plaka")
        cropped_frame.pack(fill=tk.BOTH, expand=True)
        
        self.cropped_canvas = tk.Canvas(cropped_frame, bg=self.colors['input_bg'],
                                      highlightbackground=self.colors['border'],
                                      highlightthickness=2)
        self.cropped_canvas.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
        
    def setup_right_panel(self, parent):
        # Ücretlendirme alanı
        billing_frame = ttk.LabelFrame(parent, text="💰 Ücretlendirme", 
                                     style='Custom.TLabelframe', padding=20)
        billing_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(billing_frame, text="Süre Seçimi:", 
                 style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 8))
        
        self.duration_var = tk.StringVar()
        duration_combo = ttk.Combobox(billing_frame, textvariable=self.duration_var,
                                    values=list(self.pricing.keys()),
                                    style='Custom.TCombobox', state='readonly')
        duration_combo.pack(fill=tk.X, pady=(0, 12))
        duration_combo.bind('<<ComboboxSelected>>', self.calculate_price)
        
        # Ücret gösterimi
        price_frame = tk.Frame(billing_frame, bg=self.colors['secondary_bg'])
        price_frame.pack(fill=tk.X, pady=(0, 12))
        
        tk.Label(price_frame, text="Ücret:", bg=self.colors['secondary_bg'],
                fg=self.colors['text_secondary'], font=('Segoe UI', 11)).pack(anchor=tk.W)
        
        self.price_label = tk.Label(price_frame, text="0 TL", 
                                   bg=self.colors['secondary_bg'],
                                   fg=self.colors['accent_button'],
                                   font=('Segoe UI', 16, 'bold'))
        self.price_label.pack(anchor=tk.W)
        
        # Tabloya ekle butonu
        ttk.Button(billing_frame, text="💳 Tabloya Ekle", 
                  command=self.add_to_billing_table,
                  style='Success.TButton').pack(fill=tk.X, pady=(8, 0))
        
        # Ücretlendirme tablosu
        table_frame = ttk.LabelFrame(parent, text="📊 Ücretlendirme Tablosu", 
                                   style='Custom.TLabelframe', padding=15)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview için scrollbar
        tree_container = tk.Frame(table_frame, bg=self.colors['secondary_bg'])
        tree_container.pack(fill=tk.BOTH, expand=True)
        
        # Treeview
        columns = ('Sıra', 'Plaka', 'Süre', 'Ücret', 'Tarih')
        self.billing_tree = ttk.Treeview(tree_container, columns=columns, show='headings',
                                       style='Custom.Treeview', height=12)
        
        # Sütun başlıkları
        self.billing_tree.heading('Sıra', text='#')
        self.billing_tree.heading('Plaka', text='Plaka')
        self.billing_tree.heading('Süre', text='Süre')
        self.billing_tree.heading('Ücret', text='Ücret')
        self.billing_tree.heading('Tarih', text='Tarih')
        
        # Sütun genişlikleri
        self.billing_tree.column('Sıra', width=40, anchor=tk.CENTER)
        self.billing_tree.column('Plaka', width=80, anchor=tk.CENTER)
        self.billing_tree.column('Süre', width=80, anchor=tk.CENTER)
        self.billing_tree.column('Ücret', width=70, anchor=tk.CENTER)
        self.billing_tree.column('Tarih', width=90, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_container, orient=tk.VERTICAL, command=self.billing_tree.yview)
        self.billing_tree.configure(yscrollcommand=scrollbar.set)
        
        self.billing_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Toplam ücret
        total_frame = tk.Frame(table_frame, bg=self.colors['secondary_bg'], height=40)
        total_frame.pack(fill=tk.X, pady=(10, 0))
        total_frame.pack_propagate(False)
        
        self.total_label = tk.Label(total_frame, text="Toplam: 0 TL", 
                                   bg=self.colors['secondary_bg'],
                                   fg=self.colors['accent_button'],
                                   font=('Segoe UI', 14, 'bold'))
        self.total_label.pack(expand=True)
        
    def create_image_frame(self, parent, title):
        """Görüntü frame'i oluştur"""
        frame = tk.Frame(parent, bg=self.colors['secondary_bg'], relief='groove', bd=2)
        
        title_label = tk.Label(frame, text=title,
                              bg=self.colors['tertiary_bg'],
                              fg=self.colors['text_primary'],
                              font=('Segoe UI', 13, 'bold'),
                              pady=12)
        title_label.pack(fill=tk.X)
        
        return frame
    
    def load_model(self):
        """YOLO modelini yükle"""
        file_path = filedialog.askopenfilename(
            title="YOLO Model Dosyasını Seçin",
            filetypes=[("YOLO models", "*.pt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.model = YOLO(file_path)
                self.model_path_var.set(os.path.basename(file_path))
                self.model_status_label.config(text="✅ Model başarıyla yüklendi", 
                                             foreground=self.colors['success'])
            except Exception as e:
                messagebox.showerror("Hata", f"Model yüklenirken hata oluştu:\n{str(e)}")
                self.model_status_label.config(text="❌ Model yüklenemedi", 
                                             foreground=self.colors['warning'])
    
    def select_image(self):
        """Görüntü dosyasını seç"""
        file_path = filedialog.askopenfilename(
            title="Görüntü Dosyasını Seçin",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.original_image = cv2.imread(file_path)
                self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
                
                self.show_image_on_canvas(self.original_image, self.original_canvas)
                
                # Sonuçları temizle
                self.cropped_plate = None
                self.result_var.set("")
                self.confidence_label.config(text="")
                self.cropped_canvas.delete("all")
                
                # Canvas'a placeholder text ekle
                self.add_placeholder_text(self.cropped_canvas, "Plaka tespiti için\n'Plaka Tespit Et' butonuna tıklayın")
                
            except Exception as e:
                messagebox.showerror("Hata", f"Görüntü yüklenirken hata oluştu:\n{str(e)}")
    
    def detect_plate(self):
        """Plaka tespiti yap"""
        if self.model is None:
            messagebox.showwarning("Uyarı", "Önce bir model yüklemelisiniz!")
            return
        
        if self.original_image is None:
            messagebox.showwarning("Uyarı", "Önce bir görüntü seçmelisiniz!")
            return
        
        try:
            results = self.model(self.original_image, conf=0.5)
            
            if len(results[0].boxes) > 0:
                boxes = results[0].boxes
                confidences = boxes.conf.cpu().numpy()
                best_idx = np.argmax(confidences)
                
                box = boxes.xyxy[best_idx].cpu().numpy().astype(int)
                x1, y1, x2, y2 = box
                confidence = confidences[best_idx]
                
                self.cropped_plate = self.original_image[y1:y2, x1:x2]
                
                self.show_image_on_canvas(self.cropped_plate, self.cropped_canvas)
                
                self.confidence_label.config(text=f"🎯 Tespit Güven Skoru: {confidence:.3f}")
                
                # Orijinal görüntü üzerine kutu çiz
                img_with_box = self.original_image.copy()
                cv2.rectangle(img_with_box, (x1, y1), (x2, y2), (245, 204, 21), 4)  # Sarı kutu
                self.show_image_on_canvas(img_with_box, self.original_canvas)
                
            else:
                messagebox.showinfo("Bilgi", "Görüntüde plaka tespit edilemedi!")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Plaka tespiti sırasında hata oluştu:\n{str(e)}")
    
    def run_ocr(self):
        """Tesseract OCR ile karakter tanıma"""
        if self.cropped_plate is None:
            messagebox.showwarning("Uyarı", "Önce plaka tespiti yapmalısınız!")
            return

        try:
           # Griye çevir
            gray = cv2.cvtColor(self.cropped_plate, cv2.COLOR_BGR2GRAY)

            # Gürültü azaltma (Median Blur)
            denoised = cv2.medianBlur(gray, 3)  # Kernel boyutu 3 veya 5 olabilir, test edebilirsin

            # Eşikleme (Otsu ile)
            _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # OCR
            custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            text = pytesseract.image_to_string(denoised, config=custom_config, lang='eng')

            # Sonuçları işle
            text = text.strip().upper().replace(' ', '').replace('\n', '')
        
            if len(text) > 2:
                self.result_var.set(text)
                self.confidence_label.config(text="📝 Tesseract OCR ile başarıyla tanındı.")
            else:
                messagebox.showinfo("Bilgi", "Plaka üzerinde okunabilir metin bulunamadı!")
        
        except Exception as e:
            messagebox.showerror("Hata", f"OCR işlemi sırasında hata oluştu:\n{str(e)}")
    
    def calculate_price(self, event=None):
        """Seçilen süreye göre ücreti hesapla"""
        duration = self.duration_var.get()
        if duration in self.pricing:
            price = self.pricing[duration]
            self.price_label.config(text=f"{price} TL")
        else:
            self.price_label.config(text="0 TL")
    
    def add_to_billing_table(self):
        """Plaka ve ücret bilgisini tabloya ekle"""
        plate = self.result_var.get()
        duration = self.duration_var.get()
        
        if not plate:
            messagebox.showwarning("Uyarı", "Önce plaka tespiti yapmalısınız!")
            return
        
        if not duration:
            messagebox.showwarning("Uyarı", "Lütfen süre seçimi yapın!")
            return
        
        price = self.pricing[duration]
        current_time = datetime.now().strftime("%d.%m.%Y %H:%M")
        
        # Tabloya ekle
        row_number = len(self.billing_data) + 1
        self.billing_data.append({
            'sira': row_number,
            'plaka': plate,
            'sure': duration,
            'ucret': price,
            'tarih': current_time
        })
        
        # Treeview'e ekle
        self.billing_tree.insert('', 'end', values=(
            row_number, plate, duration, f"{price} TL", current_time
        ))
        
        # Toplam ücreti güncelle
        total = sum(item['ucret'] for item in self.billing_data)
        self.total_label.config(text=f"Toplam: {total} TL")
        
        messagebox.showinfo("✅ Başarılı", f"Plaka {plate} tabloya eklendi!")
        
        # Formu temizle
        self.duration_var.set("")
        self.price_label.config(text="0 TL")
    
    def show_image_on_canvas(self, image, canvas):
        """Görüntüyü canvas üzerine göster"""
        canvas.update()
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            canvas.after(100, lambda: self.show_image_on_canvas(image, canvas))
            return
        
        h, w = image.shape[:2]
        aspect_ratio = w / h
        
        if canvas_width / canvas_height > aspect_ratio:
            new_height = canvas_height - 25
            new_width = int(new_height * aspect_ratio)
        else:
            new_width = canvas_width - 25
            new_height = int(new_width / aspect_ratio)
        
        resized_image = cv2.resize(image, (new_width, new_height))
        pil_image = Image.fromarray(resized_image)
        photo = ImageTk.PhotoImage(pil_image)
        
        canvas.delete("all")
        canvas.create_image(canvas_width//2, canvas_height//2, image=photo, anchor=tk.CENTER)
        canvas.image = photo
    
    def add_placeholder_text(self, canvas, text):
        """Canvas'a placeholder text ekle"""
        canvas.delete("all")
        canvas.create_text(canvas.winfo_width()//2, canvas.winfo_height()//2,
                          text=text, fill=self.colors['placeholder'],
                          font=('Segoe UI', 13), anchor=tk.CENTER)
    
    def copy_result(self):
        """Sonucu panoya kopyala"""
        result = self.result_var.get()
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            messagebox.showinfo("✅ Başarılı", "Plaka metni panoya kopyalandı!")
        else:
            messagebox.showwarning("Uyarı", "Kopyalanacak metin yok!")
    
    def clear_all(self):
        """Tüm sonuçları temizle"""
        self.original_image = None
        self.cropped_plate = None
        self.result_var.set("")
        self.confidence_label.config(text="")
        self.original_canvas.delete("all")
        self.cropped_canvas.delete("all")
        
        # Placeholder textleri ekle
        self.add_placeholder_text(self.original_canvas, "Görüntü seçmek için\n'Fotoğraf Seç' butonuna tıklayın")
        self.add_placeholder_text(self.cropped_canvas, "Plaka tespiti için\n'Plaka Tespit Et' butonuna tıklayın")

def main():
    root = tk.Tk()
    app = PlateRecognitionApp(root)
    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = PlateRecognitionApp(root)
    root.mainloop()