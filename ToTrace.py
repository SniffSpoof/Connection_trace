# -----------------------------------------------------------
# Open Source information gathering of host project
#
# (C) 2022 Fedor Alekseev, Novosibirsk, Russia
# Released under GNU Public License (GPL)
# email fedor.alekseev13@yandex.ru
# -----------------------------------------------------------


from tkinter import Tk, INSERT
from tkinter import scrolledtext 
from tkinter import Tk, BOTH, Menu, Label, Entry
from tkinter.ttk import Frame, Button, Style
from tkinter import messagebox as mbox

import matplotlib.pyplot as plt
import networkx as nx

import subprocess


class Tools():

	"""
	Singleton class that defines methods for working with the network, 
	and methods for presenting information in a graphical interface
	"""
	
	def ping(self, host) -> "CriticalPingError":
	
		"""
		The ping method uses the standard ping command to get 
		the following information: connection success, connection time
		"""
	
		command = "ping "+host
		try:
			res = subprocess.check_output(command)
		except:
			return res.decode("CP866")

		output_result = res.decode("CP866") #Windows decoding
		return output_result


	def trace(self, host) -> "CriticalTraceError":
	
		"""
		The trace method uses the standard tracert command to get 
		the following information: connection success, connection time, 
		IP address of intermediate host
		"""
	
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
			if("Превышен" not in i):	#Doesnt include failed connections
				temp.append(i.split("	"))
		temp = temp[1:-1]

		graph = nx.Graph() #NetworkX object
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
	

class App(Frame):

	"""
	Application class. It implements all logic of the graphical interface
	and the connection with the methods of Tools class
	"""

	def __init__(self, parent, tools):
		Frame.__init__(self, parent)
		self.parent = parent
		self.__СenterWindow()
		self.__initUI()
		self.tools = tools
 
	def __initUI(self):
		window = self.parent
		window.title("_ToTrace_")
		
		self.lbl = Label(window, text="Enter Host:")
		self.lbl.grid(column=0, row=0)
		
		self.txt = Entry(window,width=50)
		self.txt.grid(column=0, row=1)
		
		self.btn_trace = Button(window, text="Trace", command=self._Tracing)
		self.btn_trace.grid(column=1, row=1)
		
		self.btn_ping = Button(window, text="Ping", command=self._Pinging)
		self.btn_ping.grid(column=1, row=0)
		
		self.scrtxt = scrolledtext.ScrolledText(window, width=65, height=33)  
		self.scrtxt.grid(column=0, row=2)
		
		menubar = Menu(self.master)
		self.master.config(menu=menubar)
		fileMenu = Menu(menubar)
		fileMenu.add_command(label="Exit", command=self.__Exit)
		menubar.add_cascade(label="Menu", menu=fileMenu)
 
	def __Exit(self):
		self.quit()
		
	def __Tool_Wrapper(self, f):
		def Wrapped():
			self.scrtxt.insert(INSERT, '\n')
			text_from_txt = self.txt.get()
			result = f(text_from_txt)
			self.scrtxt.insert(INSERT, result)
		return Wrapped
	
	def _Tracing(self):
		c = self.__Tool_Wrapper(self.tools.trace)
		c()
		plt.show()
		
	def _Pinging(self):
		c = self.__Tool_Wrapper(self.tools.ping)
		c()
		
	def __СenterWindow(self):
	#Centering app window on screen, using info of you screen
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
