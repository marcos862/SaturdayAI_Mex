'''
Exercise 1

Create a program that asks the user to enter their name and their age. 
Print out a message addressed to them that tells them the year that 
they will turn 100 years old.

Extras:
 1. Add on to the previous program by asking the user for another number 
    and printing out that many copies of the previous message. 
    (Hint: order of operations exists in Python)
 2. Print out that many copies of the previous message on separate lines. 
    (Hint: the string "\n is the same as pressing the ENTER button)

'''
import datetime

currYear = datetime.date.today().year

name = input("Introduce your name: ")
age = input("Now, introduce your age: ")
calc = (100 - int(age)) + currYear
repeats = input("How Many times do you want to repeat the msg? ")
outputStr = "Hi {}, you will have 100 years in the year\n".format(name, calc)
print(outputStr * int(repeats))
