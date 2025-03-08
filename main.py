import os
import customtkinter as ctk
from json import load,dump


base_Dirs = ["C://Program Files/EA Games/", "C://Program Files/Epic Games/","C://Program Files (x86)/Steam/steamapps/common/","C://Program Files (x86)/Ubisoft/Ubisoft Game Launcher/games"]

def ui():
   ux = ctk.CTk()
   
   ux.title("One Game Launcher")
   ux.geometry("1200x800")
   title = ctk.CTkLabel(ux,text="One Game Launcher",anchor="center",text_color="white",font=("Arial",50, "bold"))
   title.pack(pady=10)

   scrlframe = ctk.CTkScrollableFrame(ux,height=700,width=1100)
   scrlframe.pack(pady=30)

   with open("savedDir.json", "r") as file:
      ea = load(file)
   
   def make_buttons():
      columns = 5
      row = 0
      col = 0  
      for name, dir in ea.items():
         icon_path = f"icons/{name}.png"

         def on_enter(event):
           if event.widget.winfo_height() == 200:
              event.widget.configure(width=200, height=270)  

         def on_leave(event):
           if event.widget.winfo_height() == 270:
              event.widget.configure(width=200, height=250)
         button = ctk.CTkButton(scrlframe,text=name,text_color="white",command=lambda d=dir: os.startfile(d),width=200,height=250,fg_color="#444444",hover_color="#d6d3d2")
         button.bind("<Enter>", on_enter)
         button.bind("<Leave>", on_leave)
         button.grid(row=row,column = col,padx = 10,pady = 10)
         col += 1
         if col >= columns:
            col = 0
            row += 1

   make_buttons()
   ux.mainloop()

def setup():
   with open("savedDir.json","w") as file:
      x = scan()
      y = special_scan(x)
      dump(y,file)
      
def scan():
    dirs = {}
    for dir in base_Dirs:
       if os.path.exists(dir):
           for content in os.scandir(dir):
            if content.is_dir():
                for contentx in os.scandir(os.path.join(dir,content.name)):
                    if contentx.name.endswith(".exe") and contentx.name not in ("EAAntiCheat.GameServiceLauncher.exe", "UnityCrashHandler64.exe", "dowser.exe") and "trial" not in contentx.name.lower():
                        dirs[content.name] = contentx.path
                    else:
                        continue
            else:
                continue
       else:
         continue
    return dirs
       
def special_scan(table):
   dir = "C://Users"
   users = []
   for user in os.scandir(dir):
      if user.name not in ("Default", "Public") and user.is_dir():
        users.append(user.name)

   for user in users:
       dir = f"C://Users/{user}/AppData/Local/Roblox/Versions"
       if os.path.exists(dir):
          for fold in os.scandir(dir):
             if fold.is_dir() and len(os.listdir(fold)) > 0:
                for file in os.scandir(fold):
                   if file.name.endswith(".exe") and file.name not in ("RobloxStudioInstaller.exe","RobloxCrashHandler.exe","RobloxPlayerInstaller.exe","RobloxPlayerLauncher.exe","RobloxStudioLauncherBeta.exe"):
                      table[f"Roblox For {user}"] = file.path
                   else:
                      continue 
             else:
                continue
       else:
          continue
   return table


if __name__ == "__main__":
   setup()
   ui()
