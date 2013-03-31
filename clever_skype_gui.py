
"""
Connects Skype to cleverbot

Note:
	You'll need to download and install the following before this will run.

	cleverbot:
	: http://code.google.com/p/pycleverbot/ 

	Skype4Py:
	: http://sourceforge.net/projects/skype4py/

	WxPython
	: http://www.wxpython.org/ 

	Alternatively, you could just run the .exe if you're on windows. 

"""



import wx
import Skype4Py
import cleverbot
import sys
import os
import webbrowser
import threading
import Queue
import time
from botBuilder import *


class SuperFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, size=(320,390))
		self.SetTitle("Clever Skype - v.1.1")
		icoPath = resource_path('images\\icon.ico')
		ico = wx.Icon(icoPath, wx.BITMAP_TYPE_ICO)
		self.SetIcon(ico)

		self.running = False
		font = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'Verdana')
		self.initMenuBar()

		# This is serves as the message pump 
		# between all the threads. 
		self.msg_queue = Queue.Queue()

		panel = wx.Panel(self, -1)
		panel.SetBackgroundColour("white")

		# Used for keping the center column in tact
		main_hsizer = wx.BoxSizer(wx.HORIZONTAL)
		main_hsizer.AddStretchSpacer(1)

		# sizer that actually holds all the widgets
		vsizer = wx.BoxSizer(wx.VERTICAL)
		vsizer.AddSpacer(12)

		self.img = wx.Bitmap('images\\clever_skype_logo.png')
		self.logo = wx.StaticBitmap(panel, -1, self.img)
		vsizer.Add(self.logo, 0, wx.ALIGN_CENTER_HORIZONTAL)
		vsizer.AddSpacer(8)
		
		self.statusLabel = wx.StaticText(panel, label="Status")
		self.statusLabel.SetFont(font)
		vsizer.Add(self.statusLabel, 0, wx.ALIGN_LEFT | wx.LEFT, 1)
		vsizer.AddSpacer(5)
		

		self.statusBox = wx.TextCtrl(panel, -1, 
							"Click the Start button to begin.", 
							size=(240,100), 
							style=wx.TE_MULTILINE | wx.TE_READONLY)
		vsizer.Add(self.statusBox, 5, wx.CENTER | wx.EXPAND)
		vsizer.AddSpacer(15)
		
		btn_hsizer = wx.BoxSizer(wx.HORIZONTAL)
		self.startButton = wx.Button(panel, -1, " Start Clever Skype ")
		self.Bind(wx.EVT_BUTTON, self.onStartButtonDown, self.startButton)
		btn_hsizer.Add(self.startButton, 0, wx.ALIGN_LEFT)
		
		btn_hsizer.AddStretchSpacer(1)
		
		self.stopButton = wx.Button(panel, -1, " Stop Clever Skype ")
		self.Bind(wx.EVT_BUTTON, self.onStopButtonDown, self.stopButton)
		self.stopButton.Disable()
		btn_hsizer.Add(self.stopButton, 0, wx.ALIGN_RIGHT)

		vsizer.Add(btn_hsizer, 1, wx.EXPAND)

		main_hsizer.Add(vsizer, 0, wx.EXPAND)
		
		main_hsizer.AddStretchSpacer(1)

		panel.SetSizer(main_hsizer)
		# self.Centre()
		self.Show()

	def initMenuBar(self):
		menuBar = wx.MenuBar()
		fileMenu = wx.Menu()
		fOption = fileMenu.Append(wx.ID_CLOSE, "&Close")
		self.Bind(wx.EVT_MENU, self.OnClose, fOption)


		helpMenu = wx.Menu()
		hOption = helpMenu.Append(wx.ID_HELP_CONTEXT, "&Launch help page")
		self.Bind(wx.EVT_MENU, self.onLaunchHelp, hOption)

		helpMenu.AppendSeparator()

		aboutOption = helpMenu.Append(wx.ID_ABOUT, "&About")
		self.Bind(wx.EVT_MENU, self.onAbout, aboutOption)


		menuBar.Append(fileMenu, "&File")
		menuBar.Append(helpMenu, "&Help")

		self.SetMenuBar(menuBar)

	def OnClose(self, evt):
		self.Destroy()
		sys.exit()

	def onLaunchHelp(self, evt):
		wx.BeginBusyCursor() 
		self.launchBrowser()
  		wx.EndBusyCursor() 

	def launchBrowser(self):
		address = 'https://github.com/Audionautics/Clever-Skype'
		webbrowser.open(address, new=2) 
	
	def onAbout(self, e):
		description = "Just a silly little toy."
		
		info = wx.AboutDialogInfo()

		# info.SetIcon(wx.Icon('hunter.png', wx.BITMAP_TYPE_PNG))
		info.SetName('Clever Skype')
		info.SetVersion('1.1')
		info.SetDescription(description)
		# Need to update to github address
		info.SetWebSite('https://github.com/Audionautics/')
		wx.AboutBox(info)

	def stillRunning(self):
		return self.running


	# def spawn_bot(self, skype, user):
	# 	robot = SkypeBot(skype, user)
	# 	while True:
	# 		if not self.newMessageReceived(robot):
	# 			continue # Wait for user input

	# 		self.statusBox.AppendText('\nSkype message from: %s \n'
	# 				% robot.user.Handle)
	# 		self.statusBox.AppendText('    contents: "%s"\n\n' 
	# 				% str(robot.getCurrentMessageBody()))
			
	# 		robot.update()
	# 		robot.getCleverResponse()
	# 		self.statusBox.AppendText('Posting Clever bot\'s respoonse to %s.\n' % robot.user.Handle)
	# 		self.statusBox.AppendText('Msg: %s.\n' % robot.msg)

	# 		if not self.stillRunning():
	# 			break

	# 		time.sleep(.4) 	

	def getUsersOnline(self, skype, usersOnline):
		for i in skype.Friends:
			if (i.OnlineStatus == 'ONLINE' and 
								i.Handle not in usersOnline and 
								i.Handle != "echo123"):

				usersOnline.append(i)

	def onStartButtonDown(self, e):
		self.running = True
		self.statusBox.Clear()

		skype = Skype4Py.Skype()
		skype.Attach()

		usersOnline = []
		self.getUsersOnline(skype, usersOnline)

		

		statusUpdater = StatusUpdater(self.msg_queue, self.postMsg)
		statusUpdater.setDaemon(True)
		statusUpdater.start()

		self.bots = []
		for user in (usersOnline):
			print 'starting bot for user', user.Handle
			t = Bot(skype, user, self.msg_queue)
			t.setDaemon(True)
			t.start()
			self.bots.append(t)


		self.startButton.Disable()
		self.stopButton.Enable()

	def onStopButtonDown(self, e):
		self.statusBox.AppendText('\n\n\n\nDisconnecting CleverSkype.')
		self.running = False
		
		for bot in self.bots:
			bot._shutdown()

		for bot in self.bots:
			print bot.is_alive() 

		self.startButton.Enable()
		self.stopButton.Disable()
		self.statusBox.AppendText('\nDone.')

	def postMsg(self, msg):
		self.statusBox.AppendText(msg)


