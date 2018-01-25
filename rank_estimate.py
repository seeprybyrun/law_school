import random
import itertools
from operator import add
from math import floor

NUM_TRIALS = 10000
SIGMA = 0.5

def main():

	average_percentiles = {}
	min_percentiles = {}
	max_percentiles = {}
	previous_occurrences = {}

	for i in range(NUM_TRIALS):
		distro = perform_semester_trial()
		for score in set(distro):
			first_index = distro.index(score)
			last_index = len(distro) - 1 - distro[::-1].index(score)
			percentile = 100 - 100*(float(first_index) + float(last_index))/float(2*len(distro))
			if score not in average_percentiles:
				average_percentiles[score] = percentile
				min_percentiles[score] = percentile
				max_percentiles[score] = percentile
				previous_occurrences[score] = 1
			else:
				average_percentiles[score] = ((previous_occurrences[score]*average_percentiles[score])+percentile)/(previous_occurrences[score]+1)
				min_percentiles[score] = min(min_percentiles[score], percentile)
				max_percentiles[score] = max(max_percentiles[score], percentile)
				previous_occurrences[score] += 1

	print 'Semester GPA\t\tEstimated Percentile'
	for score in sorted(average_percentiles.keys(), reverse=True):
		if previous_occurrences[score] >= 0.2*NUM_TRIALS:
			print '{:.3f}\t\t\t\t{:.2f}-{:.2f} (avg: {:.2f})'.format(score, min_percentiles[score], max_percentiles[score], average_percentiles[score])
			

def perform_semester_trial():

	ac = [(i,random.gauss(0,1)) for i in range(40)]
	bd = [(i,random.gauss(0,1)) for i in range(41)]
	abcd = ac + bd
	abcd_gpas = compute_grades(ac, distros[0]) + compute_grades(bd, distros[1])
	abcd_gpas = map(add, abcd_gpas, compute_grades(abcd, distros[2]))
	abcd_gpas = map(add, abcd_gpas, compute_grades(abcd, distros[3]))
	abcd_gpas = map(add, abcd_gpas, compute_grades(abcd, distros[4]))
	abcd_gpas = map(add, abcd_gpas, compute_grades(abcd, distros[5]))
	abcd_gpas = [x/5.0 for x in abcd_gpas]

	ef = [(i,random.gauss(0,1)) for i in range(40)]
	gh = [(i,random.gauss(0,1)) for i in range(40)]
	efgh = ef + gh
	efgh_gpas = compute_grades(ef, distros[6]) + compute_grades(gh, distros[7])
	efgh_gpas = map(add, efgh_gpas, compute_grades(efgh, distros[8]))
	efgh_gpas = map(add, efgh_gpas, compute_grades(efgh, distros[9]))
	efgh_gpas = [x/3.0 for x in efgh_gpas]

	ij = [(i,random.gauss(0,1)) for i in range(40)]
	kl = [(i,random.gauss(0,1)) for i in range(40)]
	ijkl = ij + kl
	ijkl_gpas = compute_grades(ij, distros[10]) + compute_grades(kl, distros[11])
	ijkl_gpas = map(add, ijkl_gpas, compute_grades(ijkl, distros[12]))
	ijkl_gpas = map(add, ijkl_gpas, compute_grades(ijkl, distros[13]))
	ijkl_gpas = [x/3.0 for x in ijkl_gpas]

	mn = [(i,random.gauss(0,1)) for i in range(40)]
	op = [(i,random.gauss(0,1)) for i in range(39)]
	mnop = mn + op
	mnop_gpas = map(add, compute_grades(mnop, distros[14]), compute_grades(mnop, distros[15]))
	mnop_gpas = map(add, mnop_gpas, compute_grades(mnop, distros[16]))
	mnop_gpas = [x/3.0 for x in mnop_gpas]

	all_gpas = abcd_gpas + efgh_gpas + ijkl_gpas + mnop_gpas
	all_gpas = [truncate(x,3) for x in all_gpas]
	return sorted(all_gpas, reverse=True)

