
import sys, os, csv

SQL_SYNTAX = [
    "Date",
    "Month",
    "Location",
    "Type",
]

SQL_DIR = "../sql"
O_DIR = "/generated_views"

HELP_STRING = """ """

def format_string(string):
    string = string.replace(" - ", "_")
    string = string.replace(" ", "_")
    string = string.replace("-", "_")
    string = string.replace("./", "")
    string = string.replace(".\\", "")
    string = string.split("/")[-1]
    return string

def csv2sql(csv_file):
    sql = ""
    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        
        table_name = csv_file.replace(".csv", "")
        table_name = format_string(table_name)
        
        table = f"CREATE TABLE {table_name} ("
        
        table_header = []
        for i in range(len(header)):
            h = format_string(header[i])

            if (i == len(header)-1):
                comma = ""
            else:   comma = ","

            if h in SQL_SYNTAX:
                h += "_"
                table += f"{h} CHAR(255)"+comma
            else:
                table += f"{h} CHAR(255)"+comma
    
            table_header.append(h)

        table += ");" 
        print(table)
    
    sql += table

    with open(f"{csv_file}", "r") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            insert = f"INSERT INTO {table_name}"  
            insert += " VALUES("
    
            for i in range(len(row)):
                if i == len(row)-1:
                    comma = ""
                else:
                    comma = ","
                insert += f'"{row[i]}"'+comma
    
            insert += ");"
            sql += insert
        
    return sql
    

def cmd_ui(ui):
    flag = 0
    if "-o" or "--one-file" in ui:
        flag = 1
    elif "-h" or "--help" in ui:
        print(HELP_STRING)
        return True
    elif "-d" or "--no-file" in ui:
        pass

    w_dir = []
    for i in ui:
        if (i.split(".")[-1] == "csv") and (os.path.exists(i)):
            w_dir.append(i)
        if (os.path.isdir(i)):
            w_dir.append(i)
    
    for d in w_dir:
        if (os.path.isdir(d)):
            for g in os.listdir(d):
                if (g.split(".")[-1] == "csv"):
                    dd = g.replace(".csv", ".sql")
                    if flag == 1:
                        with open(f"{SQL_DIR}/{O_DIR}.sql", "w+") as f:
                            sql = csv2sql(f"{d}/{g}")
                            f.write(sql)
                    else:
                        with open(f"{SQL_DIR}/{dd}", "w+") as f:
                            sql = csv2sql(f"{d}/{g}")
                            f.write(sql)
        if d.split(".")[-1] == "csv":
            dd = d.replace(".csv", ".sql")           
            if flag == 1:
                with open(f"{SQL_DIR}/{O_DIR}.sql", "w+") as f:
                    sql = csv2sql(d)
                    f.write(sql)
            else:
                with open(f"{SQL_DIR}/{dd}", "w+") as f:
                    sql = csv2sql(d)
                    f.write(sql)
                

if __name__ == "__main__" :
    cmd_ui(sys.argv[1:])