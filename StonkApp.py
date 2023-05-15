import mplfinance as mpf
import mysql.connector as con
import numpy
import pandas as pd
import webcolors
import yfinance as yf
import os
from pathlib import Path

from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDTextButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.screenmanager import FadeTransition, ScreenManager, Screen, SwapTransition, NoTransition
from kivy.config import Config
from kivy.lang import Builder
from kivy.metrics import dp

from current_price import *
from stocks_main_new import *
from finding_stock import *

cur_file_path = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')

def per_pass():
    p_pass = ''
    if Path(f'{cur_file_path}/password.txt').is_file():
        with open(f'{cur_file_path}/password.txt','r') as file:
            p_pass = file.readline()
    return p_pass

def temp_pass():
    t_passw = ''
    if Path(f'{cur_file_path}/temp_password.txt').is_file():
        with open(f'{cur_file_path}/temp_password.txt','r') as file:
            t_passw = file.readline()
    return t_passw

theme = 'Light' #or 'Dark'

if theme == 'Dark':
    color = '#FFFFFF'
else:
    color = '#000000'

update_prices(symbol_list)

symbol_list = [
    "AAPL","TSLA","ADBE","GOOGL","AMZN","SONY","SPOT","MSFT","FB","KO","SNAP","GME",
    "MRNA","NFLX","QCOM","SQ","COIN","INFY","BA","ZM"
]

company_name_list = [
    "Apple Inc.","Tesla Inc.","Adobe Inc.", "Alphabet Inc.","Amazon, Inc.",
    "Sony Group Corporation","Spotify Technology S.A.","Microsoft Corporation","Facebook,Inc.",
    "The Coca-Cola Company","Snap Inc.","Gamestop Corporation","Moderna, Inc.","Netflix, Inc.","Qualcomm Incorporated",
    "Square, Inc.","Coinbase Global, Inc.","Infosys Ltd","Boeing Company (The)","Zoom video communications, Inc."
]

icon_list=[
    'apple','bolt','adobe','google','amazon','alpha-s','spotify',"microsoft",
    'facebook','bottle-soda-classic','snapchat','gamepad-variant','','netflix','alpha-q-circle','numeric-0-box-outline',
    'alpha-c-circle','','airplane-takeoff','video-box'
]

hexxx = [
    color,'#D0D0D0','#CC0000','#4081EC','#F48944',color,'#04C149','#68C6FF','#3053FF','#990000','#EECB4A','#CD2E2E','','#E50914',
    '#3053FF',color,'#154FE9','','#0037A2','#519CFE'
]

def torgb(hexx):
    deci = ''
    try:
        deci = list(numpy.array(webcolors.hex_to_rgb(str(hexx)))/255)
    except:
        pass
    return deci

class PassScreen(MDScreen):
    def show_dialogb(self):
        close_button = MDFlatButton(
            text = 'Close',
            font_size = 15,
            on_release = self.close_dialogb,
            opacity = 0.5)
        self.dialogb = MDDialog(
                    title = "SQL password",
                    auto_dismiss = False,
                    type="custom",
                    #size_hint = (0.7, 1),
                    content_cls = BoxInDialog(),
                    buttons = [close_button]
                    )
        self.dialogb.open()

    def close_dialogb(self, obj):
        self.dialogb.dismiss()
        self.change()

    def change(self):
        self.manager.current = 'main'
        self.manager.transition = FadeTransition(duration=0)

class BoxInDialog(MDBoxLayout):
    
    def check_connect(self, passww):
        try:
            import mysql.connector as con
            mycon = con.connect(host=" localhost",
                            user="root", 
                            passwd=passww)

            if mycon.is_connected():
                self.ids.passww.helper_text = 'Connected'
                return True
        except Exception as e:
            print(e)
            self.ids.passww.helper_text = 'Wrong Password'
            return False

    def eye_but_press(self):
        cur_icon = self.ids.eye_but.icon
        if cur_icon == 'eye-off':
            self.ids.eye_but.icon = 'eye'
            self.ids.passww.password = False
        else:
            self.ids.eye_but.icon = 'eye-off'
            self.ids.passww.password = True

    def go_but_press(self, password, state_checkbox):
        if state_checkbox == 'down':
            self.save_pass()
            self.ids.passww.helper_text = 'Connected & Saved'
        else:
            with open(f'{cur_file_path}/temp_password.txt', 'w') as file:
                file.writelines(self.ids.passww.text)

    def save_pass(self):
        with open(f'{cur_file_path}/password.txt', 'w') as file:
            file.writelines(self.ids.passww.text)

class MainScreen(MDScreen):
    def Pressed(self):
        text = self.ids.symbol_field.text
        if text.isalpha():
            timeperiod = '1y'
            t_passw = temp_pass()
            passw = per_pass()
            onpress(t_passw if t_passw != '' else passw,text, timeperiod)
        elif text.isdigit() or text.isspace():
            self.ids.fieldd.helper_text = 'Only LETTERS allowed'

class Table(MDScreen):
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        prices = price_list()
        col_d=[
            ("No.", dp(10)),
            ("Symbol", dp(20)),
            ("Symbol", dp(70)),
            ("Current Price($)", dp(30))
        ]
        row_d=[
            (str(i+1), symbol_list[i], (icon_list[i], (torgb(hexxx[i]) if torgb(hexxx[i]) != '' else None), company_name_list[i]), f'${prices[i]}') for i in range(20)
        ]
        data_tables = MDDataTable(
            pos_hint={"center_x": .5, "center_y": .5},
            size_hint=(0.9, 0.9),
            elevation=15,
            #use_pagination=True,
            rows_num=20,
            column_data=col_d,
            row_data=row_d)
        data_tables.bind(on_row_press= self.on_row_press)
        self.add_widget(data_tables)

    def on_row_press(self, instance_table, instance_row):
        click = instance_row.text
        x , position = type_col(click)
        print(x, position, type(position))
        passw = per_pass()
        t_passw = temp_pass()
        onpress(t_passw if t_passw != '' else passw, symbol_list[position], '1y')

sm = ScreenManager()
sm.add_widget(PassScreen(name='pass'))
sm.add_widget(MainScreen(name='main'))    

class StonkkApp(MDApp):

    def build(self):
        screen = Builder.load_file('layout.kv')
        self.theme_cls.theme_style = theme
        self.theme_cls.primary_palette = 'Gray'
        return screen
    
    def pwd_present(obj):
        my_file = Path(f'{cur_file_path}/password.txt')
        presentt = False

        def check_connect(passww):
            try:
                import mysql.connector as con
                mycon = con.connect(host=" localhost",
                                user="root", 
                                passwd=passww)
                if mycon.is_connected():
                    connect = True
            except Exception as e:
                print(e)
                connect = False
            return connect

        if my_file.is_file():
            with open(f'{cur_file_path}/password.txt','r') as file:
                passs = file.readline()
                connect = check_connect(passs)
                if connect == True:
                    presentt = True
        return presentt

StonkkApp().run()
if Path(f'{cur_file_path}/temp_password.txt').is_file():
    os.remove(f'{cur_file_path}/temp_password.txt')
    print('temp file deleted')