
# Import modules
from tkinter import *
from tkinter import messagebox
from datetime import datetime
import pytz
import requests
import json

software_version = 'v1.1'
IST = pytz.timezone('America/New_York')


app = Tk()

# App Geometry and components
app.geometry("700x480+600+300")
app.title(f"Callsign Checker  {software_version}")
app.iconbitmap("Images_Icons\local_repeater.ico")
app.resizable(False, True)
app.config(background = '#293241')

## DEFAULT values
CALLSIGN = 'KB1YTW'

# Color value reference
top_left_frame_bg  = "#5c4ce1"
top_right_frame_bg = '#867ae9'

# Frame details
frame1 = Frame(app, height = 120, width=180, bg= top_left_frame_bg, bd=1, relief = FLAT)
frame1.place(x=0,y=0)

frame2 = Frame(app, height = 120, width=520, bg= top_right_frame_bg, bd=1, relief = FLAT)
frame2.place(x=180,y=0)

frame3 = Frame(app, height = 30, width=700, bg= 'black', bd=1, relief = RAISED)
frame3.place(x=0,y=120)

# Labels
label_date_now = Label(text="Current Date", bg = top_left_frame_bg, font = 'Verdana 12 bold')
label_date_now.place(x=20, y=40)

label_time_now = Label(text="Current Time", bg = top_left_frame_bg, font = 'Verdana 12')
label_time_now.place(x=20, y=60)

label_callsign = Label(text="Callsign", bg = top_right_frame_bg, font = 'Verdana 11')
label_callsign.place(x=220, y=15)

label_search_repeat = Label(text="Search Callsign", bg = top_right_frame_bg, font = 'Verdana 8')
label_search_repeat.place(x=570, y=70)
   
label_head_result = Label(text="Status    Class      Expires        Name                Address             City        State        Zip          Country", bg = 'black', fg='white', font = 'Verdana 8 bold')
label_head_result.place(x=10, y=125)


# Entry boxes
callsign_text_var = StringVar()
callsign_textbox = Entry(app,width = 11, bg = '#eaf2ae', fg= 'black', textvariable = callsign_text_var, font='verdana 11')
callsign_textbox['textvariable'] = callsign_text_var
callsign_textbox.place(x= 220, y=40)

## TEXT BOX - for RESULTs
result_box_status = Text(app, height = 20, width = 8, bg='#293241',fg='#ecfcff', relief=FLAT, font='verdana 8')
result_box_status.place(x= 7 , y= 152)
result_box_privileges = Text(app, height = 20, width = 10, bg='#293241',fg='#ecfcff', relief=FLAT, font='verdana 8')
result_box_privileges.place(x= 75 , y= 152)
result_box_expires = Text(app, height = 20, width = 15, bg='#293241',fg='#ecfcff', relief=FLAT, font='verdana 8')
result_box_expires.place(x= 110 , y= 152)
result_box_name = Text(app, height = 20, width = 15, bg='#293241',fg='#ecfcff', relief=FLAT, font='verdana 8')
result_box_name.place(x= 200 , y= 152)
result_box_address = Text(app, height = 20, width = 15, bg='#293241',fg='#ecfcff', relief=FLAT, font='verdana 8')
result_box_address.place(x= 285 , y= 152)
result_box_city = Text(app, height = 20, width = 15, bg='#293241',fg='#ecfcff', relief=FLAT, font='verdana 8')
result_box_city.place(x= 400 , y= 152)
result_box_state = Text(app, height = 20, width = 8, bg='#293241',fg='#ecfcff', relief=FLAT, font='verdana 8')
result_box_state.place(x= 480 , y= 152)
result_box_zip = Text(app, height = 20, width = 10, bg='#293241',fg='#ecfcff', relief=FLAT, font='verdana 8')
result_box_zip.place(x= 525 , y= 152)
result_box_country = Text(app, height = 20, width = 15, bg='#293241',fg='#ecfcff', relief=FLAT, font='verdana 8')
result_box_country.place(x= 580 , y= 152)


## Defining Functions

# Input Callsign
def fill_callsign():
    curr_callsign = get_callsign
    callsign_text_var.set = curr_callsign

def get_callsign():
    response_callsign = input()
    return response_callsign

def update_clock():
    raw_TS = datetime.now(IST)
    date_now = raw_TS.strftime("%d %b %Y")
    time_now = raw_TS.strftime("%H:%M:%S %p")
    formatted_now = raw_TS.strftime("%m-%d-%Y")
    label_date_now.config(text = date_now)
    # label_date_now.after(500, update_clock)
    label_time_now.config(text = time_now)
    label_time_now.after(1000, update_clock)
    return formatted_now

def new_api_call(CALLSIGN):
    headers = {'User-Agent': 'My User Agent 1.0', 'From': 'lafountainp@comcast.net'}
    request_link = f"http://api.hamdb.org/{CALLSIGN}/json/callsignapi"
    response = requests.get(request_link, headers = headers)
    resp_JSON = response.json()['hamdb']['callsign']
    return resp_JSON

def clear_result_box():
    result_box_status.delete('1.0', END)
    result_box_privileges.delete('1.0', END)
    result_box_expires.delete('1.0', END)
    result_box_name.delete('1.0', END)
    result_box_address.delete('1.0', END)
    result_box_city.delete('1.0', END)
    result_box_state.delete('1.0', END)
    result_box_zip.delete('1.0', END)
    result_box_country.delete('1.0', END)

def search_callsign_avl():
    clear_result_box()
    CALLSIGN = callsign_text_var.get().strip()
    resp_JSON = new_api_call(CALLSIGN)

    try:
        if len(resp_JSON) == 0:
            messagebox.showinfo("INFO","Callsign Not Available")

        status          = resp_JSON['status']
        privileges      = resp_JSON['class']
        expires         = resp_JSON['expires']
        name            = resp_JSON['name']
        address         = resp_JSON['addr1']
        city            = resp_JSON['addr2']
        state           = resp_JSON['state']
        zip             = resp_JSON['zip']
        country         = resp_JSON['country']
                    
        result_box_status.insert(END, f"{status:^6s}")
        result_box_status.insert(END,"\n")
        result_box_privileges.insert(END, f"{privileges:<8s}")
        result_box_privileges.insert(END,"\n")
        result_box_expires.insert(END, f"{expires:<8s}")
        result_box_expires.insert(END,"\n")
        result_box_name.insert(END, f"{name:<8s}")
        result_box_name.insert(END,"\n")
        result_box_address.insert(END, f"{address:<8s}")
        result_box_address.insert(END,"\n")
        result_box_city.insert(END, f"{city:<8s}")
        result_box_city.insert(END,"\n")
        result_box_state.insert(END, f"{state:<8s}")
        result_box_state.insert(END,"\n")
        result_box_zip.insert(END, f"{zip:<8s}")
        result_box_zip.insert(END,"\n")
        result_box_country.insert(END, f"{country:<8s}")
        result_box_country.insert(END,"\n")
            
    except KeyError as KE:
        messagebox.showerror("ERROR","No Available Info for Callsign")
        print (callsign_text_var.get())

# Buttons
search_repeater_image = PhotoImage(file= "Images_Icons\search-icon.png")
search_repeater_btn = Button(app, image=search_repeater_image, bg= top_right_frame_bg, command = search_callsign_avl, relief= RAISED)
search_repeater_btn.place(x = 600,y = 25)

update_clock()

app.mainloop()