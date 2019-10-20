from fastapi import FastAPI
import pymysql

app = FastAPI()


#Ideal para conec pois nao mostra a senha, utlizando o de baixo para testes. 

#class TestProjeto(unittest.TestCase):
#    @classmethod
#    def setUpClass(cls):
#        global config
#        cls.connection = pymysql.connect(
#            host=config['HOST'],
#            user=config['USER'],
#            password=config['PASS'],
#            database='p_megadados'
#        )

#   @classmethod
#   def tearDownClass(cls):
#       cls.connection.close()

def connect_db(host='localhost',user='root',password='MegaDados',database='rede_passaros'):
    conn = pymysql.connect(
        host='localhost',
        user='megadados',
        password='linux123',
        database='p_megadados')
    return conn

#Adiciona Usuario
@app.post("/usuarios/{id_usuario}")
def adiciona_usuario(conn, nome, email, cidade):
    conn = connect_db()
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO usuario (nome, EMAIL, cidade) VALUES (%s, %s, %s)', (nome, email, cidade))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {nome} na tabela perigo')

#Encontra Usuario
@app.get("/usuarios/{id_usuario}")
def acha_usuario(conn, nome):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario FROM usuario WHERE nome = %s', (nome))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None		
#Muda nome do Usuario
@app.put("/usuarios/{id_usuario}")
def muda_nome_usuario(conn, id_usuario, novo_nome):
    conn = connect_db()
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE usuario SET nome=%s where id_usuario=%s', (novo_nome, id_usuario))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso alterar nome do id {id} para {novo_nome} na tabela usuario')
#Remove usuario
@app.delete("/usuario/{id_usuario}")
def remove_usuario(conn, id_usuario):
    conn = connect_db()    
    with conn.cursor() as cursor:
        try:
        	cursor.execute('UPDATE usuario SET ativo = False WHERE id_usuario=%s', (id_usuario))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso remover usuario de id {id} na tabela usuario')
#Lista usuarios
@app.get("/usuario/{id_usuario}")
def lista_usuarios(conn):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario from usuario')
        res = cursor.fetchall()
        usuarios = tuple(x[0] for x in res)
        return usuarios

#Checa se usuario existe        
@app.get("/usuario/{id_usuario}")
def checa_ativo(conn, id_usuario):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('SELECT ativo FROM usuario WHERE id_usuario = %s', (id_usuario))
        res = cursor.fetchone()
        if res:
            return res[0] #Retorna se está 1 ou 0
        else:
            return -1

#Adiciona Passaros
@app.post("/passaros/{id_passaro}")
def adiciona_passaro(conn, especie):
    conn = connect_db()
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO passaro (especie) VALUES (%s)', (especie))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {especie} na tabela comida')
#Encontra um passaro especifico
@app.get("/passaros/{id_passaro}")
def acha_passaro(conn, especie):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_passaro FROM passaro WHERE especie = %s', (especie))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None
#Deleta passaros            
@app.delete("/passaros/{id_passaro}")
def remove_passaro(conn, id_passaro):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM passaro WHERE id_passaro=%s', (id_passaro))

#Lista todos os passaros
@app.get("/passaros/{id_passaro}")
def lista_passaros(conn):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_passaro from passaro')
        res = cursor.fetchall()
        passaros = tuple(x[0] for x in res)
        return passaros

#Adiciona preferencia de um passaro para um usuario
@app.post("/preferencias/{id_usuario}/{id_passaro}")
def adiciona_preferencia_a_usuario(conn, id_usuario, id_passaro):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO usuario_passaro VALUES (%s, %s)', (id_usuario, id_passaro))

#Remove preferencia de um passaro para um usuario
@app.delete("/preferencias/{id_usuario}/{id_passaro}")
def remove_preferencia_de_usuario(conn, id_usuario, id_passaro):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM usuario_passaro WHERE id_usuario=%s AND id_passaro=%s',(id_usuario, id_passaro))

#Lista todas as preferencias de um usuario
@app.get("/preferencias/{id_usuario}")
def lista_prefenrecias_de_usuario(conn, id_usuario):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_passaro FROM usuario_passaro WHERE id_usuario=%s', (id_usuario))
        res = cursor.fetchall()
        preferencias = tuple(x[0] for x in res)
        return preferencias

#Lista todas as preferencias(id_usuarios) de um certo passaro 
@app.get("/preferencias/{id_passaro}")
def lista_preferencias_de_passaro(conn, id_passaro):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario FROM usuario_passaro WHERE id_passaro=%s', (id_passaro))
        res = cursor.fetchall()
        usuarios = tuple(x[0] for x in res)
        return usuarios

