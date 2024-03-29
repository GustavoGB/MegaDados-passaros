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

    
        #Inserimos algum posts
        titulo = 'Primeiro post'
        texto = titulo
        url = 'https://'
        adiciona_post(conn, titulo, id, texto, url)

        #Guardamos o id do post
        id_post = acha_post(conn, id, titulo)
        #Removemos o usuario
        remove_usuario(conn, id)

        #Checamos se ele foi desativado
        res = checa_ativo(conn, id)
        self.assertFalse(res)

        #Checamos se o post foi desativado
        res = checa_ativo_post(conn, id_post)
        self.assertFalse(res)



    def test_adiciona_tags(self):

        conn = self.__class__.connection
        email = '@'
        cidade = 'SP'
        nome = 'VictorLM' #Adicionando o usuario que será marcado
        nome2 = 'Gustavo'
        adiciona_usuario(conn, nome, email, cidade)
        #Adiciona outro usuario para teste
        adiciona_usuario(conn, nome2, email, cidade)

        #adicionando o passaro que será marcado
        adiciona_passaro(conn, "Pomba")

        #Checa se o passaro existe
        id_passaro = acha_passaro(conn, "Pomba")
        self.assertIsNotNone(id_passaro)

        # Checa se o usuario existe.
        id_usuario = acha_usuario(conn, nome)
        self.assertIsNotNone(id_usuario)
        # Checa se o usuario 2 existe.
        id_usuario2 = acha_usuario(conn, nome2)
        self.assertIsNotNone(id_usuario2)

        res = lista_usuarios(conn)
        self.assertCountEqual(res, (id_usuario, id_usuario2))

    
        #Inserimos algum posts
        titulo = 'Primeiro post'
        texto = "Olha pra ser sincero @VictorLM, @Gustavo, eu não gosto de #Pomba."
        url = 'https://'
        adiciona_post(conn, titulo, id_usuario, texto, url)

        #Guardamos o id do post
        id_post = acha_post(conn, id_usuario, titulo)

        #Adiciona tags em tags de usuario e passaro
        adiciona_tags(conn,id_post)
        res = lista_tags_usuario(conn, id_usuario)
        #Confere se a tag foi adicionada corretamente
        self.assertEqual(res, (id_post, ))

        res = lista_tags_usuario(conn, id_usuario2)
        #Confere se a tag foi adicionada corretamente
        self.assertEqual(res, (id_post, ))

        res = lista_tags_passaro(conn, id_passaro)
        #Confere se a tag foi adicionada corretamente
        self.assertEqual(res, (id_post,))
    
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

    def test_adiciona_post(self):
        conn = self.__class__.connection

        #Cria usuario
        email = '@'
        cidade = 'SP'
        adiciona_usuario(conn, 'José', email, cidade)
        id_usuario = acha_usuario(conn, 'José')

        #Checa se foi criado
        self.assertIsNotNone(id_usuario)
        
        #Cria post
        adiciona_post(conn, 'Exemplo', id_usuario, 'Texto', 'http://')

        #Checa se foi criado
        self.assertIsNotNone(lista_posts_usuario(conn, id_usuario)) #Lista todos os posts do usuario

        #Tenta adicionar post sem título
        try:
            adiciona_post(conn, None, id_usuario, 'Texto', 'http://')
            self.fail('Nao deveria ter adicionado o post sem título.')
        except ValueError as e:
            pass
                
    def test_remove_post(self):
        conn = self.__class__.connection

        #Cria usuario
        email = '@'
        cidade = 'RJ'
        adiciona_usuario(conn, 'Bruno Dratcu', email, cidade)
        id_usuario = acha_usuario(conn, 'Bruno Dratcu')

        #Checa se foi criado
        self.assertIsNotNone(id_usuario)

        adiciona_post(conn, 'Meu pássaro favorito', id_usuario, 'Canário', 'https://')

        #Acha o post
        id_post = acha_post(conn, id_usuario, 'Meu pássaro favorito')#Supondo que um usuario nao tenha posts com o mesmo titulo
        self.assertIsNotNone(id_post)

        #Removemos o post
        remove_post(conn, id_post)

        #Checamos se o post foi desativado
        res = checa_ativo_post(conn, id_post)
        self.assertFalse(res)

    def test_lista_posts(self):
            conn = self.__class__.connection

            # Verifica que ainda não tem posts no sistema.
            res = lista_posts(conn)
            self.assertFalse(res)

            #Cria usuario
            email = '@'
            cidade = 'RJ'
            adiciona_usuario(conn, 'Bruno Dratcu', email, cidade)
            id_usuario = acha_usuario(conn, 'Bruno Dratcu')

            #Checa se foi criado
            self.assertIsNotNone(id_usuario)

            # Adiciona alguns posts.
            adiciona_post(conn, 'Meu pássaro favorito', id_usuario, 'Canário', 'https://')
            adiciona_post(conn, 'Passarinho', id_usuario, 'lalala', 'https://')
            adiciona_post(conn, 'Animais', id_usuario, 'Periquito', 'https://')

            l_ids = []
            id1 = acha_post(conn, id_usuario,'Meu pássaro favorito') 
            id2 = acha_post(conn, id_usuario,'Passarinho') 
            id3 = acha_post(conn, id_usuario,'Animais') 
            l_ids.append(id1)
            l_ids.append(id2)
            l_ids.append(id3)

            # Verifica se os posts foram adicionados corretamente.
            res = lista_posts(conn) #Lista todos os posts, não apenas de um usuário
            self.assertCountEqual(res, l_ids)

            # Remove os posts.
            for p in res:
                remove_post(conn, p)

            # Verifica que todos posts foram removidos.
            for p in res:
                ativo = checa_ativo_post(conn, p)
                self.assertFalse(ativo)

    def test_adiciona_visualizacao(self):
            conn = self.__class__.connection

            #Cria usuario
            email = '@'
            cidade = 'RJ'
            adiciona_usuario(conn, 'Bruno Draco', email, cidade)
            id_usuario = acha_usuario(conn, 'Bruno Draco')

            #Checa se foi criado
            self.assertIsNotNone(id_usuario)

            #Cria o post de um usuario
            titulo = 'Meu último post'
            adiciona_post(conn, titulo, id_usuario, 'Cacatua', 'https://')
            id_post = acha_post(conn, id_usuario, titulo)
            #Checa se foi criado
            self.assertIsNotNone(id_post)

            #Um usuario visualiza o post
            adiciona_visualizacao(conn, id_usuario,id_post,"Iphone X", "Firefox", "'192.168.4.13")
            
            #Checa se esta visualizado
            res = lista_visualizacao(conn, id_post)
            self.assertIsNotNone(res)

    def test_joinha(self):
        conn = self.__class__.connection

        #Cria usuario
        email = '@'
        cidade = 'RJ'
        adiciona_usuario(conn, 'Bruno Draco', email, cidade)
        id_usuario = acha_usuario(conn, 'Bruno Draco')

        #Checa se foi criado
        self.assertIsNotNone(id_usuario)

        #Cria o post de um usuario
        titulo = 'Meu último post'
        adiciona_post(conn, titulo, id_usuario, 'Cacatua', 'https://')
        id_post = acha_post(conn, id_usuario, titulo)
        #Checa se foi criado
        self.assertIsNotNone(id_post)
        
        #O usuario visualiza o post
        adiciona_visualizacao(conn, id_usuario,id_post,"Iphone X", "Firefox", "'192.168.4.13")
        
        #Checa se esta visualizado
        res = lista_visualizacao(conn, id_post)
        self.assertIsNotNone(res)

        #O usuário registra um joinha
        adiciona_joinha(conn, id_usuario, id_post, 1)
        res = lista_joinhas_post(conn, id_post)
        #Checa se esta registrado
        self.assertCountEqual(res, (id_usuario,))

        #Checa se deu joinha mesmo
        res = lista_joinha_unico(conn, id_usuario, id_post)
        self.assertTrue(res)

        #Troca para anti-joinha
        adiciona_joinha(conn, id_usuario, id_post, 0)

        #Checa se deu anti-joinha mesmo
        res =lista_joinha_unico(conn, id_usuario, id_post)
        self.assertFalse(res)

        #Remove o joinha
        remove_joinha(conn, id_usuario, id_post)
        #Checa se foi removido
        res = lista_joinhas_post(conn, id_post)
        self.assertFalse(res)

        #Confere se não adiciona dois joinhas do mesmo usuario no mesmo post
        adiciona_joinha(conn, id_usuario, id_post, 0)
        adiciona_joinha(conn, id_usuario, id_post, 0)
        #Lista
        res = lista_joinhas_post(conn, id_post)
        self.assertCountEqual(res, (id_usuario,)) #Só pode ter um
    
    def test_procedure_consulta_posts(self):
        conn = self.__class__.connection
        #Cria usuario
        email = '@'
        cidade = 'RJ'
        adiciona_usuario(conn, 'Bruno Draco', email, cidade)
        id_usuario = acha_usuario(conn, 'Bruno Draco')

        #Checa se foi criado
        self.assertIsNotNone(id_usuario)

        #Cria vários posts do usuario
        titulo = 'Meu primeiro post'
        adiciona_post(conn, titulo, id_usuario, 'Cacatua', 'https://')
        id_post1 = acha_post(conn, id_usuario, titulo)
        #Checa se foi criado
        self.assertIsNotNone(id_post1)

        titulo = 'Meu segundo post'
        adiciona_post(conn, titulo, id_usuario, 'Cacatua', 'https://')
        id_post2 = acha_post(conn, id_usuario, titulo)
        #Checa se foi criado
        self.assertIsNotNone(id_post2)

        titulo = 'Meu terceiro post'
        adiciona_post(conn, titulo, id_usuario, 'Cacatua', 'https://')
        id_post3 = acha_post(conn, id_usuario, titulo)
        #Checa se foi criado
        self.assertIsNotNone(id_post3)

        #Consulta ordem cronológica reversa dos posts
        res = procedure_consulta_posts(conn, id_usuario) 
        self.assertEqual(res, (id_post1, id_post2, id_post3))
    
    def test_procedure_usuario_popular(self):
        conn = self.__class__.connection
        email = '@'
        cidade = 'SP'
        nome = 'VictorLM' #Adicionando o usuario
        adiciona_usuario(conn, nome, email, cidade)
        #Adiciona outro usuario para teste
        nome2 = 'Gustavo'
        adiciona_usuario(conn, nome2, email, cidade)

        #Para efeitos de teste, adiciona um usuário que não cria nenhum post
        nome3 = "Claudio"
        cidade2 = "RJ"
        #De outra cidade diferente
        adiciona_usuario(conn, nome3, email, cidade2)


        # Checa se o usuario existe.
        id_usuario = acha_usuario(conn, nome)
        self.assertIsNotNone(id_usuario)
        # Checa se o usuario 2 existe.
        id_usuario2 = acha_usuario(conn, nome2)
        self.assertIsNotNone(id_usuario2)
       # Checa se o usuario 3 existe.
        id_usuario3 = acha_usuario(conn, nome3)
        self.assertIsNotNone(id_usuario3)

        res = lista_usuarios(conn)
        self.assertCountEqual(res, (id_usuario, id_usuario2, id_usuario3))

    
        #Inserimos algum posts
        titulo = 'Primeiro post'
        texto = "Olha pra ser sincero @Claudio, @Gustavo, eu não gosto de #Pomba."
        url = 'https://'
        adiciona_post(conn, titulo, id_usuario, texto, url)

        titulo2 = "Segundo post"
        texto2 = "Vou marcar só o @Claudio."
        adiciona_post(conn, titulo2, id_usuario, texto2, url)

        #Guardamos o id do post
        id_post = acha_post(conn, id_usuario, titulo)
        id_post2 = acha_post(conn, id_usuario, titulo2)

        #Adiciona tags
        adiciona_tags(conn,id_post)
        adiciona_tags(conn,id_post2)
        res = lista_tags_usuario(conn, id_usuario3)
        #Confere se as tags foi adicionada corretamente
        self.assertEqual(res, (id_post, id_post2))

        #Confere a view do usuário mais popular
        #Precisa ser o Claudio e o Gustavo, que foi marcado num post a mais
        #Os dois estão em cidades diferentes, mas o VictorLM não (que não deve aparecer pois nao é marcado)
        num = 2 #Passa-se o número de cidades que deseja-se pesquisar
        res = procedure_usuario_popular(conn, num)
        self.assertEqual(res, ((nome3, cidade2), (nome2, cidade))) #Como são duas, esperamos dois resultados
    
    def test_procedure_lista_referencias(self):
        conn = self.__class__.connection
        email = '@'
        cidade = 'SP'
        nome = 'VictorLM' #Adicionando o usuario
        adiciona_usuario(conn, nome, email, cidade)
        #Adiciona outro usuario para teste
        nome2 = 'Gustavo'
        adiciona_usuario(conn, nome2, email, cidade)
        #Adiciona outro usuario para teste
        nome3 = 'Claudio'
        adiciona_usuario(conn, nome3, email, cidade)

        # Checa se o usuario existe.
        id_usuario = acha_usuario(conn, nome)
        self.assertIsNotNone(id_usuario)
        # Checa se o usuario 2 existe.
        id_usuario2 = acha_usuario(conn, nome2)
        self.assertIsNotNone(id_usuario2)
        # Checa se o usuario 3 existe.
        id_usuario3 = acha_usuario(conn, nome3)
        self.assertIsNotNone(id_usuario3)

        res = lista_usuarios(conn)
        self.assertCountEqual(res, (id_usuario, id_usuario2, id_usuario3))

        #Inserimos algum posts
        titulo = 'Primeiro post'
        texto = "Olha pra ser sincero @Gustavo, eu não gosto de #Pomba."
        url = 'https://'
        adiciona_post(conn, titulo, id_usuario, texto, url)

        titulo2 = "Segundo post"
        texto2 = "Vou marcar só o @Gustavo."
        adiciona_post(conn, titulo2, id_usuario, texto2, url)

        #Terceiro post, mas criado por outro usuario
        titulo3 = "Post"
        texto3 = "Vou marcar o @Gustavo."
        adiciona_post(conn, titulo3, id_usuario3, texto3, url)

        #Guardamos o id do post
        id_post = acha_post(conn, id_usuario, titulo)
        id_post2 = acha_post(conn, id_usuario, titulo2)
        id_post3 = acha_post(conn, id_usuario3, titulo3)


        #Adiciona tags
        adiciona_tags(conn,id_post)
        adiciona_tags(conn,id_post2)
        adiciona_tags(conn,id_post3)

        res = lista_tags_usuario(conn, id_usuario2)
        #Confere se as tags foi adicionada corretamente
        self.assertEqual(res, (id_post, id_post2, id_post3))

        #Confere a função que lista os usuários que referenciam o Gustavo
        #Deve retornar tanto o VictorLM quanto o Claudio
        res = procedure_lista_referencias(conn, id_usuario2)
        self.assertEqual(res, (id_usuario, id_usuario3))

    def test_view_aparelho_browser(self):
        conn = self.__class__.connection
        #Cria usuario que vai criar o post
        email = '@'
        cidade = 'RJ'
        nome = 'Usuario'
        adiciona_usuario(conn, nome, email, cidade)
        id_usuario = acha_usuario(conn, nome)
        #Cria o usuario que vai visualizar o post
        nome2 = 'Usuario2'
        adiciona_usuario(conn, nome2, email, cidade)
        id_usuario2 = acha_usuario(conn, nome2)
        #Cria outro usuario que vai visualizar o post
        nome3 = 'Usuario3'
        adiciona_usuario(conn, nome3, email, cidade)
        id_usuario3 = acha_usuario(conn, nome3)
        #Cria o usuario que vai visualizar o post
        nome4 = 'Usuario4'
        adiciona_usuario(conn, nome4, email, cidade)
        id_usuario4 = acha_usuario(conn, nome4)


        #Checa se foi criado
        self.assertIsNotNone(id_usuario)
        self.assertIsNotNone(id_usuario2)
        self.assertIsNotNone(id_usuario3)
        self.assertIsNotNone(id_usuario4)


        #Cria o post de um usuario
        titulo = 'Meu último post'
        adiciona_post(conn, titulo, id_usuario, 'Cacatua', 'https://')
        id_post = acha_post(conn, id_usuario, titulo)
        #Checa se foi criado
        self.assertIsNotNone(id_post)

        #Usuarios visualizam o post
        adiciona_visualizacao(conn, id_usuario2 ,id_post,"Iphone X", "Firefox", "'192.168.4.13")
        adiciona_visualizacao(conn, id_usuario3 ,id_post,"Iphone 7", "Chrome", "'192.168.4.13")
        adiciona_visualizacao(conn, id_usuario4 ,id_post,"Iphone 8", "Explorer", "'192.168.4.13")

        #Checa se esta visualizado
        res = lista_visualizacao(conn, id_post)
        self.assertIsNotNone(res)

        tabela_cruzada = (('Iphone X', 'Firefox'), ('Iphone 7', 'Chrome'), ('Iphone 8', 'Explorer'))

        #Chama a view
        res = view_aparelho_browser(conn)
        self.assertEqual(res, tabela_cruzada)

    def test_view_url_passaros(self):
        conn = self.__class__.connection
        email = '@'
        cidade = 'SP'
        nome = 'VictorLM' #Adicionando o usuario que será marcado
        adiciona_usuario(conn, nome, email, cidade)

        #adicionando o passaro que será marcado
        adiciona_passaro(conn, "Pomba")

        #Checa se o passaro existe
        id_passaro = acha_passaro(conn, "Pomba")
        self.assertIsNotNone(id_passaro)

        # Checa se o usuario existe.
        id_usuario = acha_usuario(conn, nome)
        self.assertIsNotNone(id_usuario)

    
        #Inserimos algum posts
        titulo = 'Primeiro post'
        texto = "Eu não gosto de #Pomba."
        url = 'https://'
        adiciona_post(conn, titulo, id_usuario, texto, url)

        #Guardamos o id do post
        id_post = acha_post(conn, id_usuario, titulo)

         #Adiciona tags
        adiciona_tags(conn,id_post)

        res = lista_tags_passaro(conn, id_passaro)
        #Confere se a tag foi adicionada corretamente
        self.assertEqual(res, (id_post,))

        #Adiciona a url
        adiciona_url_passaro(conn, id_passaro, id_post)
        res = view_url_passaros(conn)
        self.assertTrue(res) 
    

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
