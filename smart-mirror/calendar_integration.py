from tkinter import *

# Sample local events data
local_events = [
    "2025-01-03 10:00:00: Meeting with Team",
    "2025-01-03 12:00:00: Lunch with Client",
    "2025-01-03 15:00:00: Project Deadline"
]

def get_local_events():
    print("Fetching local events...")  # Debugging statement
    return local_events

def update_calendar():
    print("Updating calendar...")  # Debugging statement
    events = get_local_events()
    if not events:
        events_label.config(text='No upcoming events found.')
    else:
        events_text = "\n".join(events)
        events_label.config(text=events_text)
    root.after(60000, update_calendar)
    print("Calendar updated.")  # Debugging statement

root = Tk()
root.title('Smart Mirror - Local Calendar')

events_label = Label(root, font=('Helvetica', 15), justify=LEFT, wraplength=400)
events_label.pack(pady=20)

print("Starting application...")  # Debugging statement
update_calendar()
root.mainloop()
print("Application running.")  # Debugging statement
