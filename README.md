<p align="center">
	<img src="https://github.com/Audionautics/Clever-Skype/raw/master/doc_images/Clever_skype.PNG?raw=true")/>
</p>

ABOUT
=====
----------------------------
Clever-Skype connects the chat output of Skype's chat window to the input of www.cleverbot.com.

In one of my english classes, we were tasked with creating marketing copy for a made up product. 
While I got busy photoshopping Aristotle's head being launched out of a cannon ( my product was a 
"logic bomb" ) A classmate came up with the idea of providing a service which had machines respond 
to all of the inane, pointless chatter we're bombarded with throughout the day. 

I thought such a thing wasn't so far fetched. And thus, Clever Skype was born. 


Requirements
============
---------------------------------
cleverbot:
: http://code.google.com/p/pycleverbot/ 

Skype4Py:
: http://sourceforge.net/projects/skype4py/

WxPython
: http://www.wxpython.org/

Usage
=====

Launch CleverSkype and click the Start Clever Skype button. If this is the first time your running the program, 
Skype will ask you whether or not you want to allow external programs to access. Select "allow."

<p align="center">
	<img src="https://github.com/Audionautics/Clever-Skype/raw/master/doc_images/allow_connection.PNG?raw=true")/>
</p>

Note:
##
I couldn't find any methods in the Skype API to test whether or not it has access, so the program just assumes that you're going to allow it, and this charges forward. The downside of this however, is that the CleverSkype will lockup and need to be force-quit if you don't allow it access as it's just sitting there waiting for access. Without a way to test, that's just kind of a clunky-ness that had to be there. 

----------------------------------------

Once connected, anytime a friend chats with you, CleverSkype with start a new conversation with cleverbot.com. Each conversation runs in its own thread, and it will carry on unique conversations with each of your contacts. 

<p align="center">
	<img src="https://github.com/Audionautics/Clever-Skype/raw/master/doc_images/skype_w_cs.PNG?raw=true")/>
</p>

---------------------------------------------

Once you're friends have ceased to be your friends, you can stop CleverSkype by clicking the "stop" button, or simply exiting the program from the file menu. 

That's it! 













