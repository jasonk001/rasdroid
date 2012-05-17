# -*- coding: utf-8 -*-
import os, sys, mutagen,tidy,time,shutil,hashlib,locale

from stat import *
from mutagen.easyid3 import EasyID3
from mutagen.asf import ASF
from xml.etree import ElementTree as ET
from xml.dom.minidom import parse, parseString

def runXmlGen():
	
	xmlFileData = '<?xml version="1.0" encoding="UTF-8"?>\n<tracks>\n'
	
	xmlFileData = walktree("/musicdrive/WMA/",xmlFileData)

	xmlFileData = xmlFileData + '\n</tracks>'
	#print xmlFileData
	xmlFile = "/var/www/library.xml"
	albumFile = "/var/www/albums.xml"
	artistFile = "/var/www/artists.xml"
	
	#Delete all files in image folder
	for root,dirs,files in os.walk("/var/www/images/"):
		for f in files:
			fullpath = os.path.join(root,f)
			os.remove(fullpath)
	
	for root,dirs,files in os.walk("/var/www/artists/"):
		for f in files:
			fullpath = os.path.join(root,f)
			os.remove(fullpath)
	
	for root,dirs,files in os.walk("/var/www/albums/"):
		for f in files:
			fullpath = os.path.join(root,f)
			os.remove(fullpath)
		
	f = open(xmlFile,"w+")
	f.writelines(xmlFileData)
	f.close()
	
	albumFileData = getAlbumXML(xmlFileData)
	f= open(albumFile,"w+")
	f.writelines(albumFileData)
	f.close()
	
	artistFileData = getArtistXML(xmlFileData)
	f= open(artistFile,"w+")
	f.writelines(artistFileData)
	f.close()

def walktree(top,xmlFileData):
	'''recursively descend the directory tree rooted at top,
	   calling the callback function for each regular file'''
	fileID = 0
	newData = xmlFileData
	for f in os.listdir(top):
		pathname = os.path.join(top, f)
		
		mode = os.stat(pathname).st_mode
		if S_ISDIR(mode):
			# It's a directory, recurse into it
			newData = walktree(pathname, newData)
			
		elif S_ISREG(mode):
			# It's a file
			fileName, fileExtension = os.path.splitext(pathname)
			if fileExtension == ".mp3" or fileExtension == ".wma":
				newData = newData + getFileInfo(pathname,fileExtension,fileID)
				fileID = fileID + 1
		else:
			# Unknown file type, print a message
			print 'Skipping %s' % pathname
			
	return newData

def getFileInfo(file,fileExtension,fileID):
	trackXML = ""
	skip = False
	
	if fileExtension == ".mp3":
		try:
			audio = EasyID3(file)
		except mutagen.id3.ID3NoHeaderError as noid3ex:
			skip = True
		fileType ="mp3"
		#print EasyID3.pprint(audio)
	else:	
		if fileExtension == ".wma":
			audio = ASF(file)
			fileType ="wma"
			#print ASF.pprint(audio)
	
	if(skip == False):
		title = "unknown"
		albumTitle = "unknown"
		artist = "unknown"
		trackNumber = "0"
		performer = "unknown"
		
		#get file info
		if audio.has_key('title'): 
			title = audio['title'][0]
		else:
			if audio.has_key('Title'):
				title = audio['Title'][0]
				
		if audio.has_key('WM/AlbumTitle'): 
			albumTitle = audio['WM/AlbumTitle'][0]
		else:
			if audio.has_key('album'): 
				albumTitle = audio['album'][0]
		
		if audio.has_key('artist'): 
			artist = audio['artist'][0]
		else: 
			if audio.has_key('Author'): artist = audio['Author'][0]
		
		if audio.has_key('performer'): 
			
			performer = audio['performer'][0]
			
			if audio.has_key('WM/AlbumArtist'): 
				performer = audio['WM/AlbumArtist'][0]
				
		if audio.has_key('tracknumber'): 
			trackNumber = audio['tracknumber'][0]
		else:
			if audio.has_key('WM/TrackNumber'): 
				trackNumber = audio['WM/TrackNumber'][0]
		
		#If we don't have a performer by now then use the artist field
		if performer == "unknown":
			performer = artist
		
		if albumTitle == "James Bond":
			print audio.keys
		#look up file in xml, if exists get playcount, lastplayed etc or mark as new
		try:
			trackXML = trackXML + getTrackToXML(fileID,file,title,albumTitle,artist,trackNumber,performer,fileType)
		except Exception as ex:
			print file
			raise
	else:
		print "Skipping " + file
		#print "added " + file
		#print file
		#print fileID
		#print title
		#print albumTitle
		#print artist
		#print trackNumber
		#print performer
	
	return trackXML

