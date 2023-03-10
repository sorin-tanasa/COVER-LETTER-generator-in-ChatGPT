#!/usr/bin/env python
# coding: utf-8

# ### Setup
# 

# In[ ]:


pip install transformers


# In[ ]:


pip install openai


# In[ ]:


pip install fpdf


# In[ ]:


pip install pandas


# In[ ]:


import os
import openai
import tkinter as tk
from tkinter import scrolledtext
from datetime import date
from fpdf import FPDF
import pandas as pd 


#Created a small software to automate date

def text_editor(txt):
    print("text coming in editing window is:", txt)
    # Create a tkinter window
    window = tk.Tk()
    window.title("Text Editor")

    # Create a scrolledtext widget to display the text
    text_widget = scrolledtext.ScrolledText(window, width=100, height=20)
    text_widget.insert(tk.END, txt)
    text_widget.pack()

    # Create a function to save the modified text
    def save_text():
        modified_text = text_widget.get("1.0", tk.END)
        global newtext
        newtext = modified_text.replace("} {", "")[1:-1]
        window.destroy()
        print("newtext in editing window is:", newtext)
        return newtext
    
    save_button = tk.Button(window, text="Save", command=save_text)
    save_button.pack()

    # Start the tkinter event loop
    window.mainloop()
    return newtext


class PDF(FPDF):
    def __init__(self, head, titl, txt, pth, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.details = head
        self.title = titl
        self.text = txt
        self.path= pth 
        
    def header(self):
        self.set_y(15)
        self.set_left_margin(20)
        self.set_font('Calibri Bold', '', 11)
        self.set_text_color(169, 169, 169)
        self.set_line_width(1)
        self.cell(0, 4, self.details)
        
    def content(self):
        self.set_y(28)
        self.set_left_margin(20)
        self.set_right_margin(20)
        self.set_font('Calibri', '', 11)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 4, self.text)         
        self.ln()
        
    def application(self):
        self.set_left_margin(90 - (len(self.title) / 2))
        self.set_y(45)
        self.set_font('Calibri Bold', '', 12)
        self.set_text_color(90, 90, 90)
        self.set_line_width(1)
        self.cell(0, 4, self.title, 'C')
        self.set_left_margin(0)
        
    def date_format(self):
        dt=date.today()
        DAY=str(dt.day)[-1]
        if int(dt.day)<21  and int(dt.day)>9:
            fdate="%sth of %s, %s"% (dt.day, dt.strftime('%B'), dt.year)
        else:
            if DAY=="0":
                fdate="%sth of %s, %s"%  (dt.day, dt.strftime('%B'), dt.year)
            elif DAY=="1":      
                fdate="%sst of %s, %s"%  (dt.day, dt.strftime('%B'), dt.year)
            elif DAY=="2":
                fdate="%snd of %s, %s"%  (dt.day, dt.strftime('%B'), dt.year)
            elif DAY=="3":
                fdate="%srd of %s, %s"%  (dt.day, dt.strftime('%B'), dt.year)
            else:
                fdate="%sth of %s, %s"%  (dt.day, dt.strftime('%B'), dt.year)
        return fdate  
    
    def date(self):
        self.set_y(28)
        self.set_left_margin(172 - len(self.date_format()))
        self.set_font('Calibri', '', 11)
        self.set_text_color(0, 0, 0)
        self.cell(0, 4, self.date_format())
        self.set_left_margin(0)
        
    def print_chapter(self):
        # Fonts need to be placed in the directory you are working set by os.chdir
        os.chdir(path)
        self.add_font('Calibri Italic', '', 'Fonts/Calibri Italic.ttf', uni=True)
        self.add_font('Calibri', '', 'Fonts/Calibri Regular.ttf', uni=True)
        self.add_font('Calibri Bold', '', 'Fonts/calibrib.ttf', uni=True)        
        self.add_page()        
        self.header()
        self.content()
        self.application()
        self.date()
       
        # Adding graphics
        self.rect(10, 21, 190, 0.5, style='F')

# Set working path:
path=r"C:\***********\Cover letter writer in ChatGPT turbo 3.5"
os.chdir(path)


# To use ChatGPT, you need some things first. You need an API key, which you can get by signing in here:
# https://platform.openai.com/account with your google account. 
# 
# You will need two things to proceed: an organization account name, which you can find at: 
# https://platform.openai.com/account/org-settings, 
# 
# and an API key, which you will create at https://platform.openai.com/account/api-keys. 
# 
# To access OpenAI, fill in your details bellow: 
# 

# In[ ]:


openai.organization = "org-################3rQOwmJZ"
openai.api_key = "sk-#########################k2s9exFtajU26W"
openai.Model.list()


# Note: Kee your eye on your expenses here: https://platform.openai.com/account/usage
# 

