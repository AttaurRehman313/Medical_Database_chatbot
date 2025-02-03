import sqlite3
import pickle
import datetime
# Connect to the database and create the table
def initialize_database():
    conn = sqlite3.connect('History.db')
    cursor = conn.cursor()
    # Create the history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            user_id INTEGER PRIMARY KEY,
            memory BLOB NOT NULL,
            time TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
initialize_database()

def find_user(user_id):
    """
    Function to check if a user exists in the database.
    """
    try:
        conn = sqlite3.connect('History.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM history WHERE user_id=?", (user_id,))
        user = cursor.fetchone()
        return user is not None  # Return True or False based on existence
    except sqlite3.OperationalError as e:
        print(f"SQL Error: {str(e)}")
        return None
    except sqlite3.DatabaseError as e:
        print(f"Database Error: {str(e)}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None
    finally:
        conn.close()

def add_user(user_id, memory):
    """
    Function to add a new user to the database for the first message.
    """
    try:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        memory_binary = pickle.dumps(memory)  # Convert memory to binary
    except Exception as e:
        print("Error in memogy : ",str(e))
    try:
        conn = sqlite3.connect('History.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO history (user_id, memory, time) VALUES (?, ?, ?)", (user_id, memory_binary, current_time))
        conn.commit()

        return "User added successfully."
    except sqlite3.OperationalError as e:
        return f"SQL Error: {str(e)}"
    except sqlite3.DatabaseError as e:
        return f"Database Error: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
    finally:
        conn.close()

def update_user_record(user_id, memory):
    """
    Function to update the history and time of the last query by user.
    """
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    memory_binary = pickle.dumps(memory)
    try:
        conn = sqlite3.connect("History.db")
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE history
            SET memory=?, time=?
            WHERE user_id=?
        ''', (memory_binary, current_time, user_id))
        conn.commit()
        if cursor.rowcount == 0:
            return "No record found to update!"
        else:
            return "Record updated successfully."
    except sqlite3.OperationalError as e:
        return f"SQL Error: {e}"
    except sqlite3.DatabaseError as e:
        return f"Database Error: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"
    finally:
        conn.close()

def read_user_record(user_id):
    """
    Function to read data for context.
    """
    try:
        conn = sqlite3.connect("History.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM history WHERE user_id=?", (user_id,))
        user = cursor.fetchone()

        if user:
            user = list(user)
            user[1] = pickle.loads(user[1])  # Unpickle the BLOB data
            return tuple(user)  # Convert back to tuple if necessary
        else:
            return None  # User not found
    except sqlite3.OperationalError as e:
        print(f"SQL Error: {str(e)}")
        return None
    except sqlite3.DatabaseError as e:
        print(f"Database Error: {str(e)}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None
    finally:
        conn.close()

