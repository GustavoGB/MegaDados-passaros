import io
import json
import logging
import os
import os.path
import re
import subprocess
import unittest
import pymysql

from projeto import *

class TestProjeto(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global config
        cls.connection = pymysql.connect(
            host=config['HOST'],
            user=config['USER'],
            password=config['PASS'],
            database='p_megadados'
        )

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

    def setUp(self):
        conn = self.__class__.connection
        with conn.cursor() as cursor:
            cursor.execute('START TRANSACTION')

    def tearDown(self):
        conn = self.__class__.connection
        with conn.cursor() as cursor:
            cursor.execute('ROLLBACK')

    def test_adiciona_usuario(self):
        conn = self.__class__.connection
    
        nome = 'João Das Neves'
        email = '@hotmail'
        cidade = 'SP'
        adiciona_usuario(conn, nome, email, cidade)

        # Checa se o usuario existe.
        id = acha_usuario(conn, nome)
        self.assertIsNotNone(id)

        # Tenta achar um usuario inexistente.
        id = acha_usuario(conn, 'Jonas')
        self.assertIsNone(id)

    def test_remove_usuario(self):
        conn = self.__class__.connection
        email = '@'
        cidade = 'SP'
        adiciona_usuario(conn, 'Gustavo', email, cidade)
        id = acha_usuario(conn, 'Gustavo')

        res = lista_usuarios(conn)
        self.assertCountEqual(res, (id,))

        remove_usuario(conn, id)

        res = checa_ativo(conn, id)
        self.assertFalse(res)

    def test_muda_nome_usuario(self):
        conn = self.__class__.connection

        email = '@'
        cidade = 'SP'
        adiciona_usuario(conn, 'Victor', email, cidade)
        id = acha_usuario(conn, 'Victor')

        muda_nome_usuario(conn, id, 'Vitor')

        # Verifica se mudou.
        id_novo = acha_usuario(conn, 'Vitor')
        self.assertEqual(id, id_novo)

    def test_lista_usuarios(self):
        conn = self.__class__.connection

        # Verifica que ainda não tem usuarios no sistema.
        res = lista_usuarios(conn)
        self.assertFalse(res)

        # Adiciona alguns usuarios.
        usuarios_id = []
        email = '@'
        cidade = 'SP'
        for nome in ('Alexandra', 'Gabriela', 'Giovanna'):
            adiciona_usuario(conn, nome, email, cidade)
            usuarios_id.append(acha_usuario(conn, nome))

        # Verifica se os usuarios foram adicionados corretamente.
        res = lista_usuarios(conn)
        self.assertCountEqual(res, usuarios_id)

        # Remove os usuarios.
        for nome in usuarios_id:
            remove_usuario(conn, nome)

        # Verifica que todos os usuarios foram removidos logicamente.
        for nome in usuarios_id:
            res = checa_ativo(conn, nome)        
            self.assertFalse(res)

    def test_adiciona_passaro(self):
        conn = self.__class__.connection

        passaro = 'Pomba'

        # Adiciona passaro não existente.
        adiciona_passaro(conn, passaro)

        # Tenta adicionar o mesmo passaro duas vezes.
        try:
            adiciona_passaro(conn, passaro)
            self.fail('Nao deveria ter adicionado a mesma espécie duas vezes.')
        except ValueError as e:
            pass

        # Checa se o passaro existe.
        id = acha_passaro(conn, passaro)
        self.assertIsNotNone(id)

        # Tenta achar um passaro inexistente.
        id = acha_passaro(conn, 'esfiha')
        self.assertIsNone(id)

    def test_remove_passaro(self):
        conn = self.__class__.connection
        adiciona_passaro(conn, 'Águia')
        id = acha_passaro(conn, 'Águia')

        res = lista_passaros(conn)
        self.assertCountEqual(res, (id,))

        remove_passaro(conn, id)

        res = lista_passaros(conn)
        self.assertFalse(res)

    #def test_muda_nome_passaro(self):
     #   conn = self.__class__.connection

      #  adiciona_passaro(conn, 'Beija-flor')
       # adiciona_passaro(conn, 'Gavião')
        #id = acha_passaro(conn, 'Gavião')

        # Tenta mudar nome para algum nome já existente.
        #try:
         #   muda_nome_passaro(conn, id, 'alface')
          #  self.fail('Não deveria ter mudado o nome.')
        #except ValueError as e:
         #   pass

        # Tenta mudar nome para nome inexistente.
        #muda_nome_comida(conn, id, 'azeitona')

    def test_lista_passaros(self):
        conn = self.__class__.connection

        # Verifica que ainda não tem passaros no sistema.
        res = lista_passaros(conn)
        self.assertFalse(res)

        # Adiciona alguns passaros.
        passaros_id = []
        for p in ('Periquito', 'Canário', 'Calopsita'):
            adiciona_passaro(conn, p)
            passaros_id.append(acha_passaro(conn, p))

        # Verifica se os passaros foram adicionados corretamente.
        res = lista_passaros(conn)
        self.assertCountEqual(res, passaros_id)

        # Remove os passaros.
        for p in passaros_id:
            remove_passaro(conn, p)

        # Verifica que todos passaros foram removidos.
        res = lista_passaros(conn)
        self.assertFalse(res)

    #@unittest.skip('Em desenvolvimento.')
    def test_adiciona_preferencia_a_usuario(self):
        conn = self.__class__.connection

        # Cria alguns passaros.
        adiciona_passaro(conn, 'Cacatua')
        id_cacatua = acha_passaro(conn, 'Cacatua')

        adiciona_passaro(conn, 'Periquito')
        id_periquito = acha_passaro(conn, 'Periquito')

        # Cria alguns usuarios.
        email = '@'
        cidade = 'SP'
        adiciona_usuario(conn, 'José', email, cidade)
        id_jose = acha_usuario(conn, 'José')
        
        adiciona_usuario(conn, 'Mário', email, cidade)
        id_mario = acha_usuario(conn, 'Mário')
        
        adiciona_usuario(conn, 'Malaquias', email, cidade)
        id_malaquias = acha_usuario(conn, 'Malaquias')

        adiciona_usuario(conn, 'Pedro', email, cidade)
        id_pedro = acha_usuario(conn, 'Pedro')

        # Conecta comidas e perigos.
        adiciona_preferencia_a_usuario(conn, id_jose, id_cacatua)
        adiciona_preferencia_a_usuario(conn, id_jose, id_periquito)
        adiciona_preferencia_a_usuario(conn, id_mario, id_cacatua)
        adiciona_preferencia_a_usuario(conn, id_mario, id_periquito)
        adiciona_preferencia_a_usuario(conn, id_malaquias, id_cacatua)
        adiciona_preferencia_a_usuario(conn, id_pedro, id_periquito)

        res = lista_prefenrecias_de_usuario(conn, id_jose)
        self.assertCountEqual(res, (id_cacatua, id_periquito))

        res = lista_prefenrecias_de_usuario(conn, id_mario)
        self.assertCountEqual(res, (id_cacatua, id_periquito))

        res = lista_prefenrecias_de_usuario(conn, id_malaquias)
        self.assertCountEqual(res, (id_cacatua,))

        res = lista_prefenrecias_de_usuario(conn, id_pedro)
        self.assertCountEqual(res, (id_periquito,))

        # Testa se a remoção de uma comida causa a remoção das relações entre essa comida e seus perigos.
        remove_passaro(conn, id_periquito)

        res = lista_prefenrecias_de_usuario(conn, id_jose)
        self.assertCountEqual(res, (id_cacatua,))

        res = lista_prefenrecias_de_usuario(conn, id_mario)
        self.assertCountEqual(res, (id_cacatua,))

        res = lista_prefenrecias_de_usuario(conn, id_malaquias)
        self.assertCountEqual(res, (id_cacatua,))

        res = lista_prefenrecias_de_usuario(conn, id_pedro)
        self.assertFalse(res)

def run_sql_script(filename):
    global config
    with open(filename, 'rb') as f:
        subprocess.run(
            [
                config['MYSQL'], 
                '-u', config['USER'], 
                '-p' + config['PASS'], 
                '-h', config['HOST']
            ], 
            stdin=f
        )

def setUpModule():
    filenames = [entry for entry in os.listdir() 
        if os.path.isfile(entry) and re.match(r'.*_\d{3}\.sql', entry)]
    for filename in filenames:
        run_sql_script(filename)

def tearDownModule():
    run_sql_script('tear_down.sql')

if __name__ == '__main__':
    global config
    with open('config_tests.json', 'r') as f:
        config = json.load(f)
    logging.basicConfig(filename=config['LOGFILE'], level=logging.DEBUG)
    unittest.main(verbosity=2)