# ### Job description inputting

# 1. Manual version

# In[ ]:


JOB_DESCRIPTIONS=[]
job_number = 5   # set number of jobs you will process this round
while job_number>=1:
    JOB_DESCRIPTIONS.append(input())
    job_number-=1
JOB_DESCRIPTIONS


# 2. Automated version

# In[ ]:


df=pd.DataFrame(pd.read_excel("job description database.xlsx"))
df


# In[ ]:


#with open(r"G:\last desktop\jobs application\cv alternatives\cover letter formats custom.txt") as f:
with open("cover-letter-format-custom.txt") as f:    
    template = f.readlines()
print(template)


# In[ ]:


#with open(r"G:\last desktop\jobs application\cv alternatives\cv text.txt") as f:
with open("cv.txt") as f:
    cv = f.readlines()
print(cv)


# ### GPT response generation

# 1. Manual version

# In[ ]:


#Cover letters are generatd in ChatGPT 3.5 Turbo
cover_letters=[]

manual_script=""" Given that this is the job description: %s  and my resume is:
        %s, write me a complete cover letter under 1000 words addressed to Dear Hiring Manager, in the %s format 
        , making sure only relevant experiences and skills that are mentioned in my CV are mentioned and it's easy to read,
        not too cluttered with technical jargon."""

counter=0
for DESCRIPTION in JOB_DESCRIPTIONS:
    counter+=1
    if counter<3:
        command=manual_script %(DESCRIPTION,cv, template)
        #print(command)
        cover_letters.append([openai.ChatCompletion.create(model="gpt-3.5-turbo-0301", 
                                                           messages=[{"role": "system", "content": command}], 
                                                           max_tokens=1000)]) # max tokens keeps the output size in control
    else:
        print("could not perform task")
        break
print("In total, I created %s raw cover letters" %counter) 
print("output is: ", cover_letters)

#Give it few seconds or a minute to write the prompt.


# 2. Automated version

# In[ ]:


df2=df.iloc[:,[2,3,6,7,10,11]].drop_duplicates(keep='last')

cover_letters=[]

counter=0
for index, row in df2.iterrows():
    counter+=1
    if counter<3:
        command=""" There is a job opening at %s company in %s for %s. Given that this is the job description:
        %s (and, if not n.a., this is the required experience, %s, and the company description: %s), and my resume is:
        %s,, write me a complete cover letter under 1000 words addressed to Dear Hiring Manager, in the %s format 
        (just fill in the prompts in the brackets with stuff in my CV!!!), making sure only relevant experiences 
        and skills that are mentioned in my CV are mentioned and it's easy to read, not too cluttered with technical 
        jargon.""" %(row[0],row[1],row[2],row[3],row[4],row[5],cv, template)
        #print(command)
        cover_letters.append([openai.ChatCompletion.create(model="gpt-3.5-turbo-0301", 
                                                           messages=[{"role": "system", "content": command}],
                                                           max_tokens=1000)]) # max tokens keeps the output size in control
    else:
        print("could not perform task")
        break
print("In total I created %s screenplays" %cover_letters)    
print("output is: ", cover_letters)


# ### Text editing and saving to PDF

# 1. Manual version

# In[ ]:


# Modify here for your contact details
header="              John Doe    |   (555) 555-5555   |   john.doe@gmail.com   |   linkedin.com/in/john-doe"

counter=0
for response,desc in zip(cover_letters, JOB_DESCRIPTIONS):
    counter+=1
    title = 'Application for the Data Analyst position'
    x=text_message = response[0]['choices'][0]['message']['content']
    textraw = "\n\n\n\n\n\n\n\n"+x
    print("description of job is :", desc)
    text=text_editor(textraw)
    pdf = PDF(header, title, text,path)
    pdf.set_title(title)
    pdf.print_chapter()
    pdf.output("John Doe Cover Letter %s.pdf"%counter, 'F')
    # set your prefered save destination on your pc and change name of file to suit your need


# 1. Automated version

# In[ ]:


# Modify here for your contact details
header="              John Doe    |   (555) 555-5555   |   john.doe@gmail.com   |   linkedin.com/in/john-doe"


counter=0
for response,desc in zip(cover_letters, df.iloc[:3,7]):
    counter+=1
    title = 'Application for the Data Analyst position'
    x=text_message = response[0]['choices'][0]['message']['content']
    textraw = "\n\n\n\n\n\n\n\n"+x
    print("description of job is :", desc)
    text=text_editor(textraw)
    pdf = PDF(header, title, text,path)
    pdf.set_title(title)
    pdf.print_chapter()
    pdf.output("John Doe Cover Letter %s.pdf"%counter, 'F')
    # set your prefered save destination on your pc and change name of file to suit your need

