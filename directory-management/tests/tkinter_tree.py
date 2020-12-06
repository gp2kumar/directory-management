import os
import tkinter as tk
import tkinter.ttk as ttk


class App(object):
    def __init__(self, master, path):
        self.nodes = dict()
        frame = tk.Frame(master)
        btn = tk.Button(master, text="get path", width=12, height=3, font='Helvetica 11 bold', command=self.get_path)
        btn.place(x=100,y=100)
        self.tree = ttk.Treeview(frame)
        ysb = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
        xsb = ttk.Scrollbar(frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.tree.heading('#0', text='Project tree', anchor='w')

        self.tree.grid()
        ysb.grid(row=0, column=1, sticky='ns')
        xsb.grid(row=1, column=0, sticky='ew')
        frame.grid()

        abspath = os.path.abspath(path)
        self.insert_node('', abspath, abspath)
        self.tree.bind('<<TreeviewOpen>>', self.open_node)

    def insert_node(self, parent, text, abspath):
        node = self.tree.insert(parent, 'end', text=text, open=False)
        if os.path.isdir(abspath):
            self.nodes[node] = abspath
            self.tree.insert(node, 'end')

    def open_node(self, event):
        print ("tree opened")
        node = self.tree.focus()
        abspath = self.nodes.pop(node, None)
        if abspath:
            self.tree.delete(self.tree.get_children(node))
            for p in os.listdir(abspath):
                self.insert_node(node, p, os.path.join(abspath, p))

    def get_path(self):
        curItem = self.tree.focus()
        # print (self.tree.item(curItem))
        # print(self.tree.selection())
        print (self.tree.item(curItem))
        print(self.tree.item(self.tree.parent(curItem)))


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root, path=r'C:\Users\pradeep\PycharmProjects\directory-management')
    root.mainloop()