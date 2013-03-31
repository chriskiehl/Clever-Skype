import Skype4Py
import cleverbot

class SkypeBot:
	def __init__(self, skype, user):
		self.s = skype
		self.user = user
		self.cb = cleverbot.Session()
		self.currentMsgDatetime = self.getCurrentMessageDatetime()
		self.currentMsg = self.getCurrentMessageBody()
		self.msg = ''
	
	def getCurrentMessageDatetime(self):
		# print self.user.Handle
		chat = self.s.Messages(self.user.Handle)
		# print str(chat[0])
		ID =  chat[0].Id
		return self.s.Message(ID).Datetime

	def getCurrentMessageBody(self):
		chat = self.s.Messages(self.user.Handle)
		# print str(chat[0])
		ID =  chat[0].Id
		return self.s.Message(ID).Body		

	def postSkypeMsg(self, msg):
		print 'Posting Clever bot\'s respoonse to %s\'s chat.' % self.user.Handle
		self.s.SendMessage(self.user.Handle, msg)

	def update(self):
		self.currentMsgDatetime = self.getCurrentMessageDatetime()
		self.currentMsg = self.getCurrentMessageBody()

	def escapeChars(self, inString):
		tmp = inString.split("'")
		outstring = ''.join(tmp)
		return outstring

	def getCleverResponse(self):
		print 'Sending %s\'s messgae to CleverBot' % self.user.Handle
		msg = self.escapeChars(self.currentMsg)
		print self, msg
		cleverResponse = self.cb.Ask(msg)
		self.msg = cleverResponse
		self.postSkypeMsg(cleverResponse)
		print cleverResponse



if __name__ == '__main__':
	import Skype4Py

	skype = Skype4Py.Skype()
	skype.Attach()

	user = None
	for i in skype.Friends:
		print i 
		if 'cleverer' in i.Handle:
			user = i
			break


