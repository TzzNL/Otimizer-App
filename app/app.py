import os
import tkinter as tk
import customtkinter as ctk
from PIL import Image
from tkinter import filedialog
import shutil
import psutil
import time
import threading


path = "./common/user_info.txt" ## user info path 
theme = "./defaul_theme.json" ## default theme modified by h0l7
newuser = "./common/new_user.png" ## new user icon



ctk.set_default_color_theme(theme)

def app():
    main_menu()

def main_menu():
    
    main = ctk.CTk()

    main.geometry("800x500")
    main.title("Tzz App")

    batterry_lbl = ctk.CTkLabel(main,text="",font=("Helvetica", 13))
    batterry_lbl.place(x=560,y=10)

    def updated_battery():
        battery = psutil.sensors_battery()
        percent = battery.percent
        percent_formated = percent,"%"
        batterry_lbl.configure(text=percent_formated)
        main.after(1000,updated_battery)

    def update_time():
        current_time = time.strftime('%H:%M')
        hour_lbl.configure(text=current_time)
        main.after(1000, update_time)  # Update every 1 second
    
    hour_lbl = ctk.CTkLabel(main, text="", font=("Helvetica", 13))
    hour_lbl.place(x=500,y=10)

    with open(path,"r") as file:
       username = file.read()

    user_foto = ctk.CTkImage(Image.open("./common/default.png"),size=(25,25),)
    user_fotolbl = ctk.CTkLabel(main,image=user_foto,width=30,text="")
    user_fotolbl.place(x = 620, y = 10)

    user_namelbl = ctk.CTkLabel(main,text=username,font=("Helvetica", 13))
    user_namelbl.place(x=670, y = 10 )

    imagecfg = ctk.CTkImage(Image.open("./common/config.png",), size=(20,20))

    def update_progress(): ## UPDATING PROGRESS BAR 1 SEC DELAY
        memory_usage = psutil.virtual_memory().percent
        memory_usage_formated= memory_usage,"%"
        memory_progress = memory_usage / 100.0
        memory_canvas.itemconfig(progress_arc_memory, extent=-360 * memory_progress)
        usage_mem.configure(text=memory_usage_formated)

        cpu_usage = psutil.cpu_percent()
        cpu_usage_formated = cpu_usage,"%"
        cpu_progress = cpu_usage / 100.0
        cpu_canvas.itemconfig(progress_arc_cpu, extent=-360 * cpu_progress)
        usage_cpu.configure(text=cpu_usage_formated)

        main.after(1000, update_progress)

    def monitor_resource_usage():
        update_thread = threading.Thread(target=update_progress)
        update_thread.daemon = True
        update_thread.start()


    ## MEMORY MONITOR CANVAS
    memory_canvas = ctk.CTkCanvas(main,width=200,height=250,bg="#1a1a1a")
    memory_canvas.place(x = 30, y = 80)

    ## CPU MONITOR CANVAS
    cpu_canvas = ctk.CTkCanvas(main,width=200,height=250,bg="#1a1a1a")
    cpu_canvas.place(x = 260, y = 80)

    progress_arc_memory = memory_canvas.create_arc( ## CREATING A CONFERENCE CANVAS FOR MEMORY
    50, 50, 150, 150,
    style=tk.ARC,
    start=90,
    outline="#5913c2",
    width=3
    )

    progress_arc_cpu = cpu_canvas.create_arc( ## CREATING A CONFERENCE CANVAS FOR CPU
    50, 50, 150, 150,
    style=tk.ARC,
    start=90,
    outline="#5913c2",
    width=3
    )

    cpu_lbl = ctk.CTkLabel(cpu_canvas,text="CPU Usage",font=("Arial Bold",14))
    cpu_lbl.place(x=15,y=5)

    memory_lbl = ctk.CTkLabel(memory_canvas,text="Memory Usage",font=("Arial Bold",14))
    memory_lbl.place(x=15,y=5)


    usage_cpu = ctk.CTkLabel(cpu_canvas,text="",font=("Arial Bold",14))
    usage_cpu.place(x=83,y=87)

    
    usage_mem = ctk.CTkLabel(memory_canvas,text="",font=("Arial Bold",14))
    usage_mem.place(x=83,y=87)

    monitor_resource_usage() ## STARTING MONITOR CPU AND MEMORY USAGE FROM THE DEVICE
    update_time() ## START MONITORING REAL TIME IN THE DEVICE
    updated_battery() ## START MONITORING THE BATTERY FROM THE DEVICE
    main.mainloop()

