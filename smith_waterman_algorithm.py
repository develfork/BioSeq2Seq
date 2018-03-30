import sys

database_sequence = []
substitution_symbols = [] # from substitution_matrix.txt
substitution_values = [] # from substitution_matrix.txt
user_input = []
scoring_matrix = []
max_score = []
gap_value = -2

def read_from_files():
	# database sequence disk read
	global database_sequence
	openfile =  open('database_sequence_example.fa', 'r')
	readfile = openfile.read().split('\n')
	database_sequence = [letter for letters in [line for line in readfile[1:] if len(line)>0] for letter in letters]
	openfile.close()
	
	# substitution matrix disk read
	openfile = open('substitution_matrix_example.txt','r')
	readfile = openfile.read().split('\n')
	# reading the substitution matrix symbols
	global substitution_symbols
	substitution_symbols = [symbol for symbol in readfile[0] if symbol!=' ']
	# reading the substitution matrix values
	global substitution_values
	substitution_values = [map(int,number) for number in [line.split(' ') for line in readfile[1:] if len(line)>0]]
	openfile.close()

def maxtuple(a, b):
	return (a, b)[a[0]<b[0]]

def get_user_input():
	global user_input
	user_input = [letter for letters in raw_input("please input your dna sequence\n") for letter in letters]

def get_substitution_value(a, b):
	a_index = substitution_symbols.index(a)
	b_index = substitution_symbols.index(b)
	return substitution_values[a_index][b_index]

def smith_waterman():
	global scoring_matrix
	global gap_value
	global max_score
	max_score = [-1000,-1,-1]
	scoring_matrix = [[0 for x in range(len(user_input)+1)] for y in range(len(database_sequence)+1)]
	for index_i, element_i in enumerate(database_sequence):
		for index_j, element_j in enumerate(user_input):
			substitution_value = get_substitution_value(element_i, element_j)
			scoring_matrix[index_i+1][index_j+1] = max(scoring_matrix[index_i][index_j]+substitution_value, scoring_matrix[index_i][index_j+1]+gap_value, scoring_matrix[index_i+1][index_j]+gap_value, scoring_matrix[index_i+1][index_j+1])
			max_score = maxtuple(max_score, [scoring_matrix[index_i+1][index_j+1],index_i+1,index_j+1])

	result = []
	while max_score != 0 :
		substitution_value = get_substitution_value(database_sequence[max_score[1]], user_input[max_score[2]])
		max_score_temp = maxtuple ([scoring_matrix[max_score[1]-1][max_score[2]-1]+substitution_value , max_score[1]-1 , max_score[2]-1], [scoring_matrix[max_score[1]][max_score[2]-1]+gap_value,max_score[1]][max_score[2]-1], [scoring_matrix[max_score[1]-1][max_score[2]]+gap_value,max_score[1]-1][max_score[2]])
		if max_score[2] != max_score_temp[2] and max_score[1] != max_score_temp[1] :
			result.append ([database_sequence[max_score[1]],user_input[max_score[2]]])
		else if max_score[2] != max_score_temp[2] and max_score[1] == max_score_temp[1] :
			result.append (['-',user_input[max_score[2]]])
		else if max_score[2] == max_score_temp[2] and max_score[1] != max_score_temp[1] :
			result.append ([database_sequence[max_score[1]],'-'])
		max_score = max_score_temp


				
			
	

if __name__ == '__main__':
	read_from_files()
	print database_sequence
	print substitution_symbols
	print substitution_values
	get_user_input()
	get_substitution_value
	print user_input
	smith_waterman()
	print scoring_matrix
	print max_score
