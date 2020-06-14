import requests
import bs4
import tkinter as tk
from PIL import ImageTk, Image
import time
import plyer
import threading

def get_html_data(url):
    data = requests.get(url)
    return data


def get_corona_detail():
    url = "https://www.mohfw.gov.in/"
    html_data = get_html_data(url)
    bs = bs4.BeautifulSoup(html_data.text, "html.parser")
    # print(bs)
    li = ('blue', 'green', 'red', 'orange')
    l = ("Active Cases", "Cured / Discharged", "Deaths", "Migrated")
    alldetails = ""
    for i in range(0, 4):
        info = bs.find("div", class_='site-stats-count').find_all("li", class_="bg-" + str(li[i]))  # gives all 4
        for j in info:
            data = j.find("strong").get_text()
            alldetails += l[i] + " : " + data + '\n'
    return alldetails


if __name__ == '__main__':
    get_corona_detail()

#notification
def notify_user():
    plyer.notification.notify(
    title="Covid-19 Update",
    message=get_corona_detail(),timeout=10)
    time.sleep(20)

# refresh button function
def refresh():
    new_data = get_corona_detail()
    print("refreshing....")
    main_label["text"] = new_data


# creating a gui
root = tk.Tk()
root.geometry("550x500")
root.iconbitmap("corona.png")
root.title("Covid 19 Live Data Tracker app for India")
root.configure(bg="olive drab")
f = ("franklin gothic heavy", 25, "bold")
# file=open("c.png")
banner = ImageTk.PhotoImage(Image.open("corona.png"))
banner_label = tk.Label(root, image=banner, bg="white", relief="solid")
banner_label.pack()
main_label = tk.Label(root, text=get_corona_detail(), font=f, bg="white", padx=20, relief="solid")
main_label.pack()
# refresh button
btn = tk.Button(root, text="REFRESH", font=f, command=refresh)
btn.pack()
t1=threading.Thread(target=notify_user)
t1.setDaemon(True)
t1.start()
root.mainloop()

