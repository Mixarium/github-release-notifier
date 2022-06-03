from tkinter import *
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import datetime

# some but not all defined functions for later


def curtime():
    return str(datetime.datetime.now()).split('.')[0]


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

# everything for the One-time Check tab
awaitlink = Label(onetimechecktab, text='Type the link of the github project here.', font=("Segoe UI Light", 12))
awaitlink.grid(row=0, column=0)
url_entry = Entry(onetimechecktab, width=40)
url_entry.grid(row=1, column=0)

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
        relabel1 = Label(onetimechecktab, text="  You haven't entered a URL with HTTP/HTTPS protocols yet.",
                         font=("Segoe UI Light", 10))
        relabel1.grid(row=4, column=0)
        relabel1.after(2000, lambda: relabel1.destroy())
    else:
        if urlcheck2 != 'github.com':
            relabel2 = Label(onetimechecktab, text="You've entered an URL other than Github.",
                             font=("Segoe UI Light", 10))
            relabel2.grid(row=4, column=0)
            relabel2.after(2000, lambda: relabel2.destroy())
        else:
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            try:
                spanv = soup.find('span', class_="css-truncate css-truncate-target text-bold mr-2").text
                date = soup.find('div', class_="text-small color-fg-muted").text
                relabel3 = Label(onetimechecktab, text=f'{spanv}, released on {date}',
                                 font=("Segoe UI Light", 11, "bold"))
                relabel3.grid(row=4, column=0)
                relabel3.after(4000, lambda: relabel3.destroy())
            except AttributeError:
                relabel4 = Label(onetimechecktab, text="You're on Github, but not on the page of a project.",
                                 font=("Segoe UI Light", 10))
                relabel4.grid(row=4, column=0)
                relabel4.after(2000, lambda: relabel4.destroy())


onetimecheckbutton = Button(onetimechecktab, text='Check the latest release', font=("Segoe UI Light", 12),
                            command=relcheck)
onetimecheckbutton.grid(row=2, column=0)

# everything for the Interval Check tab
awaitlink2 = Label(intervalchecktab, text='Type the Github repository URL in order to start the automatic check.',
                   font=("Segoe UI Light", 12))
awaitlink2.grid()
url_entry2 = Entry(intervalchecktab, width=40)
url_entry2.grid()

runningautocheck = True


def autocheck():
    global runningautocheck
    runningautocheck = True
    url = str(url_entry2.get())
    try:
        urlcheck1 = url.split('://')[1]
        urlcheck2 = urlcheck1.split('/')[0]
    except IndexError:
        rerelabel1 = Label(intervalchecktab, text="  You haven't entered a URL with HTTP/HTTPS protocols yet.",
                           font=("Segoe UI Light", 10))
        rerelabel1.grid(row=4, column=0)
        rerelabel1.after(2000, lambda: rerelabel1.destroy())
    else:
        if urlcheck2 != 'github.com':
            rerelabel2 = Label(intervalchecktab, text="You've entered an URL other than Github.",
                               font=("Segoe UI Light", 10))
            rerelabel2.grid(row=4, column=0)
            rerelabel2.after(2000, lambda: rerelabel2.destroy())
        else:
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            try:
                spanv = soup.find('span', class_="css-truncate css-truncate-target text-bold mr-2").text

                def mainautocheck():
                    if runningautocheck:
                        updatedspan = soup.find('span', class_="css-truncate css-truncate-target text-bold mr-2").text
                        if spanv != updatedspan:
                            rerelabel3 = Label(intervalchecktab,
                                               text=f'New release found at {curtime()} ({updatedspan})',
                                               font=("Segoe UI Light", 11, "bold"))
                            rerelabel3.grid(row=4, column=0)
                        else:
                            rerelabel3 = Label(intervalchecktab,
                                               text=f'''No new release detected at {curtime()}.
Current version: {spanv}''',
                                               font=("Segoe UI Light", 11, "bold"))
                            rerelabel3.grid(row=4, column=0)
                            rerelabel3.after(30000, lambda: mainautocheck())
                    else:
                        rerelabel5 = Label(intervalchecktab, text='Automatic check stopped',
                                           font=("Segoe UI Light", 11, "bold"))
                        rerelabel5.grid(row=4, column=0)
                        rerelabel5.after(2000, lambda: rerelabel5.destroy())

                mainautocheck()
            except AttributeError:
                rerelabel4 = Label(intervalchecktab, text="You're on Github, but not on the page of a project.",
                                   font=("Segoe UI Light", 10))
                rerelabel4.grid(row=5, column=0)
                rerelabel4.after(5000, lambda: rerelabel4.destroy())


def stopautocheck():
    global runningautocheck
    runningautocheck = False


intervalcheckbutton = Button(intervalchecktab, text='Check the latest release', font=("Segoe UI Light", 12),
                             command=autocheck)
intervalcheckbutton.grid()

stopintervcheckbutton = Button(intervalchecktab, text='Stop the automatic check', font=("Segoe UI Light", 12),
                               command=stopautocheck)
stopintervcheckbutton.grid(row=3, column=0)

window.mainloop()
