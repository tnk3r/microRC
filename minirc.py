#!/usr/bin/python

# v0.2.3b

# AUTHOR : tink3r
#remote.syst3m@gmail.com or tink3r@unknownode.info
# Please Ask for Fork Request for any new additional features that have been added.

# Tkinter was used for beginning developers to start with un-modified linux/mac python environment
# I created this software during a prep week to control a 360 degree Camera array over wireless with low bandwidth connectivity.

# Get Camera status is not implemented. It increases traffic on the triangulated radios and increases pps dramatically. Therefore it was not implemented.
# It would need an additional thread and parser to get status, this is not included in this script. I dont recommend adding it to this utility.

import sys, os, time, re, hashlib
import socket
from Tkinter import *

main = Tk()
main.title('DragonSoftRemote')
main.geometry('700x400')
main.config(bg='gray10')
main.resizable(FALSE,FALSE)

menubar = Menu(main)
filemenu = Menu(menubar, tearoff=0)
main.config(menu=menubar)

filemenu.add_command(label="Exit", command=main.quit)
menubar.add_cascade(label="File", menu=filemenu)

port = StringVar()
port.set("TCP")
portValue = StringVar()
portValue.set(1111)

def connectEpic(event):
	global sock
	if port.get() == "TCP":
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server = (str(remoteEpic1.get()), int(portValue.get()))
		sock.connect(server)
		connectButton.config(image=connect_pressed)
		connectTally = Label(main, text='connected!',fg='green', bg='gray10')
		connectTally.place(x=340,y=25)

connect = PhotoImage(file="icons/connect.gif")
connect_pressed = PhotoImage(file="icons/connect_pressed.gif")
connectButton = Label(main, image=connect, bd=0, bg='gray10')
connectButton.place(x=283, y=22)
connectButton.bind("<Button-1>", connectEpic)
remoteEpic1 = StringVar()
remoteEpic1.set("10.10.10.2")
epic1 = Label(main, text="CAM 1", fg="white", bg="gray10")
epic1.place(x=50,y=25)
epicIPField1 = Entry(main, justify=RIGHT, width=15, cursor='xterm', textvariable=remoteEpic1, bg='black', fg='white', highlightthickness=0)
epicIPField1.place(x=100,y=25)
recglow = StringVar()
recglow.set("0")

def setFPS(event):
	FPS = float(fpsField.get()) * 1001
	FPS = str(FPS)
	MESSAGE = str("#$EXT:"+"S:"+"SENSFPS:"+FPS+":\n")
	if port.get() == "TCP":
		sock.sendall(MESSAGE)
	if port.get() == "UDP":
		sock.sendto(MESSAGE, (epicIPField1.get(), int(portValue.get())))

fpsValue = StringVar()
fpsField = Entry(main,width=16, justify=RIGHT, textvariable=fpsValue, fg='white', bg='black', highlightthickness=0)
fpsField.place(x=10, y=283)
fpsField.bind('<Return>',setFPS)
fpsField.bind('<Tab>',setFPS)
fpsLabel = Label(main, width=16, text="FPS" , fg="white", bg="black")
fpsLabel.place(x=10,y=225)
fpsList = ('6', '12', '20', '22', '23.98', '24', '25', '29.97', '30', '36', '40', '47.96','48', '50', '59.94','60', '72', '90', '96', '100', '120')
fpsMenu = OptionMenu(main, fpsValue, command=setFPS, *fpsList)
fpsMenu.config(bg='black', width=14, justify=RIGHT)
fpsMenu.place(x=10,y=250)

def setProjectFPS(event):
	PROJECT_RATE = float(projectFPS.get()) * 1000
	PROJECT_RATE = str(PROJECT_RATE)
	MESSAGE = str("#$EXT:"+"S:"+"PROJFPS:"+PROJECT_RATE+":\n")
	if port.get() == "TCP":
		sock.sendall(MESSAGE)