def getHash(strData):
	try:
		m= hashlib.md5()
		m.update(strData)
		hashmd5 = m.hexdigest()
	except Exception:
		print strData
		raise
		
	return hashmd5

def tidyXML(xmlString):
	return str(tidy.parseString(xmlString,input_xml=True,output_xml=True,wrap=0,input_encoding="utf8",output_encoding="utf8"))
	
def getTrackToXML(fileID,filePath,title,albumTitle,artist,trackNumber,performer,filetype):
	
	artistEncoded = encodeMyString(artist)
	albumTitleEncoded = encodeMyString(albumTitle)
	
	if(filetype=="wma"):
		
		albumID = getHash(albumTitleEncoded)
		artistID = getHash(artistEncoded)
	else:
		albumID = getHash(albumTitleEncoded)
		artistID = getHash(artistEncoded)
	
	newTrackInfo = "<track>\n"
	newTrackInfo = newTrackInfo + "<trackid>" + str(fileID) + "</trackid>\n"
	newTrackInfo = newTrackInfo + "<trackalbumid>" + albumID + "</trackalbumid>\n"
	newTrackInfo = newTrackInfo + "<trackartistid>" + artistID + "</trackartistid>\n"
	newTrackInfo = newTrackInfo + "<filepath>" + filePath + "</filepath>\n"
	newTrackInfo = newTrackInfo + "<title>" + encodeMyString(title) + "</title>\n"
	newTrackInfo = newTrackInfo + "<albumtitle>" + albumTitleEncoded + "</albumtitle>\n"
	newTrackInfo = newTrackInfo + "<artist>" + artistEncoded + "</artist>\n"
	newTrackInfo = newTrackInfo + "<tracknumber>" + str(trackNumber) + "</tracknumber>\n"
	
	#newTrackInfo = newTrackInfo + u"<performer>" + unicode(performer,'utf-8') + u"</performer>\n"
	newTrackInfo = newTrackInfo + "<performer>" + encodeMyString(performer) + "</performer>\n"
	
	#newTrackInfo = newTrackInfo + "<image>" + "http://192.168.200.131/images/" + str(fileID) + ".jpg" + "</image>\n"
	newTrackInfo = newTrackInfo + "</track>\n"
	
	
	newTrackInfo = tidyXML(newTrackInfo)
	
	return newTrackInfo

def encodeMyString(strEnc):
	try:
		encodedStr = str(strEnc.encode("utf-8"))
	except AttributeError as attrex:
		#print strEnc
		encodedStr = str(strEnc.value)
	except Exception as ex:
		print strEnc
		raise

	return encodedStr
	
def copyDefaultArt(destinationFilePath):
	sourceFilePath = "/var/www/NoAlbumArt_small.jpg"
	
	try:
		shutil.copyfile(encodeMyString(sourceFilePath),destinationFilePath)
	except IOError as e:
		print "Error copying default album art" + str(e)
		raise

def copyArt(albumID,filePath):
	fileFolder = os.path.split(filePath)[0]
	sourceFilePath = fileFolder+"/AlbumArtSmall.jpg"
	destinationFilePath = "/var/www/images/" + str(albumID) + ".jpg"
	
	try:
		shutil.copyfile(encodeMyString(sourceFilePath),destinationFilePath)
	except IOError as e:
		#print "Couldn't find file" + str(e)
		copyDefaultArt(destinationFilePath)
		#copy the no album art file instead
		
		#print sourceFilePath
		#print destinationFilePath

