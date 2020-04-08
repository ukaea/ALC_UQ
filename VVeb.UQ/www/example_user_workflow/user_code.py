# --- Read file
filename = 'input_mc.csv'
file_read = open(filename, 'r')
values = []
for line in file_read:
    array_tmp = line.split()
    values.append(float(array_tmp[0]))
file_read.close()

# --- Do some state-of-the-art calculations
result = 0.0
for i in range(len(values)):
  result = result + values[i]

file_out = open('user_output.dat','w')
file_out.write('Sum of values is:')
file_out.write(str(result))
file_out.close()
