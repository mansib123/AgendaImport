from db_table import db_table
import sys
import xlrd

### Define and create the SQLite table schema for Agenda table 
agenda_table = db_table("agenda", { "id" : "INTEGER PRIMARY KEY AUTOINCREMENT",
                             "date": "TEXT NOT NULL", 
                             "time_start": "TEXT NOT NULL", 
                             "time_end": "TEXT NOT NULL",
                             "session_type": "TEXT NOT NULL",
                             "title": "TEXT NOT NULL",
                             "location": "TEXT",
                             "description": "TEXT",
                             "speakers": "TEXT",
                             "session_id": "INTEGER NOT NULL" })

#### Opening the Agenda Excel file
# file_path = "agenda.xls"
file_path = sys.argv[1]
book = xlrd.open_workbook(file_path)
sh = book.sheet_by_index(0)

### Parse and store the content of the excel file in the Agenda table/database
"""session Id allows to associate subsessions with their corresponding sessions. 
All the subsession of a session will have the same session Id to ensure faster search of subsessions of a session""" 
session_id = 0
for rx in range(15, sh.nrows):
    """ The data that need to be stored in table starts from row16 in excel. 
    Hence, reading data from row16 """
    # Reading the data from the file
    row = sh.row_values(rx)
    # Inserting the row values into the table
    if str(row[3]) != "Sub":
        """session_id should only be increamented if new session is there"""
        session_id = session_id + 1
    
    agenda_table.insert({"date": str(row[0]), 
                    "time_start": str(row[1]), 
                    "time_end": str(row[2]),
                    "session_type": str(row[3]),
                    "title": str(row[4]),
                    "location": str(row[5]),
                    "description": str(row[6]),
                    "speakers": str(row[7]),
                    "session_id": session_id })
    
agenda_table.close()