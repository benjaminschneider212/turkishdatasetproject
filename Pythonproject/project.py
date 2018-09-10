######################
######################
##### The Great ######
#####   Python  ######
#####   Project ######
######################
######################


#the working directory I need to be in
#		cd Desktop
#		cd Pythonproject
#		cd pdfminer.six-20170720

#Note for other readers:
# 		change the working directories for you to run code properly. All relevant data generated is included, but this code will not run for you without proper directory setting

#relevant libraries to import the html code and parse text
from bs4 import BeautifulSoup
import urllib2
import re
import csv
import wget
import ssl
import time
from unicode_tr import unicode_tr
from unicode_tr.extras import slugify
from string import digits

######################
## Function Library ##
######################

#the terminal function needs numbers without spaces. This function takes normal range function and return numbers only sep by comma. This is for the creating of html files farther down
def transferpagenums(x,y):
	nums=range(x,y)
	nums=str(nums)
	print nums.replace(" ", "")


#this charatcer fixes the # and replaces them with i
def charfix(string):
	look=list(string)
	for i in range(0,len(look)):
		if look[i]=="#":
			look[i]="i"
		else:
			pass
	return "".join(look)

#this is the monster function that opens the data and organizes it to be sorted
def dataopener(parnum):
	web_page = urllib2.urlopen("file:///Users/benjaminschneider/Desktop/Pythonproject/pdfminer.six-20170720/par%d.html"%parnum)
	all_html = BeautifulSoup(web_page.read())
	oldtextentries=all_html.find_all("div")
	positions=[]
	for line in oldtextentries:
		positions.append([re.findall(r"writing-mode:lr-tb", line["style"]),re.findall(r"top:\d+px", line["style"])])
	textentries=[]
	for line in oldtextentries:
		if "writing-mode:lr-tb" in line["style"]:
			textentries.append(line)
		else:
			pass
	betterpositions=[]
	for line in positions:
		if line[0]==[]:
			pass
		else:
			betterpositions.append(line[1])
	newnums=orderproperly(betterpositions)
	data=[]
	while len(newnums)>0:
		ref=newnums[0]
		newnums.pop(0)
		for i in range(len(newnums)):#add
			if ref==newnums[i]:
				newnums.pop(i)
				break
			else:
				pass
		counter=0
		while counter<len(textentries): ##########
			base=re.findall(r"top:\d+px", textentries[counter]["style"])
			track=[]
			if ref==base[0]:
				track.append(textentries[counter].get_text())
				orderer=re.findall(r"left:\d+px", textentries[counter]["style"])
				baseint=re.findall(r"\d+", orderer[0])
				baseintint=int(baseint[0])
				textentries.pop(counter)
				for i in range(len(textentries)):
					base1=re.findall(r"top:\d+px", textentries[i]["style"])
					if base==base1:
						orderer2=re.findall(r"left:\d+px", textentries[i]["style"])
						baseint2=re.findall(r"\d+", orderer2[0])
						baseintint2=int(baseint2[0])
						if baseintint>baseintint2:
							textext=track[0]
							track.pop(0)
							track.append(textentries[i].get_text())
							track.append(textext)
							textentries.pop(i)
							break
						else:
							track.append(textentries[i].get_text())
							textentries.pop(i)
							break
					else:
						pass
				for line in track:
					data.append(line)
			else:
				counter+=1
	ref=data[0]
	newdata=[]
	for i in range(len(data)):
		if data[i]==ref:
			pass
		else:
			newdata.append(data[i])
	newnewdat=[]
	for line in newdata:
		try:
			int(line)
		except:
			newnewdat.append(line)
	if parnum==23:
		look=newnewdat
		newnewdat=[]
		for line in look:
			if u"YASAMA D\xd6NEM\u0130" in line:
				pass
			else:
				newnewdat.append(line)
	else:
		pass
	if parnum==23:
		newnewdat.append("2007 - 2011")
	else:
		newnewdat.append(re.findall(r"\d{4} - \d{4}", ref))
	if parnum==4:
		observationcombineremove(640,641,newnewdat)
		observationcombineremove(135,136,newnewdat)
	elif parnum==5:
		observationcombineremove(756,757,newnewdat)
		observationcombineremove(3,4,newnewdat)
	elif parnum==6:
		observationcombineremove(215,216,newnewdat)
	elif parnum==7:
		observationcombineremove(971,972,newnewdat)
		observationcombineremove(766,767,newnewdat)
		observationcombineremove(541,542,newnewdat)
		observationcombineremove(72,73,newnewdat)
		observationcombineremove(39,40,newnewdat)
	elif parnum==8:
		observationcombineremove(896,897,newnewdat)
		observationcombineremove(323,324,newnewdat)
	elif parnum==9:
		observationcombineremove(443,444,newnewdat)
	elif parnum==10:
		observationcombineremove(71,72,newnewdat)
	elif parnum==13:
		observationcombineremove(227,228,newnewdat)
	elif parnum==17:
		for i in (828,827,826,825,824,823,822):
			newnewdat.pop(i)
		observationcombineremove(320,321,newnewdat)
		newnewdat.pop(196)
	elif parnum==22:
		for i in (1108,1107,1106):
			newnewdat.pop(i)
	elif parnum==23:
		observationcombineremove(649,650,newnewdat)
		observationcombineremove(644,645,newnewdat)
		observationcombineremove(563,564,newnewdat)
	else:
		pass
	finaldat=[]
	for line in newnewdat:
		finaldat.append(charfix(line))
	return finaldat

