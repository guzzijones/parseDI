from slpp import SLPP 
import re

class diObj(object):
	def __init__(self,type,name,luaData):
		self.objectType=type
		self.objectName=name
		self.objectKey=type+name
		self.DictLuaData=luaData
		self.DictTotal={}
		self.setDict()
	def setDict(self):
		self.DictTotal["Name"]=self.objectName
		self.DictTotal["Type"]=self.objectType
		self.DictTotal["luaData"]=self.DictLuaData
	def __str__(self):
		return str(self.DictTotal)
	def __eq__(self,objectTest):
		return (objectTest.objectType==self.objectType and objectTest.ObjectName==self.objectName)

class diObjFile(SLPP):
	def __init__(self,filename):
		SLPP.__init__(self)
		self.filename=filename;
		self.diObjects={}
		self.version=""

		self.setString();
		self.readVersion();
		self.decode();
		
	def setString(self):
		f = open(self.filename,'r')
		try:
			text=f.read()
			##todo remove all comments correctly
				#for each character 
				#if =" then ignore until next " without a preceding backslash
				#if / with preceding / then blank out everything until \n
			#currently only removes comments that start at the beginning of a line
			reg = re.compile('^//.*$', re.M)
			text = reg.sub('', text, 0)
			self.text = text	
			self.len = len(self.text)
		finally:
			f.close()

	def readVersion(self):
		self.white()
		wordFound = self.word()
		if wordFound=="version":
			self.next_chr();
			self.version = self.value();
			#print "version: ", self.version;
			self.next_chr();#skip semicolon
			self.next_chr();
#decode
	def decode(self):
		self.white()
		while self.ch:	
			wordFound = self.word()
			if wordFound=="object":
				self.next_chr();
				objectType= self.value()
				self.next_chr()
				objectName=self.value()
				self.next_chr()
				luaData = self.value()
				self.next_chr()
				self.next_chr()
				tmpdicObj=diObj(objectType,objectName,luaData)
				self.diObjects[tmpdicObj.objectKey]=tmpdicObj.DictTotal
				self.white()

__all__ = ['diObjFile']