projectFPS = StringVar()
projectFPS.set("PROJECTRATE")
projectRateList = ('23.98', '24', '25', '29.97', '30', '47.96', '48', '50', '59.94')
projectMenu = OptionMenu(main, projectFPS, command=setProjectFPS, *projectRateList)
projectMenu.config(bg='black', width=8, justify=RIGHT)
projectMenu.place(x=150,y=250)

def setRC(event):
	if RCValue.get() == "3:1":
		REDCODE = int(3)
	if RCValue.get() == "4:1":
		REDCODE = int(4)
	if RCValue.get() == "5:1":
		REDCODE = int(5)
	if RCValue.get() == "6:1":
		REDCODE = int(6)
	if RCValue.get() == "7:1":
		REDCODE = int(7)
	if RCValue.get() == "8:1":
		REDCODE = int(8)
	if RCValue.get() == "9:1":
		REDCODE = int(9)
	if RCValue.get() == "10:1":
		REDCODE = int(10)
	if RCValue.get() == "11:1":
		REDCODE = int(11)
	if RCValue.get() == "12:1":
		REDCODE = int(12)
	REDCODE = REDCODE * 100
	MESSAGE = str("#$EXT:"+"S:"+"RCTARGET:"+str(REDCODE)+":\n")
	if port.get() == "TCP":
		sock.sendall(MESSAGE)

RCValue = StringVar()
RCValue.set("RC")
rcList = ('3:1','4:1','5:1','6:1','7:1','8:1','9:1','10:1','11:1','12:1')
RCMenu = OptionMenu(main, RCValue, command=setRC, *rcList)
RCMenu.config(bg='black', width=8, justify=RIGHT)
RCMenu.place(x=230,y=250)

def setFStop(event):
	FSTOP = float(fstopField.get()) * 10
	FSTOP = str(FSTOP)
	MESSAGE = str("#$EXT:"+"S:"+"APRTR:"+FSTOP+":\n")
	if port.get() == "TCP":
		sock.sendall(MESSAGE)

fstopValue = StringVar()
fstopField = Entry(main,width=16, justify=RIGHT, textvariable=fstopValue, fg='white', bg='black', highlightthickness=0)
fstopField.place(x=540, y=163)
fstopField.bind('<Return>',setFStop)
fstopField.bind('<Tab>',setFStop)
fstopLabel = Label(main, width=16, text="F-Stop" , fg="white", bg="black")
fstopLabel.place(x=540,y=105)
fstopList = ('2', '2.4', '2.8', '3.4', '4', '4.8', '5.6', '6.3', '8', '9.5', '11', '13.5', '16')
fstopMenu = OptionMenu(main, fstopValue, command=setFStop, *fstopList)
fstopMenu.config(bg='black', width=14, justify=RIGHT)
fstopMenu.place(x=540,y=130)

def setWB(event):
	WhiteBalance = int(whiteBalanceField.get())
	WhiteBalance = str(WhiteBalance)
	MESSAGE = str("#$EXT:"+"S:"+"COLTMP:"+WhiteBalance+":\n")
	if port.get() == "TCP":
		sock.sendall(MESSAGE)

wbValue = StringVar()
whiteBalanceField = Entry(main,width=16, justify=RIGHT, textvariable=wbValue, fg='white', bg='black', highlightthickness=0)
whiteBalanceField.place(x=280, y=163)
whiteBalanceField.bind('<Return>',setWB)
whiteBalanceField.bind('<Tab>',setWB)
whiteBalanceLabel = Label(main, width=16, text="WhiteBalance" , fg="white", bg="black")
whiteBalanceLabel.place(x=280,y=105)
whiteBalanceList = ('3000', '3200', '3500', '3800', '4000', '4300', '4500', '4800', '5000', '5200', '5600', '6000', '6500', '7000')
whiteBalanceMenu = OptionMenu(main, wbValue, command=setWB, *whiteBalanceList)
whiteBalanceMenu.config(bg='black', width=14, justify=RIGHT)
whiteBalanceMenu.place(x=280,y=130)