for i in range(1,24):
	data=dataopener(i)
	data2=datasorter(data)
	print i,data2[-1]

#this combines error unique text entries in the data opener function
def observationcombineremove(x,y,data):
	data[x]="%s %s"%(data[x],data[y])
	data.pop(y)
	return data

#this puts the data in order after it is sufficiently organized
def datasorter(data):
	datadat=[]
	for line in data:
		if line!="":
			datadat.append(line)
	newdata=[]
	counter=len(datadat)-1
	track=0
	if counter%4!=0:
		counter-=2
		track+=1
	counter/=4
	for i in range(counter):
		i*=4
		newdata.append(datadat[i])
		newdata.append(datadat[i+2])
		newdata.append(datadat[i+1])
		newdata.append(datadat[i+3])
	if track==1:
		newdata.append(datadat[-3])
		newdata.append(datadat[-2])
	newdata.append(datadat[-1])
	return newdata

#this gets the matched items in order so that it is region region entry entry
def orderproperly(doubleslist):
	nums=[]
	for line in doubleslist:
		baseint=re.findall(r"\d+", line[0])
		nums.append(int(baseint[0]))
	newnums=selectionsort(nums)
	outputdoubles=[]
	for num in newnums:
		outputdoubles.append("top:%spx"%num)
	return outputdoubles

#this just gets things in order
def selectionsort(x):#beginning of this is same
	newx=x[:]
	output=[]
	while len(newx)>0:#while loop used because I remove lowest option
		val=min(newx) #finds the min value
		output.append(val)#append the lowest to the new list
		for i in range(0,len(newx)):
			if newx[i]==val: #this removes the first iteration of the value so not all of the same value are removed
				newx.pop(i)
				break
			else: #keep looking
				pass
	return output 


#need to fix this to get names right, but otherwise ok
def megaparser():
	with open('TurkMP.csv', 'wb') as f:
		w = csv.DictWriter(f, fieldnames = ("Region", "Name", "Party", "YOB", "Kurdish","English","Arabic","Farsi","Armenian","French","German", "Year", "Parliament")) #set up the csv fields
		w.writeheader()
		for i in range(1,24):
			dat=dataopener(i)
			data=datasorter(dat)
			parnum=i
			year=data[-1]
			data.pop(-1)
			for i in range(len(data)/2):
				entry={}
				entry["Year"]=year
				entry["Parliament"]=parnum
				i*=2
				datasplit=re.split(r'\n', data[i+1])
				entry["Region"]=data[i].encode("utf-8")
				kurd=0
				for line in datasplit:
					if u'Kürt' in line:
						kurd+=1
						break
					else:
						pass
				entry["Kurdish"]=kurd
				english=0
				for line in datasplit:
					if u'İngiliz' in line:
						english+=1
						break
					else:
						pass
				entry["English"]=english
				arabic=0
				for line in datasplit:
					if u'Arapça' in line:
						arabic+=1
						break
					else:
						pass
				entry["Arabic"]=arabic
				farsi=0
				for line in datasplit:
					if u'Farsça' in line:
						farsi+=1
						break
					else:
						pass
				entry["Farsi"]=farsi
				armenian=0
				for line in datasplit:
					if u'Ermenice' in line:
						armenian+=1
						break
					else:
						pass
				entry["Armenian"]=armenian
				german=0
				for line in datasplit:
					if u'Almanca' in line:
						german+=1
						break
					else:
						pass
				entry["German"]=german
				french=0
				for line in datasplit:
					if u'Fransızca' in line:
						french+=1
						break
					else:
						pass
				entry["French"]=french
				if parnum<7:
					if ")" in datasplit[1]:
						stuff="%s%s"%(datasplit[0],datasplit[1])
						#name = stuff.translate(None, digits)
						entry["Name"]=stuff.encode("utf-8")
						entry["Party"]=""
						yob=re.findall(r"\d{4}", datasplit[2])
					else:
						stuff=datasplit[0]
						# name = stuff.translate(None, digits)
						entry["Name"]=stuff.encode("utf-8")
						entry["Party"]=""
						yob=re.findall(r"\d{4}", datasplit[1])
				else:
					if ")" in datasplit[1]:
						stuff="%s%s"%(datasplit[0],datasplit[1])
						# name = stuff.translate(None, digits)
						entry["Name"]=stuff.encode("utf-8")
						entry["Party"]=datasplit[2].encode("utf-8")
						yob=re.findall(r"\d{4}", datasplit[3])
					else:
						stuff=datasplit[0]
						# name = stuff.translate(None, digits)
						entry["Name"]=stuff.encode("utf-8")
						entry["Party"]=datasplit[1].encode("utf-8")
						yob=re.findall(r"\d{4}", datasplit[2])
				if yob!=[]:
					entry["YOB"]=yob[0].encode("utf-8")
				else:
					entry["YOB"]=""
				w.writerow(entry)

