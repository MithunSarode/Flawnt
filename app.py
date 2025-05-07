import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from PIL import Image, ImageTk, ImageOps, ImageDraw
import cv2
import numpy as np
from sklearn.cluster import KMeans
import colorsys
import os
import threading
import time

class ColorAnalyzer:
    def __init__(self):
        self.season_types = {
            'Deep Autumn': {
                'desc': 'Your rich and bold features give you a striking, intense look with natural depth.',
                'undertone': 'Warm',
                'undertone_desc': 'Your skin has warm undertones, reflecting golden, peachy, or yellow hues in natural light.',
                'palette': ['#7B3F00', '#A9746E', '#8B5C2A', '#A0522D', '#6B4226'],
                'cosmetics': {
                    'Foundations': ['Golden Beige', 'Warm Honey'],
                    'Blushes': ['Terracotta', 'Warm Peach'],
                    'Lipsticks': ['Brick Red', 'Burnt Sienna']
                }
            },
            'Warm Autumn': {
                'desc': 'You have a warm, earthy glow that harmonizes with rich, golden colors.',
                'undertone': 'Warm',
                'undertone_desc': 'Your skin leans toward golden, peachy, or yellow undertones.',
                'palette': ['#D2691E', '#CD853F', '#B87333', '#DAA520', '#8B4513'],
                'cosmetics': {
                    'Foundations': ['Honey', 'Golden Tan'],
                    'Blushes': ['Apricot', 'Warm Coral'],
                    'Lipsticks': ['Copper', 'Terracotta']
                }
            },
            'Soft Autumn': {
                'desc': 'You have a muted, gentle look that pairs beautifully with soft, earthy colors.',
                'undertone': 'Warm',
                'undertone_desc': 'Your undertones are warm but subtle, often with a beige or olive tint.',
                'palette': ['#C2B280', '#BC987E', '#D2B48C', '#A67B5B', '#9E7B4F'],
                'cosmetics': {
                    'Foundations': ['Soft Beige', 'Neutral Tan'],
                    'Blushes': ['Muted Peach', 'Soft Coral'],
                    'Lipsticks': ['Rosewood', 'Dusty Coral']
                }
            },
            'Deep Winter': {
                'desc': 'You have a dramatic, high-contrast appearance that shines in cool, bold shades.',
                'undertone': 'Cool',
                'undertone_desc': 'Your skin has cool undertones with hints of blue, pink, or cool beige.',
                'palette': ['#000000', '#4B0082', '#2F4F4F', '#8B0000', '#003366'],
                'cosmetics': {
                    'Foundations': ['Cool Espresso', 'Mocha'],
                    'Blushes': ['Berry', 'Plum'],
                    'Lipsticks': ['Wine', 'Crimson']
                }
            },
            'Cool Winter': {
                'desc': 'Your clear, icy coloring suits bright, high-contrast cool tones.',
                'undertone': 'Cool',
                'undertone_desc': 'Skin tones have blue or rosy undertones, often porcelain or deep ebony.',
                'palette': ['#4169E1', '#00008B', '#9932CC', '#8A2BE2', '#C71585'],
                'cosmetics': {
                    'Foundations': ['Porcelain', 'Cool Almond'],
                    'Blushes': ['Pink Ice', 'Cool Rose'],
                    'Lipsticks': ['Fuchsia', 'Magenta']
                }
            },
            'Bright Winter': {
                'desc': 'You have a striking appearance that thrives in clear, cool, and vivid colors.',
                'undertone': 'Cool',
                'undertone_desc': 'Cool undertones that suit high contrast and jewel tones.',
                'palette': ['#00FFFF', '#00BFFF', '#FF1493', '#9400D3', '#4682B4'],
                'cosmetics': {
                    'Foundations': ['Ivory', 'Cool Beige'],
                    'Blushes': ['Cool Pink', 'Icy Plum'],
                    'Lipsticks': ['Raspberry', 'Cherry Red']
                }
            },
            'Bright Spring': {
                'desc': 'You shine in clear, vivid colors with a fresh and lively brightness.',
                'undertone': 'Warm',
                'undertone_desc': 'Your undertones are warm with a bright, golden glow.',
                'palette': ['#FFD700', '#FFA07A', '#FF69B4', '#00FA9A', '#FF8C00'],
                'cosmetics': {
                    'Foundations': ['Golden Ivory', 'Warm Nude'],
                    'Blushes': ['Coral Pink', 'Soft Peach'],
                    'Lipsticks': ['Poppy Red', 'Bright Coral']
                }
            },
            'Warm Spring': {
                'desc': 'You glow in golden, creamy tones that reflect a sunlit warmth.',
                'undertone': 'Warm',
                'undertone_desc': 'Warm and golden skin undertones, sometimes with peach or apricot hints.',
                'palette': ['#FFDAB9', '#FFA500', '#F0E68C', '#E9967A', '#DAA520'],
                'cosmetics': {
                    'Foundations': ['Warm Beige', 'Peachy Nude'],
                    'Blushes': ['Golden Peach', 'Apricot'],
                    'Lipsticks': ['Coral', 'Warm Rose']
                }
            },
            'Light Spring': {
                'desc': 'You look best in light, warm pastels that are soft and fresh.',
                'undertone': 'Warm',
                'undertone_desc': 'Light warm undertones with peachy, creamy tones.',
                'palette': ['#FFFACD', '#FFE4B5', '#FAD6A5', '#FFDAB9', '#FFB6C1'],
                'cosmetics': {
                    'Foundations': ['Light Warm', 'Soft Ivory'],
                    'Blushes': ['Light Coral', 'Petal Peach'],
                    'Lipsticks': ['Peachy Pink', 'Light Coral']
                }
            },
            'Light Summer': {
                'desc': 'You suit soft, cool pastels and delicate, airy colors.',
                'undertone': 'Cool',
                'undertone_desc': 'Cool undertones with a soft, rosy or bluish tint.',
                'palette': ['#B0C4DE', '#D8BFD8', '#AFEEEE', '#ADD8E6', '#F0F8FF'],
                'cosmetics': {
                    'Foundations': ['Cool Ivory', 'Neutral Porcelain'],
                    'Blushes': ['Cool Rose', 'Light Pink'],
                    'Lipsticks': ['Soft Rose', 'Dusty Pink']
                }
            },
            'Cool Summer': {
                'desc': 'Your soft, elegant appearance pairs well with cool, powdery shades.',
                'undertone': 'Cool',
                'undertone_desc': 'Your skin has cool pink, blue, or neutral undertones.',
                'palette': ['#778899', '#C0C0C0', '#B0E0E6', '#D3D3D3', '#A9A9A9'],
                'cosmetics': {
                    'Foundations': ['Neutral Beige', 'Cool Buff'],
                    'Blushes': ['Cool Mauve', 'Rosy Pink'],
                    'Lipsticks': ['Plum Pink', 'Mauve Rose']
                }
            },
            'Soft Summer': {
                'desc': 'You have a low-contrast look that harmonizes with gentle, muted cool shades.',
                'undertone': 'Cool',
                'undertone_desc': 'Your undertones are soft and cool, sometimes with a hint of neutral beige.',
                'palette': ['#A8B2BD', '#BDBDC6', '#C1A192', '#A9A9A9', '#B6AFA9'],
                'cosmetics': {
                    'Foundations': ['Soft Beige', 'Neutral Cool'],
                    'Blushes': ['Muted Rose', 'Soft Plum'],
                    'Lipsticks': ['Dusty Rose', 'Muted Berry']
                }
            }
        }

    def analyze(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            return None
        
        # Convert to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Convert to HSV for better skin detection
        image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Define skin color ranges in HSV
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        
        # Create skin mask
        mask = cv2.inRange(image_hsv, lower_skin, upper_skin)
        
        # Apply morphological operations to clean up the mask
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # Get skin pixels
        skin_pixels = cv2.bitwise_and(image_rgb, image_rgb, mask=mask)
        
        # Reshape for clustering
        pixels = skin_pixels.reshape(-1, 3)
        pixels = pixels[pixels.sum(axis=1) > 0]  # Remove black pixels
        
        if len(pixels) == 0:
            return None
        
        # Use K-means to find dominant colors
        kmeans = KMeans(n_clusters=3, random_state=42)
        kmeans.fit(pixels)
        
        # Get the dominant colors
        colors = kmeans.cluster_centers_.astype(int)
        dominant = colors[0]
        
        # Convert to HSV for better undertone analysis
        h, s, v = colorsys.rgb_to_hsv(dominant[0]/255, dominant[1]/255, dominant[2]/255)
        
        # Determine season based on HSV values
        if v < 0.4:  # Deep
            if h < 0.1:  # Cool
                season = 'Deep Winter'
            else:  # Warm
                season = 'Deep Autumn'
        elif v > 0.7:  # Light
            if h < 0.1:  # Cool
                season = 'Light Summer'
            else:  # Warm
                season = 'Light Spring'
        else:  # Medium
            if h < 0.1:  # Cool
                season = 'Cool Summer'
            else:  # Warm
                season = 'Warm Autumn'
        
        return {
            'season': season,
            'dominant_rgb': tuple(dominant),
            'palette': self.season_types[season]['palette'],
            'desc': self.season_types[season]['desc'],
            'undertone': self.season_types[season]['undertone'],
            'undertone_desc': self.season_types[season]['undertone_desc'],
            'cosmetics': self.season_types[season]['cosmetics']
        }

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind('<Enter>', self.show)
        widget.bind('<Leave>', self.hide)

    def show(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, _, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 30
        y = y + cy + self.widget.winfo_rooty() + 30
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, background="#ffffe0", relief='solid', borderwidth=1, font=("tahoma", 9))
        label.pack(ipadx=4)

    def hide(self, event=None):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

class FlawntApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Flawnt Color Analysis')
        self.root.geometry('900x1000')
        self.root.minsize(800, 900)
        self.analyzer = ColorAnalyzer()
        self.theme = 'flatly'
        self.history = []
        self.sidebar = None
        self.content = None
        self.camera_running = False
        self.captured_image = None
        self.captured_path = None
        self.analysis = None
        
        # Configure custom styles with pink theme
        self.style = tb.Style()
        self.style.configure('Custom.TButton', font=('Montserrat', 10))
        self.style.configure('Title.TLabel', font=('Montserrat', 28, 'bold'))
        self.style.configure('Subtitle.TLabel', font=('Montserrat', 16))
        self.style.configure('Card.TFrame', padding=25)
        self.style.configure('Header.TLabel', font=('Montserrat', 14, 'bold'))
        self.style.configure('Body.TLabel', font=('Montserrat', 11))
        self.style.configure('Small.TLabel', font=('Montserrat', 9))
        
        # Set theme colors with pink palette
        self.colors = {
            'primary': '#FF69B4',      # Hot Pink
            'secondary': '#FFB6C1',    # Light Pink
            'success': '#FFC0CB',      # Pink
            'info': '#FFB6C1',         # Light Pink
            'warning': '#FFC0CB',      # Pink
            'danger': '#FF1493',       # Deep Pink
            'light': '#FFF0F5',        # Lavender Blush
            'dark': '#DB7093'          # Pale Violet Red
        }
        
        # Configure custom button styles
        self.style.configure('Pink.TButton',
                           background=self.colors['primary'],
                           foreground='white',
                           font=('Montserrat', 10))
        
        self.style.configure('LightPink.TButton',
                           background=self.colors['secondary'],
                           foreground='white',
                           font=('Montserrat', 10))
        
        self.create_sidebar()
        self.show_home()

    def create_sidebar(self):
        if self.sidebar:
            self.sidebar.destroy()
        self.sidebar = tb.Frame(self.root, bootstyle='dark', width=250)
        self.sidebar.pack(side=LEFT, fill=Y)
        self.sidebar.pack_propagate(False)
        
        # Logo section with pink theme
        logo_frame = tb.Frame(self.sidebar, bootstyle='dark')
        logo_frame.pack(fill=X, pady=(40, 30))
        
        # App logo and title with pink accent
        logo = tb.Label(logo_frame, text='💖', font=('Arial', 32))
        logo.pack()
        title = tb.Label(logo_frame, text='Flawnt', 
                        font=('Montserrat', 28, 'bold'),
                        foreground=self.colors['primary'])
        title.pack()
        subtitle = tb.Label(logo_frame, text='Color Analysis', 
                          font=('Montserrat', 12),
                          foreground=self.colors['secondary'])
        subtitle.pack()
        
        # Navigation section with pink buttons
        nav_frame = tb.Frame(self.sidebar, bootstyle='dark')
        nav_frame.pack(fill=X, pady=20)
        
        navs = [
            ('🏠 Home', self.show_home),
            ('🕑 History', self.show_history),
            ('🌗 Theme', self.toggle_theme),
            ('👤 Profile', self.show_profile)
        ]
        
        for txt, cmd in navs:
            btn = tb.Button(nav_frame, text=txt, 
                          bootstyle='secondary', width=25,
                          command=cmd, style='Pink.TButton')
            btn.pack(pady=10, padx=20)
        
        # Decorative separator with pink color
        separator = tb.Separator(self.sidebar, orient='horizontal', 
                               bootstyle='secondary')
        separator.pack(fill=X, pady=30, padx=20)
        
        # Version and info with pink accents
        info_frame = tb.Frame(self.sidebar, bootstyle='dark')
        info_frame.pack(side=BOTTOM, fill=X, pady=20)
        
        version = tb.Label(info_frame, text='v1.0.0', 
                         font=('Montserrat', 9),
                         foreground=self.colors['secondary'])
        version.pack()
        
        copyright = tb.Label(info_frame, text='© 2024 Flawnt', 
                           font=('Montserrat', 9),
                           foreground=self.colors['secondary'])
        copyright.pack()

    def clear_content(self):
        if self.content:
            self.content.destroy()
        self.content = tb.Frame(self.root, bootstyle='light')
        self.content.pack(side=LEFT, fill=BOTH, expand=True)

    def show_home(self):
        self.clear_content()
        
        # Main content frame with pink background
        main_frame = tb.Frame(self.content, bootstyle='light', padding=40)
        main_frame.pack(fill=BOTH, expand=True)
        
        # Top bar with search and share
        top_bar = tb.Frame(main_frame, bootstyle='light')
        top_bar.pack(fill=X, pady=(0, 20))
        
        # Search frame with modern design
        search_frame = tb.Frame(top_bar, bootstyle='light')
        search_frame.pack(side=LEFT, fill=X, expand=True)
        
        # Search entry with pink border
        search_entry = tb.Entry(search_frame, 
                              width=30,
                              font=('Montserrat', 10))
        search_entry.pack(side=LEFT, padx=(0, 10))
        search_entry.insert(0, 'Search color palettes...')
        search_entry.bind('<FocusIn>', lambda e: search_entry.delete(0, 'end') if search_entry.get() == 'Search color palettes...' else None)
        search_entry.bind('<FocusOut>', lambda e: search_entry.insert(0, 'Search color palettes...') if search_entry.get() == '' else None)
        
        # Search button with pink styling
        search_btn = tb.Button(search_frame, 
                             text='🔍',
                             width=3,
                             style='Pink.TButton',
                             command=lambda: self.search_palettes(search_entry.get()))
        search_btn.pack(side=LEFT)
        
        # Share button with modern design
        share_btn = tb.Button(top_bar, 
                            text='📤 Share',
                            width=10,
                            style='LightPink.TButton',
                            command=self.share_palette)
        share_btn.pack(side=RIGHT)
        
        # Welcome section with pink theme
        welcome_frame = tb.Frame(main_frame, bootstyle='light')
        welcome_frame.pack(fill=X, pady=(0, 40))
        
        tb.Label(welcome_frame, text='Welcome to Flawnt', 
                style='Title.TLabel',
                foreground=self.colors['primary']).pack(anchor=W)
        
        tb.Label(welcome_frame, text='Discover your perfect color palette', 
                style='Subtitle.TLabel',
                foreground=self.colors['secondary']).pack(anchor=W)
        
        # Main card with pink border
        card = tb.Frame(main_frame, bootstyle='secondary', padding=30)
        card.pack(fill=X, pady=(0, 40))
        
        # AI Guide Image with pink border
        try:
            ai_img = Image.open('ai_guide.png').resize((240, 280))
        except FileNotFoundError:
            ai_img = Image.new('RGB', (240, 280), self.colors['light'])
        ai_img_tk = ImageTk.PhotoImage(ai_img)
        ai_img_label = tk.Label(card, image=ai_img_tk, 
                              bd=2, relief='ridge')
        ai_img_label.image = ai_img_tk
        ai_img_label.pack(pady=(0, 30))
        
        # Steps section with pink accents
        steps = tb.Frame(card, bootstyle='light')
        steps.pack(fill=X, pady=10)
        
        tb.Label(steps, text='How it works:', 
                style='Header.TLabel',
                foreground=self.colors['primary']).pack(anchor=W)
        
        steps_list = [
            ('💖', 'Take a clear selfie or upload a photo'),
            ('💝', 'Crop to focus on your face'),
            ('💗', 'Get your personalized color palette!')
        ]
        
        for icon, text in steps_list:
            step_frame = tb.Frame(steps, bootstyle='light')
            step_frame.pack(fill=X, pady=8)
            tb.Label(step_frame, text=icon, 
                    font=('Montserrat', 14)).pack(side=LEFT, padx=(0, 15))
            tb.Label(step_frame, text=text, 
                    style='Body.TLabel',
                    foreground=self.colors['secondary']).pack(side=LEFT)
        
        # Action buttons with pink styling
        btn_frame = tb.Frame(main_frame, bootstyle='light')
        btn_frame.pack(pady=30)
        
        camera_btn = tb.Button(btn_frame, text='📸 Open Camera', 
                             bootstyle='danger', width=25,
                             command=self.show_camera,
                             style='Pink.TButton')
        camera_btn.pack(pady=10)
        
        upload_btn = tb.Button(btn_frame, text='📤 Upload Photo', 
                             bootstyle='secondary', width=25,
                             command=self.upload_photo,
                             style='LightPink.TButton')
        upload_btn.pack(pady=10)
        
        # Tips section with pink theme
        tips = tb.Frame(main_frame, bootstyle='light', padding=25)
        tips.pack(fill=X, pady=20)
        
        tb.Label(tips, text='💖 Selfie Tips', 
                style='Header.TLabel',
                foreground=self.colors['primary']).pack(anchor=W)
        
        tips_list = [
            '✨ Stand in front of good natural light',
            '👓 Take off your glasses',
            '😊 Use a neutral expression',
            '🎯 Keep your face centered',
            '💄 Remove heavy makeup if possible'
        ]
        
        for tip in tips_list:
            tb.Label(tips, text=tip, 
                    style='Body.TLabel',
                    foreground=self.colors['secondary']).pack(anchor=W, pady=4)

    def show_camera(self):
        self.clear_content()
        self.camera_running = True
        
        # Main camera frame with pink styling
        cam_frame = tb.Frame(self.content, bootstyle='light', padding=30)
        cam_frame.pack(pady=40, padx=40)
        
        # Camera title with pink theme
        title_frame = tb.Frame(cam_frame, bootstyle='light')
        title_frame.pack(fill=X, pady=(0, 20))
        
        tb.Label(title_frame, text='📸 Camera', 
                font=('Montserrat', 24, 'bold'),
                foreground=self.colors['primary']).pack()
        
        tb.Label(title_frame, text='Take a clear photo of your face', 
                font=('Montserrat', 12),
                foreground=self.colors['secondary']).pack()
        
        # Camera preview with pink border
        preview_frame = tb.Frame(cam_frame, bootstyle='secondary', padding=10)
        preview_frame.pack(pady=(0, 30))
        
        self.cam_label = tk.Label(preview_frame, width=480, height=360, 
                                 bd=3, relief='ridge', bg=self.colors['light'])
        self.cam_label.pack()
        
        # Control buttons with pink styling
        btns = tb.Frame(self.content, bootstyle='light')
        btns.pack(pady=20)
        
        capture_btn = tb.Button(btns, text='📸 Capture', 
                              width=20,
                              style='Pink.TButton',
                              command=self.capture_photo)
        capture_btn.pack(side=LEFT, padx=15)
        
        upload_btn = tb.Button(btns, text='📤 Upload', 
                             width=20,
                             style='LightPink.TButton',
                             command=self.upload_photo)
        upload_btn.pack(side=LEFT, padx=15)
        
        self.update_camera()

    def update_camera(self):
        if not self.camera_running:
            return
        cap = getattr(self, 'cap', None)
        if cap is None:
            self.cap = cv2.VideoCapture(0)
            cap = self.cap
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = img.resize((320, 240))
            img_tk = ImageTk.PhotoImage(img)
            self.cam_label.imgtk = img_tk
            self.cam_label.config(image=img_tk)
        self.root.after(30, self.update_camera)

    def capture_photo(self):
        if not hasattr(self, 'cap') or self.cap is None:
            return
        ret, frame = self.cap.read()
        if ret:
            self.camera_running = False
            self.cap.release()
            self.cap = None
            temp_path = 'captured_photo.jpg'
            cv2.imwrite(temp_path, frame)
            self.captured_path = temp_path
            self.show_crop_dialog(temp_path)

    def upload_photo(self):
        file_path = filedialog.askopenfilename(filetypes=[('Image files', '*.jpg *.jpeg *.png')])
        if file_path:
            self.camera_running = False
            if hasattr(self, 'cap') and self.cap:
                self.cap.release()
                self.cap = None
            self.captured_path = file_path
            self.show_crop_dialog(file_path)

    def show_crop_dialog(self, img_path):
        crop_win = tk.Toplevel(self.root)
        crop_win.title('Crop Image')
        img = Image.open(img_path)
        img = ImageOps.exif_transpose(img)
        img = img.resize((320, 320))
        img_tk = ImageTk.PhotoImage(img)
        canvas = tk.Canvas(crop_win, width=320, height=320)
        canvas.pack()
        canvas.create_image(0, 0, anchor='nw', image=img_tk)
        canvas.imgtk = img_tk
        # Simple square crop selector
        rect = canvas.create_rectangle(60, 60, 260, 260, outline='red', width=2)
        def crop_and_continue():
            x1, y1, x2, y2 = canvas.coords(rect)
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            cropped = img.crop((x1, y1, x2, y2)).resize((220, 260))
            cropped_path = 'cropped_photo.jpg'
            cropped.save(cropped_path)
            self.captured_path = cropped_path
            crop_win.destroy()
            self.show_preview()
        tb.Button(crop_win, text='Crop & Continue', bootstyle='danger', command=crop_and_continue).pack(pady=8)

    def show_preview(self):
        self.clear_content()
        card = tb.Frame(self.content, bootstyle='secondary', padding=18)
        card.pack(pady=30, padx=30, fill=X)
        img = Image.open(self.captured_path)
        img = img.resize((220, 260))
        img_tk = ImageTk.PhotoImage(img)
        img_label = tk.Label(card, image=img_tk, bd=2, relief='ridge')
        img_label.image = img_tk
        img_label.pack()
        tb.Button(self.content, text='Analyze', bootstyle='danger', width=20, command=self.analyze_image).pack(pady=24)

    def analyze_image(self):
        self.clear_content()
        spinner = ttk.Progressbar(self.content, mode='indeterminate', length=200)
        spinner.pack(pady=60)
        tb.Label(self.content, text='Analyzing...', font=('Montserrat', 14, 'bold'), bootstyle='danger').pack(pady=10)
        spinner.start(10)
        threading.Thread(target=self.run_analysis, args=(spinner,), daemon=True).start()

    def run_analysis(self, spinner):
        time.sleep(1.2)  # Simulate processing
        self.analysis = self.analyzer.analyze(self.captured_path)
        self.history.append((self.captured_path, self.analysis))
        self.root.after(100, lambda: self.show_results(spinner))

    def show_results(self, spinner):
        if spinner:
            spinner.stop()
        self.clear_content()
        
        # Create main container frame with gradient background
        container = tb.Frame(self.content, bootstyle='light')
        container.pack(fill=BOTH, expand=True)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(container, bg='#F8F9FA', highlightthickness=0)
        scrollbar = tb.Scrollbar(container, orient="vertical", command=canvas.yview)
        
        # Configure canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side=RIGHT, fill=Y)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        
        # Create frame for content
        content_frame = tb.Frame(canvas, bootstyle='light')
        
        # Create window in canvas for the frame
        canvas_window = canvas.create_window((0, 0), window=content_frame, anchor="nw")
        
        # Configure canvas scrolling region
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        # Configure canvas width
        def configure_canvas_width(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        # Bind events
        content_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_canvas_width)
        
        # Mouse wheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        # Bind mousewheel to canvas
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # Header section with decorative elements
        header_frame = tb.Frame(content_frame, bootstyle='light', padding=(40, 40, 40, 20))
        header_frame.pack(fill=X)
        
        # Decorative line
        line = tb.Separator(header_frame, orient='horizontal', bootstyle='secondary')
        line.pack(fill=X, pady=(0, 20))
        
        # Season icon and title with modern design
        icon_frame = tb.Frame(header_frame, bootstyle='light')
        icon_frame.pack(pady=(0, 20))
        
        # Large decorative icon
        icon = tk.Label(icon_frame, text='🎨', font=('Arial', 64))
        icon.pack()
        
        # Season name with enhanced typography
        tb.Label(header_frame, text=self.analysis['season'], 
                font=('Montserrat', 32, 'bold'),
                foreground='#2C3E50').pack()
        
        # Description with modern card design
        desc_card = tb.Frame(content_frame, bootstyle='light', padding=30)
        desc_card.pack(pady=(0, 30), padx=40, fill=X)
        
        # Add subtle shadow effect
        desc_card.configure(relief='solid', borderwidth=1)
        
        tb.Label(desc_card, text=self.analysis['desc'], 
                style='Body.TLabel',
                foreground='#34495E',
                wraplength=600,
                justify='center',
                font=('Montserrat', 12)).pack()
        
        # Color palette section with enhanced design
        palette_card = tb.Frame(content_frame, bootstyle='light', padding=30)
        palette_card.pack(pady=(0, 30), padx=40, fill=X)
        
        # Add subtle shadow effect
        palette_card.configure(relief='solid', borderwidth=1)
        
        # Section header with icon
        header = tb.Frame(palette_card, bootstyle='light')
        header.pack(fill=X, pady=(0, 25))
        
        tb.Label(header, text='🎨', font=('Arial', 24)).pack(side=LEFT, padx=(0, 10))
        tb.Label(header, text='Your Color Palette', 
                style='Header.TLabel',
                font=('Montserrat', 20, 'bold'),
                foreground='#2C3E50').pack(side=LEFT)
        
        # Create a frame for color swatches with modern layout
        colors_frame = tb.Frame(palette_card)
        colors_frame.pack()
        
        # Display each color with enhanced design
        for color in self.analysis['palette']:
            color_frame = tb.Frame(colors_frame, bootstyle='light')
            color_frame.pack(fill=X, pady=10)
            
            # Larger color swatch with enhanced border
            swatch_frame = tb.Frame(color_frame, bootstyle='light')
            swatch_frame.pack(side=LEFT, padx=(0, 20))
            
            swatch = tk.Label(swatch_frame, width=16, height=6, 
                            bg=color, relief='solid', bd=1)
            swatch.pack()
            
            # Color information with improved layout
            info_frame = tb.Frame(color_frame, bootstyle='light')
            info_frame.pack(side=LEFT, fill=Y)
            
            # Display hex code with enhanced styling
            tb.Label(info_frame, text=color, 
                    font=('Montserrat', 14, 'bold'),
                    foreground='#34495E').pack(anchor=W)
            
            # Add tooltip with color information
            ToolTip(swatch, f"Color: {color}")
        
        # Undertone section with modern card
        undertone_card = tb.Frame(content_frame, bootstyle='light', padding=30)
        undertone_card.pack(pady=(0, 30), padx=40, fill=X)
        
        # Add subtle shadow effect
        undertone_card.configure(relief='solid', borderwidth=1)
        
        # Section header with icon
        header = tb.Frame(undertone_card, bootstyle='light')
        header.pack(fill=X, pady=(0, 20))
        
        tb.Label(header, text='✨', font=('Arial', 24)).pack(side=LEFT, padx=(0, 10))
        tb.Label(header, text='Skin Undertone', 
                style='Header.TLabel',
                font=('Montserrat', 20, 'bold'),
                foreground='#2C3E50').pack(side=LEFT)
        
        # Undertone information with enhanced typography
        tb.Label(undertone_card, text=self.analysis['undertone'], 
                font=('Montserrat', 18, 'bold'),
                foreground='#34495E').pack(anchor=W, pady=(0, 10))
        
        tb.Label(undertone_card, text=self.analysis['undertone_desc'], 
                style='Body.TLabel',
                foreground='#34495E',
                wraplength=600,
                font=('Montserrat', 12)).pack(anchor=W)
        
        # Cosmetics recommendations with modern design
        rec_card = tb.Frame(content_frame, bootstyle='light', padding=30)
        rec_card.pack(pady=(0, 30), padx=40, fill=X)
        
        # Add subtle shadow effect
        rec_card.configure(relief='solid', borderwidth=1)
        
        # Section header with icon
        header = tb.Frame(rec_card, bootstyle='light')
        header.pack(fill=X, pady=(0, 20))
        
        tb.Label(header, text='💄', font=('Arial', 24)).pack(side=LEFT, padx=(0, 10))
        tb.Label(header, text='Recommended Cosmetics', 
                style='Header.TLabel',
                font=('Montserrat', 20, 'bold'),
                foreground='#2C3E50').pack(side=LEFT)
        
        # Cosmetics categories with enhanced layout
        for cat in ['Foundations', 'Blushes', 'Lipsticks']:
            box = tb.Frame(rec_card, bootstyle='light', padding=20)
            box.pack(fill=X, pady=10)
            
            # Category header with icon
            cat_header = tb.Frame(box, bootstyle='light')
            cat_header.pack(fill=X, pady=(0, 10))
            
            icon_map = {'Foundations': '🎨', 'Blushes': '💋', 'Lipsticks': '💄'}
            tb.Label(cat_header, text=icon_map[cat], 
                    font=('Arial', 16)).pack(side=LEFT, padx=(0, 10))
            
            tb.Label(cat_header, text=cat, 
                    font=('Montserrat', 16, 'bold'),
                    foreground='#2C3E50').pack(side=LEFT)
            
            # Items with bullet points
            for item in self.analysis['cosmetics'][cat]:
                item_frame = tb.Frame(box, bootstyle='light')
                item_frame.pack(fill=X, pady=3)
                
                tb.Label(item_frame, text='•', 
                        font=('Montserrat', 12),
                        foreground='#34495E').pack(side=LEFT, padx=(0, 10))
                
                tb.Label(item_frame, text=item, 
                        style='Body.TLabel',
                        foreground='#34495E',
                        font=('Montserrat', 12)).pack(side=LEFT)
        
        # Export button with modern design
        export_frame = tb.Frame(content_frame, bootstyle='light', padding=(0, 0, 40, 40))
        export_frame.pack(fill=X)
        
        export_btn = tb.Button(export_frame, 
                             text='💾 Export Results', 
                             width=25,
                             bootstyle='info',
                             font=('Montserrat', 12),
                             command=self.export_result)
        export_btn.pack()
        
        # Update scroll region when content changes
        content_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def show_history(self):
        self.clear_content()
        
        # Title with modern styling
        header_frame = tb.Frame(self.content, bootstyle='light', padding=20)
        header_frame.pack(fill=X)
        
        tb.Label(header_frame, text='Analysis History', 
                font=('Montserrat', 24, 'bold'),
                bootstyle='danger').pack()
        
        # History items with enhanced cards
        for idx, (img_path, analysis) in enumerate(reversed(self.history[-10:])):
            frame = tb.Frame(self.content, bootstyle='secondary', padding=15)
            frame.pack(pady=8, padx=30, fill=X)
            
            # Thumbnail with border
            img = Image.open(img_path).resize((80, 90))
            img_tk = ImageTk.PhotoImage(img)
            img_label = tk.Label(frame, image=img_tk, bd=2, relief='ridge')
            img_label.image = img_tk
            img_label.pack(side=LEFT, padx=10)
            
            # Analysis info with improved typography
            info = tb.Frame(frame, bootstyle='secondary')
            info.pack(side=LEFT, padx=10, fill=X, expand=True)
            
            tb.Label(info, text=analysis['season'], 
                    font=('Montserrat', 12, 'bold'),
                    bootstyle='danger').pack(anchor=W)
            
            tb.Label(info, text=f"Undertone: {analysis['undertone']}", 
                    font=('Montserrat', 10)).pack(anchor=W)
            
            # View button with modern styling
            view_btn = tb.Button(frame, text='👁️ View', 
                               bootstyle='info', width=10,
                               command=lambda a=analysis: self.show_history_result(a),
                               style='Custom.TButton')
            view_btn.pack(side=RIGHT, padx=10)

    def show_history_result(self, analysis):
        self.analysis = analysis
        self.show_results(spinner=None)

    def show_profile(self):
        self.clear_content()
        
        # Main profile container with padding and light background
        profile_container = tb.Frame(self.content, bootstyle='light', padding=40)
        profile_container.pack(fill=BOTH, expand=True)
        
        # Header section with icon and title
        header_frame = tb.Frame(profile_container, bootstyle='light')
        header_frame.pack(fill=X, pady=(0, 30))
        
        tb.Label(header_frame, text='👤', font=('Arial', 40)).pack(side=LEFT, padx=(0, 15))
        tb.Label(header_frame, text='Your Profile', font=('Montserrat', 28, 'bold'), foreground='#2C3E50').pack(side=LEFT)
        
        # Decorative separator
        tb.Separator(profile_container, orient='horizontal', bootstyle='secondary').pack(fill=X, pady=(0, 30))
        
        # Personal Information Card
        personal_card = tb.Frame(profile_container, bootstyle='light', padding=30)
        personal_card.pack(fill=X, pady=(0, 30))
        personal_card.configure(relief='solid', borderwidth=1)
        
        # Section header with icon
        personal_header = tb.Frame(personal_card, bootstyle='light')
        personal_header.pack(fill=X, pady=(0, 20))
        tb.Label(personal_header, text='📝', font=('Arial', 20)).pack(side=LEFT, padx=(0, 10))
        tb.Label(personal_header, text='Personal Information', font=('Montserrat', 18, 'bold'), foreground='#2C3E50').pack(side=LEFT)
        
        # Personal info fields (grid layout)
        info_frame = tb.Frame(personal_card, bootstyle='light')
        info_frame.pack(fill=X)
        
        # First row
        tb.Label(info_frame, text='First Name:', font=('Montserrat', 11)).grid(row=0, column=0, sticky=W, padx=5, pady=5)
        tb.Entry(info_frame, width=18).grid(row=0, column=1, sticky=W, padx=5, pady=5)
        tb.Label(info_frame, text='Last Name:', font=('Montserrat', 11)).grid(row=0, column=2, sticky=W, padx=5, pady=5)
        tb.Entry(info_frame, width=18).grid(row=0, column=3, sticky=W, padx=5, pady=5)
        
        # Second row
        tb.Label(info_frame, text='Date of Birth:', font=('Montserrat', 11)).grid(row=1, column=0, sticky=W, padx=5, pady=5)
        tb.Entry(info_frame, width=18).grid(row=1, column=1, sticky=W, padx=5, pady=5)
        tb.Label(info_frame, text='Gender:', font=('Montserrat', 11)).grid(row=1, column=2, sticky=W, padx=5, pady=5)
        gender_combo = ttk.Combobox(info_frame, values=['Male', 'Female', 'Other'], width=16)
        gender_combo.grid(row=1, column=3, sticky=W, padx=5, pady=5)
        
        # Third row
        tb.Label(info_frame, text='Email:', font=('Montserrat', 11)).grid(row=2, column=0, sticky=W, padx=5, pady=5)
        tb.Entry(info_frame, width=18).grid(row=2, column=1, sticky=W, padx=5, pady=5)
        tb.Label(info_frame, text='Phone:', font=('Montserrat', 11)).grid(row=2, column=2, sticky=W, padx=5, pady=5)
        tb.Entry(info_frame, width=18).grid(row=2, column=3, sticky=W, padx=5, pady=5)
        
        # Color Preferences Card
        color_card = tb.Frame(profile_container, bootstyle='light', padding=30)
        color_card.pack(fill=X, pady=(0, 30))
        color_card.configure(relief='solid', borderwidth=1)
        
        # Section header with icon
        color_header = tb.Frame(color_card, bootstyle='light')
        color_header.pack(fill=X, pady=(0, 20))
        tb.Label(color_header, text='🎨', font=('Arial', 20)).pack(side=LEFT, padx=(0, 10))
        tb.Label(color_header, text='Color Preferences', font=('Montserrat', 18, 'bold'), foreground='#2C3E50').pack(side=LEFT)
        
        # Favorite color input
        fav_color_frame = tb.Frame(color_card, bootstyle='light')
        fav_color_frame.pack(fill=X, pady=(0, 15))
        tb.Label(fav_color_frame, text='Favorite Colors:', font=('Montserrat', 11)).pack(side=LEFT, padx=(0, 10))
        tb.Entry(fav_color_frame, width=8).pack(side=LEFT)
        color_box = tk.Label(fav_color_frame, width=3, height=1, bg='#FFFFFF', relief='ridge', bd=1)
        color_box.pack(side=LEFT, padx=(5, 0))
        
        # Style Preferences
        style_frame = tb.Frame(color_card, bootstyle='light')
        style_frame.pack(fill=X, pady=(10, 0))
        tb.Label(style_frame, text='Style Preferences:', font=('Montserrat', 11)).pack(anchor=W)
        
        # Style options (modern checkboxes)
        styles = ['Casual', 'Formal', 'Business', 'Sporty', 'Bohemian', 'Minimalist']
        for style in styles:
            cb_frame = tb.Frame(style_frame, bootstyle='light')
            cb_frame.pack(anchor=W, pady=2)
            cb = tb.Checkbutton(cb_frame, text=style, bootstyle='round-toggle', font=('Montserrat', 10))
            cb.pack(side=LEFT)

    def toggle_theme(self):
        self.theme = 'darkly' if self.theme == 'flatly' else 'flatly'
        self.root.style.theme_use(self.theme)

    def export_result(self):
        if not self.analysis:
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension='.png',
            filetypes=[('PNG Image', '*.png')]
        )
        
        if file_path:
            # Create a modern export image
            img = Image.new('RGB', (600, 800), 'white')
            draw = ImageDraw.Draw(img)
            
            # Add title
            draw.text((30, 30), f"Flawnt Color Analysis", fill='#333333', font=('Arial', 24, 'bold'))
            draw.text((30, 70), f"Season: {self.analysis['season']}", fill='#333333', font=('Arial', 18))
            draw.text((30, 110), f"Undertone: {self.analysis['undertone']}", fill='#333333', font=('Arial', 16))
            
            # Add color palette
            y = 160
            for color in self.analysis['palette']:
                draw.rectangle([30, y, 100, y+40], fill=color)
                draw.text((120, y+10), color, fill='#333333', font=('Arial', 14))
                y += 60
            
            # Add cosmetics recommendations
            y += 20
            draw.text((30, y), "Recommended Cosmetics:", fill='#333333', font=('Arial', 16, 'bold'))
            y += 40
            
            for cat in ['Foundations', 'Blushes', 'Lipsticks']:
                draw.text((30, y), f"{cat}:", fill='#333333', font=('Arial', 14, 'bold'))
                y += 30
                for item in self.analysis['cosmetics'][cat]:
                    draw.text((50, y), f"• {item}", fill='#333333', font=('Arial', 12))
                    y += 25
                y += 10
            
            img.save(file_path)
            messagebox.showinfo("Success", "Results exported successfully!")

    def search_palettes(self, query):
        if query and query != 'Search color palettes...':
            # Create a new window for search results
            search_window = tk.Toplevel(self.root)
            search_window.title('Search Results')
            search_window.geometry('600x400')
            
            # Style the search results window
            search_window.configure(bg=self.colors['light'])
            
            # Search results header
            header = tb.Frame(search_window, bootstyle='light')
            header.pack(fill=X, pady=20, padx=20)
            
            tb.Label(header, 
                    text=f'Results for: {query}',
                    font=('Montserrat', 16, 'bold'),
                    foreground=self.colors['primary']).pack()
            
            # Results frame with scrollbar
            results_frame = tb.Frame(search_window, bootstyle='light')
            results_frame.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))
            
            # Add some sample results (you can replace this with actual search logic)
            sample_results = [
                'Warm Autumn Palette',
                'Cool Summer Colors',
                'Spring Pastels',
                'Winter Jewel Tones'
            ]
            
            for result in sample_results:
                result_frame = tb.Frame(results_frame, bootstyle='secondary', padding=10)
                result_frame.pack(fill=X, pady=5)
                
                tb.Label(result_frame, 
                        text=result,
                        font=('Montserrat', 12),
                        foreground=self.colors['secondary']).pack(side=LEFT)
                
                view_btn = tb.Button(result_frame,
                                   text='View',
                                   width=8,
                                   style='Pink.TButton',
                                   command=lambda r=result: self.view_search_result(r))
                view_btn.pack(side=RIGHT)

    def share_palette(self):
        # Create a share dialog
        share_window = tk.Toplevel(self.root)
        share_window.title('Share Palette')
        share_window.geometry('400x300')
        
        # Style the share window
        share_window.configure(bg=self.colors['light'])
        
        # Share options header
        header = tb.Frame(share_window, bootstyle='light')
        header.pack(fill=X, pady=20, padx=20)
        
        tb.Label(header, 
                text='Share Your Palette',
                font=('Montserrat', 16, 'bold'),
                foreground=self.colors['primary']).pack()
        
        # Share options
        options_frame = tb.Frame(share_window, bootstyle='light')
        options_frame.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))
        
        share_options = [
            ('📱 Share on Social Media', self.share_social),
            ('📧 Share via Email', self.share_email),
            ('💾 Save to Gallery', self.save_to_gallery),
            ('🔗 Copy Link', self.copy_link)
        ]
        
        for text, command in share_options:
            btn = tb.Button(options_frame,
                          text=text,
                          width=25,
                          style='LightPink.TButton',
                          command=command)
            btn.pack(pady=10)

    def view_search_result(self, result):
        # Placeholder for viewing search results
        messagebox.showinfo('View Result', f'Viewing: {result}')

    def share_social(self):
        # Placeholder for social media sharing
        messagebox.showinfo('Share', 'Sharing to social media...')

    def share_email(self):
        # Placeholder for email sharing
        messagebox.showinfo('Share', 'Sharing via email...')

    def save_to_gallery(self):
        # Placeholder for saving to gallery
        messagebox.showinfo('Save', 'Saving to gallery...')

    def copy_link(self):
        # Placeholder for copying link
        messagebox.showinfo('Copy', 'Link copied to clipboard!')

if __name__ == '__main__':
    root = tb.Window(themename='flatly')
    app = FlawntApp(root)
    root.mainloop() 