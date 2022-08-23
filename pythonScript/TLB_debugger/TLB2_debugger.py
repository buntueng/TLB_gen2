import tkinter as tk
import tkinter.ttk as ttk
import sys
import glob
import serial
import time
    
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

class Tlb2DebuggerApp:
    def __init__(self, master=None):
        # build ui
        self.toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        self.left_frame = ttk.Frame(self.toplevel1)
        self.status_text = tk.Text(self.left_frame)
        self.status_text.configure(height='5', state='disabled', width='40')
        self.status_text.grid(column='0', columnspan='3', padx='10', row='5', sticky='w')
        self.pc_command_text = tk.Text(self.left_frame)
        self.pc_command_text.configure(height='25', width='40')
        self.pc_command_text.grid(column='0', columnspan='3', padx='10', pady='0 10', row='7', rowspan='15', sticky='w')
        self.status_label = ttk.Label(self.left_frame)
        self.status_label.configure(text='Status')
        self.status_label.grid(column='0', padx='10', pady='10', row='4', sticky='w')
        self.cmd_list_label = ttk.Label(self.left_frame)
        self.cmd_list_label.configure(text='Command')
        self.cmd_list_label.grid(column='0', padx='10', pady='10', row='6', sticky='w')
        self.connect_button = ttk.Button(self.left_frame)
        self.connect_button.configure(text='connect', width='17')
        self.connect_button.grid(column='2', columnspan='2', padx='20', pady='10 40', row='0', rowspan='5', sticky='ns')
        self.connect_button.configure(command=self.connect_button_pressed)
        self.load_button = ttk.Button(self.left_frame)
        self.load_button.configure(text='LOAD', width='17')
        self.load_button.grid(column='4', padx='10 0', pady='0 30', row='7', sticky='ns')
        self.load_button.configure(command=self.load_button_pressed)
        self.save_button = ttk.Button(self.left_frame)
        self.save_button.configure(state='disabled', text='SAVE', width='17')
        self.save_button.grid(column='4', padx='10 0', pady='0 30', row='8', sticky='ns')
        self.save_button.configure(command=self.save_button_pressed)
        self.clear_button = ttk.Button(self.left_frame)
        self.clear_button.configure(state='disabled', text='CLEAR', width='17')
        self.clear_button.grid(column='4', padx='10 0', pady='0 30', row='9', sticky='ns')
        self.clear_button.configure(command=self.clear_button_pressed)
        self.run_button = ttk.Button(self.left_frame)
        self.run_button.configure(state='disabled', text='RUN', width='17')
        self.run_button.grid(column='4', padx='10 0', row='10', sticky='ns')
        self.run_button.configure(command=self.run_button_pressed)
        self.cmd_scrollbar = ttk.Scrollbar(self.left_frame,command=self.pc_command_text.yview)
        self.cmd_scrollbar.configure(orient='vertical')
        self.cmd_scrollbar.grid(column='3', pady='0 10', row='7', rowspan='15', sticky='nsw')
        self.status_scrollbar = ttk.Scrollbar(self.left_frame,command=self.status_text.yview)
        self.status_scrollbar.configure(orient='vertical')
        self.status_scrollbar.grid(column='3', row='5', sticky='nsw')
        self.pclink_label = ttk.Label(self.left_frame)
        self.pclink_label.configure(text='PC Link')
        self.pclink_label.grid(column='0', padx='10', pady='10', row='0', sticky='w')
        self.pc_port_combobox = ttk.Combobox(self.left_frame)
        self.pc_port_combobox.configure(width='15')
        self.pc_port_combobox.grid(column='1', row='0', sticky='w')
        self.master_node_label = ttk.Label(self.left_frame)
        self.master_node_label.configure(text='Master')
        self.master_node_label.grid(column='0', padx='10', row='1', sticky='w')
        self.master_port_combobox = ttk.Combobox(self.left_frame)
        self.master_port_combobox.configure(width='15')
        self.master_port_combobox.grid(column='1', row='1', sticky='w')
        self.label3 = ttk.Label(self.left_frame)
        self.label3.configure(text='Node 1')
        self.label3.grid(column='0', padx='10', row='2', sticky='w')
        self.node1_port_combobox = ttk.Combobox(self.left_frame)
        self.node1_port_combobox.configure(width='15')
        self.node1_port_combobox.grid(column='1', pady='10', row='2', sticky='w')
        self.node2_label = ttk.Label(self.left_frame)
        self.node2_label.configure(text='Node2')
        self.node2_label.grid(column='0', padx='10', row='3', sticky='w')
        self.node2_port_combobox = ttk.Combobox(self.left_frame)
        self.node2_port_combobox.configure(width='15')
        self.node2_port_combobox.grid(column='1', row='3', sticky='w')
        self.left_frame.configure(height='768', width='400')
        self.left_frame.grid(column='0', row='0', sticky='ns')
        self.right_frame = ttk.Frame(self.toplevel1)
        self.monitor_text = tk.Text(self.right_frame)
        self.monitor_text.configure(height='44', insertunfocussed='none', state='disabled', width='45')
        self.monitor_text.grid(column='0', padx='10', pady='0 20', row='1', rowspan='15', sticky='nsw')
        self.monitor_label = ttk.Label(self.right_frame)
        self.monitor_label.configure(text='หน้าต่าง monitor')
        self.monitor_label.grid(column='0', padx='10', pady='10', row='0', sticky='w')
        self.clear_monitor_button = ttk.Button(self.right_frame)
        self.clear_monitor_button.configure(state='disabled', text='เคลียร์ข้อความ', width='17')
        self.clear_monitor_button.grid(column='2', padx='10', pady='0 30', row='1', sticky='nsew')
        self.clear_monitor_button.configure(command=self.clear_monitor_button_pressed)
        self.save_monitor_button = ttk.Button(self.right_frame)
        self.save_monitor_button.configure(state='disabled', text='บันทึก', width='17')
        self.save_monitor_button.grid(column='2', padx='10', row='2', sticky='nsew')
        self.save_monitor_button.configure(command=self.save_monitor_button_pressed)
        self.monitor_scrollbar = ttk.Scrollbar(self.right_frame,command=self.monitor_text.yview)
        self.monitor_scrollbar.configure(orient='vertical')
        self.monitor_scrollbar.grid(column='1', pady='0 20', row='1', rowspan='15', sticky='nsw')
        self.right_frame.configure(height='768', width='624')
        self.right_frame.grid(column='1', row='0', sticky='n')
        self.toplevel1.configure(height='200', width='200')
        self.toplevel1.geometry('1024x768')
        self.toplevel1.resizable(False, False)
        self.toplevel1.title('TLB gen2 - Debugger')
        self.toplevel1.grid_anchor('center')
        # =========== set tag to 
        self.monitor_text.tag_config('node1', background="aquamarine", foreground="black")
        self.monitor_text.tag_config('node2', background="azure1", foreground="black")
        self.monitor_text.tag_config('node3', background="bisque", foreground="black")

        # send feedback
        self.pc_command_text['yscrollcommand'] = self.cmd_scrollbar.set
        self.status_text['yscrollcommand'] = self.status_scrollbar.set
        self.monitor_text['yscrollcommand'] = self.monitor_scrollbar.set

        # create comport objects
        self.pc_link = serial.Serial()
        # scan for available serial port 
        self.scan_serial_port()
        # Main widget
        self.mainwindow = self.toplevel1
    
    def scan_serial_port(self):
        list_available_ports = list_serial_ports()
        if len(list_available_ports)>0:
            self.pc_port_combobox['values'] = list_available_ports
            self.master_port_combobox['values'] = list_available_ports
            self.node1_port_combobox['values'] = list_available_ports
            self.node2_port_combobox['values'] = list_available_ports
        else:
            self.toplevel1.after(5000,self.scan_serial_port)


    def run(self):
        self.mainwindow.mainloop()

    def connect_button_pressed(self):
        #print(self.pc_port_combobox.get())
        try:
            self.pc_link.baudrate = 115200
            self.pc_link.port = self.pc_port_combobox.get()
            
            print("pass")
        except:
            print("error")


    def load_button_pressed(self):
        if self.pc_link.is_open:
            self.pc_link.writelines(b'hello')
            print("GG")
        else:
            self.pc_link.open()
            print("FF")

    def save_button_pressed(self):
        pass

    def clear_button_pressed(self):
        pass

    def run_button_pressed(self):
        pass

    def clear_monitor_button_pressed(self):
        pass

    def save_monitor_button_pressed(self):
        pass


if __name__ == '__main__':
    app = Tlb2DebuggerApp()
    app.run()


