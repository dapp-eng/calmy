from kivy.uix.screenmanager import ScreenManager, SlideTransition, FadeTransition, WipeTransition
from kivymd.app import MDApp
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
)
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivymd.uix.tooltip import MDTooltip, MDTooltipPlain
from kivymd.icon_definitions import md_icons
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.button import MDButton, MDButtonText
from kivy.uix.widget import Widget
from kivymd.uix.anchorlayout import AnchorLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.divider import MDDivider
from kivymd.uix.textfield import MDTextField
from kivymd.uix.scrollview import ScrollView
from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemSupportingText, MDListItemTertiaryText, MDListItemTrailingCheckbox
from kivy.metrics import dp
from kivy.metrics import sp
from kivy.config import Config
from kivy.core.text import LabelBase
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Line, Color
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import StringProperty, ListProperty, NumericProperty, BooleanProperty, ObjectProperty
import matplotlib.pyplot as plt
from matplotlib import font_manager
import random
import math
import sqlite3
import os
import sys
import json
import locale
import shutil
from fpdf import FPDF
from kivy.utils import platform
from datetime import datetime, timedelta

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

LabelBase.register(name="Poppins-Regular", fn_regular=resource_path("assets/fonts/Poppins-Regular.ttf"))
LabelBase.register(name="Poppins-SemiBold", fn_regular=resource_path("assets/fonts/Poppins-SemiBold.ttf"))
LabelBase.register(name="Poppins-Medium", fn_regular=resource_path("assets/fonts/Poppins-Medium.ttf"))
LabelBase.register(name="Poppins-Bold", fn_regular=resource_path("assets/fonts/Poppins-Bold.ttf"))

def get_persistent_db():
    app_data = os.path.join(os.getenv('APPDATA', os.path.expanduser("~/.config")), "Calmy!")
    os.makedirs(app_data, exist_ok=True)
    return os.path.join(app_data, 'data.db')

def get_db():
    persistent_db = get_persistent_db()
    if not os.path.exists(persistent_db):
        if getattr(sys, 'frozen', False):
            data_db = os.path.join(sys._MEIPASS, 'data', 'data.db')
        else:
            data_db = os.path.join(os.path.dirname(__file__), 'data', 'data.db')
        
        if os.path.exists(data_db):
            shutil.copy(data_db, persistent_db)
    return persistent_db

DATABASE_PATH = get_db()

def get_user(username, password):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_data WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user
    
def create_data_table():
    if not os.path.exists(DATABASE_PATH):
        pass
    else:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_lengkap TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            tanggal_lahir TEXT,
            program TEXT,
            jenis_kelamin TEXT,
            usia INTEGER,
            tinggi_badan INTEGER,
            berat_badan INTEGER,
            level_aktivitas TEXT,
            bmi_value REAL DEFAULT 0,
            bmr_value REAL DEFAULT 0,
            target_calories REAL DEFAULT 0,
            daily_calories REAL DEFAULT 0,
            daily_data TEXT
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS calories_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            nama_makanan TEXT NOT NULL,
            jumlah REAL NOT NULL,
            satuan TEXT NOT NULL,
            kalori REAL NOT NULL,
            kategori TEXT NOT NULL,
            tanggal DATE DEFAULT CURRENT_DATE,
            FOREIGN KEY (username) REFERENCES user_data(username)
            )
        ''')
        
        conn.commit()
        conn.close()

def hitung_usia(tanggal_lahir):
    birth_date = datetime.strptime(tanggal_lahir, "%d/%m/%Y")
    today = datetime.today()
    usia = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return usia

def get_greeting():
    app = App.get_running_app()
    user_data = app.user_data
    tanggal_lahir = user_data["tanggal_lahir"]
    current_hour = datetime.now().hour
    today = datetime.now().strftime("%m-%d")
    user_birthdate = datetime.strptime(tanggal_lahir, "%d/%m/%Y")
    
    if user_birthdate.strftime("%m-%d") == today:
        return "Selamat Ulang Tahun"
    elif 5 <= current_hour < 12:
        return "Selamat Pagi"
    elif 12 <= current_hour < 15:
        return "Selamat Siang"
    elif 15 <= current_hour < 18:
        return "Selamat Sore"
    else:
        return "Selamat Malam"

class AnalogClock(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update_clock, 1)

    def update_clock(self, *args):
        self.canvas.clear()
        now = datetime.now()
        hour = (now.hour % 12) + (now.minute / 60.0)
        minute = now.minute
        second = now.second

        with self.canvas:
            Color(0.125, 0.227, 0.290, 1)
            Line(circle=(self.center_x, self.center_y, self.width / 2 - 10), width=2)
            Color(0.125, 0.227, 0.290, 1)
            self.draw_hand(hour * 30, 0.45)
            Color(0.125, 0.227, 0.290, 1)
            self.draw_hand(minute * 6, 0.65)
            Color(0.988, 0.671, 0.196, 1)
            self.draw_hand(second * 6, 0.8)

    def draw_hand(self, angle, length):
        angle_rad = math.radians(-angle + 90)
        x = self.center_x + length * (self.width / 2 - 10) * math.cos(angle_rad)
        y = self.center_y + length * (self.height / 2 - 10) * math.sin(angle_rad)
        Line(points=[self.center_x, self.center_y, x, y], width=2)

class CircularProgressBar(AnchorLayout):
    set_value = NumericProperty(0)
    value = NumericProperty(0)
    progress_value = NumericProperty(0)
    bar_color = ListProperty([0, 1, 0])
    bar_width = NumericProperty(18)
    text = StringProperty("0%")
    duration = NumericProperty(1)
    counter = 0
    last_date = StringProperty("")
    animation = None
    warning = False
    
    def __init__(self, **kwargs):
        super(CircularProgressBar, self).__init__(**kwargs)
    
    def animate(self):
        if self.value == 0:
            self.percent_counter()
            return
        self.animation = Clock.schedule_interval(self.percent_counter, self.duration/self.value*1.25)
    
    def reset_animation(self):
        if self.animation:
            Clock.unschedule(self.animation)
        self.counter = 0
        self.text = "0%"
        self.set_value = 0
        self.bar_color = [0, 1, 0]
        self.warning = False
    
    def percent_counter(self, *args):
        if self.counter < self.value:
            self.counter += 1
            self.text = f"{self.counter}%"
            self.set_value = self.counter
            if self.counter <= 50:
                self.bar_color = [0, 1, 0]
            elif 50 < self.counter <= 70:
                self.bar_color = [0.988, 0.671, 0.196]
            elif 51 < self.counter <= 100:
                self.bar_color = [1, 0, 0]
            elif self.counter > 100:
                self.show_warning()
        else:
            if self.animation:
                Clock.unschedule(self.animation)
                self.animation = None
    
    def update_progress(self, dt):
        today_date = datetime.now().strftime("%d-%m-%Y")
        if self.last_date != today_date:
            self.progress_value = 0
            self.last_date = today_date
    
    def show_warning(self):
        if not self.warning:
            warning = MDDialog(
                MDDialogIcon(
                    icon="alert-outline",
                    theme_font_size="Custom",
                    font_size="35sp",
                ),
                MDDialogHeadlineText(
                    text="Peringatan!",
                    theme_font_name="Custom",
                    font_name="Poppins-Bold",
                ),
                MDDialogSupportingText(
                    text="Konsumsi kalori anda telah melebihi target kalori harian. Mohon perhatikan pola makan Anda!",
                    theme_font_name="Custom",
                    font_name="Poppins-Medium",
                    theme_font_size="Custom",
                    font_size="16sp",
                ),
                MDDialogButtonContainer(
                    Widget(),
                    MDButton(
                        MDButtonText(text="Oke", theme_font_name="Custom", font_name="Poppins-Regular"),
                        style="text",
                        on_release=lambda x: self.close_dialog(warning),
                    ),
                    spacing="8dp",
                ),
            )
            warning.open()
            self.warning = True
    
    def close_dialog(self, dialog):
        dialog.dismiss()      
            
Builder.load_string('''
<CircularProgressBar>:
    canvas.before:
        Color:
            rgba: root.bar_color + [0.3]
        Line:
            width: root.bar_width
            ellipse: (self.x, self.y, self.width, self.height, 0, 360)
    canvas.after:
        Color:
            rgb: root.bar_color
        Line:
            width: root.bar_width
            ellipse: (self.x, self.y, self.width, self.height, 0, max(root.set_value*3.6, 1))
    
    MDLabel:
        text: root.text
        theme_font_name: "Custom"
        theme_font_size: "Custom"
        font_size: "35sp"
        font_name: "Poppins-Bold"
        pos_hint: {"center_x": .5, "center_y": .5}
        halign: "center"
        theme_text_color: "Custom"
        text_color: root.bar_color
