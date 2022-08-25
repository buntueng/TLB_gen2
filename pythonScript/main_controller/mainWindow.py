import tkinter as tk
import tkinter.ttk as ttk
import serial
import time

class MainControllerApp:
    def __init__(self, master=None):
        self.parameter_file_location = ""
        self.comport = serial.Serial()
        self.comport.baudrate = 115200
        self.comport.timeout = 2
        self.comport_available = False
        self.load_parameters()
        self.main_state = 0
        self.state_timer = 0
        # build ui
        self.toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        self.topFrame = ttk.Frame(self.toplevel1)
        self.box1_entry = ttk.Entry(self.topFrame)
        self.box1_entry.configure(justify='center', state='readonly', width='15')
        _text_ = '''BOX1'''
        self.box1_entry['state'] = 'normal'
        self.box1_entry.delete('0', 'end')
        self.box1_entry.insert('0', _text_)
        self.box1_entry['state'] = 'readonly'
        self.box1_entry.grid(column='0', padx='30 20', pady='20', row='0', sticky='ew')
        self.box2_entry = ttk.Entry(self.topFrame)
        self.box2_entry.configure(justify='center', state='readonly', width='15')
        _text_ = '''BOX2'''
        self.box2_entry['state'] = 'normal'
        self.box2_entry.delete('0', 'end')
        self.box2_entry.insert('0', _text_)
        self.box2_entry['state'] = 'readonly'
        self.box2_entry.grid(column='1', row='0', sticky='ew')
        self.box3_entry = ttk.Entry(self.topFrame)
        self.box3_entry.configure(justify='center', state='readonly', width='15')
        _text_ = '''BOX3'''
        self.box3_entry['state'] = 'normal'
        self.box3_entry.delete('0', 'end')
        self.box3_entry.insert('0', _text_)
        self.box3_entry['state'] = 'readonly'
        self.box3_entry.grid(column='2', padx='20', row='0', sticky='ew')
        self.entry4 = ttk.Entry(self.topFrame)
        self.entry4.configure(justify='center', state='readonly', width='15')
        _text_ = '''BOX4'''
        self.entry4['state'] = 'normal'
        self.entry4.delete('0', 'end')
        self.entry4.insert('0', _text_)
        self.entry4['state'] = 'readonly'
        self.entry4.grid(column='3', padx='0 30', row='0', sticky='ew')
        self.topFrame.configure(height='100', width='500')
        self.topFrame.grid(column='0', row='0', sticky='ew')
        self.middleFrame = ttk.Frame(self.toplevel1)
        self.status_label = ttk.Label(self.middleFrame)
        self.status_label.configure(justify='left', text='status')
        self.status_label.grid(column='0', padx='20', row='0', sticky='w')
        self.status_text = tk.Text(self.middleFrame)
        self.status_text.configure(height='5', width='56')
        self.status_text.grid(column='0', padx='20 5', pady='5', row='1')
        self.middleFrame.configure(height='100', width='500')
        self.middleFrame.grid(column='0', row='1', sticky='ew')
        self.bottom_frame = ttk.Frame(self.toplevel1)
        self.message_label = ttk.Label(self.bottom_frame)
        self.message_label.configure(text='Message')
        self.message_label.grid(column='0', padx='20', pady='5', row='0', sticky='w')
        self.message_text = tk.Text(self.bottom_frame)
        self.message_text.configure(height='15', width='56')
        self.message_text.grid(column='0', padx='20 5', pady='5 15', row='1')
        self.message_scrollbar = ttk.Scrollbar(self.bottom_frame)
        self.message_scrollbar.configure(orient='vertical')
        self.message_scrollbar.grid(column='1', pady='5', row='1', sticky='ns')
        self.bottom_frame.configure(height='500', width='500')
        self.bottom_frame.grid(column='0', row='2', sticky='ew')
        self.toplevel1.configure(height='200', width='500')
        self.toplevel1.title('TLB controller')

        self.init_widget()
        # Main widget
        self.mainwindow = self.toplevel1
        #self.test_messagetext()                        this is a debugging function
        # self.update_hilight_status()                  call this function after update status_text widget
        self.run_main_state()
    
    def run(self):
        self.mainwindow.mainloop()

    def init_widget(self):
        self.message_scrollbar.configure(command=self.message_text.yview)
        self.status_text.configure(state=tk.DISABLED)
        self.message_text.configure(state=tk.DISABLED)
        self.status_text.tag_config('odd', background="aquamarine", foreground="black")
        self.status_text.tag_config('even', background="azure1", foreground="black")
        self.message_text.tag_config('pc', background="aquamarine", foreground="black")
        self.message_text.tag_config('device', background="azure1", foreground="black")
        self.message_text['yscrollcommand'] = self.message_scrollbar.set

    def test_messagetext(self):
        self.message_text.configure(state=tk.NORMAL)
        self.status_text.configure(state=tk.NORMAL)
        self.status_text.insert(tk.END,"TTT\n")
        self.status_text.insert(tk.END,"TTT\n")
        self.status_text.insert(tk.END,"TTT\n")
        self.status_text.insert(tk.END,"KKK\n")
        self.status_text.insert(tk.END,"BBB\n")

        for i in range(30):
            self.message_text.insert(tk.END,"TTTT\n")
        self.status_text.configure(state=tk.DISABLED)
        self.message_text.configure(state=tk.DISABLED)

    def load_parameters(self):
        try:
            parameter_file = open(self.parameter_file_location,"r")
            params_list = parameter_file.readline().split(',')
            self.comport.port = params_list[0]
            parameter_file.close()
            self.comport.open()
            if self.comport.is_open:
                self.comport_available = True
            else:
                self.comport_available = False
        except:
            self.comport_available = False
    
    def run_main_state(self):
        if self.main_state == 0:
            if self.comport_available == True:
                self.main_state = 1
                self.mainwindow.after(3000,self.run_main_state)             # wait 3 seconds for serial port is ready to send data
        elif self.main_state == 1:  # try to send CMD through serial port        
            try:                    
                self.main_state = 2
            except:
                pass
        elif self.main_state == 2:  # read response from serial port
            try:
                pass
            except:
                pass
        

    
    def update_hilight_status(self):
        number_of_line = int(self.status_text.index(tk.END).split('.')[0]) - 2
        if number_of_line >= 0:
            for current_index in range(number_of_line):
                if current_index % 2 == 0:
                    self.status_text.tag_add("odd","{}.0".format(current_index+1), "{}.0+1lines".format(current_index+1))
                else:
                    self.status_text.tag_add("even","{}.0".format(current_index+1), "{}.0+1lines".format(current_index+1))


if __name__ == '__main__':
    app = MainControllerApp()
    app.run()


