import PIL
from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from tkinter import filedialog
from tkinter import messagebox

import serial.tools.list_ports

import vlc

import csv


ports = serial.tools.list_ports.comports()

connected_to_Arduino = False

portsList = []
for onePort in ports:
    portsList.append(str(onePort))
    print(str(onePort))


def connect_to_arduino(comport, baudrate=9600):
    global ser
    ser = serial.Serial(comport, baudrate)
    global connected_to_Arduino
    connected_to_Arduino = True

def send_string_to_arduino(stringtosend):
    try:
        ser.write((stringtosend + "\r").encode('utf-8'))
    except Exception as e:
        print(e)
        log_box.insert(END, "Error sending to Arduino: \n")
        log_box.insert(END, (str(e) + "\n"))
        log_box.insert(END, ("-------------" + "\n"))
        messagebox.showerror(title="Error sending to Arduino", message="Error sending to Arduino: " + str(e))

def close_connection_to_arduino():
    ser.close()
    global connected_to_Arduino
    connected_to_Arduino = False



root = ttk.Window(title="Johannes Feuerwerk", themename="darkly",resizable=(False,False))


headline = ttk.Label(root, text="Feuerwerk Steuerung", style="danger.TLabel", font=('Helvetica', 35))
headline.grid(row=1, column=1, padx=10, pady=10)


### Show Log

show_log_frame = ttk.Labelframe(root, text='Log', style='info.TLabelframe')
show_log_frame.grid(row=5, column=1, padx=10, pady=15)


log_box = ScrolledText(show_log_frame, padding=5, height=10, autohide=True)
log_box.pack(fill=BOTH, expand=YES)


log_box.insert(END, "Application ready... \n")

media = vlc.MediaPlayer()


selectedPort = StringVar(root)

videofilepath = StringVar(root)
timecodefilepath = StringVar(root)

connected_to_Arduino_textvar = StringVar(root)
connected_to_Arduino_textvar.set("Disconnected")

connectbtntextvar = StringVar(root)
connectbtntextvar.set("Connect")

timecodepositions = []
timecodecommands = []

