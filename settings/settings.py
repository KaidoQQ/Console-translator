import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod

class MainSettings():
  def __init__(self,x,y,name):
    self.root = tk.Tk()
    try:
      if isinstance(x,int) and isinstance(y,int):
        self.root.geometry(f"{x}x{y}")
      else:
        print("=== x and y must be int! ===")
        raise Exception
      self.root.title(f"{name}")

      self.progress = ttk.Progressbar(self.root, mode="indeterminate", length=300)
      self.progress.pack(pady=10)
      self.progress.pack_forget()

      self.main_frame = tk.Frame(self.root)
      self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


    except Exception as e:
      print(f"❌ [ERROR]  ON CREATION {e}")


  def start(self):
    print("❇️ APP STARTED ❇️")
    self.root.mainloop()

menu = MainSettings(689,425,"Jopa")
menu.start()