#Adiciona post na rede social
@app.post("/posts/{titulo}/{id_usuario}/{texto}/{url}")
def adiciona_post(conn, titulo, id_usuario, texto, url):
    conn = connect_db()
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO post (titulo, id_usuario, texto, url) VALUES (%s, %s, %s, %s)', (titulo, id_usuario, texto, url))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso adcionar {titulo} na tabela post')

#Remove post da rede social
@app.delete("/posts/{id_post}")
def remove_post(conn, id_post):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('UPDATE post SET ativo = False WHERE id_post = %s', (id_post))

#Lista posts de usuario
@app.get("/posts/{id_post}/{id_usuario}")
def lista_posts_usuario(conn, id_usuario):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_post FROM post WHERE id_usuario=%s', (id_usuario))
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts

#Lista todos os posts
@app.get("/posts/{id_post}")
def lista_posts(conn):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_post FROM post')
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts

#Encontra post baseado no titulo e no usuario
@app.get("/posts/{id_post}/{id_usuario}/{titulo}")
def acha_post(conn, id_usuario, titulo):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_post FROM post WHERE id_usuario=%s AND titulo=%s', (id_usuario, titulo))
        res = cursor.fetchone()
        if res:
            return res[0] 
        else:
            return None
        
#Adiciona tag usuario e tag passaros
@app.post("/tag_usuario/{id_post}/{id_usuario}")
@app.post("/tag_passaro/{id_post}/{id_passaro}")
def adiciona_tags(conn, id_post):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('SELECT texto FROM post WHERE id_post=%s', id_post)
        res = cursor.fetchone()
        ##Parsear o res, se tiver @ add ao tag_usuario, se tiver # add ao tag_passaro.
        try:
            texto = str(res[0])
            tags_usuario = []
            lista_texto = texto.split()
            for palavra in lista_texto:
                i = palavra.find("@")
                if(i!=-1):
                    if(palavra.find(",")):
                        virgula = palavra.find(",")
                        palavra = palavra[1:virgula]
                        tags_usuario.append(palavra)
                    elif(palavra.find(".")):
                        ponto = palavra.find(".")
                        palavra = palavra[1:ponto]
                        tags_usuario.append(palavra)
                    else:
                        tags_usuario.append(palavra)

            tags_passaro = []
            for palavra in lista_texto:
                i = palavra.find("#")
                if(i!=-1):
                    if(palavra.find(",")):
                        virgula = palavra.find(",")
                        palavra = palavra[1:virgula]
                        tags_passaro.append(palavra)
                    elif(palavra.find(".")):
                        ponto = palavra.find(".")
                        palavra = palavra[1:ponto]
                        tags_passaro.append(palavra)
                    else:
                        tags_passaro.append(palavra)

        except Exception as e:
            return -1   

        for usuario in tags_usuario:
            id_usuario = acha_usuario(conn, usuario)
            if (id_usuario != None):
                try:
                    cursor.execute('INSERT INTO tag_usuario (id_post, id_usuario) VALUES (%s, %s)', (id_post, id_usuario))
                except pymysql.err.IntegrityError as e:
                    raise ValueError(f'Não posso adcionar {id_usuario} na tabela tag_usuario')
        for passaro in tags_passaro:
            id_passaro = acha_passaro(conn, passaro)
            if (id_passaro != None):
                try:
                    cursor.execute('INSERT INTO tag_passaro (id_post, id_passaro) VALUES (%s, %s)', (id_post, id_passaro))
                except pymysql.err.IntegrityError as e:
                    raise ValueError(f'Não posso adcionar {id_passaro} na tabela tag_passaro')

#Lista tags do usuarios baseado em marcacoes de post
@app.get("/tags_usuario/{id_post}/{id_usuario}")
def lista_tags_usuario(conn, id_usuario):
    conn = connect_db() 
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_post FROM tag_usuario WHERE id_usuario=%s', id_usuario)
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts

#Lista tags de passaros basedo em marcacoes de post
@app.get("/tags_passaro/{id_post}/{id_passaro}")
def lista_tags_passaro(conn, id_passaro):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_post FROM tag_passaro WHERE id_passaro=%s', id_passaro)
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts

