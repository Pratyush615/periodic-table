#“Periodic Table of Elements.csv.” Github, 6 June 2017, gist.github.com/GoodmanSciences/c2dd862cd38f21b0ad36b8f96b4bf1ee. Accessed 8 Apr. 2023.

#--------Importing Modules-----------

import math
import pandas as pd
import tkinter as tk
from tkinter import messagebox
import random as rand

#-------------SETUP--------------------

#Defining variables needed for creating and spacing out the electrons and their orbitals
different_radii = {'1':7,'2':9,'3':12,'4':15,'5':17,'6':19,'7':21}
spacing=0

#Defining variables needed for the button layout
num_columns = 10
num_rows = 9
row = 0
color_of_button = 'WHITE'

#A dictionary which stores the colors for each type of corresponding element
types_of_elements = {'Alkali metals':'#1F51FF', 'Alkaline earth metals':'#FF3131', 'Transition metals':'#39FF14','Post-transition metals':'#83EEFF','Metalloids':'#FF10F0','Reactive nonmetals':'#9D00FF','Noble gases':'#FFFF33','Transition Metal':'#39FF14','Lanthanides':'#2D9A4D','Actinides':'#C47926','Unknown properties':'#808080'}

#Reading the CSV file from which the program derives its data
elementsdf = pd.read_csv("Periodic.csv")

#Initializing the Tkinter window and giving it a title
root = tk.Tk()
root.title("Perioidic Table of Elements")

#--------------------FUNCTIONS------------------------

# ^Main Function 1^ : Element Search System
def search():

    element_searched = enter_element.get()

    #These if and elif statements are used to convert the input we get from the user into data that this program can use. It is also used to detect input that won't work.


    #This detects if the input the user has used to request for an element is a number (searching by atomic number)
    if element_searched.isdigit():
        #Detects if the input is within the acceptable/working range
        if int(element_searched) >0 and int(element_searched) <=118:
            #subtracting by one to get the index
            element_searched=int(element_searched)-1
            print(element_searched)
            #Calls the element_clicked function uwith the index of the element searched
            element_clicked(int(element_searched))
        else:
            #Opens warning messagebox to inform user that the input in the searchbox was wrong
            tk.messagebox.showwarning("Alert", "The atomic number must be between 1 and 118!")

    #This detects if the input the user has used to request for an element is greater than 2 characters in length (searching by the full element name)
    elif len(element_searched) >2:
        try:
            #Capitalize the first letter because that is how it is saved as in our data
            element_searched = element_searched.capitalize()  
            #Locating what row in the data the element is on      
            locate_row = elementsdf.loc[elementsdf['Element'] == element_searched]
            #Getting the atomic number of the element and then subtracting by one to get the index as that is how the program gets the data in the function
            element = int(locate_row.iloc[0]['AtomicNumber'])-1
            #Calls the element_clicked function with the index of the element searched
            element_clicked(element)
        except:
            #Opens warning messagebox to inform user that the input in the searchbox was wrong
            tk.messagebox.showwarning("Alert", "This element could not be found, please make sure to use valid characters!")

    #This detects if the input the user has used to request for an element is less than or equal to 2 characters in length (searching by symbol)
    else:
        try:
            #Capitalize the first letter because that is how it is saved as in our data
            element_searched = element_searched.capitalize()   
            #Locating what row in the data the element is on      
            locate_row = elementsdf.loc[elementsdf['Symbol'] == element_searched]
            #Getting the atomic number of the element and then subtracting by one to get the index as that is how the program gets the data in the function
            element = int(locate_row.iloc[0]['AtomicNumber'])-1
            #Calls the element_clicked function with the index of the element searched
            element_clicked(element)
        except:
            #Opens warning messagebox to inform user that the input in the searchbox was wrong
            tk.messagebox.showwarning("Alert", "This element could not be found, please make sure to use valid characters!")
            