def csvreader(timecodefile):
    try:
        with open(timecodefile, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                print(row)
                timecodepositions.append(row[0])
                timecodecommands.append(row[1])
            print(timecodepositions)
            print(timecodecommands)
            log_box.insert(END, "Timecode file loaded: \n")
            log_box.insert(END, (str(timecodepositions) + "\n"))
            log_box.insert(END, (str(timecodecommands) + "\n"))
            log_box.insert(END, ("-------------" + "\n"))
    except:
        log_box.insert(END, "Error loading Timecode file: \n")
        log_box.insert(END, "-------------" + "\n")
        messagebox.showerror(title="Timecode load failed", message="Error loading Timecode file")



def connectbtnclick():
    if(connected_to_Arduino == False):
        try:
            sel_port = str(str(selectedPort.get()).split(" ")[0]).rstrip('\n').rstrip('\r')
            print("------")
            print(sel_port)
            connect_to_arduino(sel_port)
            connected_to_Arduino_textvar.set("Connected")
            connectbtntextvar.set("Disconnect")
        except Exception as e:
            print(e)
            log_box.insert(END, "Connection failed: \n")
            log_box.insert(END, (str(e) + "\n"))
            log_box.insert(END, ("-------------" + "\n"))
            messagebox.showerror(title="Connection failed", message="Error connecting to Arduino: " + str(e))
    else:
        try:
            close_connection_to_arduino()
            connected_to_Arduino_textvar.set("Disconnected")
            connectbtntextvar.set("Connect")
        except Exception as e:
            print(e)
            log_box.insert(END, "Disconnection failed: \n")
            log_box.insert(END, (str(e) + "\n"))
            log_box.insert(END, ("-------------" + "\n"))
            messagebox.showerror(title="Disconnection failed", message="Error disconnecting from Arduino: " + str(e))

def load_video_file():
    try:
        filename = filedialog.askopenfilename()
        print(filename)
        videofilepath.set(filename)
        log_box.insert(END, "Video file loaded: \n")
        log_box.insert(END, (str(filename) + "\n"))
        log_box.insert(END, ("-------------" + "\n"))
    except Exception as e:
        print(e)
        log_box.insert(END, "Video file load failed: \n")
        log_box.insert(END, (str(e) + "\n"))
        log_box.insert(END, ("-------------" + "\n"))
        messagebox.showerror(title="Video file load failed", message="Error loading video file")


def load_timecode_file():
    try:
        filename = filedialog.askopenfilename()
        print(filename)
        timecodefilepath.set(filename)
        csvreader(filename)
    except Exception as e:
        print(e)
        log_box.insert(END, "Timecode file load failed: \n")
        log_box.insert(END, (str(e) + "\n"))
        log_box.insert(END, ("-------------" + "\n"))
        messagebox.showerror(title="Timecode file load failed", message="Error loading Timecode file")

def start_show_btn_click():
    global connected_to_Arduino
    if (connected_to_Arduino == False):
        messagebox.showerror(title="Not connected", message="You need to connect to the Arduino first")
    else:
        try:
            global media
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
                        send_string_to_arduino(timecodecommands[index])
                        log_box.insert(END, "Command send to Arduino: ")
                        log_box.insert(END, (str(timecodecommands[index]) + "\n"))
                        log_box.insert(END, ("-------------" + "\n"))
                else:
                    root.update()

        except Exception as e:
            print(e)
            log_box.insert(END, "Show failed: \n")
            log_box.insert(END, (str(e) + "\n"))
            log_box.insert(END, ("-------------" + "\n"))
            messagebox.showerror(title="Show failed", message="Error playing show: " + str(e))

def stop_show_btn_click():
    try:
        global media
        media.stop()
        log_box.insert(END, "Show stopped \n")
        log_box.insert(END, ("-------------" + "\n"))
    except Exception as e:
        print(e)
        log_box.insert(END, "Show stop failed: \n")
        log_box.insert(END, (str(e) + "\n"))
        log_box.insert(END, ("-------------" + "\n"))
        messagebox.showerror(title="Show stop failed", message="Error stopping show: " + str(e))

def simulate_show_btn_click():

    try:
        global media
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
                    log_box.insert(END, "[Simulaton] Command send to Arduino: ")
                    log_box.insert(END, (str(timecodecommands[index]) + "\n"))
                    log_box.insert(END, ("-------------" + "\n"))
                    lastindex = index
            else:
                root.update()
    except Exception as e:
        print(e)
        log_box.insert(END, "Simulation failed: \n")
        log_box.insert(END, (str(e) + "\n"))
        log_box.insert(END, ("-------------" + "\n"))
        messagebox.showerror(title="Simualtion failed", message="Error playing the simulation: " + str(e))

### Connect to Arduino frame

Connect_to_Arduino_frame = ttk.Labelframe(root, text='Connect to Arduino', style='info.TLabelframe')
Connect_to_Arduino_frame.grid(row=2, column=1, padx=10, pady=15)

select_Port_combobox = ttk.Combobox(Connect_to_Arduino_frame, values=portsList, state='readonly', textvariable=selectedPort)
select_Port_combobox.grid(row=1, column=1, padx=5, pady=10)

connect_to_arduino_button = ttk.Button(Connect_to_Arduino_frame, bootstyle="primary", textvariable=connectbtntextvar, command=connectbtnclick)
connect_to_arduino_button.grid(row=1, column=2, padx=5, pady=10)

connection_status_lbl = ttk.Label(Connect_to_Arduino_frame, text="Connection Status: ")
connection_status_lbl.grid(row=2, column=1, padx=5, pady=5)

current_connection_stauts_lbl = ttk.Label(Connect_to_Arduino_frame, textvariable=connected_to_Arduino_textvar)
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

stop_show_btn = ttk.Button(show_control_frame, text="Stop show", bootstyle="danger", command=stop_show_btn_click)
stop_show_btn.grid(row=1, column=2, padx=5, pady=5)

reboot_Arduinos = ttk.Button(show_control_frame, text="Simulate show", bootstyle="warning", command=simulate_show_btn_click)
reboot_Arduinos.grid(row=1, column=3, padx=5, pady=5)





root.mainloop()