#Adiciona uma view
@app.post("/view/{id_usuario}/{id_post}/{id_post}/{id_aparelho}/{aparelho}/{browser}/{ip}") 
def adiciona_visualizacao(conn, id_usuario, id_post, aparelho, browser, ip):
      conn = connect_db()
      with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO visualizacao (id_usuario, id_post, aparelho, browser, ip) VALUES (%s, %s, %s, %s, %s)', (id_usuario, id_post, aparelho, browser, ip))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso adcionar {id_usuario} na tabela visualizacao')

#Lista os valores de uma visulizacao
@app.get("/view/{id_post}")
def lista_visualizacao(conn, id_post):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario FROM visualizacao WHERE id_post=%s', id_post)
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts
#Lista os posts que estao ativos
@app.get("/posts/{id_post}/{ativo}")
def checa_ativo_post(conn, id_post):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('SELECT ativo FROM post WHERE id_post = %s', (id_post))
        res = cursor.fetchone()
        if res:
            return res[0] #Retorna se está 1 ou 0
        else:
            return -1
#Adiciona Joinha nos posts            
@app.post("/posts/{id_post}/{id_usario}/{joinha}")
def adiciona_joinha(conn, id_usuario, id_post, joinha):
    conn = connect_db()
    with conn.cursor() as cursor:
        try: #Checa se o joinha existe, se existe troca o existente
            cursor.execute('SELECT estado FROM joinha WHERE id_usuario=%s AND id_post=%s', (id_usuario, id_post))
            res = cursor.fetchone()
            if res: #Troca o existente
                if(joinha == 1):
                    cursor.execute('UPDATE joinha SET estado = True WHERE id_usuario=%s AND id_post=%s', (id_usuario, id_post))
                if(joinha == 0):
                    cursor.execute('UPDATE joinha SET estado = False WHERE id_usuario=%s AND id_post=%s', (id_usuario, id_post))
            else:
                #Cria um novo joinha
                if(joinha == 1):
                    cursor.execute('INSERT INTO joinha (id_usuario, id_post, estado) VALUES (%s, %s, True)', (id_usuario, id_post))
                if(joinha == 0):
                    cursor.execute('INSERT INTO joinha (id_usuario, id_post, estado) VALUES (%s, %s, False)', (id_usuario, id_post))

        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso adcionar {joinha} na tabela joinha')

#Remove algum joinha
@app.delete("/posts/{id_post}/{id_usario}/{joinha}")
def remove_joinha(conn, id_usuario, id_post):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM joinha WHERE id_usuario=%s AND id_post=%s', (id_usuario, id_post))

#Lista os joinhas em um post
@app.get("/posts/{id_post}/{joinha}")
def lista_joinhas_post(conn, id_post):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario FROM joinha WHERE id_post = %s', (id_post))
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts

#Lista joinhas de um post de um usuario especifico
@app.get("/posts/{id_post}/{id_usuario}/{joinha}")
def lista_joinhas_usuario(conn, id_usuario):
     conn = connect_db()
     with conn.cursor() as cursor:
        cursor.execute('SELECT id_post FROM joinha WHERE id_usuario = %s', (id_usuario))
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts

#Lista joinha unico de um post para cada usuario(estado joinha ou anti-joinha)
@app.get("/posts/{id_post}/{id_usuario}/{joinha}/{estado}")
def lista_joinha_unico(conn, id_usuario, id_post):
     conn = connect_db()
     with conn.cursor() as cursor:
        cursor.execute('SELECT estado FROM joinha WHERE id_usuario=%s AND id_post=%s', (id_usuario, id_post))
        res = cursor.fetchone()
        if res:
            return res[0] #Retorna se está 1 ou 0
        else:
            return -1

#lista as views
@app.get("/view")
def view_aparelho_browser(conn):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM aparelho_browser')
        res = cursor.fetchall()
        return res

#Lista posts
@app.get("/posts/{id_post}/{id_usuario}")
def procedure_consulta_posts(conn, id_usuario):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('CALL consulta_posts(%s)', (id_usuario))
        res = cursor.fetchall()
        ret = tuple(x[0] for x in res)
        return ret

#Lista usuarios mais comentados em sua cidade
@app.get("/nomes/cidades/{id_usuario}") 
def procedure_usuario_popular(conn, num):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('CALL usuario_popular(%s)', (num) )
        res = cursor.fetchall()
        return res
#Lista as referencias de usuarios em posts
@app.get("/referencias/{id_usuario}")
def procedure_lista_referencias(conn, id_usuario):
    with conn.cursor() as cursor:
        cursor.execute('CALL lista_referencias(%s)', (id_usuario) )
        res = cursor.fetchall()
        ret = tuple(x[0] for x in res)
        return ret
                