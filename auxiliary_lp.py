import numpy as np 
from pdb import set_trace
import math

from commons import pivoting, put_tableux_form, put_pl_form, parse_to_fpi,put_identity_matrix,put_canonical_form
from primal_simplex import solve as solve_primal_simplex

def transform_b_positive(matrix):
	for index in range(1,(matrix.shape[0])):
		if matrix[index,-1] < 0:
			matrix[index,:] = (-1)*matrix[index,:] 
	return matrix

def zero_vector_b(matrix):
	matrix_A_lines = (matrix.shape[0]-1)
	matrix[0,:] = 0
	return matrix

def solve(matrix):
	print("Solving auxiliary pl.")

	base_columns = np.zeros(matrix.shape[0])
	print("FPI")
	matrix = parse_to_fpi(matrix)
	print(matrix)

	print("B POSITIVO")
	matrix = transform_b_positive(matrix)
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
	print("forma canonica")
	matrix = put_canonical_form(matrix,base_columns)
	print(matrix)
	#solve_primal_simplex(matrix)


	#matrix = put_tableux_form(matrix)

	#primal_simplex(matrix)
	#put_pl_form(matrix)