#I used this code to extract text and HTML code for the poster
web_page = urllib2.urlopen("file:///Users/benjaminschneider/Desktop/Pythonproject/pdfminer.six-20170720/par1.html")
all_html = BeautifulSoup(web_page.read())
oldtextentries=all_html.find_all("div")

for i in (5,6):
	print oldtextentries[i]

for i in (5,6):
	print charfix(oldtextentries[i].get_text())


#runs the csv
megaparser()



### NOTES FOR EXCEPTION HANDLING

#the issue right now looks like that there are sometimes extra spaces between death date and the rest of the text. Need to figure this out!
# 4: 136->135, 641->640
# 5: 4->3, 757->756
# 6: 216->215
# 7: 40->39, 73->72, 542->541, 767->766, 972->971
# 8: 324->323, 897->866
# 9: 444->443
# 10: 72->71
# 13: 228->227
# 17: cut 196, 321->320, cut: 822-828
# 22: cut 1106-1108
# 23: correct and 564->563 ,645->644 650->649

####################
####################
##### Code for #####
#### making the ####
#### HTML files ####
####################
####################

# most of this below was just to create the HTML files. I have it at the bottom so
# all of the analysis is at the top. Most of this functions are to be run in the
# main terminal using the pdfminer main function pdf2txt.py This has to be downloaded 
# and the working directory in the main terminal needs to be det appropriates. I put
# the PDFs in the folder with the function and all of the HTML files are output
# into the sample folder.

################
## first book ##
################

# par 1
# transferpagenums(34,90)
# 	for terminal 
# pdf2txt.py -p 34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89 -t html -o par1.html samples/Cilt1.pdf

# par 2
# transferpagenums(107,149) 
# 	for terminal 
# pdf2txt.py -p 107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148 -t html -o par2.html samples/Cilt1.pdf

# par 3
# transferpagenums(159,201) 
# 	for terminal 
# pdf2txt.py -p 159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200 -t html -o par3.html samples/Cilt1.pdf

# par 4
# transferpagenums(211,255)
# 	for terminal 
# pdf2txt.py -p 211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254 -t html -o par4.html samples/Cilt1.pdf

# par 5
# transferpagenums(265,321)
# 	for terminal 
# pdf2txt.py -p 265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,281,282,283,284,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,305,306,307,308,309,310,311,312,313,314,315,316,317,318,319,320 -t html -o par5.html samples/Cilt1.pdf

# par 6
# transferpagenums(331,390)
# 	for terminal 
# pdf2txt.py -p 331,332,333,334,335,336,337,338,339,340,341,342,343,344,345,346,347,348,349,350,351,352,353,354,355,356,357,358,359,360,361,362,363,364,365,366,367,368,369,370,371,372,373,374,375,376,377,378,379,380,381,382,383,384,385,386,387,388,389 -t html -o par6.html samples/Cilt1.pdf

# par 7
# transferpagenums(399,461)
# 	for terminal 
# pdf2txt.py -p 399,400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,418,419,420,421,422,423,424,425,426,427,428,429,430,431,432,433,434,435,436,437,438,439,440,441,442,443,444,445,446,447,448,449,450,451,452,453,454,455,456,457,458,459,460 -t html -o par7.html samples/Cilt1.pdf

# par 8
# transferpagenums(473,536)
# 	for terminal 
# pdf2txt.py -p 473,474,475,476,477,478,479,480,481,482,483,484,485,486,487,488,489,490,491,492,493,494,495,496,497,498,499,500,501,502,503,504,505,506,507,508,509,510,511,512,513,514,515,516,517,518,519,520,521,522,523,524,525,526,527,528,529,530,531,532,533,534,535 -t html -o par8.html samples/Cilt1.pdf