# ^Main Function 2^ : element being clicked detection + Creation of Search button
def element_clicked(element):
    
    global spacing
    
    #Locating and Storing the data for the element that was requested in an appropriately named variable
    atomic_number = elementsdf.iloc[element,0]
    element_name = elementsdf.iloc[element,1]
    number_of_neutrons = elementsdf.iloc[element,4]
    atomic_mass = elementsdf.iloc[element,3]
    period = elementsdf.iloc[element,7]
    group = elementsdf.iloc[element,8]

    #Creating another Tkinter Page + titling
    element_page = tk.Tk()
    element_page.title(element_name)
    
    #Creating a canvas to use to draw the element's atomic model on
    canvas = tk.Canvas(element_page, width=1400, height=1000)
    canvas.pack()

    #This forloop creates a proton every time it is executed
    for i in range(0, atomic_number):
        #Sets x and y coordinates to be in a spiral shape with the random module being used to a
        xcoord = (i*math.sin(i)/8) + rand.randint(890, 900)
        ycoord = (i*math.cos(i)/8) + rand.randint(490, 500)
        radius = 8
        #creates a circle represent
        proton = canvas.create_oval(xcoord-radius,ycoord-radius,xcoord+radius,ycoord+radius,fill='red')

    #This forloop creates a neutron every time it is executed
    for i in range(0, number_of_neutrons):
        xcoord = (i*math.sin(i)/8) + rand.randint(890, 900)
        ycoord = (i*math.cos(i)/8) + rand.randint(490, 500)
        radius = 8
        #creates a circle represent
        neutron = canvas.create_oval(xcoord-radius,ycoord-radius,xcoord+radius,ycoord+radius,fill='white')

        #It lowers the neutron depths on the screen so the neutrons do not overlap all the protons
        if i%2 or i%3 or i%5:
            canvas.lower(neutron)

    #Gets the electron configuation of the atom
    locate_element = elementsdf.loc[elementsdf['Element'] == element_name]
    electron_config = locate_element.iloc[0]['ElectronConfiguration']

    #Splitting the electron configuration and splitting of based off every space, turning it into a list
    split = electron_config.split(' ')

    for t in split:
        
        radius=different_radii.get(t[0])
        #Creates the orbital 
        orbital_trail = canvas.create_oval(895-math.pow(radius,2), 495-math.pow(radius,2), 895+math.pow(radius,2), 495+math.pow(radius,2), width=1)   

        for k in range(0,int(t[2:])):

            spacing+=99
            angle=math.pi*spacing/14

            x_coord = 895+radius*math.cos(angle)*radius
            y_coord = 495+radius*math.sin(angle)*radius

            electron = canvas.create_oval(x_coord-5, y_coord-5, x_coord+5, y_coord+5, fill='green')     
    
    #Displaying the info on the new window created:

    #Displaying the name + position
    name = tk.Label(element_page,text=element_name,font="Times 25 bold")
    name.place(x=100,y=100)

    #Displaying the mass + position
    mass = tk.Label(element_page,text="Atomic Mass: "+str(atomic_mass),font="Times 20 bold")
    mass.place(x=100,y=200)

    mass = tk.Label(element_page,text="Atomic Number / Number of Protons / Number of Electrons: "+str(atomic_number),font="Times 20 bold")
    mass.place(x=100,y=300)

    #Displaying the neutrons + position
    num_neutrons = tk.Label(element_page,text="Number of Neutrons: "+str(number_of_neutrons),font="Times 20 bold")
    num_neutrons.place(x=100,y=400)

    #Displaying the period + position
    period = tk.Label(element_page,text="Period Number: "+str(math.ceil(period)),font="Times 20 bold")
    period.place(x=100,y=500)

    #Displaying the group + position
    group = tk.Label(element_page,text="Group Number: "+str(math.ceil(group)),font="Times 20 bold")
    group.place(x=100,y=600)

    #Keeping the tab open
    element_page.mainloop()


# ^Main Function 3^ : Creating the table with the buttons and the spacing
def create_table():
    global row,num_columns,num_rows,color_of_button

    for x in range(0,len(elementsdf['AtomicNumber'])):
        color_of_button = types_of_elements[elementsdf.iloc[row,15]]
        button = tk.Button(root,text=elementsdf.iloc[row,2],font="Times 20 bold", height=3, width= 5,background=color_of_button,highlightbackground=color_of_button,highlightthickness=3,activebackground=color_of_button, command= lambda row=row: element_clicked(row))
        button.place(x=elementsdf.iloc[row,8]*100+130, y=elementsdf.iloc[row,7]*100)

        atomic_number = tk.Label(root,text=elementsdf.iloc[row,0],font="Times 10 bold",background='#eeefef',fg='black')
        atomic_number.place(x=elementsdf.iloc[row,8]*100+190, y=elementsdf.iloc[row,7]*100+10)

        full_name = tk.Label(root,text=elementsdf.iloc[row,1],font="Times 10 bold",bg='#eeefef',fg='black')
        full_name.place(x=elementsdf.iloc[row,8]*100+136, y=elementsdf.iloc[row,7]*100+60)

        row+=1
    
#Search Button Making:

#Creating the Text on screen
search_text = tk.Label(root, text='Search For Element', font=("Times", 30))
search_text.place(x=800,y=75)

#Creating the space where the user can type in the element they want, bd sets the border length
enter_element = tk.Entry(root, bd=3)
enter_element.place(x=825,y=150)

#The Search button, we make it that it calls on the search function when it is clicked
search_button = tk.Button(root ,text='search', command=search)
search_button.place(x=882,y=200)


#--------------WRAPPING UP-------------

#Calls function
create_table()

#Keeps main window open
root.mainloop()