import sys, os
import pygtk, gtk, gobject
import pygst
pygst.require("0.10")
import gst

#! /usr/bin/env python -3 -t

import sys, os, errno, tempfile, unittest, logging , time
from multiprocessing import Process

class SingleInstance:
	"""
	If you want to prevent your script from running in parallel just instantiate SingleInstance() class. If is there another instance already running it will exist the application with the message "Another instance is already running, quitting.", returning -1 error code.

	>>> import tendo
	>>> me = SingleInstance()

	This option is very useful if you have scripts executed by crontab at small amounts of time.

	Remember that this works by creating a lock file with a filename based on the full path to the script file.
	"""
	def __init__(self):
		import sys
		self.lockfile = os.path.normpath(tempfile.gettempdir() + '/' +
		    os.path.splitext(os.path.abspath(__file__))[0].replace("/","-").replace(":","").replace("\\","-")  + '.lock')
		logging.debug("SingleInstance lockfile: " + self.lockfile)
		if sys.platform == 'win32':
			try:
				# file already exists, we try to remove (in case previous execution was interrupted)
				if os.path.exists(self.lockfile):
					os.unlink(self.lockfile)
				self.fd =  os.open(self.lockfile, os.O_CREAT|os.O_EXCL|os.O_RDWR)
			except OSError as e:
				if e.errno == 13:
					logging.error("Another instance is already running, quitting.")
					sys.exit(-1)
				print(e.errno)
				raise
		else: # non Windows
			import fcntl, sys
			self.fp = open(self.lockfile, 'w')
			try:
				fcntl.lockf(self.fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
			except IOError:
				logging.warning("Another instance is already running, quitting.")
				sys.exit(-1)

	def __del__(self):
		import sys
		if sys.platform == 'win32':
			if hasattr(self, 'fd'):
				os.close(self.fd)
				os.unlink(self.lockfile)


class GTK_Main:
	me=SingleInstance()
	playing = False
	initialised = False
	playStatus = "play"
	PLAYLIST_PATH = "/var/www/dataFile.txt"
	STATUS_PATH = '/var/www/status.txt'
	
	def __init__(self):
		#self.player = gst.Pipeline("player")
		#source = gst.element_factory_make("filesrc", "file-source")
		#decoder = gst.element_factory_make("mad", "mp3-decoder")
		#conv = gst.element_factory_make("audioconvert", "converter")
		#sink = gst.element_factory_make("alsasink", "alsa-output")
		#self.player.add(source, decoder, conv, sink)
		#gst.element_link_many(source, decoder, conv, sink)
		
		self.player = gst.element_factory_make("playbin2","player")
		fakesink = gst.element_factory_make("fakesink","fakesink")
		self.player.set_property("video-sink",fakesink)
		
		bus = self.player.get_bus()
		bus.connect("message", self.on_message)
		bus.add_signal_watch()
		self.initialised= True
		
		self.timer = gobject.timeout_add (2000,self.startPlaying)
		#self.timer2 = gobject.timeout_add (2000,self.checkState)
		
	def checkState(self):
		print "check state called"
		u = Utils()
		status = u.read_First_Line(self.STATUS_PATH)
				
		if status == "stopped":
			self.player.set_state(gst.STATE_NULL)
		
		if status == "paused":
			self.player.set_state(gst.STATE_PAUSED)
	
	def startPlaying(self):
		#print "startPLaying called"
		
		#check we are supposed to be playing anything at all
		if self.playStatus == "play":
		
			#Check if we are already playing a song
			if self.playing == False:
				
				u = Utils()
				filepath = u.read_First_Line(self.PLAYLIST_PATH)
				filepath = filepath.replace("\r","")
				filepath = filepath.replace("\n","")
				if filepath != "":
				
					if os.path.isfile(filepath):
						print "playing " + filepath
						self.player.set_property("uri", "file://" + filepath)
						#self.player.get_by_name("file-source").set_property("location", filepath)
						
						self.player.set_state(gst.STATE_PLAYING)
						print 'playing';
						self.playing = True
					else:
						print "can't find file"
						#remove it from the playlist
						self.remove_track(0);
						#To stop playback
						self.player.set_state(gst.STATE_NULL)
			
		return True
			
	def on_message(self, bus, message):
		t = message.type
		#print "message received"
		if t == gst.MESSAGE_EOS:
			self.player.set_state(gst.STATE_NULL)
			self.playing = False
			print "EOS"
			#song has finished
			self.remove_track(0)
				
		elif t == gst.MESSAGE_ERROR:
			self.playing = False
			self.player.set_state(gst.STATE_NULL)
			err, debug = message.parse_error()
			self.remove_track(0)
			print "Error: %s" % err, debug
			
	
	def remove_track(self,number):
		u = Utils();
		fin = open(self.PLAYLIST_PATH,"r");
		play_list = fin.readlines();
		fin.close();
		
		del play_list[number];
		
		fout = open(self.PLAYLIST_PATH,"w");
		fout.writelines(play_list);
		fout.close();
		
class Utils:
		
	def read_First_Line(self,filePath):
		f = open(filePath,'r')
		
		data = f.readline()
		
		return data
	

GTK_Main()
#gtk.gdk.threads_init()
gtk.main()
