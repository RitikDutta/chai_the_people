import datetime
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import pandas as pd
from tabulate import tabulate
import os
import time


class CassandraCRUD:
    def __init__(self, keyspace):
        self.keyspace = keyspace
        cloud_config= {'secure_connect_bundle': 'secure-connect-test.zip'}
        auth_provider = PlainTextAuthProvider('biTEHxuyRqFgCcFpnEMOMvkN', 'PyqybfDQpPOaLp44hlWbb1Yb7bZ2Mn5Mt-_DGMOs.qBj.JY.Z,FAnB.9ncCD+F2EsSJ7W6XD,l,3S9gZW7bgWSMQDHKvTI7Iams2.hRRz6W_biRSrttvGgs1WhAl-in9')
        self.cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
        self.session = self.cluster.connect(self.keyspace)

    def create_survey_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS survey (
            question_id int,
            date_added date,
            question text,
            options text,
            PRIMARY KEY (question_id)
        );
        """
        self.session.execute(create_table_query)
        
    def create_user_table(self):
        create_table = """
        CREATE TABLE IF NOT EXISTS user (
            user_id text,
            name text,
            gender text,
            age int,
            annual_income int,
            city text,
            marital_status text,
            qualification text,
            date_added date,
            PRIMARY KEY (user_id)
        );
        """
        self.session.execute(create_table)

    def create_response_table(self):
        create_table = """
        CREATE TABLE IF NOT EXISTS response (
            user_id text,
            question_id int,
            response text,
            date_added date,
            PRIMARY KEY (user_id, question_id),
        );
        """
        self.session.execute(create_table)

        
    def insert_survey_data(self, question_id, date_added, question, options):
        insert_query = """
        INSERT INTO survey (
        question_id, 
        date_added, 
        question,
        options
        ) VALUES ('{}', '{}', '{}', '{}')""".format(question_id, date_added, question, options)
        self.session.execute(insert_query)
        print(tabulate(self.get_db("survey"), headers='keys', tablefmt='plain'))

    def insert_user_data(self, user_id, date_added, name="", gender="", age=18, annual_income=200000, city="", marital_status="", qualification=""):
        insert_query = """
        INSERT INTO user (
        user_id,
        name,
        gender,
        age,
        annual_income,
        city,
        marital_status,
        qualification,
        date_added
        ) VALUES ('{}', '{}', '{}', {}, {}, '{}', '{}', '{}', '{}')""".format(user_id, name, gender, age, annual_income, city, marital_status, qualification, date_added)
        self.session.execute(insert_query)
        print(tabulate(self.get_db("user"), headers='keys', tablefmt='plain'))

    def insert_response_data(self, user_id, question_id, response, date_added):
        insert_query = """
        INSERT INTO response (
        user_id,
        question_id,
        response,
        date_added
        ) VALUES ('{}', {}, '{}', '{}')""".format(user_id, question_id, response, date_added)
        self.session.execute(insert_query)
        print(tabulate(self.get_db("response"), headers='keys', tablefmt='plain'))
        

        
    def delete_table(self, table_name):
        delete_table_query = "DROP TABLE " + table_name + ";"
        try:
            self.session.execute(delete_table_query)
            print("Table " + table_name + " deleted successfully")
        except Exception as e:
            print("Error deleting table: ", e)
            
    def show(self, table_name):
        query = "SELECT * FROM test_key.{};".format(table_name)
        df = pd.DataFrame(list(self.session.execute(query)))
        print(tabulate(df, headers='keys', tablefmt='fancy_grid'))
    
    def last(self, table_name):
        query = "SELECT question_id FROM test_key.{};".format(table_name)
        data = self.session.execute(query)
        df = pd.DataFrame([d for d in data])
        return df

        
    def is_present(self, user_id):
        select_query = "SELECT * FROM user WHERE user_id = %s"
        result = self.session.execute(select_query, (user_id)).one()
        return True if result else False
    
    def get_db(self, table):
        query = "SELECT * FROM {}.{}".format(self.keyspace, table)
        data = self.session.execute(query)
        df = pd.DataFrame([d for d in data])
        return df
    def test(self, uid):
        query = "SELECT user_id FROM user WHERE primary_keys = {} LIMIT 1".format(uid)

        data = self.session.execute(query)
        print(data)