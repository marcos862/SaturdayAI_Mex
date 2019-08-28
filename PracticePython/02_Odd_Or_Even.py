"""
Exercise 2

Ask the user for a number. Depending on whether the number 
is even or odd, print out an appropriate message to the user. 
Hint: how does an even / odd number react differently when divided by 2?

Extras:
 1. If the number is a multiple of 4, print out a different message.
 2. Ask the user for two numbers: one number to check (call it num) 
    and one number to divide by (check). If check divides evenly 
    into num, tell that to the user. If not, print a different 
    appropriate message.

"""

num = int(input("Insert a number: "))
otherNum = int(input("Insert another number: "))
if num % 4 == 0:
    print("The number {} is a multiple of 4".format(num))
if((num % 2) == 1):
    result = "odd"
else:
    result = "even"
print("The number {} is an {} number".format(num, result))

if num % otherNum == 0:
    print("The number {} is divided by {} evenly".format(num, otherNum))
else:
    print("The number {} is not divided by {} evenly".format(num, otherNum))