''')

def get_week_data():
    app = App.get_running_app()
    user_data = app.user_data
        
    if user_data:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
            
        cursor.execute("SELECT daily_data FROM user_data WHERE id = ?", (user_data["id"],))
        records = cursor.fetchall()
            
        today = datetime.now().date()
        start_date = today - timedelta(days=today.weekday())
            
        data = []
        for record in records:
            daily_data_list = json.loads(record[0])
            for entry in daily_data_list:
                entry_date = datetime.strptime(entry["tanggal"], '%Y-%m-%d').date()
                if start_date <= entry_date <= today:
                    data.append(entry)
            
        conn.close()
        return data

def create_weekly_chart(data, data_type="berat_badan"):
    app = App.get_running_app()
    days_of_week = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
    today = datetime.now()
    start_date = today - timedelta(days=today.weekday())
    
    if data:
        first_date = datetime.strptime(data[0]['tanggal'], '%Y-%m-%d')
    else:
        first_date = today
   
    if data_type == "berat_badan":
        values_by_date = {entry['tanggal']: float(entry['berat_badan']) for entry in data}
    elif data_type == "tinggi_badan":
        values_by_date = {entry['tanggal']: float(entry['tinggi_badan']) for entry in data}
    elif data_type == "kalori":
        values_by_date = {entry['tanggal']: float(entry['kalori']) for entry in data}
    else:
        raise ValueError("Data tidak valid")

    values = []
    for i in range(7):
        current_date = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
        if (start_date + timedelta(days=i)) < first_date:
            values.append(0)
        else:
            values.append(values_by_date.get(current_date, 0)) 

    plt.figure(figsize=(6, 4))
    plt.plot(days_of_week, values, marker='o', color='orange', label=f'{data_type.replace("_", " ").title()}')
    plt.title(f"Rekap Mingguan: {data_type.replace('_', ' ').title()}", fontsize=14, weight='bold')
    plt.xlabel("Hari", fontsize=12)
    plt.ylabel(f"{data_type.replace('_', ' ').title()}", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    
    chart_path = app.resource_path(f"assets/weekly_{data_type}.png")
    plt.savefig(chart_path)
    plt.close()
    
    return chart_path

hari_ind = {"Monday": "Sen", "Tuesday": "Sel", "Wednesday": "Rab", "Thursday": "Kam", "Friday": "Jum", "Saturday": "Sab", "Sunday": "Min"}
bulan_ind = {"January": "Jan", "February": "Feb", "March": "Mar", "April": "Apr", "May": "Mei", "June": "Jun", "July": "Jul", "August": "Agu", "September": "Sep", "October": "Okt", "November": "Nov", "December": "Des"}

quotes = [
    "Makanan sehat adalah investasi terbaik untuk tubuhmu. Mulailah hari ini, dan rasakan perubahannya besok!",
    "Tubuh yang sehat dimulai dari keputusan kecil setiap hari. Pilih makanan yang memberi gizi dan energi.",
    "Kamu adalah apa yang kamu makan. Pilih makanan yang memberi kekuatan dan bukan hanya rasa kenyang.",
    "Setiap kali kamu memilih makanan sehat, kamu sedang memberikan hadiah terbaik untuk tubuhmu.",
    "Makanan sehat bukan hanya untuk tubuh, tapi juga untuk pikiran yang lebih jernih dan penuh energi!",
    "Mengelola makanan dengan bijak hari ini akan memberi kamu tubuh yang lebih kuat dan hidup yang lebih panjang.",
    "Jaga tubuhmu dengan makanan sehat, karena tubuh yang sehat adalah kunci untuk menjalani hidup penuh semangat.",
    "Jangan lupa makan, olahraga dan istirahat yang cukup ya!!, kesehatanmu loh ><"
]

quotes2 = [
    "Healthy food is the best investment for your body. Start today, and feel the difference tomorrow!",
    "A healthy body starts with small decisions every day. Choose foods that nourish and energize.",
    "You are what you eat. Choose foods that give you strength and not just satiety.",
    "Every time you choose healthy food, you are giving your body the best gift.",
    "Healthy food is not only for your body, but also for a clearer and more energized mind!",
    "Managing your food wisely today will give you a stronger body and a longer life.",
    "Take care of your body with healthy food, because a healthy body is the key to living a vibrant life.",
    "Don't forget to eat, exercise and get enough rest!!, your health is important ><"
]

class SplashScreen(MDScreen):
    pass

class WelcomeScreen(MDScreen):
    pass

class AboutScreen(MDScreen):
    pass

class InfoScreen(MDScreen):
    pass

class Signup1Screen(MDScreen):
    pass

class Signup2Screen(MDScreen):   
    def update_helper_text(self, text_field_id, new_text):
        text_field = self.ids[text_field_id]
        text_field.error = True
        text_field.error_color = "FF0000FF"
        self.ids.error_label.text = new_text
        
    def clear_error(self):
        self.ids.error_label.text = ""
        
    def show_password(self):
        password_field1 = self.ids.passw1
        password_field2 = self.ids.passw2
        password_label = self.ids.password_label
        
        if password_field1.password:
            password_field1.password = False
            password_field2.password = False
            password_label.text = "Hide password"
        else:
            password_field1.password = True
            password_field2.password = True
            password_label.text = "Show password"
    
    def validate2(self):
        nama_lengkap = self.ids.namalengkap.text
        username = self.ids.user.text
        password = self.ids.passw1.text
        confirm_password = self.ids.passw2.text

        if not nama_lengkap:
            self.update_helper_text("namalengkap", "Nama Lengkap harus diisi!")
            return

        if " " in username:
            self.update_helper_text("user", "Username tidak boleh mengandung spasi!")
            return
        
        if len(username) > 10:
            self.update_helper_text("user", "Username tidak boleh lebih dari 10 karakter!")
            return
        
        if not username:
            self.update_helper_text("user", "Username tidak boleh kosong!")
            return
        
        if not password or not confirm_password:
            if not password:
                self.update_helper_text("passw1", "Password tidak boleh kosong!")
                return
            elif not confirm_password:
                self.update_helper_text("passw2", "Password tidak boleh kosong!")
                return
            else:
                self.update_helper_text("passw1", "Password tidak boleh kosong!")
                self.update_helper_text("passw2", "Password tidak boleh kosong!")
                return

        if password != confirm_password:
            self.update_helper_text("passw2", "Password tidak cocok!")
            return
        
        if len(password) < 8:
            self.update_helper_text("passw1", "Password harus minimal 8 karakter!")
            self.update_helper_text("passw2", "Password harus minimal 8 karakter!")
            return

        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM user_data WHERE username = ?", (username,))
        if cursor.fetchone():
            self.update_helper_text("user", "Username sudah digunakan. Pilih username lain!")
            conn.close()
            return

        conn.close()

        app = App.get_running_app()
        app.nama_lengkap = nama_lengkap
        app.username = username
        app.password = password
        app.change_screen("signup3", "fade")
    
    def reset_fields(self):
        self.ids.namalengkap.text = ""
        self.ids.user.text = "" 
        self.ids.passw1.text = ""
        self.ids.passw2.text = ""
        self.ids.error_label.text = ""
    pass

class Signup3Screen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_button = None
        
    def select_button(self, button):
        if self.selected_button and self.selected_button != button:
            self.reset_button_style(self.selected_button)
            
        self.selected_button = button
        
        button_text = button.children[0]
        self.selected_program = button_text.text
        self.ids.error_label.text = ""
        
        button.line_color = (1, 1, 1, 1)
        button_text.text_color = (1, 1, 1, 1)
        button.md_bg_color = (0.988, 0.671, 0.196, 1)
    
    def reset_button_style(self, button):
        button_text = button.children[0]
        button.md_bg_color = (0.125, 0.227, 0.290, 1)
        button_text.text_color = (1, 1, 1, 1)
        button.line_color = (1, 1, 1, 1)
    
    def next_screen(self):
        if not hasattr(self, 'selected_program') or not self.selected_program:
            self.ids.error_label.text = "Harap pilih program terlebih dahulu!"
        else:
            app = App.get_running_app()
            app.selected_program = self.selected_program
            app.change_screen("signup4", "fade")
    
    def reset_fields(self):
        if self.selected_button:
            self.reset_button_style(self.selected_button)
        self.selected_button = None
        self.selected_program = None
        self.ids.error_label.text = ""
    pass

class Signup4Screen(MDScreen):
    def on_pre_enter(self):
        self.ids.tanggal_lahir.error = False
    
    def update_helper_text(self, text_field_id, new_text):
        text_field = self.ids[text_field_id]
        text_field.error = True
        text_field.error_color = "FF0000FF"
        self.ids.error_label.text = new_text
        
    def clear_error(self):
        self.ids.error_label.text = ""
    
    def validate4(self):
        jenis_kelamin = self.ids.jkelamin.text
        tanggal_lahir = self.ids.tanggal_lahir.text
        tinggi_badan = self.ids.tb.text
        berat_badan = self.ids.bb.text

        if not jenis_kelamin or jenis_kelamin not in ["L", "P"]:
            self.update_helper_text("jkelamin", "Jenis kelamin L/P ?")
            return
        
        if not tanggal_lahir:
            self.update_helper_text("tanggal_lahir", "Tanggal lahir tidak boleh kosong!")
            return
        
        if not tinggi_badan or not tinggi_badan.isdigit():
            self.update_helper_text("tb", "Isikan tinggi badan dengan benar!")
            return
        
        if not berat_badan or not berat_badan.isdigit():
            self.update_helper_text("bb", "Isikan berat badan dengan benar!")
            return
        
        else:
            try:
                datetime.strptime(tanggal_lahir, "%d/%m/%Y")
            except ValueError:
                self.update_helper_text("tanggal_lahir", "Format tanggal lahir salah!")
                return
            
        if jenis_kelamin and tanggal_lahir and tinggi_badan.isdigit() and berat_badan.isdigit():
            app = App.get_running_app()
            usia = hitung_usia(tanggal_lahir)
            app.jenis_kelamin = jenis_kelamin
            app.tanggal_lahir = tanggal_lahir
            app.usia = usia
            app.tinggi_badan = int(tinggi_badan)
            app.berat_badan = int(berat_badan)
            app.change_screen("signup5", "fade")
    
    def reset_fields(self):
        self.ids.jkelamin.text = ""
        self.ids.tanggal_lahir.text = ""
        self.ids.tb.text = ""
        self.ids.bb.text = ""
        self.ids.jkelamin.error = False
        self.ids.tanggal_lahir.error = False
        self.ids.tb.error = False
        self.ids.bb.error = False
        self.ids.error_label.text = ""
    pass

class Signup5Screen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_button = None
        
    def select_button(self, button):
        if self.selected_button and self.selected_button != button:
            self.reset_button_style(self.selected_button)
            
        self.selected_button = button
        
        button_text = button.children[0]
        self.selected_activity = button_text.text
        self.ids.error_label.text = ""
        
        button.line_color = (1, 1, 1, 1)
        button_text.text_color = (1, 1, 1, 1)
        button.md_bg_color = (0.988, 0.671, 0.196, 1)
    
    def reset_button_style(self, button):
        button_text = button.children[0]
        button.md_bg_color = (0.125, 0.227, 0.290, 1)
        button_text.text_color = (1, 1, 1, 1)
        button.line_color = (1, 1, 1, 1)
    
    def next_screen(self):
        if not hasattr(self, 'selected_activity') or not self.selected_activity:
            self.ids.error_label.text = "Harap pilih terlebih dahulu!"
        else:
            app = App.get_running_app()
            app.selected_activity = self.selected_activity
            app.signup_user()
            app.change_screen("signup6", "fade")
    
    def reset_fields(self):
        if self.selected_button:
            self.reset_button_style(self.selected_button)
        self.selected_button = None
        self.selected_activity = None
        self.ids.error_label.text = ""
    pass

class Signup6Screen(MDScreen):
    pass

class LoginScreen(MDScreen):
    def show_password(self):
        password_field = self.ids.passw
        password_label = self.ids.password_label
        
        if password_field.password:
            password_field.password = False
            password_label.text = "Hide password"
        else:
            password_field.password = True
            password_label.text = "Show password"
     
    def chart(self):
        app = App.get_running_app()
        week_data = get_week_data()
        app.week_data = week_data
                
        weight_path = create_weekly_chart(week_data, "berat_badan")
        height_path = create_weekly_chart(week_data, "tinggi_badan")
        kalori_path = create_weekly_chart(week_data, "kalori")
                
        recap_screen = app.root.get_screen("recap")
        recap_screen.weight_path = weight_path
        recap_screen.height_path = height_path
        recap_screen.kalori_path = kalori_path
    
    def validate_login(self):
        username = self.ids.user.text
        password = self.ids.passw.text
        self.ids.error_label.text = ""

        if not username:
            self.ids.user.error = True
        if not password:
            self.ids.passw.error = True
        elif username and password:
            app = App.get_running_app()
            user = get_user(username, password)
            if user:
                columns = ["id", "nama_lengkap", "username", "password","tanggal_lahir",
                           "program", "jenis_kelamin", "usia", "tinggi_badan", "berat_badan",
                           "level_aktivitas", "bmi_value", "bmr_value", "target_calories", 
                           "daily_calories", "daily_data"]
                user_data_dict = dict(zip(columns, user))
                
                app.user_data = user_data_dict
                print(f"Sedang login: {user}")
                
                Clock.schedule_once(lambda dt: self.chart(), 2)
                
                app.change_screen("main", "fade")
            else:
                self.ids.error_label.text = "Username atau password salah"
        
    def clear_error(self):
        self.ids.error_label.text = ""
        
    def reset_fields(self):
        self.ids.user.text = ""
        self.ids.passw.text = ""
        self.ids.error_label.text = ""
    pass

class MainScreen(MDScreen):
    jk_icon = StringProperty("gender-male")
    gbr_source = StringProperty("")
    progress_value = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update_date_time, 1)
        self.update_quote()
        Clock.schedule_interval(self.update_quote, 180)
        
    def on_pre_enter(self, *args):
        super().on_enter(*args)
        app = App.get_running_app()
        Clock.schedule_once(app.update_progress_bar, 1)
        Clock.schedule_interval(app.update_daily_calories, 1)
        Clock.schedule_interval(self.update_data, 1)
        
        user_data = app.user_data

        if user_data:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM user_data WHERE id = ?", (user_data["id"],))
            db_data = cursor.fetchone()
            conn.close()
            
            if db_data:
                jenis_kelamin = db_data[6]
                self.gbr_source = app.resource_path("assets/cwo.png") if jenis_kelamin == "L" else app.resource_path("assets/cwe.png")
        
    def on_leave(self, *args):
        super().on_leave(*args)
        app = App.get_running_app()
        Clock.unschedule(app.update_daily_calories)
        Clock.unschedule(self.update_data)
    
    def update_quote(self, *args):
        random_quote = random.choice(quotes)
        self.ids.quotes.text = f'"{random_quote}"'

    def update_date_time(self, dt):
        now = datetime.now()
        days = now.strftime("%A")
        month = now.strftime("%B")
        hari = hari_ind.get(days, days)
        bulan = bulan_ind.get(month, month)
        tanggal = now.strftime(f"%d {bulan} %Y")
        jam = now.strftime("%H:%M:%S")
        self.ids.tanggal.text = f"{hari}, {tanggal}"
        self.ids.jam.text = jam
    
    def update_data(self, dt):
        app = App.get_running_app()
        user_data = app.user_data

        if user_data:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_data WHERE id = ?", (user_data["id"],))
            db_data = cursor.fetchone()
            conn.close()
            
            if db_data:
                nama_lengkap = db_data[1]
                jenis_kelamin = db_data[6]
                jk = "Laki-laki" if jenis_kelamin == "L" else "Perempuan"
                self.jk_icon = "gender-male" if jenis_kelamin == "L" else "gender-female"
                usia = db_data[7]
                tinggi_badan = db_data[8]
                berat_badan = db_data[9]
                level_aktivitas = db_data[10]
                target_calories = db_data[13]
                daily_calories = db_data[14]
                
                if level_aktivitas == "Jarang Sekali":
                    self.ids.ket.text = "Anda lebih banyak menghabiskan waktu dalam posisi diam atau hampir tidak melakukan aktivitas fisik."
                elif level_aktivitas == "Sedikit Aktif":
                    self.ids.ket.text = "Anda sesekali bergerak dengan beberapa aktivitas ringan yang tidak terlalu intens."
                elif level_aktivitas == "Aktif":
                    self.ids.ket.text = "Anda melakukan aktivitas fisik secara teratur, seperti berolahraga atau aktivitas fisik lainnya."
                elif level_aktivitas == "Sangat Aktif":
                    self.ids.ket.text = "Anda memiliki rutinitas fisik yang intens, seperti berolahraga berat, latihan keras, dan lainnya."   
                
                self.ids.jk.text = jk
                self.ids.daily_calories.text = f"{daily_calories:.2f} kkal"
                self.ids.target_calories.text = f"{target_calories:.2f} kkal"
                self.ids.tb.text = f"{tinggi_badan} cm"
                self.ids.bb.text = f"{berat_badan} kg"
                self.ids.level.text = f"'{level_aktivitas}'"
                self.ids.usia.text = f"{usia} thn"
                
                waktu_sapaan = get_greeting()
                self.ids.user.text = f"{waktu_sapaan}, {nama_lengkap}!"
                
                if waktu_sapaan == "Selamat Ulang Tahun":
                    self.ids.sapa.text = "Ditunggu traktirannya:>"
                elif waktu_sapaan == "Selamat Pagi":
                    self.ids.sapa.text = "Jangan lupa sarapan ya!"
                elif waktu_sapaan == "Selamat Siang":
                    self.ids.sapa.text = "Sudah siang nih, jangan lupa makan!"
                elif waktu_sapaan == "Selamat Sore":
                    self.ids.sapa.text = "Tetap semangat beraktivitas!"
                elif waktu_sapaan == "Selamat Malam":
                    self.ids.sapa.text = "Jangan begadang loh yaa!"
    pass

class BMIScreen(MDScreen):
    level_icon = StringProperty("emoticon-outline")
    
    def on_pre_enter(self):
        Clock.schedule_interval(self.update_data, 1)
        
    def on_leave(self):
        Clock.unschedule(self.update_data)
    
    def update_data(self, dt):
        app = App.get_running_app()
        user_data = app.user_data

        if user_data:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_data WHERE id = ?", (user_data["id"],))
            db_data = cursor.fetchone()
            
            if db_data: 
                program = db_data[5]
                usia = db_data[7]
                tinggi_badan = db_data[8]
                berat_badan = db_data[9]
                bmi_value = db_data[11]
                
                self.ids.tb.text = f"{tinggi_badan} cm"
                self.ids.bb.text = f"{berat_badan} kg"
                self.ids.usia.text = f"{usia} thn"
                self.ids.program.text = program
                
                self.ids.bmi.text = str(bmi_value)
                
                if bmi_value < 18.5:
                    self.ids.saran.text = "Cobalah untuk mengonsumsi lebih banyak makanan bergizi dan tinggi kalori. Naikkan berat badanmu dengan menjalankan program 'PENINGKATAN BERAT BADAN'"
                    self.ids.level.text = "Underweight (Kekurangan Berat Badan)"
                    self.level_icon = "emoticon-sad-outline"
                elif 18.5 <= bmi_value < 25:
                    self.ids.saran.text = "Pertahankan kesehatan dan proporsi tubuhmu dengan pola hidup sehat yang teratur. Jalankan program 'PERTAHANKAN BERAT BADAN' agar tubuhmu tetap ideal."
                    self.ids.level.text = "Normalweight (Berat Badan Ideal)"
                    self.level_icon = "emoticon-outline"
                elif 25 <= bmi_value < 30:
                    self.ids.saran.text = "Kurangi konsumsi kalori dan tingkatkan aktivitas fisik secara teratur. Jalankan program 'PENURUNAN BERAT BADAN' untuk mencapai tubuh ideal."
                    self.ids.level.text = "Overweight (Kelebihan Berat Badan)"
                    self.level_icon = "emoticon-neutral-outline"
                else:
                    self.ids.saran.text = "Obesitas. Fokuslah pada perubahan gaya hidup dengan pola makan sehat dan olahraga teratur, serta lakukan pemeriksaan kesehatan jika diperlukan. Jalankan program 'PENURUNAN BERAT BADAN'"
                    self.ids.level.text = "Obese (Obesitas)"
                    self.level_icon = "emoticon-cry-outline"
                    
            conn.close()
    pass

class BMRScreen(MDScreen):
    jk_icon = StringProperty("gender-male")
    
    def on_pre_enter(self):
        Clock.schedule_interval(self.update_data, 1)
        
    def on_leave(self):
        Clock.unschedule(self.update_data)
    
    def update_data(self, dt):
        app = App.get_running_app()
        user_data = app.user_data

        if user_data:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM user_data WHERE id = ?", (user_data["id"],))
            db_data = cursor.fetchone()

            if db_data:
                usia = db_data[7]
                tinggi_badan = db_data[8]
                berat_badan = db_data[9]
                level_aktivitas = db_data[10]
                program = db_data[5]
                
                jenis_kelamin = db_data[6]
                jk = "Laki-laki" if jenis_kelamin == "L" else "Perempuan"
                self.jk_icon = "gender-male" if jenis_kelamin == "L" else "gender-female"
                self.ids.jk.text = jk
                
                self.ids.aktivitas.text = f"'{level_aktivitas}'"
                
                bmr_value = db_data[12]
                target_calories = db_data[13]
                
                self.ids.bmr.text = f"{bmr_value:.2f} kkal"
                self.ids.calories.text = f"{target_calories:.2f} kkal"
                self.ids.program.text = f"'{program}'"
                self.ids.tb.text = f"{tinggi_badan} cm"
                self.ids.bb.text = f"{berat_badan} kg"
                self.ids.usia.text = f"{usia} thn"
    pass

class ProgramScreen(MDScreen):
    current_program = StringProperty("Pertahankan Berat Badan")
    
    def on_pre_enter(self):
        Clock.schedule_interval(self.update_data, 1)
        
    def on_leave(self):
        Clock.unschedule(self.update_data)
        
    def change_program(self, program):
        app = App.get_running_app()
        user_data = app.user_data
        
        if user_data:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()

            user_data["program"]= program
            
            cursor.execute("UPDATE user_data SET program = ? WHERE id = ?", (program, user_data["id"]))
            conn.commit()
            
            conn.close()
            
    def show_popup(self, program):
        dialog = MDDialog(
            MDDialogIcon(
                icon="information-outline",
                theme_font_size="Custom",
                font_size="35sp",
            ),
            MDDialogHeadlineText(
                text="Konfirmasi Perubahan Program?",
                theme_font_name="Custom",
                font_name= "Poppins-Bold",
            ),
            MDDialogSupportingText(
                text="Program Anda akan diubah menjadi: \n"
                f"'{program.upper()}'",
                theme_font_name="Custom",
                font_name= "Poppins-Medium",
                theme_font_size="Custom",
                font_size="16sp",
            ),
            
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Cancel", theme_font_name="Custom", font_name="Poppins-Regular"),
                    style="text",
                    on_release= lambda x: self.close_dialog(dialog),
                ),
                MDButton(
                    MDButtonText(text="Confirm", theme_font_name="Custom", font_name="Poppins-Regular",),
                    style="text",
                    on_release=lambda x: self.confirm_change(program, dialog),
                ),
                spacing="8dp",
            ),
        )
        dialog.open()
    
    def show_info(self):
        dialog = MDDialog(
            MDDialogIcon(
                icon="check-circle-outline",
                theme_font_size="Custom",
                font_size="35sp",
            ),
            MDDialogHeadlineText(
                text="Perubahan Berhasil Disimpan",
                theme_font_name="Custom",
                font_name="Poppins-Bold",
            ),
            MDDialogSupportingText(
                text="Tekan 'Selesai' untuk melanjutkan.",
                theme_font_name="Custom",
                font_name="Poppins-Medium",
                theme_font_size="Custom",
                font_size="16sp",
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Selesai", theme_font_name="Custom", font_name="Poppins-Regular"),
                    style="text",
                    on_release=lambda x: self.close_dialog(dialog),
                ),
                spacing="8dp",
            ),
        )
        dialog.open()

    def confirm_change(self, program, dialog):
        self.change_program(program)
        self.close_dialog(dialog)
        self.show_info()

    def close_dialog(self, dialog):
        dialog.dismiss()
        
    def update_data(self, dt):
        app = App.get_running_app()
        user_data = app.user_data
        
        if user_data:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM user_data WHERE id = ?", (user_data["id"],))
            db_data = cursor.fetchone()

            if db_data:
                program = db_data[5]
                
                self.ids.program.text = f"'{program}'"
                
                if program == "Peningkatan Berat Badan":
                    self.current_program = "Peningkatan Berat Badan"
                    self.ids.mainprogram.text = "Untuk menambah berat badan, tubuh perlu berada dalam surplus kalori, yaitu asupan kalori yang lebih banyak daripada yang dibakar tubuh. Oleh karena itu, program ini akan MENAMBAHKAN 700 KKAL pada total kebutuhan kalori harian berdasarkan perhitungan BMR."
                    self.ids.program1.text = "- Penurunan Berat Badan -"
                    self.ids.exprogram1.text = "Untuk menurunkan berat badan, tubuh perlu berada dalam defisit kalori, yaitu asupan kalori yang lebih sedikit daripada yang dibakar oleh tubuh. Oleh karena itu, program ini akan MENGURANGI 500 KKAL dari total kebutuhan kalori harian berdasarkan perhitungan BMR."
                    self.ids.program2.text = "- Pertahankan Berat Badan -"
                    self.ids.exprogram2.text = "Dalam program ini, kebutuhan asupan kalori harian Anda akan SAMA dengan BMR. Untuk memastikan bahwa tubuh Anda tidak mendapat asupan kalori yang berlebih atau kurang dari batas normalnya sesuai dengan perhitungan BMR."
                    
                elif program == "Pertahankan Berat Badan":
                    self.current_program = "Pertahankan Berat Badan"
                    self.ids.mainprogram.text = "Dalam program ini, kebutuhan asupan kalori harian Anda akan SAMA dengan BMR. Untuk memastikan bahwa tubuh Anda tidak mendapat asupan kalori yang berlebih atau kurang dari batas normalnya sesuai dengan perhitungan BMR."
                    self.ids.program1.text = "- Penurunan Berat Badan -"
                    self.ids.exprogram1.text = "Untuk menurunkan berat badan, tubuh perlu berada dalam defisit kalori, yaitu asupan kalori yang lebih sedikit daripada yang dibakar oleh tubuh. Oleh karena itu, program ini akan MENGURANGI 500 KKAL dari total kebutuhan kalori harian berdasarkan perhitungan BMR."
                    self.ids.program2.text = "- Peningkatan Berat Badan -"
                    self.ids.exprogram2.text = "Untuk menambah berat badan, tubuh perlu berada dalam surplus kalori, yaitu asupan kalori yang lebih banyak daripada yang dibakar tubuh. Oleh karena itu, program ini akan MENAMBAHKAN 700 KKAL pada total kebutuhan kalori harian berdasarkan perhitungan BMR."
                    
                elif program == "Penurunan Berat Badan":
                    self.current_program = "Penurunan Berat Badan"
                    self.ids.mainprogram.text = "Untuk menurunkan berat badan, tubuh perlu berada dalam defisit kalori, yaitu asupan kalori yang lebih sedikit daripada yang dibakar oleh tubuh. Oleh karena itu, program ini akan MENGURANGI 500 KKAL dari total kebutuhan kalori harian berdasarkan perhitungan BMR."
                    self.ids.program1.text = "- Pertahankan Berat Badan -"
                    self.ids.exprogram1.text = "Dalam program ini, kebutuhan asupan kalori harian Anda akan SAMA dengan BMR. Untuk memastikan bahwa tubuh Anda tidak mendapat asupan kalori yang berlebih atau kurang dari batas normalnya sesuai dengan perhitungan BMR."
                    self.ids.program2.text = "- Peningkatan Berat Badan -"
                    self.ids.exprogram2.text = "Untuk menambah berat badan, tubuh perlu berada dalam surplus kalori, yaitu asupan kalori yang lebih banyak daripada yang dibakar tubuh. Oleh karena itu, program ini akan MENAMBAHKAN 700 KKAL pada total kebutuhan kalori harian berdasarkan perhitungan BMR."
    pass

class DailyScreen(MDScreen):
    image_files = []
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_quote()
        Clock.schedule_interval(self.update_quote, 180)
        
        app = App.get_running_app()
        self.image_folder = app.resource_path("assets/food/")
        self.image_files = self.get_image(self.image_folder)
        
        self.set_image()
        Clock.schedule_interval(self.set_image, 180)
    
    def on_pre_enter(self, *args):
        super().on_enter(*args)
        app = App.get_running_app()
        Clock.schedule_interval(app.update_daily_calories, 1)
        self.update_calories("breakfast")
        self.update_calories("lunch")
        self.update_calories("dinner")
        self.update_calories("snack")
        Clock.schedule_once(app.update_progress_bar, 1)
        Clock.schedule_interval(self.update_data, 1)
    
    def on_leave(self, *args):
        super().on_leave(*args)
        app = App.get_running_app()
        Clock.unschedule(app.update_daily_calories)
        Clock.unschedule(self.update_data)
        Clock.unschedule(self.set_image)
    
    def get_image(self, folder_path):
        if not os.path.exists(folder_path):
            print(f"Folder not found: {folder_path}")
            return []
        
        supported_extensions = ['jpg', 'jpeg', 'png']
        return [
            os.path.join(folder_path, file)
            for file in os.listdir(folder_path)
            if file.split('.')[-1].lower() in supported_extensions
        ]
    
    def set_image(self, *args):
        if self.image_files:
            random_image = random.choice(self.image_files)
            self.ids.image_widget.source = random_image
            self.ids.image_widget.reload()
    
    def update_quote(self, *args):
        random_quote2 = random.choice(quotes2)
        self.ids.quotes2.text = f'"{random_quote2}"'
        
    def update_data(self, dt):
        app = App.get_running_app()
        user_data = app.user_data

        if user_data:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM user_data WHERE id = ?", (user_data["id"],))
            db_data = cursor.fetchone()
            conn.close()
            
            if db_data:
                target_calories = db_data[13]
                daily_calories = db_data[14]
                bmi_value = db_data[11]
                bmr_value = db_data[12]
                
                self.ids.total.text = f"{daily_calories:.2f} kkal"
                self.ids.daily_calories.text = f"{daily_calories:.2f} kkal"
                self.ids.target.text = f"{target_calories:.2f} kkal"
                self.ids.target_calories.text = f"{target_calories:.2f} kkal"
                self.ids.bmi.text = str(bmi_value)
                self.ids.bmr.text = f"{bmr_value:.2f} kkal"
    
    def update_calories(self, kategori):
        app = App.get_running_app()
        username = app.user_data["username"]
        
        tanggal = datetime.today().strftime('%Y-%m-%d')

        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT nama_makanan, jumlah, satuan, kalori 
            FROM calories_data
            WHERE username = ? AND kategori = ? AND tanggal = ?
        """, (username, kategori, tanggal))

        category_data = cursor.fetchall()
        conn.close()

        label_id = kategori
        
        if category_data:
            total_kalori = sum(row[3] for row in category_data)
            self.ids[label_id].text = f"{total_kalori}"
        else:
            self.ids[label_id].text = "0"
    
    def get_food(self, category):
        app = App.get_running_app()
        user_data = app.user_data
        username = user_data["username"]
        
        today_date = datetime.now().strftime('%Y-%m-%d')
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT nama_makanan, jumlah, satuan, kalori 
            FROM calories_data
            WHERE username = ? AND category = ? AND tanggal = ?
        """, (username, category, today_date))
        
        foods = [f"{row[0]} - {int(row[1])} {row[2]} - {int(row[3])} kkal" for row in cursor.fetchall()]
        
        conn.close()
        return foods
    
    def show_food(self, category):
        foods = self.get_food(category)
        if not foods:
            foods = ["Tidak ada makanan ditambahkan."]

        menu_items = []
        for food in foods:
            menu_items.append(
                {
                    "viewclass": "MDLabel",
                    "text": food,
                    "theme_text_color": "Custom",
                    "text_color": (0.125, 0.227, 0.290, 1),
                    "font_name": "Poppins-SemiBold",
                    "halign": "left",
                    "padding": "16.5dp",
                    "size_hint_y": None,
                    "height": dp(52),
                }
            )
            menu_items.append(
                {
                    "viewclass": "MDDivider",
                    "height": dp(1),
                }
            )

        menu = MDDropdownMenu(
            items=menu_items,
            caller=self.ids.get(f"{category}_button"),
            theme_width="Custom",
            width=dp(350),
            max_height=dp(200),
        )
        menu.open()
    
    pass

class FoodScreen(MDScreen):
    all_data = []
    checked_items = {}
    filtered_data = []

    def on_pre_enter(self, *args):
        if not self.all_data:
            self.load_all_data()
        self.load_food_list()

    def load_all_data(self):
        app = App.get_running_app()
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT nama, jumlah, satuan, kalori FROM makanan")
        self.all_data = cursor.fetchall()
        conn.close()

    def load_food_list(self):
        self.ids.food_list.clear_widgets()
        
        checked_items = [row for row in self.filtered_data if self.checked_items.get(row[0], False)]
        unchecked_items = [row for row in self.filtered_data if not self.checked_items.get(row[0], False)]
        
        sorted_data = checked_items + unchecked_items
        displayed_data = sorted_data[:20]

        for row in displayed_data:
            item = MDListItem(
                MDListItemHeadlineText(
                    text=f"{row[0]}",
                    theme_text_color="Custom",
                    text_color=(0.125, 0.227, 0.290, 1),
                    theme_font_name = "Custom",
                    theme_font_size = "Custom",
                    font_name="Poppins-SemiBold",
                    font_size="15sp",
                ),
                MDListItemHeadlineText(
                    text=f"{int(row[1])} {row[2]} / {int(row[3])} kkal",
                    theme_text_color="Custom",
                    text_color=(0.125, 0.227, 0.290, 0.7),
                    theme_font_name = "Custom",
                    theme_font_size = "Custom",
                    font_name="Poppins-Medium",
                    font_size="13sp",
                ),
                MDListItemTrailingCheckbox(
                    active=self.checked_items.get(row[0], False),
                    on_release=lambda checkbox, name=row[0]: self.toggle_item(checkbox, name)
                ),
            )
            self.ids.food_list.add_widget(item)
            
        self.update_food_selected()

    def on_search_text(self, filter_text):
        if filter_text:
            self.filtered_data = [
                row for row in self.all_data
                if filter_text.lower() in row[0].lower()
            ][:20]
        else:
            self.filtered_data = self.all_data[:]

        self.load_food_list()
    
    def toggle_item(self, checkbox, name):
        self.checked_items[name] = checkbox.active
        self.update_food_selected()
    
    def update_food_selected(self):
        selected_count = sum(1 for checked in self.checked_items.values() if checked)
        self.ids.food_selected.text = f"Makanan dipilih: {selected_count}"
    
    def save_checked_food(self):
        app = App.get_running_app()
        username = app.user_data["username"]

        if not any(self.checked_items.values()):
            self.show_noitems()
            return
            
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        kategori = app.food_category
        tanggal = datetime.now().strftime('%Y-%m-%d')

        for food_name, is_checked in self.checked_items.items():
            if is_checked:
                food = next((row for row in self.all_data if row[0] == food_name), None)
                if food:
                    nama_makanan = food[0]
                    jumlah = food[1]
                    satuan = food[2]
                    kalori = food[3]

                    cursor.execute("""
                        INSERT INTO calories_data (username, nama_makanan, jumlah, satuan, kalori, kategori, tanggal)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (username, nama_makanan, jumlah, satuan, kalori, kategori, tanggal))
                    conn.commit()

        conn.close()
        self.show_success()

    def show_success(self):
        dialog = MDDialog(
            MDDialogIcon(
                icon="check-circle-outline",
                theme_font_size="Custom",
                font_size="35sp",
            ),
            MDDialogHeadlineText(
                text="Berhasil!",
                theme_font_name="Custom",
                font_name="Poppins-Bold",
            ),
            MDDialogSupportingText(
                text="Makanan yang Anda pilih telah berhasil ditambahkan.",
                theme_font_name="Custom",
                font_name="Poppins-Medium",
                theme_font_size="Custom",
                font_size="16sp",
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Oke", theme_font_name="Custom", font_name="Poppins-Regular"),
                    style="text",
                    on_release=lambda x: (self.close_dialog(dialog), self.reset_checkboxes()),
                ),
                spacing="8dp",
            ),
        )
        dialog.open()
    
    def show_noitems(self):
        dialog = MDDialog(
            MDDialogIcon(
                icon="alert-outline",
                theme_font_size="Custom",
                font_size="35sp",
            ),
            MDDialogHeadlineText(
                text="Perhatian!",
                theme_font_name="Custom",
                font_name="Poppins-Bold",
            ),
            MDDialogSupportingText(
                text="Anda masih belum memilih makanan apapun!",
                theme_font_name="Custom",
                font_name="Poppins-Medium",
                theme_font_size="Custom",
                font_size="16sp",
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Oke", theme_font_name="Custom", font_name="Poppins-Regular"),
                    style="text",
                    on_release=lambda x: self.close_dialog(dialog),
                ),
                spacing="8dp",
            ),
        )
        dialog.open()
    
    def close_dialog(self, dialog):
        dialog.dismiss()
    
    def reset_checkboxes(self):
        app = App.get_running_app()
        app.change_screen("daily", "fade")
        self.checked_items.clear()
        self.load_food_list()
        self.ids.food_selected.text = "Makanan dipilih: 0"
        
    pass

class RecapScreen(MDScreen):
    weight_path = StringProperty()
    height_path = StringProperty()
    kalori_path = StringProperty()
     
    def on_pre_enter(self):
        app = App.get_running_app()
        current_data = get_week_data()
        
        if current_data != app.week_data:
            weight_path = create_weekly_chart(current_data, "berat_badan")
            height_path = create_weekly_chart(current_data, "tinggi_badan")
            kalori_path = create_weekly_chart(current_data, "kalori")
                
            self.weight_path = weight_path
            self.height_path = height_path
            self.kalori_path = kalori_path 
            
        Clock.schedule_once(self.update_data, 0.5)
    
    def update_data(self, dt):
        app = App.get_running_app()
        user_data = app.user_data

        if user_data:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM user_data WHERE id = ?", (user_data["id"],))
            db_data = cursor.fetchone()
            
            if db_data:
                locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')
                today_day = datetime.now().strftime('%A')
                
                tinggi_badan = db_data[8]
                berat_badan = db_data[9]
                
                self.ids.tb.text = f"{tinggi_badan} cm"
                self.ids.bb.text = f"{berat_badan} kg"
                self.ids.day.text = str(today_day)
                
                self.ids.weight_chart.source = self.weight_path
                self.ids.height_chart.source = self.height_path
                self.ids.kalori_chart.source = self.kalori_path
                
                self.ids.weight_chart.reload()
                self.ids.height_chart.reload()
                self.ids.kalori_chart.reload()
    
    def generate_pdf(self):
        app = App.get_running_app()
        pdf_path = app.resource_path("assets/weekly_recap.pdf")

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        for path in [self.weight_path, self.height_path, self.kalori_path]:
            pdf.add_page()
            pdf.image(path, x=10, y=10, w=190)

        pdf.output(pdf_path)
        return pdf_path

    def download_pdf(self):
        pdf_path = self.generate_pdf()
        
        if platform == 'win' or platform == 'linux' or platform == 'macosx':
            user_home = os.path.expanduser("~")
            download_folder = os.path.join(user_home, "Downloads") 
            
            if not os.path.exists(download_folder):
                os.makedirs(download_folder)
            
            final_path = os.path.join(download_folder, "weekly_recap.pdf")
            shutil.copy(pdf_path, final_path)
            
            print(f"PDF berhasil disimpan di: {final_path}")
            self.show_info(final_path)
        else:
            print(f"Platform {platform} tidak dikenali untuk pengunduhan PDF.")
        
    def show_info(self, pdf_path):
        app = App.get_running_app()
        dialog = MDDialog(
            MDDialogIcon(
                icon="check-circle-outline",
                theme_font_size="Custom",
                font_size="35sp",
            ),
            MDDialogHeadlineText(
                text="PDF Berhasil Disimpan!",
                theme_font_name="Custom",
                font_name="Poppins-Bold",
            ),
            MDDialogSupportingText(
                text=f"Cek lokasi file di {pdf_path} pada device Anda.",
                theme_font_name="Custom",
                font_name="Poppins-Medium",
                theme_font_size="Custom",
                font_size="16sp",
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Selesai", theme_font_name="Custom", font_name="Poppins-Regular"),
                    style="text",
                    on_release=lambda x: self.close_dialog(dialog),
                ),
                spacing="8dp",
            ),
        )
        dialog.open()
    
    def close_dialog(self, dialog):
        dialog.dismiss()
                
    pass

class UpdateScreen(MDScreen):
    selected_activity = StringProperty("")
    current_weight = StringProperty("")
    current_height = StringProperty("")
    manual_selection = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_button = None

    def select_button(self, button, manual=True):
        if self.selected_button and self.selected_button != button:
            self.reset_button_style(self.selected_button)

        self.selected_button = button

        button_text = button.children[0]
        self.selected_activity = button_text.text

        button.line_color = (0.125, 0.227, 0.290, 1)
        button_text.text_color = (1, 1, 1, 1)
        button.md_bg_color = (0.988, 0.671, 0.196, 1)
        
        if manual:
            self.manual_selection = True
            self.change_activity_level(self.selected_activity)

    def reset_button_style(self, button):
        button_text = button.children[0]
        button.md_bg_color = (1, 1, 1, 1)
        button_text.text_color = (0.125, 0.227, 0.290, 1)
        button.line_color = (0.125, 0.227, 0.290, 1)

    def on_pre_enter(self):
        self.manual_selection = False
        Clock.schedule_interval(self.update_data, 1)
    
    def on_leave(self):
        Clock.unschedule(self.update_data)

    def change_data(self, column, value):
        app = App.get_running_app()
        user_data = app.user_data

        if user_data:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            
            user_data[column] = value

            cursor.execute(f"UPDATE user_data SET {column} = ? WHERE id = ?", (value, user_data["id"]))
            conn.commit()

            conn.close()

    def show_popup(self, column, value):
        dialog = MDDialog(
            MDDialogIcon(
                icon="information-outline",
                theme_font_size="Custom",
                font_size="35sp",
            ),
            MDDialogHeadlineText(
                text="Konfirmasi Perubahan?",
                theme_font_name="Custom",
                font_name="Poppins-Bold",
            ),
            MDDialogSupportingText(
                text="Perubahan Anda akan disimpan sebagai data baru dan akan mengubah data lama Anda.",
                theme_font_name="Custom",
                font_name="Poppins-Medium",
                theme_font_size="Custom",
                font_size="16sp",
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Cancel", theme_font_name="Custom", font_name="Poppins-Regular"),
                    style="text",
                    on_release=lambda x: self.close_dialog(dialog),
                ),
                MDButton(
                    MDButtonText(text="Confirm", theme_font_name="Custom", font_name="Poppins-Regular"),
                    style="text",
                    on_release=lambda x: self.confirm_change(column, value, dialog),
                ),
                spacing="8dp",
            ),
        )
        dialog.open()
    
    def show_info(self):
        app = App.get_running_app()
        dialog = MDDialog(
            MDDialogIcon(
                icon="check-circle-outline",
                theme_font_size="Custom",
                font_size="35sp",
            ),
            MDDialogHeadlineText(
                text="Perubahan Berhasil Disimpan",
                theme_font_name="Custom",
                font_name="Poppins-Bold",
            ),
            MDDialogSupportingText(
                text="Tekan 'Selesai' untuk melanjutkan.",
                theme_font_name="Custom",
                font_name="Poppins-Medium",
                theme_font_size="Custom",
                font_size="16sp",
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Selesai", theme_font_name="Custom", font_name="Poppins-Regular"),
                    style="text",
                    on_release=lambda x: self.close_dialog(dialog),
                ),
                spacing="8dp",
            ),
        )
        dialog.open()
    
    def show_error(self):
        app = App.get_running_app()
        dialog = MDDialog(
            MDDialogIcon(
                icon="alert-outline",
                theme_font_size="Custom",
                font_size="35sp",
            ),
            MDDialogHeadlineText(
                text="Tidak Valid!",
                theme_font_name="Custom",
                font_name="Poppins-Bold",
            ),
            MDDialogSupportingText(
                text="Pastikan data yang Anda masukkan tepat!",
                theme_font_name="Custom",
                font_name="Poppins-Medium",
                theme_font_size="Custom",
                font_size="16sp",
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Oke", theme_font_name="Custom", font_name="Poppins-Regular"),
                    style="text",
                    on_release=lambda x: self.close_dialog(dialog),
                ),
                spacing="8dp",
            ),
        )
        dialog.open()
    
    def update_data(self, dt):
        app = App.get_running_app()
        user_data = app.user_data

        if user_data:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM user_data WHERE id = ?", (user_data["id"],))
            db_data = cursor.fetchone()
            conn.close()

            if db_data:
                tinggi_badan = db_data[8]
                berat_badan = db_data[9]
                level_aktivitas = db_data[10]
                
                self.current_height = str(tinggi_badan)
                self.current_weight = str(berat_badan)
                
                for button in self.ids.activity.children:
                    button_text = button.children[0].text
                    if button_text == level_aktivitas:
                        self.select_button(button, manual=False)
                        break

    def confirm_change(self, column, value, dialog):
        self.change_data(column, value)
        self.close_dialog(dialog)
        self.show_info()

    def close_dialog(self, dialog):
        dialog.dismiss()

    def change_height(self, new_height):
        if len(new_height) > 3:
            self.show_error()
        if not new_height:
            self.show_error()
        elif len(new_height) <= 3:
            self.show_popup("tinggi_badan", new_height)
            self.current_height = new_height

    def change_weight(self, new_weight):
        if len(new_weight) > 3:
            self.show_error()
        if not new_weight:
            self.show_error()
        elif len(new_weight) <= 3:
            self.show_popup("berat_badan", new_weight)
            self.current_weight = new_weight

    def change_activity_level(self, activity_level):
        self.show_popup("level_aktivitas", activity_level)
        self.selected_activity = activity_level
    
    pass

class VerifScreen(MDScreen):
    error_count = 0 
    is_locked = False
    
    def on_pre_enter(self):
        self.ids.tanggal_lahir.error = False
    
    def update_helper_text(self, text_field_id, new_text):
        text_field = self.ids[text_field_id]
        text_field.error = True
        text_field.error_color = "FF0000FF"
        self.ids.error_label.text = new_text
    
    def clear_fields(self):
        self.ids.namalengkap.text = ""
        self.ids.tanggal_lahir.text = ""
    
    def clear_error(self):
        self.ids.error_label.text = ""
        
    def lock_user(self):
        self.is_locked = True
        self.ids.error_label.text = "Anda telah gagal sebanyak 3 kali. Tunggu 1 menit..."
        Clock.schedule_once(self.unlock_user, 60)
        
    def unlock_user(self, *args):
        self.is_locked = False
        self.error_count = 0
        self.ids.error_label.text = ""
    
    def validate(self):
        if self.is_locked:
            self.ids.error_label.text = "Anda masih dalam masa tunggu. Silahkan coba lagi nanti!"
            return
        
        app = App.get_running_app()
        user_data = app.user_data

        if user_data:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM user_data WHERE id = ?", (user_data["id"],))
            db_data = cursor.fetchone()
            conn.close()

            if db_data:
                namalengkap = db_data[1]
                tanggal_lahir = db_data[4]
                input_nama = self.ids.namalengkap.text
                input_ttl = self.ids.tanggal_lahir.text

        if not input_nama:
            self.update_helper_text("namalengkap", "Nama lengkap tidak boleh kosong!")
            self.check_error_count()
            return
        
        if input_nama != namalengkap:
            self.error_count += 1
            self.update_helper_text("namalengkap", "Nama lengkap tidak sesuai!")
            self.check_error_count()
            return
        
        if not input_ttl:
            self.update_helper_text("tanggal_lahir", "Isikan tanggal lahir dengan benar!")
            self.check_error_count()
            return
        
        if input_ttl != tanggal_lahir:
            self.error_count += 1
            self.update_helper_text("tanggal_lahir", "Tanggal lahir tidak sesuai!")
            self.check_error_count()
            return
        
        self.error_count = 0
        self.clear_error()
        self.clear_fields()
        app.change_screen("change", "fade")
    
    def check_error_count(self):
        if self.error_count >= 3:
            self.lock_user() 
    pass

class ChangeScreen(MDScreen):
    def on_pre_enter(self):
        self.ids.tanggal_lahir.error = False
    
    def clear_fields(self):
        self.ids.user.text = ""
        self.ids.namalengkap.text = ""
        self.ids.tanggal_lahir.text = ""
        self.ids.passw1.text = ""
        self.ids.passw2.text = ""
    
    def update_helper_text(self, text_field_id, new_text):
        text_field = self.ids[text_field_id]
        text_field.error = True
        text_field.error_color = "FF0000FF"
        self.ids.error_label.text = new_text

    def clear_error(self):
        self.ids.error_label.text = ""

    def show_password(self):
        password_field1 = self.ids.passw1
        password_field2 = self.ids.passw2
        password_label = self.ids.password_label

        if password_field1.password:
            password_field1.password = False
            password_field2.password = False
            password_label.text = "Hide password"
        else:
            password_field1.password = True
            password_field2.password = True
            password_label.text = "Show password"

    def change_data(self, updates):
        app = App.get_running_app()
        user_data = app.user_data

        if user_data:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            
            for column, value in updates.items():
                user_data[column] = value
                cursor.execute(f"UPDATE user_data SET {column} = ? WHERE id = ?", (value, user_data["id"]))

            conn.commit()
            conn.close()

    def validate(self):
        app = App.get_running_app()
        user_data = app.user_data

        if user_data:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM user_data WHERE id = ?", (user_data["id"],))
            db_data = cursor.fetchone()

            if db_data:
                namalengkap = db_data[1]
                username = db_data[2]
                tanggal_lahir = db_data[4]
                password = db_data[3]
                input_username = self.ids.user.text.strip()
                input_nama = self.ids.namalengkap.text.strip()
                input_ttl = self.ids.tanggal_lahir.text.strip()
                input_password = self.ids.passw1.text
                confirm_password = self.ids.passw2.text

        updates = {}

        if input_username:
            if input_username == username:
                self.update_helper_text("user", "Username sama dengan username sebelumnya!")
                return
            if " " in input_username:
                self.update_helper_text("user", "Username tidak boleh mengandung spasi!")
                return
            cursor.execute("SELECT 1 FROM user_data WHERE username = ?", (input_username,))
            if cursor.fetchone():
                self.update_helper_text("user", "Username sudah digunakan. Pilih username lain!")
                conn.close()
                return
            updates["username"] = input_username

        if input_nama:
            if input_nama == namalengkap:
                self.update_helper_text("namalengkap", "Nama lengkap sama dengan nama lengkap sebelumnya!")
                return
            updates["nama_lengkap"] = input_nama

        if input_ttl:
            if input_ttl == tanggal_lahir:
                self.update_helper_text("tanggal_lahir", "Tanggal lahir sama dengan tanggal lahir sebelumnya!")
                return
            else:
                try:
                    datetime.strptime(input_ttl, "%d/%m/%Y")
                except ValueError:
                    self.update_helper_text("tanggal_lahir", "Format tanggal lahir salah!")
                    return
            updates["tanggal_lahir"] = input_ttl

        if input_password:
            if input_password == password:
                self.update_helper_text("passw1", "Password sama dengan password sebelumnya!")
                return
            if input_password != confirm_password:
                self.update_helper_text("passw2", "Password tidak cocok!")
                return
            if len(input_password) < 8:
                self.update_helper_text("passw1", "Password harus minimal 8 karakter!")
                return
            updates["password"] = input_password

        if not updates:
            self.ids.error_label.text = "Tidak ada data yang diubah!"
            conn.close()
            return

        conn.close()

        self.show_popup(updates)

    def show_popup(self, updates):
        dialog = MDDialog(
            MDDialogIcon(
                icon="information-outline",
                theme_font_size="Custom",
                font_size="35sp",
            ),
            MDDialogHeadlineText(
                text="Konfirmasi Perubahan?",
                theme_font_name="Custom",
                font_name="Poppins-Bold",
            ),
            MDDialogSupportingText(
                text="Perubahan Anda akan disimpan sebagai data baru dan akan mengubah data lama Anda.",
                theme_font_name="Custom",
                font_name="Poppins-Medium",
                theme_font_size="Custom",
                font_size="16sp",
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Cancel", theme_font_name="Custom", font_name="Poppins-Regular"),
                    style="text",
                    on_release=lambda x: self.close_dialog(dialog),
                ),
                MDButton(
                    MDButtonText(text="Confirm", theme_font_name="Custom", font_name="Poppins-Regular"),
                    style="text",
                    on_release=lambda x: self.confirm_change(updates, dialog),
                ),
                spacing="8dp",
            ),
        )
        dialog.open()
    
    def show_info(self):
        app = App.get_running_app()
        dialog = MDDialog(
            MDDialogIcon(
                icon="check-circle-outline",
                theme_font_size="Custom",
                font_size="35sp",
            ),
            MDDialogHeadlineText(
                text="Perubahan Berhasil Disimpan",
                theme_font_name="Custom",
                font_name="Poppins-Bold",
            ),
            MDDialogSupportingText(
                text="Tekan 'Selesai' untuk melanjutkan.",
                theme_font_name="Custom",
                font_name="Poppins-Medium",
                theme_font_size="Custom",
                font_size="16sp",
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Selesai", theme_font_name="Custom", font_name="Poppins-Regular"),
                    style="text",
                    on_release=lambda x: (app.go_back(), self.close_dialog(dialog), self.clear_error(), self.clear_fields()),
                ),
                spacing="8dp",
            ),
        )
        dialog.open()

    def confirm_change(self, updates, dialog):
        self.change_data(updates)
        self.close_dialog(dialog)
        self.show_info()

    def close_dialog(self, dialog):
        dialog.dismiss()

class ProfilScreen(MDScreen):
    def on_pre_enter(self, *args):
        super().on_enter(*args)
        Clock.schedule_interval(self.update_data, 1)
    
    def update_data(self, dt):
        app = App.get_running_app()
        user_data = app.user_data

        if user_data:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM user_data WHERE id = ?", (user_data["id"],))
            db_data = cursor.fetchone()
            conn.close()
            
            if db_data:
                nama_lengkap = db_data[1]
                username = db_data[2]
                tanggal_lahir = db_data[4]
                tinggi_badan = db_data[8]
                berat_badan = db_data [9]
                
                self.ids.namalengkap.text = nama_lengkap
                self.ids.user.text = f"username: {username}"
                self.ids.bb.text = f"{berat_badan} kg"
                self.ids.tb.text = f"{tinggi_badan} cm"
                self.ids.lahir.text = str(tanggal_lahir)
                
    pass

class NotifScreen(MDScreen):
    pass

class ReviewScreen(MDScreen):
    review_text = StringProperty("")
    def on_pre_enter(self):
        self.show_weekly_review()

    def show_weekly_review(self):
        app = App.get_running_app()
        user_data = app.user_data
        username = user_data["username"] if user_data else None
        
        if username:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT daily_data FROM user_data WHERE username = ?", (username,))
            result = cursor.fetchone()

            if result and result[0]:
                daily_data = json.loads(result[0])
                week_review = self.generate_weekly_review(daily_data)
                self.review_text = week_review

            conn.close()

    def generate_weekly_review(self, daily_data):
        review_text = ""
        for entry in daily_data:
            review_text += f"Tanggal: {entry['tanggal']}\n"
            review_text += f"Kalori: {entry['kalori']} kkal\n"
            review_text += f"Berat Badan: {entry['berat_badan']} kg\n"
            review_text += f"Tinggi Badan: {entry['tinggi_badan']} cm\n\n"
        
        if not daily_data:
            review_text += "No data available."

        return review_text

    pass

KV_FILES = [
    "pre-splash.kv", "welcome.kv", "about.kv", "info.kv", "signup1.kv",
    "signup2.kv", "signup3.kv", "signup4.kv", "signup5.kv", "signup6.kv",
    "login.kv", "profil.kv", "notif.kv", "main.kv", "bmi.kv",
    "bmr.kv", "program.kv", "daily.kv", "recap.kv", "update.kv", "verif.kv",
    "change.kv", "food.kv", "review.kv"
]

class Calmy(MDApp):
    current_screen = StringProperty()
    screen_stack = []
    excluded_screens = ["pre-splash", "verif", "change", "food", "about", "info"]
    user_data = {}
    week_data = {}
    food_category = None
    
    def build(self):
        Window.maximize()
        Window.set_icon(self.resource_path("assets/jlogo.png"))

        for kv in KV_FILES:
            Builder.load_file(resource_path(kv))
        
        global screen_manager
        screen_manager = ScreenManager(transition=FadeTransition(duration=0.2))
        self.title = "CALMY! - Calories Enemy"
        self.icon = self.resource_path("assets/logoapk.ico")

        screen_manager.add_widget(SplashScreen())
        screen_manager.add_widget(WelcomeScreen())
        screen_manager.add_widget(AboutScreen())
        screen_manager.add_widget(InfoScreen())
        screen_manager.add_widget(Signup1Screen())
        screen_manager.add_widget(Signup2Screen())
        screen_manager.add_widget(Signup3Screen())
        screen_manager.add_widget(Signup4Screen())
        screen_manager.add_widget(Signup5Screen())
        screen_manager.add_widget(Signup6Screen())
        screen_manager.add_widget(LoginScreen())
        screen_manager.add_widget(ProfilScreen())
        screen_manager.add_widget(NotifScreen())
        screen_manager.add_widget(MainScreen())
        screen_manager.add_widget(BMIScreen())
        screen_manager.add_widget(BMRScreen())
        screen_manager.add_widget(ProgramScreen())
        screen_manager.add_widget(DailyScreen())
        screen_manager.add_widget(RecapScreen())
        screen_manager.add_widget(UpdateScreen())
        screen_manager.add_widget(VerifScreen())
        screen_manager.add_widget(ChangeScreen())
        screen_manager.add_widget(FoodScreen())
        screen_manager.add_widget(ReviewScreen())
        
        return screen_manager

    def change_screen(self, screen_name, transition):
        if self.root.current not in self.excluded_screens and self.root.current != screen_name:
            self.screen_stack.append(self.root.current)
        
        if transition == "wipe":
            self.root.transition = WipeTransition(duration=0.2)
        elif transition == "fade":
            self.root.transition = FadeTransition(duration=0.2)
        elif transition == "slider":
            self.root.transition = SlideTransition(direction="right", duration=0.2)
        else:
            self.root.transition = SlideTransition(direction="left", duration=0.2)
    
        self.root.current = screen_name
        self.current_screen = screen_name
    
    def go_back(self):
        if self.screen_stack:
            previous_screen = self.screen_stack.pop()
            self.change_screen(previous_screen, "fade")
    
    def resource_path(self, relative_path, *args):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    
    def menu_open(self):
        welcome_screen = self.root.get_screen("welcome")
        
        menu_items = [
            {"text": "About", "text_color": (0.125, 0.227, 0.290, 1),
             "leading_icon": "comment-question-outline",
             "leading_icon_color":(0.125, 0.227, 0.290, 1),
             "on_release": lambda x="about": self.menu_callback(x)},
            {"text": "Info",
             "text_color": (0.125, 0.227, 0.290, 1),
             "leading_icon": "information-outline",
             "leading_icon_color":(0.125, 0.227, 0.290, 1),
             "on_release": lambda x="info": self.menu_callback(x)}
        ]
        self.dropdown_menu = MDDropdownMenu(
            caller=welcome_screen.ids.menubutton,
            items=menu_items,
            width_mult= 4
        )
        
        self.dropdown_menu.open()
    
    def menu_callback(self, text_item):
        self.change_screen(text_item, "fade")
        if hasattr(self, 'dropdown_menu'):
            self.dropdown_menu.dismiss()
    
    def on_start(self):
        create_data_table()
        Clock.schedule_once(self.welcome, 20)
        Clock.schedule_interval(self.update_user_age, 1)
        Clock.schedule_interval(self.calculate_bmi, 1)
        Clock.schedule_interval(self.calculate_bmr, 1)
        Clock.schedule_interval(self.save_daily_data, 1)
        
    def welcome(self, *args):
        self.change_screen("welcome", "fade")
        
    def calculate_bmi(self, dt):
        if self.user_data:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM user_data WHERE id = ?", (self.user_data["id"],))
            db_data = cursor.fetchone()
            
            if db_data:
                tinggi_badan = db_data[8]
                berat_badan = db_data[9]
                if tinggi_badan and berat_badan:
                    tb_bmi = (int(tinggi_badan) / 100) ** 2
                    bmi = int(berat_badan) / tb_bmi
                    bmi_value = f"{bmi:.2f}"
                    
                    self.user_data["bmi_value"] = bmi_value
                    
                    cursor.execute("UPDATE user_data SET bmi_value = ? WHERE id = ?", (bmi_value, self.user_data["id"]))
                    conn.commit()
            conn.close()
    
    def calculate_bmr(self, dt):
        if self.user_data:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM user_data WHERE id = ?", (self.user_data["id"],))
            db_data = cursor.fetchone()

            if db_data:
                usia = db_data[7]
                tinggi_badan = db_data[8]
                berat_badan = db_data[9]
                level_aktivitas = db_data[10]
                program = db_data[5]
                jenis_kelamin = db_data[6]

                if tinggi_badan and berat_badan and usia and level_aktivitas and jenis_kelamin:
                    aktivitas_faktor = {
                        'Jarang Sekali': {'L': 1.4, 'P': 1.4},
                        'Sedikit Aktif': {'L': 1.78, 'P': 1.64},
                        'Aktif': {'L': 1.78, 'P': 1.64},
                        'Sangat Aktif': {'L': 2.1, 'P': 1.82},
                    }
                    faktor = aktivitas_faktor[level_aktivitas][jenis_kelamin]

                    if jenis_kelamin == 'L':
                        bmr = (66 + (13.7 * berat_badan) + (5 * tinggi_badan) - (6.8 * usia)) * faktor
                    else:
                        bmr = (665 + (9.6 * berat_badan) + (1.8 * tinggi_badan) - (4.7 * usia)) * faktor

                    if program == "Penurunan Berat Badan":
                        target_calories = bmr - 500
                    elif program == "Peningkatan Berat Badan":
                        target_calories = bmr + 700
                    else:
                        target_calories = bmr
                    
                    self.user_data["bmr_value"] = bmr
                    self.user_data["target_calories"] = target_calories

                    cursor.execute("UPDATE user_data SET bmr_value = ?, target_calories = ? WHERE id = ?", 
                                   (bmr, target_calories, self.user_data["id"]))
                    conn.commit()
            conn.close()

    def set_category(self, category):
        self.food_category = category
        self.change_screen("food", "fade")
    
    def update_user_age(self, *args):
        app = App.get_running_app()
        user = app.user_data
        
        if user:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM user_data WHERE id = ?", (user["id"],))
            db_data = cursor.fetchone()

            if db_data:
                tanggal_lahir = db_data[4]
                usia = hitung_usia(tanggal_lahir)
                user["usia"] = usia
                
                cursor.execute("UPDATE user_data SET usia = ? WHERE username = ?", (usia, user["username"]))
                
                conn.commit()
                conn.close()
    
    def update_daily_calories(self, *args):
        app = App.get_running_app()
        user_data = app.user_data

        if user_data:
            username = user_data["username"]
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()

            today_date = datetime.now().strftime('%Y-%m-%d')
            cursor.execute("""
                SELECT SUM(kalori) 
                FROM calories_data
                WHERE username = ? AND tanggal = ?
            """, (username, today_date))
            total_calories = cursor.fetchone()[0] or 0

            user_data["daily_calories"] = total_calories
            
            cursor.execute("""
                UPDATE user_data
                SET daily_calories = ?
                WHERE username = ?
            """, (total_calories, username))
            conn.commit()
            conn.close()
    
    def calculate_progress(self):
        app = App.get_running_app()
        user_data = app.user_data

        if user_data:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM user_data WHERE id = ?", (user_data["id"],))
            db_data = cursor.fetchone()
            conn.close()

            if db_data:
                target_calories = db_data[13]
                daily_calories = db_data[14]
                if target_calories > 0:
                    return (daily_calories / target_calories) * 100
                else:
                    return 0    
        return 0

    def update_progress_bar(self, *args):
        self.update_daily_calories()
        
        current_screen = self.root.get_screen(self.current_screen)
        
        if current_screen:
            if hasattr(current_screen.ids, 'progress_bar'):
                progress_bar = current_screen.ids.progress_bar
                progress = self.calculate_progress()
                progress_bar.reset_animation()
                progress_bar.value = progress
                progress_bar.animate()
    
    def save_daily_data(self, *args):
        app = App.get_running_app()
        user_data = app.user_data
        
        if user_data:
            username = user_data["username"]
            
            today_date = datetime.now().strftime('%Y-%m-%d')
            
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT daily_data FROM user_data WHERE username = ?", (username,))
            result = cursor.fetchone()

            if result and result[0]:
                daily_data = json.loads(result[0])
            else:
                daily_data = []

            existing_entry = next((entry for entry in daily_data if entry['tanggal'] == today_date), None)

            if existing_entry:
                existing_entry['kalori'] = user_data["daily_calories"]
                existing_entry['berat_badan'] = user_data["berat_badan"]
                existing_entry['tinggi_badan'] = user_data["tinggi_badan"]
            else:
                daily_data.append({
                    'tanggal': today_date,
                    'kalori': user_data["daily_calories"],
                    'berat_badan': user_data["berat_badan"],
                    'tinggi_badan': user_data["tinggi_badan"]
                })

            updated_data = json.dumps(daily_data)
            cursor.execute("UPDATE user_data SET daily_data = ? WHERE username = ?", (updated_data, username))
            conn.commit()
            conn.close()
    
    def signup_user(self):
        app = App.get_running_app()
        
        nama_lengkap = app.nama_lengkap
        username = app.username
        password = app.password
        program = app.selected_program
        jenis_kelamin = app.jenis_kelamin
        tanggal_lahir = app.tanggal_lahir
        usia = app.usia
        tinggi_badan = app.tinggi_badan
        berat_badan = app.berat_badan
        level_aktivitas = app.selected_activity
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        try:
            cursor.execute('''
            INSERT INTO user_data (nama_lengkap, username, password, tanggal_lahir, program, jenis_kelamin, usia, tinggi_badan, berat_badan, level_aktivitas)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (nama_lengkap, username, password, tanggal_lahir, program, jenis_kelamin, usia, tinggi_badan, berat_badan, level_aktivitas))
            conn.commit()
            print("Data pengguna berhasil disimpan!")
        except sqlite3.IntegrityError:
            print("Invalid data")
        finally:
            conn.close()
    
    def reset_signup(self):
        signup2_screen = self.root.get_screen("signup2")
        signup2_screen.reset_fields()

        signup3_screen = self.root.get_screen("signup3")
        signup3_screen.reset_fields()

        signup4_screen = self.root.get_screen("signup4")
        signup4_screen.reset_fields()

        signup5_screen = self.root.get_screen("signup5")
        signup5_screen.reset_fields()
    
    def logout(self):
        self.reset_signup()
        app = App.get_running_app()
        app.user_data = None
        login_screen = self.root.get_screen("login")
        login_screen.reset_fields()
        self.change_screen("welcome", "fade")
    
if __name__ == "__main__":
    Calmy().run()