# CSC 370 - Spring 2018 - Starter code for Assignment 4
#
# The code below generates a mockup of the output of report_transcript.py
# as specified in the assignment. You can copy and paste the functions in this
# program into your solution to ensure the correct formatting.
#
# B. Bird - 02/26/2018
#
# Nikola Rados
# V00801209

import psycopg2, sys

def print_header(student_id, student_name):
	print("Transcript for %s (%s)"%(str(student_id), str(student_name)) )
	
def print_row(course_term, course_code, course_name, grade):
	if grade is not None:
		print("%6s %10s %-35s   GRADE: %s"%(str(course_term), str(course_code), str(course_name), str(grade)) )
	else:
		print("%6s %10s %-35s   (NO GRADE ASSIGNED)"%(str(course_term), str(course_code), str(course_name)) )


psql_user = 'nrados' #Change this to your username
psql_db = 'nrados' #Change this to your personal DB name
psql_password = 'heheboi' #Put your password (as a string) here
psql_server = 'studdb1.csc.uvic.ca'
psql_port = 5432

conn = psycopg2.connect(dbname=psql_db,user=psql_user,password=psql_password,host=psql_server,port=psql_port)

cursor = conn.cursor()

''' The lines below would be helpful in your solution '''
if len(sys.argv) < 2:
	print('Usage: %s <student id>'%sys.argv[0], file=sys.stderr)
	sys.exit(0)
	
student_id = sys.argv[1]

cursor.execute('''select name from student where student_id = (%s);''', [student_id])
table0 = cursor.fetchall()
for row in table0:
	print_header(student_id, row[0])

cursor.execute('''with
		names as (select course_code, name, term_code from course_offering)
select student_id, term_code, course_code, name, grade from enrolment natural join names where student_id = (%s) order by term_code, course_code;''', [student_id])

table = cursor.fetchall()
for row in table:
	print_row(row[1], row[2], row[3], row[4])

cursor.close()
conn.close()
