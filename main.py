from bs4 import BeautifulSoup
import urllib.request
import random
import re
from tqdm import tqdm
import os
from tkinter import *
from tkinter import scrolledtext
from multiprocessing import freeze_support
from multiprocessing import Pool
from functools import partial
import threading

window = Tk()

class wordSpinner:
	def __init__(self, master):
		cwd = os.getcwd()
		self.tandabaca = [',','.','!','?','(',')','<','>','/','[',']','{','}','@','#','$','%','%','^','&','*','+','-','=','\\','`','~']
		self.kalimatctr = None
		self.thread_list=[]
		self.hasil=[]
		self.texttest= []
		self.master = master
		self.master.title("Text Anonim Spinner by @adnan_todod_bgs")
		self.topframe = Frame(self.master)
		self.topframe.pack(fill=BOTH)
		self.frame = Frame(self.master)
		self.frame.pack(fill=X)
		self.frame4 = Frame(self.master)
		self.frame4.pack(fill=X)
		self.frame5 = Frame(self.master)
		self.frame5.pack(fill=X)
		self.bottomframe = Frame(self.master)
		self.bottomframe.pack(fill=X)
		self.txt = scrolledtext.ScrolledText(self.frame, bd=5, relief="raised")
		self.txt.pack(side=LEFT)
		self.txt0 = scrolledtext.ScrolledText(self.frame, bd=5, relief="raised")
		self.txt0.pack(side=LEFT)
		kalimatExist = os.path.exists(cwd+'\\kalimat.txt')
		if kalimatExist:
			f = open("kalimat.txt", "r")
			self.text = f.read()
			f.close()
			self.txt.insert(INSERT, self.text)
		pengecualianExist = os.path.exists(cwd+'\\pengecualian.txt')
		if pengecualianExist:
			f = open("pengecualian.txt", "r")
			self.text = f.read()
			f.close()
			self.txt0.insert(INSERT, self.text)
		self.spin = Button(self.frame4, text="Spin", command= self.spin)
		self.spin.pack(side = TOP)
		self.txt1 = scrolledtext.ScrolledText(self.bottomframe, bd=5, relief="raised")
		self.txt1.pack(fill=X)
		self.label0 = Label(self.topframe, text = "Kalimat ")
		self.label0.pack(fill=X)
		self.label1 = Label(self.topframe, text = "Kata yang tidak di spin (pisahkan kata dengan spasi)")
		self.label1.pack(fill=X)
		self.label2 = Label(self.frame5, text = "Hasil Spin Kalimat")
		self.label2.pack(side=TOP)
		self.alllabel()
		'''
		hasilExist = os.path.exists(cwd+'\\hasil.txt')
		if hasilExist:
			f = open("hasil.txt", "r")
			self.text = f.read()
			f.close()
			self.txt1.insert(INSERT, self.text)
		'''
	def alllabel(self):
		
		self.kalimatctr = str(self.txt.get("1.0", END))
		self.label0.configure(text = "Kalimat ("+str(len(self.kalimatctr.split()))+' kata)')
		self.label0.pack(side=LEFT)
		self.master.after(1000, self.alllabel)
		
	def spin(self):
		self.clearhasil()
		text = self.txt.get("1.0", END)
		exc = self.txt0.get("1.0", END)
		hasil = self.textspin(text,exc)
		self.h = open("kalimat.txt", "w")
		self.h.write(text)
		self.h.close()
		self.i = open("pengecualian.txt", "w")
		self.i.write(exc)
		self.i.close()
		# self.j = open("hasil.txt", "w")
		# self.j.write(hasil)
		# self.j.close()	
		self.txt1.insert(INSERT, hasil)
		self.label2.configure(text = "Hasil Spin Kalimat ("+str(len(hasil.split()))+' kata)')


	def clearhasil(self):
		self.txt1.delete('0.0', END)

	def wordspin(self,word,windex):
		if word == '\n':
			self.hasil[windex] = word
			return True
		tmptanda =''
		startword = False
		newline = False
		if word[0].isupper():
			startword = True
			word = word.lower()
		for tanda in self.tandabaca:
			if tanda in word[-1]:
				tmptanda = tanda
				word = word.replace(tanda,'')
		url = 'https://kamus.sabda.org/kamus/'
		try:
			fp = urllib.request.urlopen(url+word)
			mybytes = fp.read()
			fp.close()
		except Exception as e:
			print(e)
			return exit()
		tmptxt = " "
		txtres = []
		soupel = []
		soupels = []
		html = mybytes.decode("utf8")
		
		soup = BeautifulSoup(html, 'lxml')
		soupres = soup.find_all(class_="l1")
		#print(str(soupres))
		for sel in soupres:
			if '<b>'+word+'</b>' in str(sel):
				if '<i>p</i>' in str(sel):
					soupel.append(sel)
			if '<b>'+word+'</b>' in str(sel):
				if '<i>v</i>' in str(sel):
					soupel.append(sel)
			if '<b>'+word+'</b>' in str(sel):
				if '<i>a</i>' in str(sel):
					soupel.append(sel)
		souprese = soup.find_all(class_="l2")
		#print(str(souprese))
		for sel in souprese:
			if '<b>'+word+'</b>' in str(sel):
				if '<i>p</i>' in str(sel):
					soupel.append(sel)
			if '<b>'+word+'</b>' in str(sel):
				if '<i>v</i>' in str(sel):
					soupel.append(sel)
			if '<b>'+word+'</b>' in str(sel):
				if '<i>a</i>' in str(sel):
					soupel.append(sel)
		#print(str(soupel))
		for sels in soupel:
			soupels.append(str(sels).replace(" (cak)", ""))
		tmptxt = tmptxt.join(soupels)
		regex = r'\(.*?\)'

		tmptxt = re.sub(regex,'()',tmptxt)
		#print(str(tmptxt))
		tmptxt = tmptxt.replace('<br/>','')
		tmptxt = tmptxt.replace('<br/;>','')
		tmptxt = tmptxt.replace('<p','')
		tmptxt = tmptxt.replace('</p>','')
		tmptxt = tmptxt.replace('</p>;','')
		tmptxt = tmptxt.replace('</b>','')
		tmptxt = tmptxt.replace('<b>','')
		tmptxt = tmptxt.replace('n</i> ','')
		tmptxt = tmptxt.replace('v</i> ','')
		tmptxt = tmptxt.replace('</i>;','')
		tmptxt = tmptxt.replace('</i>','')
		tmptxt = tmptxt.replace(' (<i>ki</i>)','')
		tmptxt = tmptxt.replace(' (<i>cak</i>)','')
		tmptxt = tmptxt.replace(' (ki)','')
		tmptxt = tmptxt.replace(' ()','')
		tmptxt = tmptxt.replace('(','')
		tmptxt = tmptxt.replace(')','')
		tmptxt = tmptxt.replace('·','')
		tmptxt = tmptxt.replace('--','')
		tmptxt = tmptxt.replace('-;','')
		tmptxt = tmptxt.split('<i>')
		ttxt =[]
		for mo in tmptxt:
			ttxt=ttxt+mo.split()
		ttxt = list( dict.fromkeys(ttxt) )
		#print(str(ttxt))

		for has in ttxt:
			if word == has:
				continue
			elif ',' == has[-1]:
				txtres.append(has.replace(',',''))
			elif ';' == has[-1]:
				txtres.append(has.replace(';',''))
			else:
				continue
		#print(txtres)
		if len(txtres):
			index = random.randint(0, len(txtres)-1)
			if startword:
				if tmptanda:
					self.hasil[windex] = txtres[index].capitalize()+tmptanda
					return True
				else:
					self.hasil[windex] = txtres[index].capitalize()
					return True
			else:
				if tmptanda:
					self.hasil[windex] = txtres[index]+tmptanda
					return True
				else:
					self.hasil[windex] = txtres[index]
					return True
		else:
			if startword:
				if tmptanda:
					self.hasil[windex] = word.capitalize()+tmptanda
					return True
				else:
					self.hasil[windex] = word.capitalize()
					return True
			else:
				if tmptanda:
					self.hasil[windex] = word+tmptanda
					return True
				else:
					self.hasil[windex] = word
					return True

	def sleep_thread(self):
	    self.thread_list = []
	    

	def textspin(self,words,excs):
		self.sleep_thread()
		self.hasil = []
		sword=[]
		for n in words.splitlines():
			for word in n.split():
				sword.append(word)
			sword.append('\n')
		for n in words.splitlines():
			for word in n.split():
				self.hasil.append(word)
			self.hasil.append('\n')
		#print(hasil)
		hasiltxt = ""
		#print(len(sword))
		#print(len(hasil))
		exc = ' '#['di','aku','kamu','kami','dia','saya','mereka']
		if excs == "":
			excs = " "
		excs = excs.split()
		exc =exc.split()
		exc = exc + excs
		exc = list( dict.fromkeys(exc) )
		print(exc)
		#print(exc)

		if len(exc)<1:
			for word in sword:
				windex = sword.index(word)
				t = threading.Thread(target=self.wordspin, args=(word,windex, ))
				self.thread_list.append(t)
				t.start()
			for thread in self.thread_list:
				thread.join()
		else:
			for word in sword:
				windex = sword.index(word)
				x=0
				for wexc in exc:
					wow = word
					for tanda in self.tandabaca:
						if word[0].isupper():
							wow = wow.lower()
						if tanda in word[-1]:
							wow = wow[:-1]
					if wexc == wow:
						x=1
				if x:
					self.hasil[windex] = word
				else:
					t = threading.Thread(target=self.wordspin, args=(word,windex, ))
					self.thread_list.append(t)
					t.start()
			for thread in self.thread_list:
				thread.join()
							
		for has in self.hasil:
			if has =='\n':
				hasiltxt = hasiltxt[:-1]
				hasiltxt = hasiltxt+str(has)
			else:
				hasiltxt=hasiltxt+str(has)+' '
		hasiltxt=hasiltxt[:-1]
		return hasiltxt

spinner = wordSpinner(window)
window.mainloop()
