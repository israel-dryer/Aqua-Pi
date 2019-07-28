import psycopg2 as pg

class Logger:
    
    def __init__(self, user, password, host='aquapi.c5uh7gzya75b.us-east-2.rds.amazonaws.com'):
        '''
        A data logger that connects and insert data into an AWS PostgreSQL server 
        
        Parameters
        ----------
        user : `string`
            The user name to access the database
        password : `string`
            The password to access the database
        host : 'string' (optional)
            The connection path where the datbase resides. The default is the 'aquapi' database on the AWS server            
        
        '''
        self.user = user
        self.password = password
        self.host = host
        
    def log_data(self, data):
        '''
        Insert data into PostgreSQL database
        
        Parameters
        ----------
        data : `dict`
            The data that you want to insert into the database; where the pattern is {table:table_data}
            
        Returns
        ----------
        `boolean`
            Indicates if the data connection and insert was successful
            
        '''
        try:
            conn = pg.connect(user=self.user, password=self.password, host=self.host)
        except:
            print("!CONNECTION ERROR! Invalid credentials OR no connection available!")
            return False
            
        cursor = conn.cursor()
        
        for table, values in data.items():
            # calc the number of params to insert
            cnt = len(values[0])
            params = "%s" + ",%s"*(cnt-1)
            cursor.executemany("INSERT INTO {0} VALUES({1})".format(table, params), values)
            conn.commit()
            
        conn.close()
        print("\n!ALERT! Data uploaded into SQL database")
        return True