import numpy as np 
from pdb import set_trace
import math

from commons import pivoting, put_tableux_form, put_pl_form, parse_to_fpi,canonical_form


def print_optimal_situation(matrix,base_columns):

	
	#calcula solução 
	begin_A_columns = matrix.shape[0]-1
	solution = np.zeros(matrix.shape[1] - (begin_A_columns))
	for index in range(1,len(base_columns)): #percorre quantidade de linhas 
		solution[(int(base_columns[index])-begin_A_columns)] = matrix[index,matrix.shape[1]-1]

	print("2")
	print(np.around(np.array(solution[0:-(matrix.shape[0])],dtype=float), decimals=5)   )
	print( np.around(float(matrix[0,-1]) , decimals=5))
	print(np.around( np.array(matrix[0,0:(matrix.shape[0]-1)],dtype=float), decimals=6)  )
	#conteudo = []
	#conteudo.append("2"+'\n')
	#conteudo.append(str(solution)+'\n')
	#conteudo.append(str((matrix[0,-1]).tolist())+'\n')
	#conteudo.append(str((matrix[0,0:(matrix.shape[0]-1)]).tolist()))
	#f = open('conclusao.txt', 'w')
	#f.writelines(conteudo)
	#f.close()

	#print("2")
	#print(solution)
	#print(matrix[0,-1])
	#print((matrix[0,0:(matrix.shape[0]-1)]).tolist())

def non_viability_certificate(matrix,base_columns):
	
	conteudo = []
	conteudo.append("0"+'\n')
	conteudo.append(str((matrix[0,0:(matrix.shape[0]-1)]).tolist()))
	f = open('conclusao.txt', 'w')
	f.writelines(conteudo)
	f.close()
	#print("0")
	#print((matrix[0,0:(matrix.shape[0]-1)]).tolist())


def dual_simplex(matrix,base_columns):
	#set_trace()
	inviability = 0
	b_index = find_b_negative(matrix)
	if(b_index is not None): #ainda temos entradas de b no tableaux que são negativas
		column_index = find_pivot_dual_simplex(matrix,b_index)
		if(column_index is not None):#temos, na linha b_index, valores de A negativos
			pivoting(matrix,b_index,column_index)
			base_columns[b_index] = column_index
		else: #situação de PL inviável - A da linha positivo com B da linha negativo e X>=0
			inviability = 1
			non_viability_certificate(matrix,base_columns)
	if(inviability != 1):
		state = verify_state_dual(matrix)
		if(state): #situacao de ótimo
			print_optimal_situation(matrix,base_columns)
			return
		elif(state is None):
			#executar simples primal
			pass	
		else: #False
			dual_simplex(matrix,base_columns)

def find_b_negative(matrix):
	matrix_lines = matrix.shape[0]
	for index in range(1,matrix_lines):
		if matrix[index,-1] < 0:
			return index
	return None

def find_pivot_dual_simplex(matrix,b_index):
	#TODO COLOCAR INFINITO AQUI E NA PRIMAL
	min_value = 100000000
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
	#set_trace()
	begin_C_columns = matrix.shape[0]-1
	end_C_columns = matrix.shape[1]-1
	c_negative_in_PL = all( i >=0 for i in matrix[0,begin_C_columns:end_C_columns])
	b_positive = all(i >=0 for i in matrix[1:matrix.shape[0],-1])
	if ( c_negative_in_PL ) and ( b_positive ):
		return True
	elif ( c_negative_in_PL ):
		return False #continua simplex dual
	else:
		return None #passar para simplex primal, teoricamente




def solve(matrix):

	print("Solving dual simplex.")
	matrix = parse_to_fpi(matrix)
	matrix = put_tableux_form(matrix)
	base_columns = np.zeros(matrix.shape[0])
	canonical_form(matrix,base_columns)
	dual_simplex(matrix,base_columns)
	print("oi dual")
	
