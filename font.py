# Python code to
# demonstrate readlines()
 
 
# Using readlines()
file1 = open('font.txt', 'r')
Lines = file1.readlines()
 
paths = []
names = []
style = []
# Strips the newline character
for line in Lines:
    tmp = line.split(':')
    paths.append(tmp[0]) 
    names.append(tmp[1]) 
    style.append(tmp[2]) 

print(names)