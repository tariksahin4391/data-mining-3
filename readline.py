# Writing to a file
file1 = open('temp_result_before.txt', 'w')
file1.write("\n")
file1.write("new line is here")
file1.close()

# Using readline()
file1 = open('temp_result_before.txt', 'r')
count = 0

while True:
    count += 1

    # Get next line from file
    line = file1.readline()

    # if line is empty
    # end of file is reached
    if not line:
        break
    print("Line{}: {}".format(count, line.strip()))

file1.close()

file2 = open("temp_result_before.txt", 'r')

for line in file2:
    print("Line : ", line)

file2.close()
