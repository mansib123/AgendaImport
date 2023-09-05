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
                             "speakers": "TEXT" })


def main():
    # Parse command-line arguments to retrieve the sessions conditions
    parse = argparse.ArgumentParser(description="Find agenda sessions")
    parse.add_argument("column", choices=["date", "time_start", "time_end", "title", "location", "description", "speaker"], help="Condition/Column where to search at")
    parse.add_argument("value", help="Expected Value to search for in the specified column")
    args = parse.parse_args()

    # Construct the where search query based on the column and value condition 
    if args.column == "speaker":
        """ Special case of one speaker will be handled here """
        where = {"speakers": f"%{args.value}%"}
    else:
        """ allows only exact matches of values are looked """
        where = {str(args.column): str(args.value)}
    
    results = agenda_table.select(where=where)
    if not results:
        print("No matching sessions found.")
    else:
        for session in results:
            print(list(session.values()))

if __name__ == "__main__":
    main()