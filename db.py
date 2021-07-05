import psycopg2
conn = psycopg2.connect( user="postgres", password="karimojid", host="localhost", port="5432", database="blog")
cur = conn.cursor()

def create_tables():

#Creating table as per requirement

    command = """CREATE TABLE if not exists files (
            id serial primary key,
            file_name text not null,
            file_data bytea not null,
            date_posted timestamp default current_timestamp
    )"""
    
    
    try:
        
        cur.execute(command)
        # commit the changes
        conn.commit()
        # close communication with the PostgreSQL database server
        cur.close()
        print("table created")
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
