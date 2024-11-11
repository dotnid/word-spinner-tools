from bs4 import BeautifulSoup
import urllib.request
import random
import re
from tqdm import tqdm
import os
from multiprocessing import freeze_support
from multiprocessing import Pool
from functools import partial
import threading

thread_list=[]
hasil=[]
texttest= []
def wordspin(word,windex):
	if word == '\n':
		hasil[windex] = word
		return True
	tandabaca = [',','.','!','?','(',')','<','>','/','[',']','{','}','@','#','$','%','%','^','&','*','+','-','=','\\','`','~']
	tmptanda =''
	startword = False
	commas = False
	dot = False
	tanya = False
	seru = False
	newline = False
	if word[0].isupper():
		startword = True
		word = word.lower()
	for tanda in tandabaca:
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
	vowelcounted = vowelcounter(word)
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
	souprese = soup.find_all(class_="l2")
	#print(str(souprese))
	for sel in souprese:
		if '<b>'+word+'</b>' in str(sel):
			if '<i>p</i>' in str(sel):
				soupel.append(sel)
		if '<b>'+word+'</b>' in str(sel):
			if '<i>v</i>' in str(sel):
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
		if ','in has[-1]:
			txtres.append(has.replace(',',''))
		if ';' in has[-1]:
			txtres.append(has.replace(';',''))
	#print(txtres)
	if len(txtres):
		index = random.randint(0, len(txtres)-1)
		if startword:
			if tmptanda:
				hasil[windex] = txtres[index].capitalize()+tmptanda
				return True
			else:
				hasil[windex] = txtres[index].capitalize()
				return True
		else:
			if tmptanda:
				hasil[windex] = txtres[index]+tmptanda
				return True
			else:
				hasil[windex] = txtres[index]
				return True
	else:
		if startword:
			if tmptanda:
				hasil[windex] = word.capitalize()+tmptanda
				return True
			else:
				hasil[windex] = word.capitalize()
				return True
		else:
			if tmptanda:
				hasil[windex] = word+tmptanda
				return True
			else:
				hasil[windex] = word
				return True

def sleep_thread():
    thread_list = []

def textspin(words,excs):
	sleep_thread()
	sword=[]
	for n in words.splitlines():
		for word in n.split():
			sword.append(word)
		sword.append('\n')
	for n in words.splitlines():
		for word in n.split():
			hasil.append(word)
		hasil.append('\n')
	#print(hasil)
	hasiltxt = ""
	#print(len(sword))
	#print(len(hasil))
	exc = ['di','yang','aku','kamu','kami','dia','saya','mereka','video']
	if excs == "":
		excs = " "
	exc = list( dict.fromkeys(exc) )
	#print(exc)

	if len(exc)<1:
		for word in sword:
			windex = sword.index(word)
			t = threading.Thread(target=wordspin, args=(word,windex))
			thread_list.append(t)

		for thread in tqdm(thread_list):
			thread.start()
			sleep_thread()
		for thread in tqdm(thread_list):
			thread.join()
	else:
		for word in sword:
			windex = sword.index(word)
			x=0
			for wexc in exc:
				if wexc == word:
					x=1
			if x:
				hasil[windex] = word
				continue
			else:
				t = threading.Thread(target=wordspin, args=(word,windex))
				thread_list.append(t)
				continue
		for thread in tqdm(thread_list):
				thread.start()
				sleep_thread()
		for thread in tqdm(thread_list):
			thread.join()
	for has in hasil:
		if has =='\n':
			hasiltxt = hasiltxt[:-1]
			hasiltxt = hasiltxt+str(has)
		else:
			hasiltxt=hasiltxt+str(has)+' '
	hasiltxt=hasiltxt[:-1]
	return hasiltxt

def vowelcounter(word):
	vowels = ['a','i','u','e','o']
	counted = 0
	for char in word:
		for vowel in vowels:
			if char == vowel:
				counted=counted+1

	return counted


exc=''
text='''Walaupun jalannya panjang namun dia akan melaluinya.
Kami lebih suka video panjang di Youtube karena memberikan pemahaman yang mendalam.
Banyak ahli memperkirakan bahwa resesi bakal panjang.
Pengemudi ojek online terbelenggu pendapatan rendah dan jam kerja yang panjang.
Kami sedang membaca artikel jalan panjang Maxime Bouttier hingga mampu debut di film Hollywood.
Apa dampak gas air mata bagi tubuh jangka panjang?
Puluhan kendaraan harus antre panjang di SPBU.
Presiden mengkhawatirkan musim kering panjang pada tahun mendatang.
WAGS pemain Inggris dikabarkan akan memakai gaun panjang diperhelatan piala dunia 2022.
Kami memiliki sejarah yang panjang di kota Surabaya.
Saya senang berteman dengan Muhaimin karena dia panjang akalnya.
Mereka semua mendoakan supaya anak saya panjang umurnya, lapang rizkinya.
Banyak orang tidak menyukai Fernandes karena panjang mulutnya.
Berhati-hatilah apabila di kelas anda banyak siswa yang panjang tangannya.
Bapak Budiman berencana akan membuat investasi jangka panjang bagi sekolah anaknya.
Berapa panjang penggaris yang anda miliki?
Mohon maaf, kami sekarang tidak bisa berbicara panjang lebar mengenai peristiwa kemarin.
Diana sudah mengukur panjang rumah anda dari ujung ke ujung.
Berapa ukuran panjang tanah yang anda jual di Facebook?
Kami sudah mengukur bahwa panjang meja anda sepanjang 1,5 m.
Mereka tidak mengetahui bahwa anda memiliki rencana jangka panjang yang sangat matang.
Apa yang anda lakukan pada libur panjang bulan Juni tahun depan?
Kami akan berkunjung ke rumah kakek dan nenek pada libur panjang bulan Juni tahun depan.
Mengapa harga tiket pesawat selalu mahal pada saat libur panjang.
Janganlah orang menjadi orang yang panjang tangan.
Dia akan memotong besi ini sepanjang 25 cm.'''
print(textspin(text,exc))
#wordspin('ojek',0)

