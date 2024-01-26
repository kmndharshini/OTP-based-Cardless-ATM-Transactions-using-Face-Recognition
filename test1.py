import cv2
import face_recognition
import sqlite3
from tkinter import *
from tkinter import ttk
import time
from tkinter import messagebox
import random
from PIL import ImageTk, Image
import cv2, sys, numpy, os
import urllib
import numpy as np
from subprocess import call
import time
import os
import glob
import smtplib
import base64
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys


#https://outlook.live.com/mail/0/options/mail/accounts/popImap
gmail_user = "otpproject@outlook.com"
gmail_pwd = "Pro@1234"
FROM = 'otpproject@outlook.com'
TO = ['otpproject@outlook.com'] #must be a list
otp_=random.randint(10000,100000)

# Unknown Face Warning
def warningOTP():
    processing.pack_forget()
    processingText.pack_forget()

    response = messagebox.askquestion("Invalid OTP","Try again? ")
    if response=="yes":
        processing.after(1000,start)
    else:

        root.quit()

# Unknown Face Warning
def warningUnkownFace():
    processing.pack_forget()
    processingText.pack_forget()

    response = messagebox.askquestion("Un authorised person ","sending otp to mail ")
    if response =="yes":
        mail()
    else:
        root.quit()

# Account Number Warning
def warningAccountNumber():
    processing.pack_forget()
    processingText.pack_forget()

    response = messagebox.askquestion("Invalid Account Number", "Invalid Account Number\nTry Again?")
    if response == "yes":
        processing.after(1000,start)
    else:
        root.quit()

# Pin Warning
def warningPin():
    processing.pack_forget()
    processingText.pack_forget()

    response = messagebox.askquestion("Incorrect Pin", "Incorrect Pin\nTry Again?")
    if response == "yes":
        start()
    else:
        root.quit()

# OTP Verification
def verifyOTP():
    failedText.pack_forget()
    OTPText.pack_forget()
    OTPNumInput.pack_forget()
    OTPsubmitButton.pack_forget()

    processingText = Label(root, text="Verifying OTP Code")
    processing = ttk.Progressbar(root, orient=HORIZONTAL, length=300, mode="indeterminate")
    # Showing in the Screen
    processingText.pack(pady=20)
    processing.pack()
    processing.start(10)

    # Matching OTP
    if otp_ == int(OTPNumInput.get()):

        processingText.pack_forget()
        processing.pack_forget()
        processing.after(1000, update)
    else:
        # Set error message to invalid OTP
        processing.after(1000, warningOTP)

# Asking for OTP
def mail():
    processing.pack_forget()
    processingText.pack_forget()

    global failedText
    global OTPText
    global OTPNumInput
    global OTPsubmitButton
    global otp_
    msg = MIMEMultipart()
    time.sleep(1)
    msg['Subject'] ="SECURITY"

    #BODY with 2 argument
    
    #body=sys.argv[1]+sys.argv[2]cx 
    #DO THE CHANGES HERE
    body="THIS IS FROM pantech solution your otp for logging in :"+str(otp_)
    
    #otp_text="your otp for logging in :"+str(otp_)
    msg.attach(MIMEText(body,'plain'))
    #msg.attach(MIMEText(otp_text,'plain'))
    time.sleep(1)


    ###IMAGE
    fp = open("1.jpg", 'rb')   		
    time.sleep(1)
    img = MIMEImage(fp.read())
    time.sleep(1)
    fp.close()
    time.sleep(1)
    msg.attach(img)
    time.sleep(1)


    try:
            server = smtplib.SMTP("smtp.office365.com", 587) #or port 465 doesn't seem to work!
            print ("smtp.gmail")
            server.ehlo()
            print ("ehlo")
            server.starttls()
            print ("starttls")
            server.login(gmail_user, gmail_pwd)
            print ("reading mail & password")
            server.sendmail(FROM, TO, msg.as_string())
            print ("from")
            server.close()
            print ('successfully sent the mail')
    except:
            print ("failed to send mail")
    

    

    failedText = Label(root, text="Face Recognition Failed", fg="red")
    OTPText = Label(root, text="Enter Your OTP Code")
    OTPNumInput = Entry(root, width=50, borderwidth=2)
    OTPsubmitButton = Button(root, text="Log In", width=20, height=2, bg="#2d5cf7", fg="white", command=verifyOTP)
    failedText.pack(pady=30)
    OTPText.pack(pady=10)
    OTPNumInput.pack()
    OTPsubmitButton.pack(pady=10) 
    

    
    
   
    
