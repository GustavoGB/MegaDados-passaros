import unittest
import pymysql
import json
from functools import partial
import subprocess

def run_db_query(connection, query, args=None):
    with connection.cursor() as cursor:
        print('Executando query:')
        cursor.execute(query, args)
        for result in cursor:
            print(result)
            
def return_db_results(connection, query, args=None):#Gambiarra para pegar o id
    with connection.cursor() as cursor:
        cursor.execute(query, args)
        l = []
        for result in cursor:
            l.append(result) 
        return result
    
#TESTES: INSERIR USUARIO, REMOVER USUARIO(REMOVER LOGICAMENTE TAMBÉM TODOS OS SEUS POSTS),
#  INSERIR PASSARO (NÃO DEIXAR INSERIR DOIS PASSAROS DO MESMO TIPO), TENTAR INSERIR POST SEM TÍTULO,
# INSERIR AS TAGS DE USUARIO E PASSAROS

class TestCase(unittest.TestCase):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='vlm1998',
        database='redes')

    db = partial(run_db_query, connection)

    @classmethod
    def setupClass(cls, TestCase):
        with open('script_01.sql' , 'rb') as f:
            res = subprocess.run('mysql -u root -proot < script_01.sql'.split(), stdin=f)
            print(res)       

    def test_insercao_usuario(self):
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='vlm1998',
            database='p_megadados')

        db = partial(run_db_query, connection)

        query = "INSERT INTO usuario (nome, EMAIL, cidade) VALUES ('Joao', 'joao@hotmail.com', 'SP')"
        run_db_query(connection, query)

        query = 'SELECT nome, EMAIL, cidade FROM usuario'
        self.assertEqual(return_db_results(connection, query), ('Joao', 'joao@hotmail.com', 'SP'), "Deveria retorna os atributos inseridos")
    
    def test_remove_usuario(self):
        pass #ESPERAR A CRIAÇÃO DOS TRIGGERS
        
    def test_insercao_passaro(self): #Checa inserção e a constraint unique na espécie
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='vlm1998',
            database='p_megadados')

        db = partial(run_db_query, connection)

        query = "INSERT INTO passaro (especie) VALUES ('Pomba Obesa')"
        run_db_query(connection, query)

        query = 'SELECT especie FROM passaro'
        self.assertEqual(return_db_results(connection, query), ('Pomba Obesa',), "Deveria retorna os atributos inseridos")

        try:
            query = "INSERT INTO passaro (especie) VALUES ('Pomba Obesa')"
            run_db_query(connection, query)
            self.assertEqual(True, False, "Se chegou aqui inseriu especies duplicadas")
        except:
            self.assertEqual(True, True, "Se chegou aqui é porque não inseriu especies duplicadas")

    def test_post_titulo(self):
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='vlm1998',
            database='p_megadados')

        db = partial(run_db_query, connection)
        try:
            query = "INSERT INTO post (id_usuario, texto, url) VALUES (1, 'textando o texto', 'http://')"
            run_db_query(connection, query)
            self.assertEqual(True, False, "Se chegou aqui inseriu post sem título")
        except: 
            self.assertEqual(True, True, "Se chegou aqui não inseriu post sem título")
        
    def test_tag_user(self):
        pass
    
    def test_tag_passaro(self):
        pass

if __name__ == '__main__':
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='vlm1998',
        database='redes')
    db = partial(run_db_query, connection)

    unittest.main()
    connection.close()
