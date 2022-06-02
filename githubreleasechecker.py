from tkinter import *
from tkinter import ttk
import requests
from bs4 import BeautifulSoup


window = Tk()
window.geometry("650x300")
window.resizable(False, False)
window.title("Github Release Checker")

notebook = ttk.Notebook(window)

onetimechecktab = Frame(notebook)
intervalchecktab = Frame(notebook)
settingstab = Frame(notebook)

notebook.add(onetimechecktab, text="One-time Check")
notebook.add(intervalchecktab, text="Interval Check")
notebook.add(settingstab, text="Settings")
notebook.grid()

awaitlink = Label(onetimechecktab, text='Type the link of the github project here.', font=("Segoe UI Light", 12))
awaitlink.grid(row=0, column=0)
url_entry = Entry(onetimechecktab, width=40)
url_entry.grid(row=1, column=0)
outputlabel = Label(onetimechecktab)
outputlabel.grid(row=4, column=0)

howitworkstext = Label(onetimechecktab, font=("Segoe UI", 11), text='''
How it works:
After you've entered the supposed string in the entry box, there will be a check if that string
resembles an URL. If it isn't one, then an error regarding the absence of a proper URL. Else, the 
defined function in the script will check if Github is part of the domain, If it isn't, then that
error will instead indicate that the URL is there, except it's not Github. Though if the first two
conditions mentioned are met, it'll check if the URL leads to a repository specifically. If so, the     
release name and date will be output under the button highlighted on the screen.''')
howitworkstext.grid(row=5, column=0)


def relcheck():
    url = str(url_entry.get())
    try:
        urlcheck1 = url.split('://')[1]
        urlcheck2 = urlcheck1.split('/')[0]
    except IndexError:
        Label(onetimechecktab, text="  You haven't entered a URL with HTTP/HTTPS protocols yet.", font=("Segoe UI Light", 10)).grid(row=4, column=0)
    else:
        if urlcheck2 != 'github.com':
            Label(onetimechecktab, text="You've entered an URL other than Github.", font=("Segoe UI Light", 10)).grid(row=4, column=0)
        else:
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            try:
                spanv = soup.find('span', class_="css-truncate css-truncate-target text-bold mr-2").text
                date = soup.find('div', class_="text-small color-fg-muted").text
                Label(onetimechecktab, text=f'{spanv}, released on {date}', font=("Segoe UI Light", 10, "bold")).grid(row=4, column=0)
            except AttributeError:
                Label(onetimechecktab, text="You're on Github, but not on the page of a project.", font=("Segoe UI Light", 10)).grid(row=4, column=0)


onetimecheckbutton = Button(onetimechecktab, text='Check the latest release', font=("Segoe UI Light", 12), command=relcheck)
onetimecheckbutton.grid(row=2, column=0)

window.mainloop()
