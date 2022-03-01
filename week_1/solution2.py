import sys

counter = int(sys.argv[1])

output = " " * (counter - 1)
for index in range(counter):
    output += '#'
    print(output[index:])