#################
## second book ##
#################

# #par 9
# transferpagenums(23,85)
# 	#for terminal 
# pdf2txt.py -p 23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84 -t html -o par9.html samples/Cilt2.pdf

# #par 10
# transferpagenums(93,161)
# 	#for terminal 
# pdf2txt.py -p 93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160 -t html -o par10.html samples/Cilt2.pdf

# #par 11
# transferpagenums(169,245)
# 	#for terminal 
# pdf2txt.py -p 169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244 -t html -o par11.html samples/Cilt2.pdf

# #par 12
# transferpagenums(255,312)
# 	#for terminal 
# pdf2txt.py -p 255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,281,282,283,284,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,305,306,307,308,309,310,311 -t html -o par12.html samples/Cilt2.pdf

# #par 13
# transferpagenums(319,376)
# 	#for terminal 
# pdf2txt.py -p 319,320,321,322,323,324,325,326,327,328,329,330,331,332,333,334,335,336,337,338,339,340,341,342,343,344,345,346,347,348,349,350,351,352,353,354,355,356,357,358,359,360,361,362,363,364,365,366,367,368,369,370,371,372,373,374,375 -t html -o par13.html samples/Cilt2.pdf

# #par 14
# transferpagenums(383,440)
# 	#for terminal 
# pdf2txt.py -p 383,384,385,386,387,388,389,390,391,392,393,394,395,396,397,398,399,400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,418,419,420,421,422,423,424,425,426,427,428,429,430,431,432,433,434,435,436,437,438,439 -t html -o par14.html samples/Cilt2.pdf

# #par 15
# transferpagenums(447,504)
# 	#for terminal 
# pdf2txt.py -p 447,448,449,450,451,452,453,454,455,456,457,458,459,460,461,462,463,464,465,466,467,468,469,470,471,472,473,474,475,476,477,478,479,480,481,482,483,484,485,486,487,488,489,490,491,492,493,494,495,496,497,498,499,500,501,502,503 -t html -o par15.html samples/Cilt2.pdf

# #par 16
# transferpagenums(511,568)
# 	#for terminal 
# pdf2txt.py -p 511,512,513,514,515,516,517,518,519,520,521,522,523,524,525,526,527,528,529,530,531,532,533,534,535,536,537,538,539,540,541,542,543,544,545,546,547,548,549,550,551,552,553,554,555,556,557,558,559,560,561,562,563,564,565,566,567 -t html -o par16.html samples/Cilt2.pdf


################
## third book ##
################


# #par 17
# transferpagenums(27,79)
# 	#for terminal 
# pdf2txt.py -p 27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78 -t html -o par17.html samples/Cilt3.pdf

# #par 18
# transferpagenums(85,142)
# 	#for terminal 
# pdf2txt.py -p 85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141 -t html -o par18.html samples/Cilt3.pdf

# #par 19
# transferpagenums(149,206)
# 	#for terminal 
# pdf2txt.py -p 149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205 -t html -o par19.html samples/Cilt3.pdf

# #par 20
# transferpagenums(213,282)
# 	#for terminal 
# pdf2txt.py -p 213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,281 -t html -o par20.html samples/Cilt3.pdf

# #par 21
# transferpagenums(289,358)
# 	#for terminal 
# pdf2txt.py -p 289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,305,306,307,308,309,310,311,312,313,314,315,316,317,318,319,320,321,322,323,324,325,326,327,328,329,330,331,332,333,334,335,336,337,338,339,340,341,342,343,344,345,346,347,348,349,350,351,352,353,354,355,356,357 -t html -o par21.html samples/Cilt3.pdf

# #par 22
# transferpagenums(365,435)
# 	#for terminal 
# pdf2txt.py -p 365,366,367,368,369,370,371,372,373,374,375,376,377,378,379,380,381,382,383,384,385,386,387,388,389,390,391,392,393,394,395,396,397,398,399,400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,418,419,420,421,422,423,424,425,426,427,428,429,430,431,432,433,434 -t html -o par22.html samples/Cilt3.pdf

# #par 23
# transferpagenums(441,510)
# 	#for terminal 
# pdf2txt.py -p 441,442,443,444,445,446,447,448,449,450,451,452,453,454,455,456,457,458,459,460,461,462,463,464,465,466,467,468,469,470,471,472,473,474,475,476,477,478,479,480,481,482,483,484,485,486,487,488,489,490,491,492,493,494,495,496,497,498,499,500,501,502,503,504,505,506,507,508,509 -t html -o par23.html samples/Cilt3.pdf



