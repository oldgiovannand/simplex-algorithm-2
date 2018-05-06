import numpy as np 
from pdb import set_trace
import math

from commons import pivoting, put_tableux_form, put_pl_form, parse_to_fpi

def find_c_negative(matrix): 
	begin_A_columns = matrix.shape[0]-1
	end_A_columns = matrix.shape[1]
	for index in range(begin_A_columns, end_A_columns):
		if matrix[0,index] < 0:
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

def verify_state_primal(matrix):	
	begin_C_columns = matrix.shape[0]-1
	end_C_columns = matrix.shape[1]-1
	if (all( i >=0 for i in matrix[0,begin_C_columns:end_C_columns]) ) and (all(i >=0 for i in matrix[1:,-1]) ):
		return True
	elif (all( i >=0 for i in matrix[0,begin_C_columns:end_C_columns]) ):
		return None #passar para simplex dual
	else:
		return False #continua simplex primal

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


def solve(matrix):
	print("Solving primal simplex.")
	matrix = parse_to_fpi(matrix)
	matrix = put_tableux_form(matrix)

	primal_simplex(matrix)
	put_pl_form(matrix)