# Cover letter generator in ChatGPT turbo 3.5

Applications to jobs can be a tedious task, and while resumes can be reused often, cover letters need to be personalized to particular companies and positions. If your strategy is to apply to a wide area of companies and locations, this can take quite a lot of time, which you could spend learning a new skill for a position that is hard to get. 

With the widespread use of ChatGPT, this process can be simpliied by asking OpenAI's free, for now, online tool. However, if you are skilled in Python programming, you can use the following script to take advantage of the affordable API version gpt-3.5-turbo released in March of 2023 and available until June of that year.


## Getting Started

### Installing the modules

1. OpenAI

```shell
pip install transformers # a dependency of openai
pip install openai
```

2. Pandas

```shell
pip install pandas
```

 
3. FPDF
```shell
pip install fpdf
```

We start by accessing the required libraries:

```python
### Setup the libraries, paths and folders

import os
import openai
import tkinter as tk
from tkinter import scrolledtext
from datetime import date
from fpdf import FPDF
import pandas as pd 

```

We will later on depend on a set of functions to create the cover letter. First, we need a function that opens an editing window, called "text_editor". This is because, as we know, ChatGPT doe not provide 100% accurate results. This function contains a nested function, save_text, which performs said task once you are satisfied with the content.


```python
def text_editor(txt):
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
```

The other object we need is the PDF class objet, based on the FPDF package. There, we need to define several functions that dictate aspects of the PDF template:

```python
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


```
The PDF class is a subclass of the FPDF class and it provides a customized way of generating a PDF document. The class takes four required arguments head, titl, txt and pth, which are used to set the header, title, path and content of the document respectively. Here is a brief description of the methods in the PDF class:

* __init__(self, head, titl, txt, pth, *args, **kwargs): This is the constructor method of the class, which sets the details, title, text and save path attributes. It also calls the constructor of the parent class FPDF and passes any additional arguments and keyword arguments to it.

* header(self): This method defines the header section of the PDF document, which includes the details attribute set in the constructor. It sets the font, color, and line width of the text, and adds the header text using the cell method. 

* content(self): This method defines the content section of the PDF document, which includes the text attribute set in the constructor. It sets the font, color, margins, and line width of the text, and adds the content text using the multi_cell method.

* application(self): This method defines the application section of the PDF document, which includes the title attribute set in the constructor. It sets the font, color, line width, and alignment of the text, and adds the application text using the cell method.

* date_format(self): This method defines the date format used in the PDF document, which formats the current date in the format of "dayth of month, year". It checks the day value to append the correct suffix, such as "st", "nd", "rd", or "th", to the day value.

* date(self): This method defines the date section of the PDF document, which includes the formatted date generated by the date_format method. It sets the font, color, and margins of the text, and adds the date text using the cell method.

* print_chapter(self): This method prints a chapter of the PDF document, which includes the header, content, application, and date sections. It also adds graphics to the chapter by defining a rectangle using the rect method. It uses the add_page method to add a new page to the document, and calls the header, content, application, and date methods to add their respective sections to the chapter. It also adds custom fonts to the document using the add_font method.

The fonts required can be found in the documentation in the Fonts folder. Other fonts may be placed there and refered to in the PDF class object.


An important first step now that we have all the tools we need is to access the ChatGPT API. To do that, the first step is to create account at https://platform.openai.com/account, and then create an API key. You will be taken to Settings next, where you can get your Organization ID, the one starting with "org-...". You can give a normal organization name in a different field, but it will not be used in the code itself.

<img width="954" alt="organization" src="https://user-images.githubusercontent.com/47111504/223856153-49a31b94-ec56-4414-bc29-1478fa940fb6.png">

You will also need to generate and paste the the key to ccess the API, lower in the API keys tab:

<img width="956" alt="api" src="https://user-images.githubusercontent.com/47111504/223856149-9a4b9d3c-36f5-4d85-b944-4adee1e9ee3f.png">

Once you start running the script, you should keep an eye on your usage gauge:
<img width="959" alt="usage" src="https://user-images.githubusercontent.com/47111504/223856160-aabbc67e-c8e8-41b9-976c-80c5fca0db17.png">

Now that we have both access parameters, we can place them in the script:

``` python
openai.organization = "org-****************JZ"
openai.api_key = "sk-Bq*********************************FtajU26W"
openai.Model.list()
``` 
  You should see this kind of message if succesful:
 <img width="728" alt="accessed gpt" src="https://user-images.githubusercontent.com/47111504/223870144-ca225951-d5e0-429c-a1c7-1af0c178d0a2.png">


Before we generate the query for ChatGPT, we need several dependent text files. Firt of all, is your CV/Resume. You should place in a text file esential aspect of your experience. Leave out whatever is not important for the cover letter content, because you have a limit of 4000 tokens between your query and the answer ChatGPT can generate, and you may get an error when trying to get an answer later on. I reccommend sticking to your name, bio, all your main experiences and skills. Store this in a text file and upload as such:

``` python
# Load CV 
with open(r"C:\**********\cv.txt") as f:
    cv = f.readlines()
``` 

``` python
# Optional, load custom format of cover letter
with open(r"C:\***********\cover-letter-format-custom.txt") as f:    
    template = f.readlines()
```

There are two ways to use this script to generate Cover Leters.
1. Manual upload
``` python
#This is for manual job description upload. Press Run and then paste in the open field your desired job description.
JOB_DESCRIPTIONS=[]
job_number = 2 # change here to the number of descriptions you plan to upload

while job_number>=1:
    JOB_DESCRIPTIONS.append(input())
    job_number-=1
```

