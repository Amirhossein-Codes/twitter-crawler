import requests
import searchProgram
import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk


def btn_get_followings_callback():
    values = searchProgram.search_for_followings(entry_user.get().strip())
    combobox.configure(values=values)
    combobox.set(values[0])
    textbox.insert("1.0", f"----Followings search complete. {len(values)} followings found----\n\n")


def btn_get_tweets_callback():
    global imgs_list
    imgs_list = []
    tweet_content = searchProgram.get_tweets(combobox.get(), int(tweet_amount_slider.get()))
    for tweet in enumerate(tweet_content[0]):
        textbox.insert(ctk.END, tweet[1])
    for image in enumerate(tweet_content[1]):
        with open(f'imgs/{image[0]}.jpg', 'wb') as file:
            re = requests.get(image[1])
            file.write(re.content)
        imgs_list.append(ImageTk.PhotoImage(Image.open(f'imgs/{image[0]}.jpg')))
    for image in imgs_list:
        textbox.image_create(ctk.END, image=image)


ctk.set_appearance_mode('light')
root = ctk.CTk()
root.iconbitmap('logo/logo.ico')
root.title("Amirhossein: Twitter Crawler")
root.geometry("700x700+500+50")
root.minsize(500, 500)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=2)
root.grid_columnconfigure(1, weight=1)


scrollbar = tk.Scrollbar(root)
scrollbar.grid(row=0,column=2,sticky='ns', padx=0,pady=(15,5))

textbox = tk.Text(root, font=('arial', 22 ,'bold'), relief='solid',borderwidth=0, yscrollcommand=scrollbar.set, fg='#333333')
textbox.grid(row=0, column=0, columnspan=2,padx=(15,0), pady=(15, 5), sticky="nsew")
scrollbar.config(command=textbox.yview)


combobox = ctk.CTkComboBox(master=root, values=[""],font=('arial',16))
combobox.grid(row=1, column=0, padx=(10, 5), pady=10, sticky="nswe")

button_get = ctk.CTkButton(master=root, text=" Get tweets", font=('arial', 16, 'bold'), command=btn_get_tweets_callback, image=ctk.CTkImage(Image.open('logo/twitter.png').resize((64,64))))
button_get.grid(row=1, column=1, padx=(5, 10), pady=10, sticky="nswe",columnspan=2, ipady=2)

entry_user = ctk.CTkEntry(master=root, placeholder_text="Insert User ID To Get Followings...",font=('arial',16))
entry_user.grid(row=2, column=0, padx=(10, 5), pady=(0, 10), sticky="nswe")

button_search = ctk.CTkButton(master=root, text=" Get followings", command=btn_get_followings_callback, font=('arial', 16,'bold'),image=ctk.CTkImage(Image.open('logo/person.png').resize((64,64))))
button_search.grid(row=2, column=1, padx=(5, 10), pady=(0, 10), sticky="nswe",columnspan=2, ipady=2)

def update_count_lbl(*arg):
    count_lbl.configure(text=f'Use slider below to choose tweets amount to get: Current = {int(tweet_amount_slider.get())}')


tweet_amount_slider = ctk.CTkSlider(root, from_=1, to=50,number_of_steps=49, progress_color='#00acee', fg_color='white',border_width=2, command=update_count_lbl)
tweet_amount_slider.grid(row=4, column=0, sticky='ew',padx=(10,0), pady=10,columnspan=2)

count_lbl = ctk.CTkLabel(root, text=f'Use slider below to choose tweets amount to get: Current = {int(tweet_amount_slider.get())}', font=('arial', 16,'bold'), anchor='w')
count_lbl.grid(row=3, column=0, sticky='ew', padx=(10,0),columnspan=2)


root.mainloop()
