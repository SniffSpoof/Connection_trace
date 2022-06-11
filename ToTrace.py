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

#Singleton - include ping, trace methods
class Tools():
	def ping(self, host) -> "PingError":
	
		command = "ping "+host
		try:
			res = subprocess.check_output(command)
		except:
			return res.decode("CP866")

		output_result = res.decode("CP866") #Windows decoding
		return output_result

	def trace(self, host) -> "TraceError":
		#connecting points in graph
		def add_edge(f_item, s_item, graph=None):
			graph.add_edge(f_item, s_item)

		command = "tracert "+host
		try:
			res = subprocess.check_output(command)
		except:
			return res.decode("CP866")

		output_result = res.decode("CP866")
		returnable_text = output_result
		output_result = output_result.split("\r\n")
		output_result = output_result[3:-2]
		
		temp = []
		for i in output_result:
			if("Превышен" not in i):	#doesnt include failed connections
				temp.append(i.split("	"))
		temp = temp[1:-1]

		graph = nx.Graph()
		points = []
		
		j = 0
		for i in temp:
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

		return returnable_text
	
#UI Class with logic
class App(Frame):
	def __init__(self, parent, tools):
		Frame.__init__(self, parent)
		self.parent = parent
		self.СenterWindow()
		self.initUI()
		self.tools = tools
 
	def initUI(self):
		window = self.parent
		window.title("_ToTrace_")
		
		self.lbl = Label(window, text="Enter Host:")
		self.lbl.grid(column=0, row=0)
		
		self.txt = Entry(window,width=50)
		self.txt.grid(column=0, row=1)
		
		self.btn_trace = Button(window, text="Trace", command=self.Tracing)
		self.btn_trace.grid(column=1, row=1)
		
		self.btn_ping = Button(window, text="Ping", command=self.Pinging)
		self.btn_ping.grid(column=1, row=0)
		
		self.scrtxt = scrolledtext.ScrolledText(window, width=65, height=33)  
		self.scrtxt.grid(column=0, row=2)
		
		menubar = Menu(self.master)
		self.master.config(menu=menubar)
		fileMenu = Menu(menubar)
		fileMenu.add_command(label="Exit", command=self.Exit)
		menubar.add_cascade(label="Menu", menu=fileMenu)
 
	def Exit(self):
		self.quit()
		
	def Tracing(self):
		self.scrtxt.insert(INSERT, '\n')
		text_from_txt = self.txt.get()
		
		result = self.tools.trace(text_from_txt)
		self.scrtxt.insert(INSERT, result)
		plt.show()
		
	def Pinging(self):
		self.scrtxt.insert(INSERT, '\n')
		text_from_txt = self.txt.get()
		
		result = self.tools.ping(text_from_txt)
		self.scrtxt.insert(INSERT, result)
		
	def СenterWindow(self):
		w = 620
		h = 600
		sw = self.parent.winfo_screenwidth()
		sh = self.parent.winfo_screenheight()
		x = (sw - w) / 2
		y = (sh - h) / 2
		self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))
 
def main():
	root = Tk()
	Tool_set = Tools()
	App(root, Tool_set)
	root.mainloop()

if __name__ == '__main__':
	main()
