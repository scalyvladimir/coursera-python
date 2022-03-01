from solution import FileReader

reader = FileReader('not_exist_file.txt')
print(reader.read())
with open('some_file.txt', 'w') as file:
    file.write('some text')
reader = FileReader('some_file.txt')
print(reader.read(), type(reader), sep='\n')
