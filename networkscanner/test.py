result_url =[]
with open('result.txt','r') as file:
	temp_url = file.readlines()
	result_url = temp_url

row =0            
for index in result_url:
	print(index)
	print(type(index))
	print('two:' + str(row))
	row = row +1
	
	