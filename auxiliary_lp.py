import numpy as np 
from pdb import set_trace
import math

from commons import pivoting, put_tableux_form, put_pl_form, parse_to_fpi,put_identity_matrix
from primal_simplex import solve as solve_primal_simplex

def transform_b_positive(matrix):
	for index in range(1,matrix.shape[1]):
		if matrix[index,-1] < 0:
			matrix[index,:] = (-1)*matrix[index,:] 

def solve(matrix):
	print("Solving auxiliary pl.")
	matrix = parse_to_fpi(matrix)
	transform_b_positive(matrix)
	put_identity_matrix(matrix,matrix.shape[1]-1,matrix.shape[0]-1,-1)
	print(matrix)
	solve_primal_simplex(matrix)


	#matrix = put_tableux_form(matrix)

	#primal_simplex(matrix)
	#put_pl_form(matrix)