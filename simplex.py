import numpy as np 
from pdb import set_trace
import math

from primal_simplex import solve as solve_primal_simplex
from dual_simplex import solve as solve_dual_simplex


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

	method = verify_method(matrix)

	if(method == 0):
		solve_primal_simplex(matrix)
	elif(method==1):
		solve_dual_simplex(matrix)
	else:
		print("pl auxiliar")
		#pl auxiliar
		pass
	print('final')
main()