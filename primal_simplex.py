import numpy as np 
from pdb import set_trace
import math

from commons import pivoting, put_tableux_form, put_pl_form, parse_to_fpi,canonical_form

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

def unlimited_certificate(matrix,c_index,base_columns):
	begin_A_columns = matrix.shape[0]-1
	certificate = np.zeros(matrix.shape[1] - (begin_A_columns+1))
	for index in range(1,len(base_columns)): #percorre quantidade de linhas 
		certificate[(int(base_columns[index])-begin_A_columns)] = -matrix[index,c_index]
	certificate[c_index-begin_A_columns] = 1
	
	conteudo = []
	conteudo.append("1"+'\n')
	conteudo.append(str((certificate).tolist()))
	f = open('conclusao.txt', 'w')
	f.writelines(conteudo)
	f.close()
	#print("1")
	#print(certificate.tolist())
	


def print_optimal_situation(matrix,base_columns):
	
	#calcula solução 
	begin_A_columns = matrix.shape[0]-1
	solution = np.zeros(matrix.shape[1] - (begin_A_columns+1))
	for index in range(1,len(base_columns)): #percorre quantidade de linhas 
		solution[(int(base_columns[index])-begin_A_columns)] = matrix[index,matrix.shape[1]-1]
	
	conteudo = []
	conteudo.append("2"+'\n')
	conteudo.append(str(solution)+'\n')
	conteudo.append(str((matrix[0,-1]).tolist())+'\n')
	conteudo.append(str((matrix[0,0:(matrix.shape[0]-1)]).tolist()))
	f = open('conclusao.txt', 'w')
	f.writelines(conteudo)
	f.close()

	#print("2")
	#print(solution)
	#print(matrix[0,-1])
	#print((matrix[0,0:(matrix.shape[0]-1)]).tolist())

def primal_simplex(matrix,base_columns):
	c_index = find_c_negative(matrix) 
	ilimit = 0
	if (c_index is not None): #ainda temos entradas de (-c) no tableux negativas
		line_index =  find_pivot_primal_simplex(matrix,c_index)
		if (line_index is not None): #temos, na coluna c_index escolhida, valores de A maiores que zero
			pivoting(matrix,line_index,c_index)
			base_columns[line_index] = c_index
		elif(matrix[0,c_index] < 0 ): #situação de pl ilimitada
			ilimit = 1
			unlimited_certificate(matrix,c_index,base_columns)
		else:
			raise "Deu merda - escolhi c_index = 0, com uma coluna toda menos ou igual a zero"
	if(ilimit != 1):
		state = verify_state_primal(matrix)
		if(state): #situacao de ótimo	
			print_optimal_situation(matrix,base_columns)
			return
		elif(state is None):
			#executar simples dual
			pass	
		else:
			primal_simplex(matrix,base_columns)


def solve(matrix):
	print("Solving primal simplex.")
	matrix = parse_to_fpi(matrix)
	matrix = put_tableux_form(matrix)
	base_columns = np.zeros(matrix.shape[0])
	canonical_form(matrix,base_columns)
	primal_simplex(matrix,base_columns)