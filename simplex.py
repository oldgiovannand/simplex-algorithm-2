import numpy as np 
import math

def parse_to_fpi(matrix):
	print(oi)

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
	#add identity matrix in left side
	#matriz[1:] . (-) (multiplica primeira linha por -1)
	pass

def find_c_positive(matrix): 
	begin_A_columns = matrix.shape[0]
	end_A_columns = matrix.shape[1]
	for index in range(begin_A_columns, end_A_columns):
		if matrix[0,index] >= 0:
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

	begin_A_columns = matrix.shape[0] 
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
	print (matrix)
# def main():
f = open('teste1.txt', 'r')

linhas 	= 4  #f.readline()
colunas = 7#f.readline()

# texto = f.readline()
# print(texto+'\n')
matrix = np.array([[0,0,0,-3,-2,-4,0,0,0,0],[1,0,0,1,1,2,1,0,0,4],[0,1,0,2,0,3,0,1,0,5],[0,0,1,2,1,3,0,0,1,7]],dtype=float)

# 0 0 0| 3 2 4 0 0 0 | 0
# - - - - - - - - - - - - - 
# 1 0 0| 1 1 2 1 0 0 | 4
# 0 1 0| 2 0 3 0 1 0 | 5
# 0 0 1| 2 1 3 0 0 1 | 7
#

canonical_form(matrix)
# identidade = np.identity(2,float)
# print(identidade)
# matriz = np.array(texto)
# print(matriz[0,2])
# print('\n')	
# type(matriz)

