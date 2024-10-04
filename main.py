import PIL
from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from tkinter import filedialog

import serial.tools.list_ports

import vlc

import csv


ports = serial.tools.list_ports.comports()

portsList = []
for onePort in ports:
    portsList.append(str(onePort))
    print(str(onePort))


def connect_to_arduino(comport, baudrate=9600):
    global ser
    ser = serial.Serial(comport, baudrate)

def send_string_to_arduino(stringtosend):
    ser.write(stringtosend.encode())

def close_connection_to_arduino():
    ser.close()


root = ttk.Window(title="Johannes Feuerwerk", themename="darkly",resizable=(False,False))


headline = ttk.Label(root, text="Feuerwerk Steuerung", style="danger.TLabel", font=('Helvetica', 35))
headline.grid(row=1, column=1, padx=10, pady=10)

selectedPort = StringVar(root)

videofilepath = StringVar(root)
timecodefilepath = StringVar(root)

timecodepositions = []
timecodecommands = []

def csvreader(timecodefile):
    with open(timecodefile, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            print(row)
            timecodepositions.append(row[0])
            timecodecommands.append(row[1])
        print(timecodepositions)
        print(timecodecommands)


def connectbtnclick():
    sel_port = str(str(selectedPort.get()).split(" ")[0]).rstrip('\n').rstrip('\r')
    print("------")
    print(sel_port)
    connect_to_arduino(sel_port)


def load_video_file():
    filename = filedialog.askopenfilename()
    print(filename)
    videofilepath.set(filename)


def load_timecode_file():
    filename = filedialog.askopenfilename()
    print(filename)
    timecodefilepath.set(filename)
    csvreader(filename)


def start_show_btn_click():
    
    media = vlc.MediaPlayer(videofilepath.get())
    media.play()
    lastindex = ""
    while media.get_state() != vlc.State.Ended:
        video_position = str(int(media.get_time() /1000))
        # print(video_position)

        if(video_position in timecodepositions):
            index = timecodepositions.index(video_position)
            if(lastindex != index):
                print(timecodecommands[index])
                lastindex = index
                #send_string_to_arduino(timecodecommands[index])




### Connect to Arduino frame

Connect_to_Arduino_frame = ttk.Labelframe(root, text='Connect to Arduino', style='info.TLabelframe')
Connect_to_Arduino_frame.grid(row=2, column=1, padx=10, pady=15)

select_Port_combobox = ttk.Combobox(Connect_to_Arduino_frame, values=portsList, state='readonly', textvariable=selectedPort)
select_Port_combobox.grid(row=1, column=1, padx=5, pady=10)

connect_to_arduino_button = ttk.Button(Connect_to_Arduino_frame, bootstyle="primary", text="Connect", command=connectbtnclick)
connect_to_arduino_button.grid(row=1, column=2, padx=5, pady=10)

connection_status_lbl = ttk.Label(Connect_to_Arduino_frame, text="Connection Status: ")
connection_status_lbl.grid(row=2, column=1, padx=5, pady=5)

current_connection_stauts_lbl = ttk.Label(Connect_to_Arduino_frame, style="danger", text="disconnected")
current_connection_stauts_lbl.grid(row=2, column=2, padx=5, pady=5)

### Load show files frame

Load_show_files_frame = ttk.Labelframe(root, text='Load show files', style='info.TLabelframe')
Load_show_files_frame.grid(row=3, column=1, padx=10, pady=15)

video_file_path_lbl = ttk.Label(Load_show_files_frame, text="Load Video")
video_file_path_lbl.grid(row=1, column=1, padx=5, pady=5)

video_file_path_entry = ttk.Entry(Load_show_files_frame, textvariable=videofilepath)
video_file_path_entry.grid(row=1, column=2, padx=5, pady=5)

video_file_path_browse_btn = ttk.Button(Load_show_files_frame, text="Browse", command=load_video_file)
video_file_path_browse_btn.grid(row=1, column=3, padx=5, pady=5)



timecode_file_path_lbl = ttk.Label(Load_show_files_frame, text="Load Timecode")
timecode_file_path_lbl.grid(row=2, column=1, padx=5, pady=5)

timecode_file_path_entry = ttk.Entry(Load_show_files_frame, textvariable=timecodefilepath)
timecode_file_path_entry.grid(row=2, column=2, padx=5, pady=5)

timecode_file_path_browse_btn = ttk.Button(Load_show_files_frame, text="Browse", command=load_timecode_file)
timecode_file_path_browse_btn.grid(row=2, column=3, padx=5, pady=5)


### Show control frame


show_control_frame = ttk.Labelframe(root, text='Show Control', style='info.TLabelframe')
show_control_frame.grid(row=4, column=1, padx=10, pady=15)

Start_show_btn = ttk.Button(show_control_frame, text="Start show", bootstyle="success", command=start_show_btn_click)
Start_show_btn.grid(row=1, column=1, padx=5, pady=5)

stop_show_btn = ttk.Button(show_control_frame, text="Stop show", bootstyle="danger")
stop_show_btn.grid(row=1, column=2, padx=5, pady=5)

reboot_Arduinos = ttk.Button(show_control_frame, text="Reboot Arduinos", bootstyle="warning")
reboot_Arduinos.grid(row=1, column=3, padx=5, pady=5)



### Show Log

show_log_frame = ttk.Labelframe(root, text='Show log', style='info.TLabelframe')
show_log_frame.grid(row=5, column=1, padx=10, pady=15)


log_box = ScrolledText(show_log_frame, padding=5, height=10, autohide=True)
log_box.pack(fill=BOTH, expand=YES)


log_box.insert(END, 'Insert your text here.')

root.mainloop()
