import mysql.connector
from mysql.connector import Error
# from enum import Enum

def create_server_connection(host_name, user_name, user_password):
    db_connection = None
    try:
        db_connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return db_connection


def create_database(db_connection, query):
    cursor = db_connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")


def create_db_connection(host_name, user_name, user_password, db_name):
    db_connection = None
    try:
        db_connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return db_connection


def execute_query(query, pw,db):
    # if db_connection == None:
    db_connection = create_db_connection("localhost", "root", pw, db)  # Connect to the Database        cursor = db_connection.cursor()
    cursor = db_connection.cursor()
    try:
        cursor.execute(query)
        db_connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


    
def create_phone_model_table(pw, db):
    models_query = """
            CREATE TABLE IF NOT EXISTS phone_models (
                model VARCHAR(40) PRIMARY KEY,
                guide_id INT,
                company VARCHAR(40),
                release_yr INT 
            );
            """
    execute_query(models_query, pw, db)

def create_components_table(pw, db):
    components_query = """
            CREATE TABLE IF NOT EXISTS components (
                component_id INT PRIMARY KEY,
                name VARCHAR(40),
                fastener_type VARCHAR(40) 
            );
            """
    execute_query(components_query, pw, db)

def create_graphing_rules_table(pw,db):
    rules_query = """
            CREATE TABLE IF NOT EXISTS graph_rules (
                component_1 INT,
                component_2 INT,
                model VARCHAR(40),
                relation ENUM ('connection', 'pre-requisite'),

                PRIMARY KEY (component_1, component_2, model)
            );
            """
    execute_query(rules_query, pw, db)

def create_table_dependencies(pw, db):
    alter_graph_rules_1 = """
            ALTER TABLE graph_rules 
            ADD FOREIGN KEY(component_1)
            REFERENCES components(component_id)
            -- ON DELETE SET NULL;
            """
    alter_graph_rules_2 = """
            ALTER TABLE graph_rules 
            ADD FOREIGN KEY(component_2)
            REFERENCES components(component_id)
            -- ON DELETE SET NULL;
            """

    alter_graph_rules_3 = """
            ALTER TABLE graph_rules 
            ADD FOREIGN KEY(model)
            REFERENCES phone_models(model)
            -- ON DELETE SET NULL;
            """

    create_phone_component_relations_table = """
            CREATE TABLE IF NOT EXISTS phone_component_relations (
                
                component_id INT ,
                model VARCHAR(40),

                PRIMARY KEY (component_id, model),
                FOREIGN KEY(component_id) REFERENCES components(component_id),
                FOREIGN KEY(model) REFERENCES phone_models(model)
            );
            """
    execute_query(alter_graph_rules_1, pw, db)
    execute_query(alter_graph_rules_2, pw, db)
    execute_query(alter_graph_rules_3, pw, db)
    execute_query(create_phone_component_relations_table, pw, db) 

def show_database(connection):
    show_db_query = "SHOW DATABASES"
    with connection.cursor() as cursor:
        cursor.execute(show_db_query)
        for db in cursor:
            print(db)
