import pathlib
import pygubu
import tkinter as tk
import tkinter.ttk as ttk
import sys
import serial
import glob

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "printer_debugger_ui.ui"

def list_serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(2,20)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

class PrinterDebuggerUiApp:
    def __init__(self, master=None):
        # build ui
        self.mainWindow = tk.Tk() if master is None else tk.Toplevel(master)
        self.serial_port_label = ttk.Label(self.mainWindow)
        self.serial_port_label.configure(text='Serial port')
        self.serial_port_label.grid(column='0', padx='10', pady='10', row='0')
        self.response_label = ttk.Label(self.mainWindow)
        self.response_label.configure(text='Response')
        self.response_label.grid(column='0', pady='0 10', row='2')
        self.serial_port_combobox = ttk.Combobox(self.mainWindow)
        self.serial_port_combobox.configure(width='10')
        self.serial_port_combobox.grid(column='1', padx='10', row='0')
        self.connect_button = tk.Button(self.mainWindow)
        self.connect_button.configure(height='2', justify='center', state='normal', text='Connect')
        self.connect_button.configure(width='15')
        self.connect_button.grid(column='2', padx='10', pady='10', row='0', rowspan='2')
        self.connect_button.configure(command=self.connect_button_pressed)
        self.disconnect_button = tk.Button(self.mainWindow)
        self.disconnect_button.configure(height='2', state='disabled', text='disconnect', width='15')
        self.disconnect_button.grid(column='3', padx='0 10', pady='10', row='0')
        self.disconnect_button.configure(command=self.disconnect_button_pressed)
        self.response_text = tk.Text(self.mainWindow)
        self.response_text.configure(height='20', state='disabled', width='70')
        self.response_text.grid(column='0', columnspan='12', padx='20', pady='0 20', row='3', rowspan='7', sticky='ew')
        self.fn1_button = tk.Button(self.mainWindow)
        self.fn1_button.configure(height='2', state='disabled', text='FN1', width='15')
        self.fn1_button.grid(column='13', padx='0 20', row='3', sticky='n')
        self.fn1_button.configure(command=self.fn1_button_pressed)
        self.fn2_button = tk.Button(self.mainWindow)
        self.fn2_button.configure(height='2', state='disabled', text='FN2', width='15')
        self.fn2_button.grid(column='13', padx='0 20', row='4', sticky='n')
        self.fn2_button.configure(command=self.fn2_button_pressed)
        self.fn3_button = tk.Button(self.mainWindow)
        self.fn3_button.configure(height='2', state='disabled', text='FN3', width='15')
        self.fn3_button.grid(column='13', padx='0 20', row='5', sticky='n')
        self.fn3_button.configure(command=self.fn3_button_pressed)
        self.fn4_button = tk.Button(self.mainWindow)
        self.fn4_button.configure(height='2', state='disabled', text='FN4', width='15')
        self.fn4_button.grid(column='13', padx='0 20', row='6', sticky='n')
        self.fn4_button.configure(command=self.fn4_button_pressed)
        self.fn5_button = tk.Button(self.mainWindow)
        self.fn5_button.configure(height='2', state='disabled', text='FN5', width='15')
        self.fn5_button.grid(column='13', padx='0 20', row='7', sticky='n')
        self.fn5_button.configure(command=self.fn5_button_pressed)
        self.fn6_button = tk.Button(self.mainWindow)
        self.fn6_button.configure(height='2', state='disabled', text='FN6', width='15')
        self.fn6_button.grid(column='13', padx='0 20', row='8', sticky='n')
        self.fn6_button.configure(command=self.fn6_button_pressed)
        self.fn7_button = tk.Button(self.mainWindow)
        self.fn7_button.configure(height='2', state='disabled', text='FN7', width='15')
        self.fn7_button.grid(column='13', padx='0 20', pady='0 10', row='9', sticky='n')
        self.fn7_button.configure(command=self.fn7_button_pressed)
        self.mainWindow.configure(height='400', width='700')
        self.mainWindow.resizable(False, False)
        self.mainWindow.title('printer module tester')

        # Main widget
        self.mainwindow = self.mainWindow
    
    def run(self):
        self.mainwindow.mainloop()

    def connect_button_pressed(self):
        pass

    def disconnect_button_pressed(self):
        pass

    def fn1_button_pressed(self):
        pass

    def fn2_button_pressed(self):
        pass

    def fn3_button_pressed(self):
        pass

    def fn4_button_pressed(self):
        pass

    def fn5_button_pressed(self):
        pass

    def fn6_button_pressed(self):
        pass

    def fn7_button_pressed(self):
        pass


if __name__ == '__main__':
    app = PrinterDebuggerUiApp()
    app.run()


