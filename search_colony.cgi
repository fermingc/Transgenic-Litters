#!/usr/local/bin/python3

import cgi
import jinja2
import re
import mysql.connector
import cgitb
import sys 
from datetime import datetime

cgitb.enable()

#destination: /var/www/html/fgallar1/final

form = cgi.FieldStorage()
colony_id = form.getvalue('colony_id')
colony_id = int(colony_id)

#colony_id = 2000 #remove after testing!!

# This line tells the template loader where to search for template files
templateLoader = jinja2.FileSystemLoader( searchpath="./templates" )

# This creates your environment and loads a specific template
env = jinja2.Environment(loader=templateLoader)
template = env.get_template('colony_output.html')

conn = mysql.connector.connect(user='fgallar1', password='SQLastro2',
                               host='localhost', database='fgallar1')

def formatting(value):
	value = value.replace("(", "")
	value = value.replace(")", "")
	value = value[:-1]
	return value

cursor = conn.cursor()#buffered=True?

#queries needed for wt/wt + control breedings-----------------------------------------

#wt initial count (at 5-7 days old), average
wt_ic_qry = """
select avg(ic) from litters, breeding where litters.breeding_id=breeding.breeding_id and breeding.colony_id='%s' and breeding.type='wt';
"""
cursor.execute(wt_ic_qry, (colony_id,))
wt_ic = str(cursor.fetchone())
wt_ic = formatting(wt_ic)
#print(wt_ic)

#wt final count (at wean, 21-25 days old), average
wt_fc_qry = """
select avg(fc) from litters, breeding where litters.breeding_id=breeding.breeding_id and breeding.colony_id='%s' and breeding.type='wt';
"""
cursor.execute(wt_fc_qry, (colony_id,))
wt_fc = str(cursor.fetchone())
wt_fc = formatting(wt_fc)
#print(wt_fc)

#wt litters counted for data accuracy
wt_lits_qry = """
select count(litter_id) from litters, breeding where litters.breeding_id=breeding.breeding_id and breeding.colony_id='%s' and breeding.type='wt';
"""
cursor.execute(wt_lits_qry, (colony_id,))
wt_lits = str(cursor.fetchone())
wt_lits = formatting(wt_lits)
#print(wt_lits)

#wt litters counted for data accuracy
wt_lits_qry = """
select count(litter_id) from litters, breeding where litters.breeding_id=breeding.breeding_id and breeding.colony_id='%s' and breeding.type='wt';
"""
cursor.execute(wt_lits_qry, (colony_id,))
wt_lits = str(cursor.fetchone())
wt_lits = formatting(wt_lits)
#print(wt_lits)
'''
wt_dob_qry = """
select max(dob) from litters, breeding where litters.breeding_id=breeding.breeding_id and breeding.colony_id='%s' and breeding.type='wt';
"""
cursor.execute(wt_dob_qry, (colony_id,))
wt_dob = str(cursor.fetchone())
wt_dob = wt_dob[1:-1]
wt_dob = wt_dob.strftime('%B %d, %Y')
#print(wt_lits)
'''
#queries needed for exp breedings------------------------------------------------

#exp initial count (at 5-7 days old), average
exp_ic_qry = """
select avg(ic) from litters, breeding where litters.breeding_id=breeding.breeding_id and breeding.colony_id='%s' and breeding.type='exp';
"""
cursor.execute(exp_ic_qry, (colony_id,))
exp_ic = str(cursor.fetchone())
exp_ic = formatting(exp_ic)
#print(exp_ic)

#exp final count (at wean, 21-25 days old), average
exp_fc_qry = """
select avg(fc) from litters, breeding where litters.breeding_id=breeding.breeding_id and breeding.colony_id='%s' and breeding.type='exp';
"""
cursor.execute(exp_fc_qry, (colony_id,))
exp_fc = str(cursor.fetchone())
exp_fc = formatting(exp_fc)
#print(exp_fc)

#exp litters counted for data accuracy
exp_lits_qry = """
select count(litter_id) from litters, breeding where litters.breeding_id=breeding.breeding_id and breeding.colony_id='%s' and breeding.type='exp';
"""
cursor.execute(exp_lits_qry, (colony_id,))
exp_lits = str(cursor.fetchone())
exp_lits = formatting(exp_lits)
#print(exp_lits)


print("Content-Type: text/html\n\n")
print(template.render(wt_ic=wt_ic, wt_fc=wt_fc, wt_lits=wt_lits, exp_ic=exp_ic, exp_fc=exp_fc, exp_lits=exp_lits, colony_id=colony_id))

cursor.close()
conn.close()
