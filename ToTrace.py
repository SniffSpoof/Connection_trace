from tkinter import *
from tkinter import scrolledtext 
from tkinter import Tk, BOTH, Menu
from tkinter.ttk import Frame, Button, Style
from tkinter import messagebox as mbox
import matplotlib.pyplot as plt
import subprocess
import networkx as nx
import matplotlib.pyplot as plt
from tkinter import messagebox

def trace(host):
	def add_edge(f_item, s_item, graph=None):
		graph.add_edge(f_item, s_item)

	command = "tracert "+host
	try:
		res = subprocess.check_output(command)
	except:
		return res.decode("CP866")

	ou = res.decode("CP866")
	to_out = ou
	
	ou = ou.split("\r\n")
	ou = ou[3:-2]
	b = []
	for i in ou:
		if("Превышен" not in i):
			b.append(i.split("	"))
	b = b[1:-1]

	graph = nx.Graph()
	point = []
	j = 0

	for i in b:
		j+=1
		v = i[0]
		v = v.split("  ")
		point.append(v[-1])
		graph.add_node(v[-1])
	
	for i in range(0, j-1):
		add_edge(point[i], point[i+1], graph=graph)

	nx.draw(graph,
			node_color='red',
			node_size=1000,
			with_labels=True)

	return to_out
	
class App(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent
		self.centerWindow()
		self.initUI()
 
	def initUI(self):
		window = self.parent
		window.title("_ToTrace_")
		self.lbl = Label(window, text="Enter Host:")
		self.lbl.grid(column=0, row=0)
		self.txt = Entry(window,width=50)
		self.txt.grid(column=0, row=1)
		self.btn = Button(window, text="Trace", command=self.clicked)
		self.btn.grid(column=1, row=1)
		self.tex = scrolledtext.ScrolledText(window, width=65, height=33)  
		self.tex.grid(column=0, row=2)
		
		menubar = Menu(self.master)
		self.master.config(menu=menubar)
 
		fileMenu = Menu(menubar)
		fileMenu.add_command(label="Exit", command=self.onExit)
		menubar.add_cascade(label="Menu", menu=fileMenu)
 
	def onExit(self):
		self.quit()
		
	def clicked(self):
		self.tex.insert(INSERT, ' ')
		c = self.txt.get()
		result = trace(c)
		self.tex.insert(INSERT, result)
		plt.show()
		
	def centerWindow(self):
		w = 620
		h = 600
		sw = self.parent.winfo_screenwidth()
		sh = self.parent.winfo_screenheight()
		x = (sw - w) / 2
		y = (sh - h) / 2
		self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))
 
def main():
	root = Tk()
	App(root)
	root.mainloop()

if __name__ == '__main__':
	main()