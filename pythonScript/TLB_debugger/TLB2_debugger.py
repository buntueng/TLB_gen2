import pathlib
import pygubu
import tkinter as tk
import tkinter.ttk as ttk

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "TLB2_debugger.ui"


class Tlb2DebuggerApp:
    def __init__(self, master=None):
        self.node_monitor_text = 0
        # build ui
        self.toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        self.left_frame = ttk.Frame(self.toplevel1)
        self.status_text = tk.Text(self.left_frame)
        self.status_text.configure(height='5', state='disabled', width='40')
        self.status_text.grid(column='0', padx='10', row='1', sticky='w')
        self.pc_command_text = tk.Text(self.left_frame)
        self.pc_command_text.configure(height='36', width='40')
        self.pc_command_text.grid(column='0', padx='10', pady='0 10', row='3', rowspan='15', sticky='w')
        self.status_label = ttk.Label(self.left_frame)
        self.status_label.configure(text='สถานะการทำงาน')
        self.status_label.grid(column='0', padx='10', pady='10', row='0', sticky='w')
        self.cmd_list_label = ttk.Label(self.left_frame)
        self.cmd_list_label.configure(text='PC command list')
        self.cmd_list_label.grid(column='0', padx='10', pady='10', row='2', sticky='w')
        self.connect_button = ttk.Button(self.left_frame)
        self.connect_button.configure(text='connect', width='17')
        self.connect_button.grid(column='2', padx='10', pady='0 30', row='1', sticky='ns')
        self.connect_button.configure(command=self.connect_button_pressed)
        self.load_button = ttk.Button(self.left_frame)
        self.load_button.configure(state='disabled', text='LOAD', width='17')
        self.load_button.grid(column='2', pady='0 30', row='3', sticky='ns')
        self.load_button.configure(command=self.load_button_pressed)
        self.save_button = ttk.Button(self.left_frame)
        self.save_button.configure(state='disabled', text='SAVE', width='17')
        self.save_button.grid(column='2', pady='0 30', row='4', sticky='ns')
        self.save_button.configure(command=self.save_button_pressed)
        self.clear_button = ttk.Button(self.left_frame)
        self.clear_button.configure(state='disabled', text='CLEAR', width='17')
        self.clear_button.grid(column='2', pady='0 30', row='5', sticky='ns')
        self.clear_button.configure(command=self.clear_button_pressed)
        self.run_button = ttk.Button(self.left_frame)
        self.run_button.configure(state='disabled', text='RUN', width='17')
        self.run_button.grid(column='2', row='6', sticky='ns')
        self.run_button.configure(command=self.run_button_pressed)
        self.cmd_scrollbar = ttk.Scrollbar(self.left_frame,command=self.pc_command_text.yview)
        self.cmd_scrollbar.configure(orient='vertical')
        self.cmd_scrollbar.grid(column='1', pady='0 10', row='3', rowspan='15', sticky='nsw')
        self.status_scrollbar = ttk.Scrollbar(self.left_frame,command=self.status_text.yview)
        self.status_scrollbar.configure(orient='vertical')
        self.status_scrollbar.grid(column='1', row='1', sticky='nsw')
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

        # Main widget
        self.mainwindow = self.toplevel1
    
    def run(self):
        self.mainwindow.mainloop()

    def connect_button_pressed(self):
        self.monitor_text.configure(state=tk.NORMAL)
        tags = ""
        node_id = self.node_monitor_text % 3
        if node_id == 0:
            tags = 'node1'
        elif node_id == 1:
            tags = 'node2'
        elif node_id == 2:
            tags = 'node3'
        
        message = tags + " >> CMM" + "\n"
        self.monitor_text.insert(tk.END,message,tags)
        self.monitor_text.configure(state=tk.DISABLED)
        self.node_monitor_text = self.node_monitor_text + 1

    def load_button_pressed(self):
        pass

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
