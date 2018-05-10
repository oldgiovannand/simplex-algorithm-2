import numpy as np 
from pdb import set_trace
import math

from commons import pivoting, put_tableux_form, put_pl_form, parse_to_fpi,put_identity_matrix,put_canonical_form
from primal_simplex import verify_state_primal,find_c_negative,find_pivot_primal_simplex

def transform_b_positive(matrix):
	for index in range(1,(matrix.shape[0])):
		if matrix[index,-1] < 0:
			matrix[index,:] = (-1)*matrix[index,:] 
	return matrix

def zero_vector_b(matrix):
	matrix_A_lines = (matrix.shape[0]-1)
	matrix[0,:] = 0
	return matrix

def prepare_for_primal_simplex(matrix,original_matrix,base_columns):
	print("original eh otima")	
	begin_c = matrix.shape[0]-1
	end_c = matrix.shape[1]-matrix.shape[0]-1
	print(matrix)
	print(begin_c)
	print(end_c)
	print("FPI")
	original_matrix = parse_to_fpi(original_matrix)
	print(original_matrix)

	print("matriz identidade")
	original_matrix = put_identity_matrix(original_matrix,original_matrix.shape[1]-1,original_matrix.shape[0]-1,0)
	print(original_matrix)

	print("forma de tableux")	
	original_matrix = put_tableux_form(original_matrix)
	print(original_matrix)
	original_matrix[1:original_matrix.shape[0], 0:end_c ] = matrix[1:matrix.shape[0], 0:end_c ]
	original_matrix[1:original_matrix.shape[0], -1 ] = matrix[1:matrix.shape[0], -1]
	print(original_matrix)
	print(base_columns)

	original_matrix = put_canonical_form(original_matrix,base_columns)
	print(matrix)
	print(jhdbjhadb)
	#colocar a matrix na nova base
	#executar simplex primal 
	pass#a primal tem otimo e a matriz de operacoes


def primal_simplex_auxiliar_pl(matrix,base_columns,original_matrix):
	c_index = find_c_negative(matrix) 
	ilimit = 0
	if (c_index is not None): #ainda temos entradas de (-c) no tableux negativas
		line_index =  find_pivot_primal_simplex(matrix,c_index)
		if (line_index is not None): #temos, na coluna c_index escolhida, valores de A maiores que zero
			pivoting(matrix,line_index,c_index)
			base_columns[line_index] = c_index
		elif(matrix[0,c_index] < 0 ): #situação de pl ilimitada
			pass
			#ilimit = 1
			#unlimited_certificate(matrix,c_index,base_columns)
		else:
			raise "Deu merda - escolhi c_index = 0, com uma coluna toda menor ou igual a zero"
	if(ilimit != 1):
		state = verify_state_primal(matrix)
		if(state): #situacao de ótimo	
			if ( (matrix[0,-1]) == 0 ):
				print("otimo")
				print(matrix)
				prepare_for_primal_simplex(matrix,original_matrix,base_columns)
			else:
				print("inviavel")
				print(matrix)
				print("0")
				print(str((matrix[0,0:(matrix.shape[0]-1)]).tolist())) 
			return
		elif(state is None):
			#executar simples dual
			pass	
		else:
			primal_simplex_auxiliar_pl(matrix,base_columns,original_matrix)


def solve(matrix):
	print("Solving auxiliary pl.")
	original_matrix = matrix
	base_columns = np.zeros(matrix.shape[0])
	print("FPI")
	matrix = parse_to_fpi(matrix)
	print(matrix)

	print("VETOR C ZERADO")
	matrix = zero_vector_b(matrix)
	print(matrix)
	print("matriz identidade")
	matrix = put_identity_matrix(matrix,matrix.shape[1]-1,matrix.shape[0]-1,-1)
	print(matrix)
	print("forma de tableux")
	matrix = put_tableux_form(matrix)
	print(matrix)

	print("B POSITIVO")
	matrix = transform_b_positive(matrix)
	print(matrix)

	print("forma canonica")

	end_c = matrix.shape[1]-matrix.shape[0]
	for index in range(1,(matrix.shape[0])):
		base_columns[index] =end_c
		end_c = end_c+1;
	matrix = put_canonical_form(matrix,base_columns)
	print(matrix)
	primal_simplex_auxiliar_pl(matrix,base_columns,original_matrix)