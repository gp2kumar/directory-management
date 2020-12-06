import os
import tkinter as tk
import tkinter.ttk as ttk


def open_node(event):
    global tree
    print(tree.focus())
    tree.delete(tree.get_children(tree.focus()))
    tree.insert(tree.focus(), 'end', text='pqr')

root = tk.Tk()
frame = tk.Frame(root)
frame.place(x=0,y=0)
tree = ttk.Treeview(frame)
tree.heading('#0', text='Directory Structure', anchor='w')
root_node = tree.insert('', 'end', text='abc', open=False)
print(type(root_node), root_node, tree.item(root_node))
l2=tree.insert(root_node, 'end', text='xyz')
l3=tree.insert(l2, 'end', text='xyz')
tree.bind('<<TreeviewOpen>>', open_node)
tree.place(x=0,y=0)



tree.pack()
root.mainloop()