################
## fifth book ##
################

# CID codes only, does not output characters. look into this issue after everything else is done.
# #par 24
# transferpagenums(28,303)
# 	#for terminal
# pdf2txt.py -p 28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,281,282,283,284,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302 -t html -o par24.html samples/Cilt5.pdf

















#############################
#############################
########             ########
########   ARCHIVE   ########
########             ########
#############################
#############################



# #this reads in the file. It will print whole thing so assign
# def reader(docname):
# 	with open("%s"%docname, "r") as f:
# 		text = f.read()
# 	return charfix(text)

# #this creates and object with all of them
# def masterreader():
# 	masterset=[]
# 	for i in range(1,24):
# 		masterset.append(reader("par%s.txt"%i))
# 	return masterset

# #this will create a list with each parliament as an entry in the list
# alloftheparliaments=masterreader()

# def readerline(docname):
# 	with open("%s"%docname, "r") as f:
# 		text = f.readlines()
# 	for i in range(0,len(text)):
# 		text[i]=charfix(text[i])
# 	return text

# for line in readerline("par1.txt"):
#     print line

# deathdates=[]
# for line in readerline("par1.txt"):
#     if "Ölüm Tarihi" in line:
#     	deathdates.append(re.findall(r"\d{2}\.\d{2}\.\d{4}", line))

# lit=[]
# for i in range(1,len(parsedat)):
# 	if parsedat[i-1]=="\n":
# 		lit.append(parsedat[i])

# regions=[]
# names=[]

# for line in lit:
# 	if len(line)<20:
# 		regions.append(re.findall(r"[A-ZİÜÖĞŞÇ]+", line))
# 	else:
# 		pass


# thepositions=["left:52px","left:140px","left:318px","left:406px"]
# thepositions=["left:52px","left:140px","left:318px","left:406px","left:53px","left:141px","left:319px","left:407px","left:54px","left:142px","left:320px","left:408px","left:51px","left:139px","left:317px","left:405px","left:50px","left:138px","left:316px","left:404px"]
# for line in positions:
# 	if line[0]==[]:
# 		pass
# 	else:
# 		for pos in thepositions:
# 			if pos==line[0][0]:
# 				betterpositions.append(line)
# 			else:
# 				pass
# data=[]
# for i in range(len(betterpositions)):
# 	for line in textentries:
# 		base=re.findall(r"top:\d+px", line["style"])
# 		base1=re.findall(r"left:\d+px", line["style"])
# 		if betterpositions[i][1][0]==base[0] and betterpositions[i][0][0]==base1[0]:
# 			data.append(line.get_text())
# 		else:
# 			pass

# def dataopener(parnum):
# 	web_page = urllib2.urlopen("file:///Users/benjaminschneider/Desktop/Pythonproject/pdfminer.six-20170720/par%d.html"%parnum)
# 	all_html = BeautifulSoup(web_page.read())
# 	textentries=all_html.find_all("div")
# 	positions=[]
# 	for line in textentries:
# 		positions.append([re.findall(r"writing-mode:lr-tb", line["style"]),re.findall(r"top:\d+px", line["style"])])
# 	betterpositions=[]
# 	for line in positions:
# 		if line[0]==[]:
# 			pass
# 		else:
# 			betterpositions.append(line[1])
# 	newnums=orderproperly(betterpositions)
# 	data=[]
# 	while len(newnums)>0:
# 		ref=newnums[0]
# 		newnums.pop(0)
# 		for i in range(len(textentries)):
# 			base=re.findall(r"top:\d+px", textentries[i]["style"])
# 			if ref==base[0]:
# 				data.append(textentries[i].get_text())
# 				textentries.pop(i)
# 				break
# 			else:
# 				pass
# 	ref=data[0]
# 	newdata=[]
# 	for i in range(len(data)):
# 		if data[i]==ref:
# 			pass
# 		else:
# 			newdata.append(data[i])
# 	newnewdata=[]
# 	for line in newdata:
# 		try:
# 			int(line)
# 		except:
# 			newnewdata.append(line)
# 	return newnewdata