def setTint(event):
	Tint = int(tintField.get()) * 1000
	Tint = str(Tint)
	MESSAGE = str("#$EXT:"+"S:"+"TINT:"+Tint+":\n")
	if port.get() == "TCP":
		sock.sendall(MESSAGE)

tintValue = StringVar()
tintField = Entry(main,width=16, justify=RIGHT, textvariable=tintValue, fg='white', bg='black', highlightthickness=0)
tintField.place(x=410, y=163)
tintField.bind('<Return>',setTint)
tintField.bind('<Tab>',setTint)
tintLabel = Label(main, width=16, text="Tint" , fg="white", bg="black")
tintLabel.place(x=410,y=105)
tintList = ('-5', '-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5')
tintMenu = OptionMenu(main, tintValue, command=setTint, *tintList)
tintMenu.config(bg='black', width=14, justify=RIGHT)
tintMenu.place(x=410,y=130)

def startREC(event):
	global recglow
	MESSAGE = "#$EXT:S:RECORD:2:\n"
	if recglow.get() == "0":
		recglow = StringVar()
		REC.config(image=rec_active)
		recglow.set("1")
		REC.update()
	else:
		recglow = StringVar()
	 	REC.config(image=rec)
		recglow.set("0")
		REC.update()
	if port.get() == "TCP":
		sock.sendall(MESSAGE)

rec = PhotoImage(file='icons/record.gif')
rec_active = PhotoImage(file="icons/record_pressed.gif")
REC = Label(main, bg="gray10", image=rec, highlightthickness=0, bd=0)
REC.place(x=500, y=200)
REC.bind("<Button-1>", startREC)

def setShutter(event):
	SHUTTER = int(shutterField.get()) * 1000
	SHUTTER = str(SHUTTER)
	MESSAGE = str("#$EXT:"+"S:"+"SHANGLET:"+SHUTTER+":\n")
	if port.get() == "TCP":
		sock.sendall(MESSAGE)

shutterValue = StringVar()
shutterField = Entry(main,width=16, justify=RIGHT, textvariable=shutterValue, fg='white', bg='black', highlightthickness=0)
shutterField.place(x=20, y=163)
shutterField.bind('<Return>',setShutter)
shutterField.bind('<Tab>',setShutter)
ShutterLabel = Label(main, width=16, text="Shutter" , fg="white", bg="black")
ShutterLabel.place(x=20,y=105)
ShutterList = ('45', '90', '144', '180', '216', '250', '270', '360')
ShutterMenu = OptionMenu(main, shutterValue, command=setShutter, *ShutterList)
ShutterMenu.config(bg='black', width=14, justify=RIGHT)
ShutterMenu.place(x=20,y=130)

def setISO(event):
	ISO = isoValue.get()
	MESSAGE = str("#$EXT:"+"S:"+"ISO:"+ISO+":\n")
	if port.get() == "TCP":
		sock.sendall(MESSAGE)

isoValue = StringVar()
isoField = Entry(main,width=16, justify=RIGHT, textvariable=isoValue, fg='white', bg='black', highlightthickness=0)
isoField.place(x=150, y=163)
isoField.bind('<Return>',setISO)
isoField.bind('<Tab>',setISO)

isoLabel = Label(main, width=16, text="ISO" , fg="white", bg="black")
isoLabel.place(x=150,y=105)
isoList = ('250', '320', '400', '500', '640', '800', '1000', '1280', '1600', '2000', '2500','3200','4000','5000', '6400', '12800')
isoMenu = OptionMenu(main, isoValue, command=setISO, *isoList)
isoMenu.config(bg='black', width=14, justify=RIGHT)
isoMenu.place(x=150,y=130)
main.mainloop()
