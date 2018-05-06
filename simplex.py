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
	return None

def find_b_negative(matrix):
	matrix_lines = matrix.shape[0]
	for index in range(1,matrix_lines):
		if matrix[index,-1] < 0:
			return index
	return None

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
	set_trace()
	min_value = math.inf
	min_index = None

	begin_A_columns = matrix.shape[0] -1


	for index in range(begin_A_columns,matrix.shape[1]-1):
		if matrix[b_index, index] >= 0:
			continue

		curr_value = matrix[0,index] / (-matrix[b_index,index])
		if curr_value < min_value:
			min_value = curr_value
			min_index = index

	return min_index 

def pivoting(matrix,line_index, column_index):
	for index in range(0,matrix.shape[0]):
		if index == line_index:
			matrix[index,:] = matrix[index,:]/matrix[line_index,column_index]
		else:
			matrix[index,:] = matrix[line_index,:]*( (-matrix[index,column_index])/matrix[line_index,column_index])+matrix[index,:]	
	
	print("\nPivoteamento:("+str(line_index)+","+str(column_index)+")\n")
	print (matrix)

def verify_state_primal(matrix):	
	begin_C_columns = matrix.shape[0]-1
	end_C_columns = matrix.shape[1]-1
	if (all( i >=0 for i in matrix[0,begin_C_columns:end_C_columns]) ) and (all(i >=0 for i in matrix[1:,-1]) ):
		return True
	elif (all( i >=0 for i in matrix[0,begin_C_columns:end_C_columns]) ):
		return None #passar para simplex dual
	else:
		return False #continua simplex primal

def verify_state_dual(matrix):	
	print(matrix)
	begin_C_columns = matrix.shape[0]-1
	end_C_columns = matrix.shape[1]-1
	print(begin_C_columns)
	print(end_C_columns)
	c_negative_in_PL = all( i >=0 for i in matrix[0,begin_C_columns:end_C_columns])
	b_positive = all(i >=0 for i in matrix[1:matrix.shape[0]-1,-1])
	print('c_negative_in_PL -> '+str(c_negative_in_PL))
	print('b_positive ->'+str(b_positive))
	if ( c_negative_in_PL ) and ( b_positive ):
		return True
	elif ( c_negative_in_PL ):
		return False #continua simplex dual
	else:
		return None #passar para simplex primal, teoricamente

def unlimited_certificate(matrix):
	pass

def primal_simplex(matrix):
	c_index = find_c_negative(matrix) 
	if (c_index is not None): #ainda temos entradas de (-c) no tableux negativas
		line_index =  find_pivot_primal_simplex(matrix,c_index)
		if (line_index is not None): #temos, na coluna c_index escolhida, valores de A maiores que zero
			pivoting(matrix,line_index,c_index)
		elif (matrix[0:c_index] < 0 ): #situação de pl ilimitada
			x = unlimited_certificate(matrix)
		else:
			raise "Deu merda - escolhi c_index = 0, com uma coluna toda menos ou igual a zero"

	state = verify_state_primal(matrix)
	if(state): #situacao de ótimo
		return
	elif(state is None):
		#executar simples dual
		pass	
	else:
		primal_simplex(matrix)

def dual_simplex(matrix):
	b_index = find_b_negative(matrix)
	if(b_index is not None): #ainda temos entradas de b no tableaux que são negativas
		column_index = find_pivot_dual_simplex(matrix,b_index)
		if(column_index is not None):#temos, na linha b_index, valores de A negativos
			pivoting(matrix,b_index,column_index)
		else: #situação de PL inviável - A da linha positivo com B da linha negativo e X>=0
			pass
	state = verify_state_dual(matrix)
	if(state): #situacao de ótimo
		return
	elif(state is None):
		#executar simples primal
		pass	
	else: #False
		dual_simplex(matrix)

def verify_method(matrix):
	begin_C_columns = matrix.shape[0]-1
	end_C_columns = matrix.shape[1]-1
	if (all( i >=0 for i in matrix[0,begin_C_columns:end_C_columns])) and (all(i >=0 for i in matrix[1:,-1]) ):
		return 0
	elif (all( i <=0 for i in matrix[0,begin_C_columns:end_C_columns]) ) and (not (all(i >=0 for i in matrix[1:,-1]))) :
		return 1 #passar para simplex dual
	elif (all( i >=0 for i in matrix[0,begin_C_columns:end_C_columns]) ):
		return 2 #continua PL Auxiliar


def main():

#TENTAR SEMPRE DUAL PRIMEIRO, DEPOIS PRIMAL E DEPOIS PL AUXILIAR 

#f = open('teste1.txt', 'r')

#linhas 	= 4  #f.readline()
#colunas = 7#f.readline()

	#exemplo simplex primal
	#matrix = np.array([[3,2,4,0],[1,1,2,4],[2,0,3,5],[2,1,3,7]],dtype=float)

	#exemplo simplex dual

	matrix = np.array([[-4,-8,-9,0],[2,-1,5,1],[3,-4,1,3],[-1,0,-2,-8]],dtype=float)

	print("\nMatriz inicial:\n")
	print(matrix)
	matrix = parse_to_fpi(matrix)

	method = verify_method(matrix)
	if(method == 0):

		print("simplex primal")
		matrix = put_tableux_form(matrix)
		primal_simplex(matrix)
		put_pl_form(matrix)
		#simplex_primal
		pass
	elif(method==1):
		print("simplex dual")
		matrix = put_tableux_form(matrix)
		dual_simplex(matrix)
		put_pl_form(matrix)
		#simplex_dual
		pass
	else:
		print("pl auxiliar")
		#pl auxiliar
		pass
	print('final')
main()