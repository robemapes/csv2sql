
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

def csv2sql(csv_file, insert_only=False, table_only=False):
    sql = ""
    table_name = csv_file.replace(".csv", "")
    table_name = format_string(table_name)

    if not insert_only:
        with open(csv_file, "r") as f:
            reader = csv.DictReader(f)
            header = reader.fieldnames         
            
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
    if not table_only:
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
    i_flag = False
    t_flag = False
    if "-o" in ui  or "--one-file" in ui:
        flag = 1
    if "-h" in ui or "--help" in ui:
        print(HELP_STRING)
        return True
    if "-t" in ui or "--table" in ui:
        t_flag = True
    if "-i" in ui or "--insert" in ui:
        i_flag = True
    if "-d" in ui  or "--no-file" in ui:
        pass
    if (i_flag == True and t_flag == True):
        i_flag = False
        t_flag = False
    
    print(ui)

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
                    if (i_flag):
                        qd = dd.split(".")[0]
                        qd += "_insert"
                        dd = qd+".sql" 
                    if flag == 1:
                        with open(f"{SQL_DIR}/{O_DIR}.sql", "a+") as f:
                            sql = csv2sql(f"{d}/{g}", i_flag, t_flag)
                            f.write(sql)
                    else:
                        with open(f"{SQL_DIR}/{dd}", "a+") as f:
                            sql = csv2sql(f"{d}/{g}", i_flag, t_flag)
                            f.write(sql)
        if d.split(".")[-1] == "csv":
            dd = d.replace(".csv", ".sql")
            dd = format_string(dd)
            if (i_flag):
                qd = dd.split(".")[0]
                qd += "_insert"
                dd = qd+".sql"         
            if (t_flag):
                qd = dd.split(".")[0]
                qd += "_table"
                dd = qd+".sql"         
    
            if flag == 1:
                with open(f"{SQL_DIR}/{O_DIR}.sql", "a+") as f:
                    sql = csv2sql(d, i_flag, t_flag)
                    f.write(sql)
            else:
                with open(f"{SQL_DIR}/{dd}", "w+") as f:
                    sql = csv2sql(d, i_flag, t_flag)
                    f.write(sql)
                    

if __name__ == "__main__" :
    cmd_ui(sys.argv[1:])
