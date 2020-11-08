from django.shortcuts import render

# Create your views here.
import re
from datetime import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
#import spellchecker import SpellChecker 
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from newHackApp.display.forms import patientDataInput
from django.http import JsonResponse



import csv 
#STRING MANIPULATION IMPORTS
import string
import nltk 
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= '/Users/samir/Desktop/bamboo-copilot-294917-5a623ee60ae0.json'
from google.cloud import language_v1

from nltk.corpus import words 
from nltk.metrics.distance import jaccard_distance
from nltk.util import ngrams
from nltk.metrics.distance  import edit_distance
from contractions import contractions_dict

def GenPreProcessing(text):
    lemmer = nltk.stem.WordNetLemmatizer()
    cleaner = dict((ord(punct), None) for punct in string.punctuation)

    def lClean(text): #removes punctuation marks and removes capatilized words 
        text = text.replace(text, text.lower().translate(cleaner))

        #Auto-Corrects
        text = text.split()

        #KARTI WORKING ON BELOW
        import nltk 
        #nltk.download()
        from nltk.corpus import words
        
        correct_spellings = words.words()
        
        from nltk.metrics.distance import jaccard_distance
        from nltk.util import ngrams
        from nltk.metrics.distance  import edit_distance

        index = 0
        for word in text:
            if (len(word) > 1):
                temp = [(jaccard_distance(set(ngrams(word, 2)), set(ngrams(w, 2))),w) for w in correct_spellings if w[0]==word[0]]
                #print(sorted(temp, key = lambda val:val[0])[0][1])
                text[index] = sorted(temp, key = lambda val:val[0])[0][1]
                index += 1
            else:
                
                index += 1
        #Lemmatize Words
        index = 0
        for word in text:
            text[index] = lemmer.lemmatize(word)
            index +=1
        
        #Output Formatting
        text = ' '.join(text)
        return(text)

    def expContract(text, cDict = contractions_dict):#expands shit like isn't to is not 
        for keys, words in cDict.items():
            text = text.replace(keys, words)
        #print(text)
        return (lClean((text)))
    
    text = expContract(text)
    return text

def defineScore(text):
    # Instantiates a client
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
    return sentiment.score

patientList = []

class Patient:
    def __init__(self, name, message, score, hours):
        self.name = name
        self.text = message
        self.score = score
        self.available = hours

def addNewPatient(name, message, hours, array): #WHEN YOU CLICK SUBMIT
    score = defineScore(message)
    newPatient = Patient(name, message, score, hours)
    print(name)
    print(score)
    array.append(newPatient)

def random(p):
    return p.score

def sortByScore(array):
    print(array)
    array.sort(key= lambda x: x.score)
    return array



def home(request):
    form = patientDataInput(request.POST)
    return render(request, 'extensionForm.html', {'form': form})


##########VIEW TEMPLATE FORMS:


Gname = ''
Gdescription = ''
Gavailability = ''

#@login_required
#@permission_required('catalog.can_mark_returned', raise_exception=True)
integer = 0
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def PatientDataMethod(request):
    global integer

    if (integer == 0):
        if request.method == 'POST':

            # Create a form instance and populate it with data from the request (binding):
            form = patientDataInput(request.POST)

            
            Gname = request.POST['patientName']
            Gdescription = request.POST['patientDescription']
            Gavailability = request.POST['patientAvailability']
            
            if (Gname == 'STOP'):
                integer = 1

                sortByScore(patientList)
                """
                print("now")
                for patient in patientList:
                    print("helo")
                    print(patient.name)
                    print(patient.score)
                    print(patient.text)
                """
                with open('schedule_file.csv', mode='w') as schedule_file:
                    schedule_writer = csv.writer(schedule_file, delimiter=',')
                    schedule_writer.writerow(["Patient Name", "Patient Sentiment Score", "Available Dates"])
                    for patient in patientList:
                        schedule_writer.writerow([patient.name, patient.score, patient.available])



                    return

            else:
                GprocessedText = GenPreProcessing(Gdescription)
                addNewPatient(Gname, GprocessedText, Gavailability, patientList)

            #if form.is_valid():
            #return HttpResponseRedirect('/thanks/')
        """
        else:
            form = patientDataInput()
        """
        
        return render(request, 'fronttest.html', {'form': form})
    
    

#json_File


##################

#text = description
#Part 1: Imports/Defs
#DATA IMPORTS


#GOOGLE API IMPORTS


"""
#Part 2: Read in Data
with open('/Users/samir/Desktop/Personal/Coding/NewHacksPythonFiles/PipeInputs.csv') as f:
    raw = (f.read()).lower()
#^ Imports text from CSV. 
"""
#Part 3: Pre-process




#Part 4: Google API




#print(sentimentScore)
#Part 5: Handle Output from Google
    # Name
    # Text
    # Score
    # Appointment availabilities





    # ...display value for doctor!!!!!!!!!!!!!!!!
    
"""
with open('output.csv', 'w', newline='') as f_output:
  Vtsv_output = csv.writer(f_output, delimiter='\t')
    while i < len(x_test):
      Vtsv_output.writerow(str(x) for x in (output))
      i+=1
"""



#Part 6: Sort Array/List - Account for Urgency, Date, Availability




#Part 7: Send Alerts
