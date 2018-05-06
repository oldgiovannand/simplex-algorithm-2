import numpy as np 
from pdb import set_trace
import copy
import math

def put_identity_matrix(matrix,position,size):
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

def put_tableux_form(matrix):
	matrix_A_lines = (matrix.shape[0]-1)
	matrix = put_identity_matrix(matrix,0,matrix_A_lines)
	matrix[0,:] = (-1)*matrix[0,:] 
	return matrix

def put_pl_form(matrix):
	begin_C_columns = matrix.shape[0]-1
	end_C_columns = matrix.shape[1]-1
	matrix[0,begin_C_columns:end_C_columns] = (-1)*matrix[0,begin_C_columns:end_C_columns] 

def find_c_negative(matrix): 
	begin_A_columns = matrix.shape[0]-1
	end_A_columns = matrix.shape[1]
	for index in range(begin_A_columns, end_A_columns):
		if matrix[0,index] < 0:
			return index
	return (-1)

def find_b_negative(matrix):

	column_B = matrix.shape[1]-1 #ultima coluna da matriz
	matrix_lines = matrix.shape[0]+1
	for index in range(1,matrix_lines):
		if matrix[column_B,index] < 0:
			return index
	return (-1)

def find_pivot_primal_simplex(matrix,c_index): #TRATAR O CASO EM QUE O MENOS INDICE È ZERO - REGRA DE BLAND
	min_value = math.inf
	min_index = None

	for index in range(1, matrix.shape[0]):
		if matrix[index, c_index] <= 0:
			continue

		curr_value = matrix[index, -1] / matrix[index,c_index]
		if curr_value < min_value:
			min_value = curr_value
			min_index = index

	return min_index # em caso de none, tratar PL ilimitada se c for menor que zero. C = 0, ainda nao define estado de ilimitada


def find_pivot_dual_simplex(matrix,b_index):
	min_value = math.inf
	min_index = None

	begin_A_columns = matrix.shape[0] -1
	end_A_columns = matrix.shape[1]

	for index in range(begin_A_columns,end_A_columns):
		if matrix[b_index, index] >= 0:
			continue

		curr_value = matrix[0,index] / matrix[b_index,index]
		if curr_value < min_value:
			min_value = curr_value
			min_index = index

	return min_index # em caso de none, tratar PL ilimitada se c for menor que zero. C = 0, ainda nao define estado de ilimitada

def pivoting(matrix,line_index, column_index):
	for index in range(0,matrix.shape[0]):
		if index == line_index:
			matrix[index,:] = matrix[index,:]/matrix[line_index,column_index]
		else:
			matrix[index,:] = matrix[line_index,:]*( (-matrix[index,column_index])/matrix[line_index,column_index])+matrix[index,:]	
	
	print("\nPivoteamento:("+str(line_index)+","+str(column_index)+")\n")
	print (matrix)

def verify_state(matrix):	
	begin_C_columns = matrix.shape[0]-1
	end_C_columns = matrix.shape[1]-1
	if (all( i >=0 for i in matrix[0,begin_C_columns:end_C_columns]) ) and (all(i >=0 for i in matrix[1:,-1]) ):
		return True
	elif (all( i <=0 for i in matrix[0,begin_C_columns:end_C_columns]) ):
		return None #passar para simplex dual
	else:
		return False #continua simplex primal

def primal_simplex(matrix):
	#set_trace()
	c_index = find_c_negative(matrix) #tratar caso (-1) - nao tem c negativo
	line_index =  find_pivot_primal_simplex(matrix,c_index)
	pivoting(matrix,line_index,c_index)
	state = verify_state(matrix)
	if(state):
		return
	elif(state is None):
		#executar simples dual
		pass	
	else:
		primal_simplex(matrix)


def main():

#f = open('teste1.txt', 'r')

#linhas 	= 4  #f.readline()
#colunas = 7#f.readline()

	matrix = np.array([[3,2,4,0],[1,1,2,4],[2,0,3,5],[2,1,3,7]],dtype=float)

	print("\nMatriz inicial:\n")
	print(matrix)
	matrix = parse_to_fpi(matrix)
	print(matrix)
	matrix = put_tableux_form(matrix)
	print(matrix)
	#primal_simplex(matrix)

	#primal_simplex(matrix)
#	print("\nMatriz final: \n")
#	put_pl_form(matrix)#mudar o formato para que o valor objetivo nao fique negativo na hora errada
#	print(matrix)


# identidade = np.identity(2,float)

main()