# def dataopenera(parnum):
# 	web_page = urllib2.urlopen("file:///Users/benjaminschneider/Desktop/Pythonproject/pdfminer.six-20170720/par%d.html"%parnum)
# 	all_html = BeautifulSoup(web_page.read())
# 	textentries=all_html.find_all("div")
# 	positions=[]
# 	for line in textentries:
# 		positions.append([re.findall(r"writing-mode:lr-tb", line["style"]),re.findall(r"top:\d+px", line["style"])])
# 	betterpositions=[]
# 	for line in positions:
# 		if line[0]==[]:
# 			pass
# 		else:
# 			betterpositions.append(line[1])
# 	newnums=orderproperly(betterpositions)
# 	data=[]
# 	while len(newnums)>0:
# 		ref=newnums[0]
# 		newnums.pop(0)
# 		for i in range(len(newnums)):#add
# 			if ref==newnums[i]:
# 				newnums.pop(i)
# 				break
# 			else:
# 				pass
# 		for i in range(len(textentries)):
# 			base=re.findall(r"top:\d+px", textentries[i]["style"])
# 			track=[]
# 			if ref==base[0]:
# 				track.append(textentries[i].get_text())
# 				orderer=re.findall(r"left:\d+px", textentries[i]["style"])
# 				baseint=re.findall(r"\d+", orderer[0])
# 				baseintint=int(baseint[0])
# 				textentries.pop(i)
# 				# comp.append(orderer)
# 				for i in range(len(textentries)):
# 					base1=re.findall(r"top:\d+px", textentries[i]["style"])
# 					if base==base1:
# 						orderer2=re.findall(r"left:\d+px", textentries[i]["style"])
# 						baseint2=re.findall(r"\d+", orderer2[0])
# 						baseintint2=int(baseint2[0])
# 						if baseintint>baseintint2:
# 							data.append(textentries[i].get_text())
# 							data.append(track[0])
# 							textentries.pop(i)
# 							break
# 						else:
# 							data.append(track[0])
# 							data.append(textentries[i].get_text())
# 							textentries.pop(i)
# 							break
# 					else:
# 						pass
# 				break
# 			else:
# 				pass
# 	ref=data[0]
# 	newdata=[]
# 	for i in range(len(data)):
# 		if data[i]==ref:
# 			pass
# 		else:
# 			newdata.append(data[i])
# 	newnewdata=[]
# 	for line in newdata:
# 		try:
# 			int(line)
# 		except:
# 			newnewdata.append(line)
# 	return newnewdata

# def dataopenerb(parnum):
# 	web_page = urllib2.urlopen("file:///Users/benjaminschneider/Desktop/Pythonproject/pdfminer.six-20170720/par%d.html"%parnum)
# 	all_html = BeautifulSoup(web_page.read())
# 	oldtextentries=all_html.find_all("div")
# 	positions=[]
# 	for line in oldtextentries:
# 		positions.append([re.findall(r"writing-mode:lr-tb", line["style"]),re.findall(r"top:\d+px", line["style"])])
# 	textentries=[]
# 	for line in oldtextentries:
# 		if "writing-mode:lr-tb" in line["style"]:
# 			textentries.append(line)
# 		else:
# 			pass
# 	betterpositions=[]
# 	for line in positions:
# 		if line[0]==[]:
# 			pass
# 		else:
# 			betterpositions.append(line[1])
# 	newnums=orderproperly(betterpositions)
# 	data=[]
# 	while len(newnums)>0:
# 		ref=newnums[0]
# 		newnums.pop(0)
# 		for i in range(len(newnums)):#add
# 			if ref==newnums[i]:
# 				newnums.pop(i)
# 				break
# 			else:
# 				pass
# 		while len(textentries)>0:
# 			base=re.findall(r"top:\d+px", textentries[0]["style"])
# 			track=[]
# 			if ref==base[0]:
# 				track.append(textentries[0].get_text())
# 				orderer=re.findall(r"left:\d+px", textentries[0]["style"])
# 				baseint=re.findall(r"\d+", orderer[0])
# 				baseintint=int(baseint[0])
# 				textentries.pop(0)
# 				# comp.append(orderer)
# 				for i in range(len(textentries)):
# 					base1=re.findall(r"top:\d+px", textentries[i]["style"])
# 					if base==base1:
# 						orderer2=re.findall(r"left:\d+px", textentries[i]["style"])
# 						baseint2=re.findall(r"\d+", orderer2[0])
# 						baseintint2=int(baseint2[0])
# 						if baseintint>baseintint2:
# 							textext=track[0]
# 							track.pop(0)
# 							track.append(textentries[i].get_text())
# 							track.append(textext)
# 							textentries.pop(i)
# 							break
# 						else:
# 							track.append(textentries[i].get_text())
# 							textentries.pop(i)
# 							break
# 					else:
# 						pass
# 			else:
# 				pass
# 			for line in track:
# 				data.append(line)
# 	ref=data[0]
# 	newdata=[]
# 	for i in range(len(data)):
# 		if data[i]==ref:
# 			pass
# 		else:
# 			newdata.append(data[i])
# 	newnewdata=[]
# 	for line in newdata:
# 		try:
# 			int(line)
# 		except:
# 			newnewdata.append(line)
# 	return newnewdata
# 	return data

