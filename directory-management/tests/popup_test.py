# from tkinter import *
# import sys
#
# class popupWindow(object):
#     def __init__(self,master):
#         top=self.top=Toplevel(master)
#         self.l=Label(top,text="Hello World")
#         self.l.pack()
#         self.e=Entry(top)
#         self.e.pack()
#         self.b=Button(top,text='Ok',command=self.cleanup)
#         self.b.pack()
#     def cleanup(self):
#         self.value=self.e.get()
#         self.top.destroy()
#
# class mainWindow(object):
#     def __init__(self,master):
#         self.master=master
#         self.b=Button(master,text="click me!",command=self.popup)
#         self.b.pack()
#         self.b2=Button(master,text="print value",command=lambda: sys.stdout.write(self.entryValue()+'\n'))
#         self.b2.pack()
#
#     def popup(self):
#         self.w=popupWindow(self.master)
#         self.b["state"] = "disabled"
#         self.master.wait_window(self.w.top)
#         self.b["state"] = "normal"
#
#     def entryValue(self):
#         return self.w.value
#
#
# if __name__ == "__main__":
#     root=Tk()
#     m=mainWindow(root)
#     root.mainloop()

import tkinter as tk
from tkinter import simpledialog
#
# ROOT = tk.Tk()
#
# ROOT.withdraw()
# # the input dialog
# USER_INP = simpledialog.askstring(title="Test",
#                                   prompt="What's your Name?:")
#
# # check it out
# print("Hello", USER_INP)
import shutil
# import os
# p = r"C:\Users\pradeep\AppData\Local\Temp\pradeep\test2\test5"
# # os.rename(p,os.path.join(os.path.dirname(p),"pqr1") )
# print(os.path.basename(p))
# simpledialog.Radiobutton()
#
# import tkinter as tk
#
# root = tk.Tk()
#
# v = tk.IntVar()
# v.set(1)  # initializing the choice, i.e. Python
#
# languages = [("Python", 101),
#    	     ("Perl", 102),
#     	     ("Java", 103),
#              ("C++", 104),
#              ("C", 105)]
#
# def ShowChoice():
#     print(v.get())
#
# tk.Label(root,
#          text="""Choose your favourite
# programming language:""",
#          justify = tk.LEFT,
#          padx = 20).pack()
#
# for language, val in languages:
#     simpledialog.Radiobutton(root,
#                    text=language,
#                    padx = 20,
#                    variable=v,
#                    command=ShowChoice,
#                    value=val).pack(anchor=tk.W)
#
#
# root.mainloop()
import os
p = r"C:\Users\pradeep\AppData\Local\Temp\pradeep\test2\test5"
print(os.path.basename(p))
# l = ["abc", "xyz", "pqr"]
# import os
# np= os.path.join(p, *l)
# os.makedirs(np, exist_ok=True)
#
# shutil.move(r"C:\Users\pradeep\AppData\Local\Temp\pradeep\test2\test5\abc\xyz\pqr", r"C:\Users\pradeep\AppData\Local\Temp\pradeep\test2\test5\abc")

# x = {"test1": "peep1", "test2":"peep2"}
# del x["test1"]
# print(x)
x = "pradeep_local"
print(x[:-6])