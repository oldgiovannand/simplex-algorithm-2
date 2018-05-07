import numpy as np


def put_identity_matrix(matrix, position, size,value):
	adicional_row = np.zeros(size)
	adicional_row = adicional_row+value
	identity = np.identity(size)
	sub_matrix = np.insert(identity, 0, adicional_row, axis=0)

	arrays_list = []
	for line_index in range(matrix.shape[0]):
		extended_row = np.insert(matrix[line_index], position, sub_matrix[line_index])
		arrays_list.append(extended_row)
	return np.array(arrays_list)

def parse_to_fpi(matrix):
	matrix_A_lines = (matrix.shape[0]-1)
	return put_identity_matrix(matrix,matrix_A_lines,matrix_A_lines,0)

def put_tableux_form(matrix):
	matrix_A_lines = (matrix.shape[0]-1)
	matrix = put_identity_matrix(matrix,0,matrix_A_lines,0)
	matrix[0,:] = (-1)*matrix[0,:] 
	return matrix

def put_pl_form(matrix):
	begin_C_columns = matrix.shape[0]-1
	end_C_columns = matrix.shape[1]-1
	matrix[0,begin_C_columns:end_C_columns] = (-1)*matrix[0,begin_C_columns:end_C_columns] 

def pivoting(matrix, line_index, column_index):
	for index in range(0,matrix.shape[0]):
		if index == line_index:
			matrix[index,:] = matrix[index,:]/matrix[line_index,column_index]
		else:
			matrix[index,:] = matrix[line_index,:]*( (-matrix[index,column_index])/matrix[line_index,column_index])+matrix[index,:]	
	
	f = open('primeiro.txt', 'r')
	conteudo = f.readlines()

	conteudo.append(str(matrix.tolist()))
	f = open('primeiro.txt', 'w')
	f.writelines(conteudo)
	f.close()

def canonical_form(matrix,base_columns):
	if(not verify_canonical_form(matrix,base_columns)):
		put_canonical_form(matrix,base_columns)

def verify_canonical_form(matrix,base_columns):
	pl_canonical_form = False; 

	begin_A_columns = matrix.shape[0]-1
	for index in range(begin_A_columns,matrix.shape[1]):
		count_ones = 0
		base = None
		if (matrix[0,index] == 0):
			for line in range(1,matrix.shape[0]):				
				if(matrix[line,index] == 1):
					count_ones+=1
					base = line
				elif(matrix[line,index] == 0):
					continue
				else:
					base = None
					break
		if(base is not None and count_ones == 1):
			base_columns[base] = index #para a base da linha 'base', meu pivo encontra-se na coluna base_columns[base]

	if(all( i >0 for i in base_columns)):
		return True
	else:
		return False
		#verifica se está em forma canonica
	
	return pl_canonical_form;

def put_canonical_form(matrix,base_columns):
	#coloca em forma canonica
	pass
