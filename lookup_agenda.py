from db_table import db_table
import argparse

### SQLite table schema for Agenda table 
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

def main():
    # Parse command-line arguments to retrieve the sessions conditions
    parse = argparse.ArgumentParser(description="Find agenda sessions")
    parse.add_argument("column", choices=["date", "time_start", "time_end", "title", "location", "description", "speaker"], help="Condition/Column where to search at")
    parse.add_argument("value", help="Expected Value to search for in the specified column")
    args = parse.parse_args()

    # Construct the where search query based on the column and value condition 
    if args.column == "speaker":
        """ Special case of searching of one speaker will be handled here """
        where = {"speakers": f"%{args.value}%"}
    else:
        """ allows only exact matches of values are searched """
        where = {str(args.column): str(args.value)}
    
    find_all_sesssions(where)
    agenda_table.close()
    # print("part 2 done")
    
def find_all_sesssions(where):
    """looks for both matching sessions and subsessions"""
    results = agenda_table.select(where=where)
    if not results:
        print("No matching sessions found.")
        return
    
    # printed_session_ids allows to prevent printing duplicate subsessions
    printed_session_ids = set()  
    for session in results:
        if session["session_type"] == "Session":
            """print the session and find all its subsessions and print them as well"""
            print(list(session.values())[1:-1])
            printed_session_ids.add(session["session_id"])
            find_all_subsesssions(session["session_id"])  

        elif session["session_type"] == "Sub":
            """check if subsession is not already printed. If not then print it otherwise nothing"""
            if session["session_id"] not in printed_session_ids:
                print(list(session.values())[1:-1])

def find_all_subsesssions(session_id):
    ###helper function to find all subsessions of a session and print them
    subsessions = agenda_table.select(where={"session_id": session_id, "session_type": "Sub"})
    for subs in subsessions:
        print(list(subs.values())[1:-1])

if __name__ == "__main__":
    main()