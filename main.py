from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from app.bin import MainForm  # Módulo principal de la interfaz de usuario
with open("layout/form.kv", encoding='utf8') as f:
    Builder.load_string(f.read())

class MyApp(App):
    mainForm = MainForm.CalcGridLayout()
    def build(self):
        Window.maximize()
        #Window.bind(on_close=self.mainForm.on_close_window)
        self.title = 'YOLO V5'
        #self.mainForm.console_writer("INFO", "Símbolos del sistema cargados")
        #self.mainForm.load_configuration_app_screen()
        #self.mainForm.load_configuration_app_videoref()
        #self.mainForm.load_configuration_app_engarde()
        return self.mainForm
if __name__ == '__main__':
    MyApp().run()