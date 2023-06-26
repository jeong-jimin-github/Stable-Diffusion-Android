from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.image import Image as CoreImage
import io
import base64
import requests
from kivymd.toast import toast
import certifi
import os

os.environ['SSL_CERT_FILE'] = certifi.where()
url = "http://115.138.164.135:7860/sdapi/v1/txt2img"



def get_image(prompt):
    toast('Please Wait...')
    image_data = {
    "enable_hr": "false",
    "denoising_strength": 0.7,
    "firstphase_width": 0,
    "firstphase_height": 0,
    "hr_scale": 2,
    "hr_upscaler": "R-ESRGAN 4x+ Anime6B",
    "hr_second_pass_steps": 0,
    "hr_resize_x": 0,
    "hr_resize_y": 0,
    "prompt": "masterpiece, best quality, " + prompt,
    "seed": -1,
    "subseed": -1,
    "subseed_strength": 0,
    "seed_resize_from_h": -1,
    "seed_resize_from_w": -1,
    "sampler_name": "DPM++ 2M Karras",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 10,
    "cfg_scale": 7,
    "width": 512,
    "height": 512,
    "restore_faces": "false",
    "tiling": "false",
    "do_not_save_samples": "false",
    "do_not_save_grid": "false",
    "negative_prompt": "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts,signature, watermark, username, blurry, artist name, bad_prompt",
    "eta": 0,
    "s_churn": 0,
    "s_tmax": 0,
    "s_tmin": 0,
    "s_noise": 1,
    "override_settings": {},
    "override_settings_restore_afterwards": "true",
    "script_args": [],
    "sampler_index": "DPM++ 2M Karras",
    "script_name": "",
    "send_images": "true",
    "save_images": "true",
    "alwayson_scripts": {}
    }
    
    response = requests.post(url, json=image_data)

    # Check the response status code
    if response.status_code == 200:
        # Get the image URL from the response JSON
        return response.json()['images'][0]
        
    else:
        return False
    
def api(prompt, widget):
    image = get_image(prompt.text)
    widget.texture = CoreImage(io.BytesIO(base64.b64decode(image)), ext="png").texture

def clear(widget, widget2):
    widget.text = "masterpiece, best quality, "
    widget2.texture = None

class MainApp(MDApp):
    title = "Stable Diffusion"

    def build(self):
        b = BoxLayout(orientation ='vertical', padding = 10, spacing = 10)
        bt = BoxLayout(orientation ='horizontal')
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        aimg = Image(allow_stretch = True)

        t = MDTextField(text = "", multiline = True, hint_text = "Prompt (English Only)")
        btn = MDRaisedButton(text ="Submit", size_hint =(.1, .15), pos_hint ={'center_x': .25, 'center_y': .15}, on_press = lambda x: api(t, aimg), md_bg_color = "blue")
        btnb = MDRaisedButton(text ="Clear", size_hint =(.1, .15), pos_hint ={'center_x': .75, 'center_y': .15}, on_press = lambda x: clear(t, aimg), md_bg_color = "red")

        bt.add_widget(btn)
        bt.add_widget(btnb)

        b.add_widget(aimg)
        b.add_widget(t)
        b.add_widget(bt)
        return b


MainApp().run()