#odd number parliaments will need a special consideration: 8,10,16,22 DONE
# def outputcleanly(htmllink):
# 	textentries=htmllink.find_all("div")
# 	positions=[]
# 	for line in textentries:
# 		positions.append(re.findall(r"top:\d+px", line["style"]))
# 	doubles=[]
# 	while len(positions)>0:
# 		ref=positions[0]
# 		positions.pop(0)
# 		for i in range(len(positions)):
# 			if ref==positions[i]:
# 				doubles.append(ref)
# 				positions.pop(i)
# 				break
# 			else:
# 				pass

# 	newdubs=orderproperly(doubles)
# 	data=[]
# 	for item in newdubs:
# 		for line in textentries:
# 			base=re.findall(r"top:\d+px", line["style"])
# 			if item==base[0]:
# 				data.append(line.get_text())
# 			else:
# 				pass
# 	return data

# def datasortera(parnum):
# 	data=parliamentopener(parnum)
# 	datadat=[]
# 	for line in data:
# 		if line!="":
# 			datadat.append(line)
# 	newdata=[]
# 	if parnum==10:
# 		lit=1066-990
# 		while len(datadat)>lit:
# 			newdata.append(datadat[0])
# 			datadat.pop(0)
# 	else:
# 		pass
# 	counter=len(datadat)
# 	if parnum==8 or parnum==10 or parnum==16 or parnum==22:
# 		counter-=2
# 	counter/=4
# 	for i in range(counter):
# 		i*=4
# 		newdata.append(datadat[i])
# 		newdata.append(datadat[i+2])
# 		newdata.append(datadat[i+1])
# 		newdata.append(datadat[i+3])
# 	if parnum==8 or parnum==16 or parnum==11:
# 		newdata.append(datadat[-2])
# 		newdata.append(datadat[-1])
# 	elif parnum==10:
# 		newdata.append(datadat[-4])
# 		newdata.append(datadat[-2])
# 		newdata.append(datadat[-3])
# 		newdata.append(datadat[-2])
# 		newdata.append(datadat[-1])
# 	elif parnum==20:
# 		newdata.append(datadat[-2])
# 		newdata.append(datadat[-3])
# 		newdata.append(datadat[-1])
# 	elif parnum==22:
# 		newdata.append(datadat[-4])
# 		newdata.append(datadat[-3])
# 	return newdata

# data=parliamentopener(10)
# datadat=[]
# for line in data:
# 	if line!="":
# 		datadat.append(line)
# newdata=[]
# lit=1066-990
# while len(datadat)>lit:
# 	newdata.append(datadat[0])
# 	datadat.pop(0)

# stuff=datasortera(10)
# for line in stuff:
#     print line


# def doubleopener(parnum):
# 	parnum=int(parnum)
# 	web_page = urllib2.urlopen("file:///Users/benjaminschneider/Desktop/Pythonproject/pdfminer.six-20170720/par%d.html"%parnum)
# 	all_html = BeautifulSoup(web_page.read())
# 	textentries=all_html.find_all("div")
# 	positions=[]
# 	for line in textentries:
# 		positions.append(re.findall(r"top:\d+px", line["style"]))
# 	doubles=[]
# 	tracker=[]
# 	if parnum==8:
# 		tracker.append(positions[1682])
# 		tracker.append(positions[1683])
# 	elif parnum==10:
# 		tracker.append(positions[1812])
# 		tracker.append(positions[1813])
# 	elif parnum==16:
# 		tracker.append(positions[1526])
# 		tracker.append(positions[1525])
# 	elif parnum==22:
# 		tracker.append(positions[1865])
# 		tracker.append(positions[1866])
# 	else:
# 		pass
# 	while len(positions)>0:
# 		ref=positions[0]
# 		positions.pop(0)
# 		for i in range(len(positions)):
# 			if ref==positions[i]:
# 				doubles.append(ref)
# 				positions.pop(i)
# 				break
# 			else:
# 				pass
# 	if len(tracker)>0:
# 		doubles.append(tracker[0])
# 		doubles.append(tracker[1])
# 	else:
# 		pass
# 	return orderproperly(doubles)

# #this function is to take out the labels without a proper entry below them and then I will just manually add the missing entries
# def corrector(data):
# 	newdatadat=[]
# 	for i in range(len(data)-1):
# 		if len(data[i])<25 and len(data[i+1])<25:
# 			pass
# 		else:
# 			newdatadat.append(data[i])