def truncate(x, n):
	x *= 10**n
	x = floor(x) * 1.0
	x /= 10**n

	return x

def compute_grades(students, grade_distro):
	N = len(students)
	ret = [None] * N

	while len(grade_distro) > N:
		grade_distro = delete_random_grade_from(grade_distro)

	grades = [(i, students[i][1] + random.gauss(0,SIGMA)) for i in range(N)]
	grades = sorted(grades, reverse=True, key=lambda x: x[1])

	thresholds = [sum(grade_distro[:1]),
				  sum(grade_distro[:2]),
				  sum(grade_distro[:3]),
				  sum(grade_distro[:4]),
				  sum(grade_distro[:5]),
				  sum(grade_distro[:6]),
				  sum(grade_distro[:7]),
				  sum(grade_distro[:8]),
				  sum(grade_distro[:9]),
				  sum(grade_distro[:10]),
				  sum(grade_distro[:11])]

	for i in range(N):
		student_id = grades[i][0]
		if i <= thresholds[0]:
			ret[student_id] = 4.3
		elif i <= thresholds[1]:
			ret[student_id] = 4.0
		elif i <= thresholds[2]:
			ret[student_id] = 3.7
		elif i <= thresholds[3]:
			ret[student_id] = 3.3
		elif i <= thresholds[4]:
			ret[student_id] = 3.0
		elif i <= thresholds[5]:
			ret[student_id] = 2.7
		elif i <= thresholds[6]:
			ret[student_id] = 2.3
		elif i <= thresholds[7]:
			ret[student_id] = 2.0
		elif i <= thresholds[8]:
			ret[student_id] = 1.7
		elif i <= thresholds[9]:
			ret[student_id] = 1.3
		elif i <= thresholds[10]:
			ret[student_id] = 1.0
		else:
			ret[student_id] = 0.0

	return ret


def delete_random_grade_from(distro):
	total_grades = sum(distro)
	r = random.randint(0,total_grades-1)

	running_sum = 0
	current_index = 0
	while r >= running_sum:
		running_sum += distro[current_index]
		current_index += 1

	distro[current_index-1] -= 1
	return distro


distros = [ [1,	 5,	 4,	14,	12,	3,	1,  0, 0,  0,  0, 0],
			[0,  2,	10,	15,	13,	1,  0,  0, 0,  0,  0, 0],
			[0, 12,	16,	33,	18,	2,  0,  0, 0,  0,  0, 0],
			[2, 11,	18,	31,	16,	3,	2,  0, 0,  0,  0, 0],
			[0,  9,	14,	27,	25,	6,  0,  0, 0,  0,  0, 0],
			[0,  3,	22,	51,	 9, 0,  0,  0, 0,  0,  0, 0],
			[1,	 6,	 7,	13,	 9,	3,	1,	1, 0,  0,  0, 0],
			[0,  5,	10,	16,	 6,	3,  0,  0, 0,  0,  0, 0],
			[3,	 7,	18,	30,	22,	4,	3,	0, 0,  0,  0, 0],
			[0,  8,	21,	32,	15,	3,  0,	1, 0,  0,  0, 0],
			[0,	 4,	 9,	16,	 9,	1,	1,  0, 0,  0,  0, 0],
			[1,	 3,	12,	13,	 9,	2,  0,  0, 0,  0,  0, 0],
			[1,	 9,	17,	31,	18,	3,	1,  0, 0,  0,  0, 0],
			[1,	 8,	15,	31,	18,	5,	3,  0, 0,  0,  0, 0],
			[1,	10,	17,	29,	19,	3,	1,  0, 0,  0,  0, 0],
			[0,  9,	17,	29,	20,	4,	2,  0, 0,  0,  0, 0],
			[1,	 7,	19,	26,	24,	3,  0,  0, 0,  0,  0, 0],
		  ]

if __name__ == '__main__':
	main()
