import tkinter as tk
import serial as ser                         # library name pyserial
import sys
import glob
import time

debugging = False
running_state = 0

def clear_button_pressed():
    message_text.delete("1.0",tk.END)

def connect_button_pressed():
    shown_message = ""
    shown_warning = False
    comport = select_port.get()
    if len(comport) > 1:
        comport = comport.strip()
        serial_port.baudrate = 115200
        serial_port.port = comport
        try:
            serial_port.open()
        except:
            pass
        if comport == "เลือกพอร์ต":
            shown_message = "โปรดเลือกคอมพอร์ต"
            shown_warning = True
            print(shown_message)
        else:
            if serial_port.isOpen:
                print("serial port is open")
                connect_button.configure(state=tk.DISABLED)
                start_button.configure(state=tk.NORMAL)
            else:
                serial_port.open()
                print("open serial port")

def stop_button_pressed():
    global running_state
    running_state = 0
    start_button.configure(state=tk.NORMAL)
    stop_button.configure(state=tk.DISABLED)
    clear_button.configure(state=tk.NORMAL)

def start_button_pressed():
    global running_state
    running_state = 1
    update_sensor_value()
    start_button.configure(state=tk.DISABLED)
    stop_button.configure(state=tk.NORMAL)
    clear_button.configure(state=tk.DISABLED)

def update_sensor_value():
    global running_state
    if running_state == 1:
        if serial_port.isOpen:
            while serial_port.in_waiting:
                input_message = serial_port.readline()
                message_text.insert(tk.END,input_message)
        else:
            serial_port.open()
        
        main_window.after(100,update_sensor_value)

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
            s = ser.Serial(port)
            s.close()
            result.append(port)
        except (OSError, ser.SerialException):
            pass
    return result


def check_serial():
    if debugging:
        print("function check_serial was called")
    list_available_port = list_serial_ports()
    if len(list_available_port) == 0:
        list_available_port = ['']
        main_window.after(500,check_serial)
    else:
        menu = opt["menu"]
        menu.delete(0, "end")
        for available_comport in list_available_port:
            menu.add_command(label=available_comport,command=lambda value=available_comport: select_port.set(value))
        # print("update comport")


#-------Main GUI Code------------------
main_window = tk.Tk()
main_window.title('Bus monitor >>')
window_height = 610
window_width = 850
window_gometry = str(window_width)+"x"+str(window_height)
main_window.geometry(window_gometry)
main_window.resizable(False, False)
#========== set window at center screen
screen_width = main_window.winfo_screenwidth()
screen_height = main_window.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))
main_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))


top_left_frame = tk.Frame(master=main_window)
bottom_left_frame = tk.Frame(master=main_window)
right_frame = tk.Frame(master=main_window)

top_left_frame.grid(row=0,column=0,padx=10,sticky=tk.W)
bottom_left_frame.grid(row=1,column=0,padx=10,sticky=tk.S,pady=(20,10))
right_frame.grid(row=0,column=1,rowspan=2,padx=10,sticky=tk.N,pady=20)

# ========== top left frame =========
select_port = tk.StringVar()

port_label = tk.Label(master=top_left_frame,text='คอมพอร์ต',font = ('TH Niramit AS' , 16),justify=tk.LEFT)
select_port.set("เลือกพอร์ต")
list_available_port = ['']
opt = tk.OptionMenu(top_left_frame, select_port, *list_available_port)
opt.config(width=10, font=('TH Niramit AS', 16))

encode_int = tk.IntVar()
hex_radio_button = tk.Radiobutton(master=top_left_frame,text="HEX encode",variable=encode_int,value=1)
ascii_radio_button = tk.Radiobutton(master=top_left_frame,text="ASCII encode",variable=encode_int,value=2)
check_serial()
port_label.grid(row=0,column=0,pady=10)
opt.grid(row=0,column=1)
hex_radio_button.grid(row=1,column=0,padx=10)
ascii_radio_button.grid(row=1,column=1)
encode_int.set("2")

#========== bottom widget ============
message_text = tk.Text(master=bottom_left_frame,width=80,height=30)
message_text.grid(row=0,column=0)
# ========= right frame ==============
connect_button = tk.Button(master=right_frame,text="Connect",width=20,height=2,font = ('TH Niramit AS' , 16),command=lambda:connect_button_pressed())
start_button = tk.Button(master=right_frame,text="Start",width=20,height=2,font = ('TH Niramit AS' , 16),command=lambda:start_button_pressed())
stop_button = tk.Button(master=right_frame,text="Stop",width=20,height=2,font = ('TH Niramit AS' , 16),command=lambda:stop_button_pressed())
save_button = tk.Button(master=right_frame,text="Save",width=20,height=2,font = ('TH Niramit AS' , 16))
clear_button = tk.Button(master=right_frame,text="Clear",width=20,height=2,font = ('TH Niramit AS' , 16),command=lambda:clear_button_pressed())

connect_button.grid(row=0,column=0)
start_button.grid(row=1,column=0,pady=10)
stop_button.grid(row=2,column=0)
save_button.grid(row=3,column=0,pady=10)
clear_button.grid(row=4,column=0)
# =========== disable button ========
start_button.configure(state=tk.DISABLED)
stop_button.configure(state=tk.DISABLED)
save_button.configure(state=tk.DISABLED)
clear_button.configure(state=tk.DISABLED)
# ======================================
serial_port = ser.Serial()
main_window.mainloop()
