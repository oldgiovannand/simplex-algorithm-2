import numpy as np 
from pdb import set_trace
import math

from commons import pivoting, put_tableux_form, put_pl_form, parse_to_fpi

def find_b_negative(matrix):
	matrix_lines = matrix.shape[0]
	for index in range(1,matrix_lines):
		if matrix[index,-1] < 0:
			return index
	return None

def find_pivot_dual_simplex(matrix,b_index):
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


def solve(matrix):
	print("Solving dual simplex.")
	matrix = parse_to_fpi(matrix)
	matrix = put_tableux_form(matrix)

	dual_simplex(matrix)
	put_pl_form(matrix)