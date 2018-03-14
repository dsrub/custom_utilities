# custom_utilities

```
### import packages
 
import psycopg2
import pandas as pd
```

```
### connect to redshift database
con=psycopg2.connect(dbname= 'database name', host='host', 
                     port= 'port', user='user', password= 'password')
```

```
### get a cursor
cur = con.cursor()
```

```
### define a function that takes in an SQL command (as a string) and returns a pd dataframe
### (be careful not return anything too huge)
def pd_df(sql_command):
    
    ### execute sql command
    cur.execute(sql_command)
    
    ### get list of columns
    col_list = [x[0] for x in cur.description]
    
    ### fetch all data returned
    data = cur.fetchall()
    
    ### return pd dataframe
    
    return pd.DataFrame(data, columns=col_list)
```

```
sql_command = 'SELECT * from sym.sym_am_web_data Limit 5;'
df = pd_df(sql_command)
df
```
![alt text](readme_files/df.png)


```
### close up cursor and close up the connection when you are finished
cur.close()
conn.close()
```
