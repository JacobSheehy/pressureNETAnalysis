import re
import threading

from readings.models import Reading


def parse_file(filename):
    sql_data = open(filename, 'r')
    outfile = open('readings.sql', 'w')

    line_re = re.compile('^\d+\s\d+\.\d+\s.*$')

    field_names = ('id', 'latitude', 'longitude', 'daterecorded', 'reading', 'tzoffset', 'user_id') 

    for line in sql_data:
        if line_re.findall(line):
            
  