#Face Authentication
def faceAuthentication():

    # Get video footage
    size = 4
    haar_file = r'C:\Users\Dharshini\Downloads\ATM\ATM\haarcascade_frontalface_default.xml'
    datasets = r'C:\Users\Dharshini\Downloads\ATM\ATM\datasets'
    #n=input("enter your name : ")
    
    print('Training...')
    # Create a list of images and a list of corresponding names
    (images, labels, names, id) = ([], [], {}, 0)
    for (subdirs, dirs, files) in os.walk(datasets):
        for subdir in dirs:
            names[id] = subdir
            subjectpath = os.path.join(datasets, subdir)
            for filename in os.listdir(subjectpath):
                path = subjectpath + '/' + filename
                label = id
                images.append(cv2.imread(path, 0))
                labels.append(int(label))
            id += 1
    (width, height) = (130, 100)

    # Create a Numpy array from the two lists above
    (images, labels) = [numpy.array(lis) for lis in [images, labels]]

    # OpenCV trains a model from the images
    # NOTE FOR OpenCV2: remove '.face' 
    model = cv2.face.FisherFaceRecognizer_create()
    model.train(images, labels)

    # Part 2: Use fisherRecognizer on camera stream
    face_cascade = cv2.CascadeClassifier(haar_file)
    ##with open("1.txt", mode='a') as file:
    webcam = cv2.VideoCapture(0)

    ##url="http://192.168.43.1:8080/shot.jpg"
    while True:

        (_, im) = webcam.read()
        
    ##    imgPath=urllib.urlopen(url)
    ##    imgNp=np.array(bytearray(imgPath.read()),dtype=np.uint8)
    ##    im=cv2.imdecode(imgNp,-1)
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(255,255,0),2)
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (width, height))
            #Try to recognize the face
            prediction = model.predict(face_resize)
            im2=im
            
        # cv2.imshow('OpenCV', im)
            if prediction[1]<500:
                #port.write('B')
            # print (names[prediction[0]])
                
                #print(names[prediction[0]]) 
                cv2.imshow('OpenCV', im)
                
                if names[prediction[0]]==str(n.get()):
                    print(names[prediction[0]])
                    return True
                    
            
            
                    
                else:
                    cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    cv2.imwrite('1.jpg',im2)
                    #mail()
                    return False

# Function to read data from DB
def readDB():
    connect = sqlite3.connect("bank_database.db")
    c = connect.cursor()
    number = accountNumInput.get()
    sql = "SELECT * FROM accounts WHERE contact_number = '{0}'"
    c.execute(sql.format(number))

    data = c.fetchone()
    if data is None:
        data = []
    else:
        with open('baseImage.jpg', 'wb') as f:
            f.write(data[2])
    connect.close()
    return data

# Function for authorized screen
def update():
    # Removing Elements from Screen after 3sec
    processing.pack_forget()
    processingText.pack_forget()

    # Calling UI Elements for account Options
    chcekAcount = Label(root, text="Choose Your Option", fg="black")
    balanceButton = Button(root, text="Check Balance", width=20, height=2, bg="#2d5cf7", fg="white")
    withdrawButton = Button(root, text="Withdraw Balance", width=20, height=2, bg="#2d5cf7", fg="white")
    transferButton = Button(root, text="Transfer Balance", width=20, height=2, bg="#2d5cf7", fg="white")
    # Showing in the Screen
    chcekAcount.pack(pady=15)
    balanceButton.pack(pady=10)
    withdrawButton.pack(pady=10)
    transferButton.pack(pady=10)

# Function of start screen
def next():
    global processing
    global processingText
    global contactNumber
    global n

    # Removing Elements from Screen after Button Clicked
    titleText.pack_forget()
    accountNumInput.pack_forget()
    accountPassInput.pack_forget()
    n.pack_forget()
    loginButton.pack_forget()

    # Calling UI Elements for Verifying Notice
    processingText = Label(root, text="Verifying Your Inputs")
    processing = ttk.Progressbar(root, orient=HORIZONTAL, length=300, mode="indeterminate")
    # Showing in the Screen
    processingText.pack(pady=20)
    processing.pack()
    processing.start(10)

    # read data from db
    data = readDB()
    contactNumber = data[3]

    if len(data) > 0:
        pinDB = data[1]
        # Check if pin matched
        if pinDB == int(accountPassInput.get()):
            # Process image
            
            check = faceAuthentication()
            if check:
                #result = True
                
                processing.after(1000, update)
                
                    
            else:
                # Set error message to face not matched
                processing.after(1000, warningUnkownFace)
        else:
            # Set error message to pin not matched
            processing.after(1000, warningPin)
    else:
        # Set error message to account not found
        processing.after(1000, warningAccountNumber)

# Functions to start authorization
def start():
    # Removing Elements from Screen after 3sec
    processing.pack_forget()
    processingText.pack_forget()

    global accountNumInput
    global accountPassInput
    global titleText
    global loginButton
    global n

    # Calling UI Elements
    titleText = Label(root, text="Enter Your Account Number & Password")
    accountNumInput = Entry(root, width=50, borderwidth=2)
    accountPassInput = Entry(root, width=50, borderwidth=2)
    n = Entry(root, width=50, borderwidth=2)
    loginButton = Button(root, text="Log In", width=20, height=2, bg="#2d5cf7", fg="white", command=next)

    # Showing in the Screen
    titleText.pack(pady=0)
    accountNumInput.pack(pady=10)
    accountPassInput.pack(pady=10)
    n.pack(pady=10)
    loginButton.pack(pady=10)

    accountNumInput.focus()

# Start the User Interface
root = Tk()
root.title("ATM Facial Recognition")
root.iconbitmap("Source.ico")
root.geometry("800x450")
# Calling UI Elements
logo = ImageTk.PhotoImage(Image.open("logo.png"))
my_img = Label(image=logo)
titleText = Label(root, text="Enter Your Name , Account Number & Password")
n= Entry(root, width=50, borderwidth=2)
accountNumInput = Entry(root, width=50, borderwidth=2)
accountPassInput = Entry(root, width=50, borderwidth=2)

loginButton = Button(root, text="NEXT", width=20, height=2, bg="#009B4B", fg="white", command=next)

# Showing in the Screen
my_img.pack(pady=30)
titleText.pack(pady=10)
n.pack(pady=10)
accountNumInput.pack(pady=10)
accountPassInput.pack(pady=10)

loginButton.pack(pady=20)


accountNumInput.focus()
root.mainloop()
