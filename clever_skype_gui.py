import wx
import Skype4Py, cleverbot
import sys, os, webbrowser, threading
from botBuilder import *

"""
NOTE: 

You'll need to download and install the following before this will run.

cleverbot:
: http://code.google.com/p/pycleverbot/ 

Skype4Py:
: http://sourceforge.net/projects/skype4py/

WxPython
: http://www.wxpython.org/ 

Alternatively, you could just run the .exe if you're on windows. 

"""

class SuperFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, size=(320,390))
		self.SetTitle("Clever Skype - v.1")
		icoPath = resource_path('images\\icon.ico')
		ico = wx.Icon(icoPath, wx.BITMAP_TYPE_ICO)
		self.SetIcon(ico)

		self.running = False

		self.initMenuBar()

		panel = wx.Panel(self, -1)
		panel.SetBackgroundColour("white")

		vsizer = wx.BoxSizer(wx.VERTICAL)

		# vsizer.Add(panel,1,wx.EXPAND)

		imgPath = resource_path('images\\clever_skype_logo.png')
		self.img = wx.Bitmap(imgPath)
		self.control = wx.StaticBitmap(panel, -1, self.img)
		vsizer.Add((-1,10))
		vsizer.Add(self.control, 0, wx.CENTER)
		vsizer.Add((-1, 16))

		self.statusLabel = wx.StaticText(panel, label="Status")
		vsizer.Add(self.statusLabel, 0, wx.CENTER)
		vsizer.Add((-1, 4))

		self.statusBox = wx.TextCtrl(panel, -1, "Click the Start button to begin.", 
								size=(240,100), style=wx.TE_MULTILINE | wx.TE_READONLY)
		vsizer.Add(self.statusBox, 0, wx.CENTER)
		vsizer.Add((0,25))

		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		self.startButton = wx.Button(panel, -1, " Start Clever Skype ")
		self.Bind(wx.EVT_BUTTON, self.onStartButtonDown, self.startButton)
		hsizer.Add(self.startButton, 0, wx.CENTER)
		hsizer.Add((20,-1))

		
		self.stopButton = wx.Button(panel, -1, " Stop Clever Skype ")
		self.Bind(wx.EVT_BUTTON, self.onStopButtonDown, self.stopButton)
		self.stopButton.Disable()
		hsizer.Add(self.stopButton, 0, wx.CENTER)

		vsizer.Add(hsizer, 0, wx.CENTER)

		panel.SetSizer(vsizer)
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
		webbrowser.open('https://github.com/Audionautics/Clever-Skype', new=2) 
	
	def onAbout(self, e):
		description = "Just a silly little toy."
		
		info = wx.AboutDialogInfo()

		# info.SetIcon(wx.Icon('hunter.png', wx.BITMAP_TYPE_PNG))
		info.SetName('Clever Skype')
		info.SetVersion('1.0')
		info.SetDescription(description)
		# Need to update to github address
		info.SetWebSite('https://github.com/Audionautics/')
		wx.AboutBox(info)

	def stillRunning(self):
		return self.running

	def spawn_bot(self, skype, user):
		robot = SkypeBot(skype, user)
		while True:
			if (robot.currentMsgDatetime != None and robot.currentMsgDatetime != robot.getCurrentMessageDatetime()):
				print 'hello?'
				self.statusBox.AppendText('\nSkype message from: %s \n' % robot.user.Handle)
				self.statusBox.AppendText('    contents: "%s"\n\n' % str(robot.getCurrentMessageBody()))
				
				robot.update()
				robot.getCleverResponse()
				self.statusBox.AppendText('Posting Clever bot\'s respoonse to %s.\n' % robot.user.Handle)
				self.statusBox.AppendText('Msg: %s.\n' % robot.msg)
				# print 'getting CleverBot\'s response'
				# clever_response = cb.Ask(escape_chars(current_msg))
				# post_skype_msg(s, clever_response)
				# print 'posting message:', clever_response 

			if not self.stillRunning():
				break

	

	def checkUsersOnline(self, skype, onlineList):
		for i in skype.Friends:
			if i.OnlineStatus == 'ONLINE' and i.Handle not in onlineList and i.Handle != "echo123":
				onlineList.append(i.Handle)
				threading.Thread(target=self.spawn_bot, args=((skype, i))).start()

	def onStartButtonDown(self, e):
		self.running = True
		self.statusBox.Clear()
		onlineList = []
		skype = Skype4Py.Skype()
		skype.Attach()
		for i in skype.Friends:
			print i.OnlineStatus
			print i.FullName, i.Handle
		self.checkUsersOnline(skype, onlineList)
		self.startButton.Disable()
		self.stopButton.Enable()

	def onStopButtonDown(self, e):
		self.running = False
		self.startButton.Enable()
		self.stopButton.Disable()


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