def getAlbumXML(xmlData):
	
	dom = parseString(xmlData)
	
	tracks = dom.getElementsByTagName("track")
	seen = {}
	albums = []
	
	
	for track in tracks:
		albumTitleNode = track.getElementsByTagName("albumtitle")[0]
		album = getText(albumTitleNode.childNodes)
		
		if album in seen:continue
		seen[album]=1
		albums.append(album)
	
	locale.setlocale(locale.LC_ALL,'')
	albums = sorted(albums,cmp=locale.strcoll)
		
	#Generate album XML
	indexXML = '<?xml version="1.0" encoding="UTF-8"?><albums>\n'
	for album in albums:
		albumXML = '<?xml version="1.0" encoding="UTF-8"?>'
		albumID = getHash(encodeMyString(album))
		albumHeader = "<album>\n" + "<albumid>" + str(albumID) + "</albumid><albumname>" + album + "</albumname>\n"
		indexXML = indexXML + albumHeader
		albumXML = albumXML + albumHeader
		artCopied = False
		trackCount = 0
		for albumTrack in tracks:
			
			if getText(albumTrack.getElementsByTagName("albumtitle")[0].childNodes) == album:
				if trackCount == 0:
					#Get the performer of the first track cos it will be the same for the whole album
					performer = getText(albumTrack.getElementsByTagName("performer")[0].childNodes)
				trackCount = trackCount + 1
				if artCopied == False:
					copyArt(albumID,getText(albumTrack.getElementsByTagName("filepath")[0].childNodes))
					artCopied = True
				albumXML = albumXML + albumTrack.toxml()
		
		albumFooter = "<albumperformer>" + performer + "</albumperformer>\n" + "<trackcount>" + str(trackCount) + "</trackcount>\n</album>"
		albumXML = albumXML + albumFooter
		indexXML = indexXML + albumFooter
		albumXML = tidyXML(albumXML)
		writeXMLFile("/var/www/albums/" + albumID + ".xml", albumXML)
	
	return tidyXML(indexXML)

def writeXMLFile(filepath,xmlData):
	f= open(filepath,"w+")
	f.writelines(xmlData)
	f.close()

def getArtistXML(xmlData):
	
	dom = parseString(xmlData)
	
	tracks = dom.getElementsByTagName("track")
	seen = {}
	artists = []
	
	for track in tracks:
		artistNameNode = track.getElementsByTagName("performer")[0]
		artist = getText(artistNameNode.childNodes)
		
		if artist in seen:continue
		seen[artist]=1
		artists.append(artist)
	
	locale.setlocale(locale.LC_ALL,'')
	artists = sorted(artists,cmp=locale.strcoll)
	
	#Generate album XML
	indexXML = '<?xml version="1.0" encoding="UTF-8"?><artists>\n'
	for artist in artists:
		artistXML = '<?xml version="1.0" encoding="UTF-8"?>'
		artistID = getHash(encodeMyString(artist))
		artistHeader = "<theartist>\n" + "<artistid>" + getHash(encodeMyString(artist)) + "</artistid><artistname>" + artist + "</artistname>\n"
		indexXML = indexXML + artistHeader
		artistXML = artistXML + artistHeader
		
		trackCount = 0
		for artistTrack in tracks:
			
			if getText(artistTrack.getElementsByTagName("performer")[0].childNodes) == artist:
				if trackCount == 0:
					#Get the album of the first track so that we can use it to get the album art
					albumid = getHash(getText(artistTrack.getElementsByTagName("albumtitle")[0].childNodes))
				trackCount = trackCount + 1
		
				artistXML = artistXML + artistTrack.toxml()
		
		artistFooter = "<trackcount>" + str(trackCount) + "</trackcount>\n<albumid>" + str(albumid) + "</albumid>\n</theartist>"
		artistXML = artistXML + artistFooter
		indexXML = indexXML + artistFooter
		artistXML = tidyXML(artistXML)
		
		writeXMLFile("/var/www/artists/" + artistID + ".xml", artistXML)
				
	indexXML = indexXML + "</artists>"
	#print indexXML
	return tidyXML(indexXML)

def getText(nodeList):
	rc = []
	for node in nodeList:
		if node.nodeType == node.TEXT_NODE:
			rc.append(node.data)
		return ''.join(rc)
		
def uniqueList(seq,idfun=None):
	if idfun is None:
		def idfun(x): return x
	seen = {}
	result = []
	for item in seq:
		marker=idfun(item)
		
		if marker in seen: continue
		seen[marker]=1
		result.append(item)
	return result
	
runXmlGen()