2. Automated, based on pre-existing database stored in a file. I mined mine from a famous jobs board using Beautiful Soup and Selenium. You can create your own by pasting in an excel file several job dscriptions, along with position, location, and whatever field you wish to make specific for ChatGPT to take under consideration.

``` python
df=pd.DataFrame(pd.read_excel(r"C:\*********\jobs.xlsx").iloc[:,:])
``` 
Note: The xlsx file, and by extension the dataframe for automated job description input, should have the following column names and order (or variation of choice):
Company, Location, Position available, Experience level, Company description, Job description.


The time has come to make our ask to ChatGPT.First, the manual job description input option as example:

``` python
#Cover letters are generatd in ChatGPT 3.5 Turbo
cover_letters=[]

### 1. Manual job input version:
manual_script=""" Given that this is the job description: %s  and my resume is: %s, write me a complete cover letter under 
                  1000 words addressed to Dear Hiring Manager, in the %s format, making sure only relevant experiences and skills 
                  that are mentioned in my CV are mentioned and it's easy to read, not cluttered with technical jargon."""

counter=0
for DESCRIPTION in JOB_DESCRIPTIONS:
    counter+=1
    if counter<3:
        command=manual_script %(DESCRIPTION,cv, template)
        #print(command)
        cover_letters.append([openai.ChatCompletion.create(model="gpt-3.5-turbo-0301", messages=[{"role": "system", "content": command}] 
    ,max_tokens=1000)])
    else:
        print("could not perform task")
        break
print("in total I created %s raw cover letters" %counter) 
print("output is: ", cover_letters)

#Give it few seconds or a minute to write the prompt.


### 2. Automated job input version:
cover_letters=[]
automated_script=""" There is a job opening at %s company in %s for %s position. Given that this is the job 
                     description: %s (and, if not n.a., this is the required experience, %s, and the company
                     description: %s), and my resume is: %s, write me a complete cover letter under 1500 words
                     addressed to Dear Hiring Manager, in the %s format (only fill in the prompts in the brackets
                     with content found in my CV), making sure it is easy to read, not cluttered with technical jargon."""

counter=0
for index, row in df.iterrows():
    counter+=1
    if counter<3:
        command= automated_script%(row[0],row[1],row[2],row[3],row[4],row[5],cv, template)
        print(command)
        cover_letters.append([openai.ChatCompletion.create(model="gpt-3.5-turbo-0301",prompt=command,max_tokens=1500)])
    else:
        break
print("in total I created %s cover letters" %counter)  
print("output is: ", cover_letters)

``` 

The output of this secton of the code should have this appearance in Jupyter Notebook:
<img width="603" alt="output example gpt" src="https://user-images.githubusercontent.com/47111504/223879951-a441f61c-1537-4c88-a4bf-bd25e30ba727.png">


The final component of the script is the loop using the raw cover letters and job descriptions to first edit every response and then save it to a formatted PDF file complete with header and date.

``` python
# Modify here for your contact details
header="              John Doe    |   (555) 555-5555   |   john.doe@gmail.com   |   linkedin.com/in/john-doe"
path=r'C:\*****************\CL writer'

counter=0
for response,desc in zip(cover_letters, JOB_DESCRIPTIONS): # note: JOB_DESCRIPTIONS will be replaced here with the "df" dataframe in case of automated input
    counter+=1
    title = 'Application for the Data Analyst position'
    x=text_message = response[0]['choices'][0]['message']['content']
    textraw = "\n\n\n\n\n\n\n\n"+x
    print("description of job is :", desc)
    text=text_editor(textraw)
    pdf = PDF(header, title, text,path)
    pdf.set_title(title)
    pdf.print_chapter()
    pdf.output(r'G:\Github saves\PRACTICE\Final cv tools\CL writer\John Doe Cover Letter %s.pdf'%counter, 'F')
    # set your prefered save destination on your pc and change name of file to suit your need
 ```
 This code snippet takes in two lists, cover_letters and JOB_DESCRIPTIONS, which contain the applicant's responses and the job descriptions, respectively. The program loops through each response and job description pair, and for each pair, it generates a cover letter PDF file.
 
The header variable contains the applicant's contact details, which are displayed at the top of each cover letter. The path variable contains the directory path where the cover letter PDF files will be saved.

Inside the loop, the program sets the title variable to the job position that the applicant is applying for. It then extracts the applicant's response from the response variable, and adds some extra new lines to create some space between the header and the response text. The text_editor() function is called to format the response text.

The PDF() function is called to create a new PDF object with the applicant's contact details, job position, and formatted response text. 

You will be prompted to edit the content of your cover letter in the Text editor window:
<img width="960" alt="editing view example" src="https://user-images.githubusercontent.com/47111504/223971927-e7309db6-f33f-411d-9e36-cb13d3fd9f52.png">

The job description in the terminal window will serve as a guide to correct any misunderstandings ChatGPT may have created.

The fictional example provided here produced several cover letters, including this example:
![John Doe Cover Letter 1](https://user-images.githubusercontent.com/47111504/223974646-9b3b86a7-f817-4d43-aa9d-326bd0715248.png)


Overall, the complete program can save a lot of time for job applicants who need to generate multiple cover letters with similar content. By automating the process, the program allows applicants to focus on customizing the response text for each job application.
