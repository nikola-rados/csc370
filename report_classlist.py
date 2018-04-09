# report_classlist.py
# CSC 370 - Spring 2018 - Starter code for Assignment 4
#
# The code below generates a mockup of the output of report_classlist.py
# as specified in the assignment. You can copy and paste the functions in this
# program into your solution to ensure the correct formatting.
#
# B. Bird - 02/26/2018
#
# Nikola Rados
# V00801209

import psycopg2, sys

def print_header(course_code, course_name, term, instructor_name):
	print("Class list for %s (%s)"%(str(course_code), str(course_name)) )
	print("  Term %s"%(str(term), ) )
	print("  Instructor: %s"%(str(instructor_name), ) )
	
def print_row(student_id, student_name, grade):
	if grade is not None:
		print("%10s %-25s   GRADE: %s"%(str(student_id), str(student_name), str(grade)) )
	else:
		print("%10s %-25s"%(str(student_id), str(student_name),) )

def print_footer(total_enrolled, max_capacity):
	print("%s/%s students enrolled"%(str(total_enrolled),str(max_capacity)) )


''' The lines below would be helpful in your solution'''
if len(sys.argv) < 3:
	print('Usage: %s <course code> <term>'%sys.argv[0], file=sys.stderr)
	sys.exit(0)
	
course_code, term = sys.argv[1:3]


psql_user = 'nrados' #Change this to your username
psql_db = 'nrados' #Change this to your personal DB name
psql_password = 'heheboi' #Put your password (as a string) here
psql_server = 'studdb1.csc.uvic.ca'
psql_port = 5432

conn = psycopg2.connect(dbname=psql_db,user=psql_user,password=psql_password,host=psql_server,port=psql_port)

cursor = conn.cursor()

#The .execute method sends one or more SQL statements to the server.

cursor.execute('''select instructor_name, name from course_offering where course_code = (%s) and term_code = (%s);''', [course_code, term])

table = cursor.fetchall()
for row in table:
	print_header(course_code, row[1], term, row[0])

cursor.execute('''select student_id, name, grade from enrolment natural join student where course_code = (%s) and term_code = (%s);''', [course_code, term])

table2 = cursor.fetchall()
for row in table2:
	print_row(row[0], row[1], row[2])

cursor.execute('''with
	cap as (select course_code, max_capacity 
			from course_offering 
			where course_code = (%s) and 
				term_code = (%s))
select count(*) as num, max_capacity 
	from enrolment 
	inner join cap on cap.course_code = enrolment.course_code
	where enrolment.course_code = (%s) and 
		enrolment.term_code = (%s) 
	group by enrolment.course_code, enrolment.term_code, cap.max_capacity;''', [course_code, term, course_code, term])

table3 = cursor.fetchall()
for row in table3:
	print_footer(row[0], row[1])

cursor.close()
conn.close()
