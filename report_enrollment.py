# report_enrollment.py
# CSC 370 - Spring 2018 - Starter code for Assignment 4
#
# The code below generates a mockup of the output of report_enrollment.py
# as specified in the assignment. You can copy and paste the functions in this
# program into your solution to ensure the correct formatting.
#
# B. Bird - 02/26/2018

import psycopg2, sys

def print_row(term_code, course_code, name, instructor_name, enrolled, max_capacity):
	print("%6s %10s %-35s %-25s %s/%s" %(str(term_code), str(course_code), str(name), str(instructor_name), str(enrolled), str(max_capacity)) )

psql_user = 'nrados'
psql_db = 'nrados'
psql_password = 'heheboi' #Put your password (as a string) here
psql_server = 'studdb1.csc.uvic.ca'
psql_port = 5432

#The object returned by psycopg2.connect is a "connection" object. By default, each connection object
#is configured to start a transaction when the connection is initialized (so any commands you run will
#not be committed until you use the .commit() method).
conn = psycopg2.connect(dbname=psql_db,user=psql_user,password=psql_password,host=psql_server,port=psql_port)

#To actually use the connection, you have to create a "cursor" object.
cursor = conn.cursor()

#The .execute method sends one or more SQL statements to the server.

cursor.execute('''with
			counter as (select count(*) as enrolled, course_code, term_code 
					from enrolment 
					group by course_code, term_code)
			select course_offering.term_code, course_offering.course_code, name, instructor_name, enrolled, max_capacity
				from course_offering 
				left join counter on counter.course_code = course_offering.course_code and counter.term_code = course_offering.term_code
				order by term_code, course_code;''' )

items = cursor.fetchall()
for row in items:
    print_row(*row)

cursor.close()
conn.close()
