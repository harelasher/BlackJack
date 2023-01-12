import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('example.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create a table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT,
        highscore INTEGER
    )
''')

# Insert some data
cursor.execute('''
    INSERT INTO users (username, password, highscore)
    VALUES ('alice', 'secret', 100), ('bob', 'password', 200)
''')

# Commit the changes to the database
conn.commit()

# Run a query to select all users from the table
cursor.execute('SELECT * FROM users')

# Fetch the result
users = cursor.fetchall()

# Print the result
for user in users:
    print(user)

# Close the connection
conn.close()