class StatusUpdater(threading.Thread):
	def __init__(self, queue, function):
		threading.Thread.__init__(self)
		self.queue = queue
		self.running = True
		self.postMsg = function

	def run(self):
		while self.running:
			msg = self.queue.get()
			self.postMsg(msg)
			

		self.postMsg('Shutting down CleverSkype.')

	def _shutdown(self):
		self.running = False

class Bot(threading.Thread):
	Shutdown_queue = None
	def __init__(self, skype, user, queue):
		threading.Thread.__init__(self)
		self.robot = SkypeBot(skype, user)
		self.queue = queue
		self.running = True


	def newMessageReceived(self):
		return (self.robot.currentMsgDatetime != None and 
				self.robot.currentMsgDatetime != 
				self.robot.getCurrentMessageDatetime())

	def run(self):
		while self.running:
			if not self.newMessageReceived():
				continue # Wait for user input

			self.queue.put('\nSkype message from: %s \n'
					% self.robot.user.Handle)
			self.queue.put('    contents: "%s"\n\n' 
					% str(self.robot.getCurrentMessageBody()))
			
			self.robot.update()
			
			self.robot.getCleverResponse()
			self.queue.put('Posting Clever bot\'s respoonse to %s.\n' 
					% self.robot.user.Handle)
			
			self.queue.put('Msg: %s.\n' % self.robot.msg)

			self.queue.task_done()

			time.sleep(.4) 	

	def _shutdown(self):
		self.running = False

def resource_path(relative):
    return os.path.join(
        os.environ.get(
            "_MEIPASS2",
            os.path.abspath(".")), relative)


def main():
	app = wx.App(False)
	frame = SuperFrame()
	app.MainLoop()


if __name__ == '__main__':
	main()