# #this is a master function that just takes in the number of the parliament and returns formatted data
# def parliamentopener(parnum):
# 	parnum=int(parnum)
# 	web_page = urllib2.urlopen("file:///Users/benjaminschneider/Desktop/Pythonproject/pdfminer.six-20170720/par%d.html"%parnum)
# 	all_html = BeautifulSoup(web_page.read())
# 	textentries=all_html.find_all("div")
# 	positions=[]
# 	for line in textentries:
# 		positions.append(re.findall(r"top:\d+px", line["style"]))
# 	doubles=[]
# 	tracker=[]
# 	if parnum==8:
# 		tracker.append(positions[1682])
# 		tracker.append(positions[1683])
# 	elif parnum==10:
# 		tracker.append(positions[1812])
# 		tracker.append(positions[1813])
# 	elif parnum==16:
# 		tracker.append(positions[1526])
# 		tracker.append(positions[1525])
# 	elif parnum==22:
# 		tracker.append(positions[1865])
# 		tracker.append(positions[1866])
# 	else:
# 		pass
# 	while len(positions)>0:
# 		ref=positions[0]
# 		positions.pop(0)
# 		for i in range(len(positions)):
# 			if ref==positions[i]:
# 				doubles.append(ref)
# 				positions.pop(i)
# 				break
# 			else:
# 				pass
# 	if len(tracker)>0:
# 		doubles.append(tracker[0])
# 		doubles.append(tracker[1])
# 	else:
# 		pass
# 	newdubs=orderproperly(doubles)
# 	data=[]
# 	for item in newdubs:
# 		for line in textentries:
# 			base=re.findall(r"top:\d+px", line["style"])
# 			if item==base[0]:
# 				data.append(line.get_text())
# 			else:
# 				pass
# 	if parnum<9:
# 		for i in range(len(data)):
# 			data[i]=charfix(data[i])
# 	return data

# def parser(data,parnum):
# 	with open('TurkMP.csv', 'wb') as f:
# 		range(len(data)/2)
# 		w = csv.DictWriter(f, fieldnames = ("Region", "Name", "Party", "Parliament","Years")) #set up the csv fields
# 		w.writeheader()
# 		for i in range(len(data)/2):
# 			i*=2
# 			datasplit=re.split(r'\n', data[i+1])
# 			entry={}
# 			entry["Region"]=u"%s"%slugify(data[i])
# 			if parnum<7:
# 				if ")" in datasplit[1]:
# 					entry["Name"]=u"%s%s"%(slugify(datasplit[0]),slugify(datasplit[1]))
# 					entry["Party"]=u""
# 				else:
# 					entry["Name"]=u"%s"%slugify(datasplit[0])
# 					entry["Party"]=""
# 			else:
# 				if ")" in datasplit[1]:
# 					entry["Name"]=u"%s%s"%(slugify(datasplit[0]),slugify(datasplit[1]))
# 					entry["Party"]=u"%s"%slugify(datasplit[2])
# 				else:
# 					entry["Name"]=u"%s"%slugify(datasplit[0])
# 					entry["Party"]=u"%s"%slugify(datasplit[1])
# 			w.writerow(entry)

# def parser(data,parnum):
# 	with open('TurkMP.csv', 'wb') as f:
# 		range(len(data)/2)
# 		w = csv.DictWriter(f, fieldnames = ("Region", "Name", "Party", "YOB", "Kurdish")) #set up the csv fields
# 		w.writeheader()
# 		for i in range(len(data)/2):
# 			entry={}
# 			i*=2
# 			datasplit=re.split(r'\n', data[i+1])
# 			entry={}
# 			entry["Region"]=data[i].encode("utf-8")
# 			kurd=0
# 			for line in datasplit:
# 				if u'K\xc3\xbcrt\xc3\xa7e' in line:
# 					kurd+=1
# 					break
# 				else:
# 					pass
# 			entry["Kurdish"]=kurd
# 			if parnum<7:
# 				if ")" in datasplit[1]:
# 					stuff="%s%s"%(datasplit[0],datasplit[1])
# 					entry["Name"]=stuff.encode("utf-8")
# 					entry["Party"]=""
# 				else:
# 					entry["Name"]=datasplit[0].encode("utf-8")
# 					entry["Party"]=""
# 			else:
# 				if ")" in datasplit[1]:
# 					stuff="%s%s"%(datasplit[0],datasplit[1])
# 					entry["Name"]=stuff.encode("utf-8")
# 					entry["Party"]=datasplit[2].encode("utf-8")
# 				else:
# 					entry["Name"]=datasplit[0].encode("utf-8")
# 					entry["Party"]=datasplit[1].encode("utf-8")
# 			w.writerow(entry)