def acc_menu(): ## Logged account menus code
    janela = ctk.CTk()
    janela.title("Account Menu")

    janela.geometry("700x400")
    janela.maxsize(width=700,height=400)
    janela.minsize(width=700,height=400)

    lg_accounts = ctk.CTkLabel(janela,text="Switch Account", font=("Arial Bold", 20))
    lg_accounts.place(x = 350, y = 50, anchor = tk.CENTER)

    usernew = ctk.CTkImage(Image.open(newuser), size=(80,80)) ## open new user icon
    new_user = ctk.CTkButton(janela,image=usernew,width=80,height=80,text="",fg_color="gray10",hover_color="gray11")
    new_user.place(x = 360, y = 145)


    new_userlbl = ctk.CTkLabel(janela,text="",text_color="white",font=("Arial Bold", 14),)
    new_userlbl.place(x = 360, y = 240)

    def on_enter(event):
        event.widget.config(width = 70, height = 70)
        new_userlbl.configure(text="Add account")
    def on_leave(event):
        event.widget.config(width=80,height=80)
        new_userlbl.configure(text="")

    new_user.bind("<Enter>",on_enter)
    new_user.bind("<Leave>", on_leave)

    def destroy():
        janela.withdraw()
        janela.destroy()
        app()

    if os.path.exists(path):
        photo = ctk.CTkImage(Image.open("./common/default.png"),size=(80,80))
        user_saved = ctk.CTkButton(janela,image=photo,text="",width=80,height=80,fg_color="gray10",hover_color="gray11",command=destroy)
        user_saved.place(x =250, y = 145)

        with open(path, "r") as file:
            username = file.read()

        userlbl = ctk.CTkLabel(janela,text="",font=("Arial Bold",14))
        userlbl.place(x=280, y= 230)

        def enter(event):
            event.widget.config(width = 70, height = 70)
            userlbl.configure(text=username)
        def leave(event):
            event.widget.config(width=80,height=80)
            userlbl.configure(text="")

        user_saved.bind("<Enter>",enter)
        user_saved.bind("<Leave>", leave)

    janela.mainloop()

if os.path.exists(path):
    acc_menu()
else:
    def login_account():
        root = ctk.CTk()
        root.title("Login")


        root.geometry("700x400")
        root.minsize(height=400,width=700)
        root.maxsize(height=400,width=700)
        
        fonte = ctk.CTkFont("Windows")

        username_label = ctk.CTkLabel(root,text="SIGN IN WITH ACCOUNT NAME",text_color="#0576f7")
        username_label.place(x = 20, y = 95)

        username_entry = ctk.CTkEntry(root,width=260,height=30)
        username_entry.place(x = 20, y = 120)

        password_label = ctk.CTkLabel(root,text="PASSWORD",text_color="#c0c1c2")
        password_label.place(x = 20, y = 165)

        password_entry = ctk.CTkEntry(root,width=260,height=30,show="*")
        password_entry.place(x = 20, y = 190)

        def login():
            var = remember.get()
            if var == 1: ## verify checkbox is marked or not if is save User infos 
                username = username_entry.get()
                with open(path, "w") as file:
                    file.write(username)
                    print("User Info saved")
                    root.withdraw()
                    root.destroy()
                    acc_menu()
            else:
                print("user not saved")

        remember = ctk.CTkCheckBox(root,width=30,corner_radius=1,text="Remember me",text_color="#c0c1c2")
        remember.place(x = 20, y = 240)

        login_btn = ctk.CTkButton(root,width=160,height=30,text="Sign in",cursor="hand2",command=login)
        login_btn.place(x = 60, y = 300)

        user_avatarlbl = ctk.CTkLabel(root,text="User avatar", font=("Arial Bold",14))
        user_avatarlbl.place(x=500,y= 95)

        userdefault = ctk.CTkImage(Image.open("./common/default.png"), size=(80,80))

        user_default_img = ctk.CTkLabel(root,image=userdefault,text="")
        user_default_img.place(x = 500, y =125)

    

        def open_file():
            file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")])
            if file_path:
                copy_and_display_image(file_path)

        def copy_and_display_image(source_path):
            destination_folder = "./common"  # Replace with the actual destination folder path
            new_filename = "default.png"  # Replace with the desired new filename
            destination_path = os.path.join(destination_folder, new_filename)
            
            shutil.copyfile(source_path, destination_path)  # Use shutil.copyfile instead of shutil.copy
            load_and_display_image(destination_path)
 
        def load_and_display_image(image_path):
            image = ctk.CTkImage(Image.open(image_path),size=(80,80))
            user_default_img.configure(image=image)
    

        upload_photo = ctk.CTkButton(root,width=80,height=30,text="upload",command = open_file)
        upload_photo.place(x = 500, y = 210)

        root.mainloop()

    login_account()
