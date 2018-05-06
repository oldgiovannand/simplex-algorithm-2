import numpy as np


def put_identity_matrix(matrix, position, size):
	adicional_row = np.zeros(size)
	identity = np.identity(size)
	sub_matrix = np.insert(identity, 0, adicional_row, axis=0)

	arrays_list = []
	for line_index in range(matrix.shape[0]):
		extended_row = np.insert(matrix[line_index], position, sub_matrix[line_index])
		arrays_list.append(extended_row)
	return np.array(arrays_list)

def parse_to_fpi(matrix):
	matrix_A_lines = (matrix.shape[0]-1)
	return put_identity_matrix(matrix,matrix_A_lines,matrix_A_lines)

def put_tableux_form(matrix):
	matrix_A_lines = (matrix.shape[0]-1)
	matrix = put_identity_matrix(matrix,0,matrix_A_lines)
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
	
	print("\nPivoteamento:("+str(line_index)+","+str(column_index)+")\n")
	print (matrix)

def canonical_form(matrix):
	if(not verify_canonical_form(matrix)):
		put_canonical_form(matrix)

def verify_canonical_form(matrix):
	pl_canonical_form = False; 
	#verifica se está em forma canonica
	
	return pl_canonical_form;

def put_canonical_form(matrix):
	#coloca em forma canonica
	pass
