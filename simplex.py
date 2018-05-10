import numpy as np 
from pdb import set_trace
import math

from primal_simplex import solve as solve_primal_simplex
from dual_simplex import solve as solve_dual_simplex
from auxiliary_lp import solve as solve_auxiliary_lp


def verify_method(matrix):
	begin_C_columns = 0
	end_C_columns = matrix.shape[1]-2
	if (all( i >=0 for i in matrix[0,begin_C_columns:end_C_columns])) and (all(i >=0 for i in matrix[1:,-1]) ):
		return 0
	elif (all( i <=0 for i in matrix[0,begin_C_columns:end_C_columns]) ) and (not (all(i >=0 for i in matrix[1:,-1]))) :
		return 1 #passar para simplex dual
	elif (not all( i <=0 for i in matrix[0,begin_C_columns:end_C_columns]) ) and (not (all(i >=0 for i in matrix[1:,-1]))) :
		return 2 #continua PL Auxiliar

def main():

	f = open('teste/teste1.txt', 'r')

	lines = int(f.readline()) + 1
	columns = int(f.readline()) + 1 
	matrix_str = f.readline()
	#matrix = np.array(np.mat(matrix_str).reshape(lines,columns))

	#exemplo simplex primal
	#matrix = np.array([[3,2,4,0],[1,1,2,4],[2,0,3,5],[2,1,3,7]],dtype=float)

	#exemplo simplex dual
	#matrix = np.array([[-4,-8,-9,0],[2,-1,5,1],[3,-4,1,3],[-1,0,-2,-8]],dtype=float)
	
	#exemplo PL AUXILIAR
	matrix = np.array([[4,8,9,0],[2,-1,5,1],[3,-4,1,3],[1,0,2,-8]],dtype=float)

	#exemplo ilimitada
	#matrix = np.array([[1,3,-1,0],[2,2,-1,10],[3,-2,1,10],[1,-3,1,10]],dtype = float)

	#exemplo de inviabilidade para simplex dual
	#matrix = np.array([[-1,-1,-1,-1,0],[4,10,6,2,6],[2,2,4,1,-2],[7,2,0,1,1]],dtype = float)


	print("\nMatriz inicial:\n")
	print(matrix)

	method = verify_method(matrix)

	if(method == 0):
		solve_primal_simplex(matrix)
	elif(method==1):
		solve_dual_simplex(matrix)
	else:
		solve_auxiliary_lp(matrix)
	f.close()
main()