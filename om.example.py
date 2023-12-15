import sqlite3

connection = sqlite3.connect('/chinook.db')
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

sql = '''
select LastName, CustomerId, FirstName from customers;
'''

cursor.execute(sql)
results = cursor.fetchall()
connection.close()

class User:
    def __init__(self, **kwargs):
      #  self.foo = 1
        for key, value in kwargs.items():
            setattr(self, key, value)



    def get_full_name(self, user=None):
        return f'{user.FirstName} {user.LastName}'

    def save(self):
        connection = sqlite3.connect('/chinook.db')
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        sql = f'''
        update customers 
        set 
        LastName = "{self.LastName}",
        FirstName = "{self.FirstName}"
        where
        CustomerId = {self.CustomerId}
        '''

        cursor.execute(sql)
        connection.commit()
        connection.close()


users = [
    User(**data) for data in results
]



#for user in results:
#    print(f'{user.CustomerId} {user.get_full_name()}')



