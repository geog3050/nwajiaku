#Create a script that examines a string for the occurrence of a particular letter. If the letter occurs in the text (for example, the letter Z), the string “Yes” should be printed to the Interactive Window. If the letter does not occur in the text, the string “No” should be printed.

#HINT: You can use input() function to create a list:

#mystr = input('enter a string:')

mystr = input('Enter a string: ')

letter_presence = 'L'

# Check if the letter occurs in the string
if letter_presence in mystr:
    print("Yes")
else:
    print("No")


#Create a script that examines a list of numbers (for example, 2, 8, 64, 16, 32, 4) determines the second-largest number.

#HINT: You can use mylist.sort() function to sort the array.


numbers = input('Enter a list of numbers separated by commas: ')

# Convert string to integer
numbers_list = [int(num) for num in numbers.split(',')]

# Sort in ascending order
numbers_list.sort()

if len(numbers_list) >= 2:
    second_largest = numbers_list[-2]
    print("Second-largest number:", second_largest)
else:
    print("The list should have at least two numbers to determine the second-largest.")


#Create a script that examines a list of numbers (for example, 2, 8, 64, 16, 32, 4, 16, 8) to determine whether it contains duplicates. The script should print a meaningful result, such as “The list provided contains duplicate values” or “The list provided does not contain duplicate values.” An optional addition is to remove the duplicates from the list.

#HINT: You can use list.count(value) to determine how many occurrences of a value exists in a list. 

numbers = input('Enter a list of numbers separated by commas: ')

# Convert string to integer.
numbers_list = [int(num) for num in numbers.split(',')]

# Check for duplicates
duplicates = any(numbers_list.count(num) > 1 for num in numbers_list)

# Display result
if duplicates:
    print("This list has duplicate values.")
else:
    print("This list does not have duplicate values.")
