import pymysql
 

def adiciona_usuario(conn, nome, email, cidade):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO usuario (nome, EMAIL, cidade) VALUES (%s, %s, %s)', (nome, email, cidade))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {nome} na tabela perigo')

def acha_usuario(conn, nome):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario FROM usuario WHERE nome = %s', (nome))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def muda_nome_usuario(conn, id_usuario, novo_nome):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE usuario SET nome=%s where id_usuario=%s', (novo_nome, id_usuario))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso alterar nome do id {id} para {novo_nome} na tabela usuario')

def remove_usuario(conn, id_usuario):
    with conn.cursor() as cursor:
        try:
        	cursor.execute('UPDATE usuario SET ativo = False WHERE id_usuario=%s', (id_usuario))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso remover usuario de id {id} na tabela usuario')

def lista_usuarios(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario from usuario')
        res = cursor.fetchall()
        usuarios = tuple(x[0] for x in res)
        return usuarios

def checa_ativo(conn, id_usuario):
    with conn.cursor() as cursor:
        cursor.execute('SELECT ativo FROM usuario WHERE id_usuario = %s', (id_usuario))
        res = cursor.fetchone()
        if res:
            return res[0] #Retorna se está 1 ou 0
        else:
            return -1

def adiciona_passaro(conn, especie):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO passaro (especie) VALUES (%s)', (especie))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {especie} na tabela comida')

def acha_passaro(conn, especie):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_passaro FROM passaro WHERE especie = %s', (especie))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def remove_passaro(conn, id_passaro):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM passaro WHERE id_passaro=%s', (id_passaro))

def lista_passaros(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_passaro from passaro')
        res = cursor.fetchall()
        passaros = tuple(x[0] for x in res)
        return passaros

def adiciona_preferencia_a_usuario(conn, id_usuario, id_passaro):
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO usuario_passaro VALUES (%s, %s)', (id_usuario, id_passaro))

def remove_preferencia_de_usuario(conn, id_usuario, id_passaro):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM usuario_passaro WHERE id_usuario=%s AND id_passaro=%s',(id_usuario, id_passaro))

def lista_prefenrecias_de_usuario(conn, id_usuario):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_passaro FROM usuario_passaro WHERE id_usuario=%s', (id_usuario))
        res = cursor.fetchall()
        preferencias = tuple(x[0] for x in res)
        return preferencias

def lista_preferencias_de_passaro(conn, id_passaro):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario FROM usuario_passaro WHERE id_passaro=%s', (id_passaro))
        res = cursor.fetchall()
        usuarios = tuple(x[0] for x in res)
        return usuarios

def adiciona_post(conn, titulo, id_usuario, texto, url):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO post (titulo, id_usuario, texto, url) VALUES (%s, %s, %s, %s)', (titulo, id_usuario, texto, url))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso adcionar {titulo} na tabela post')

def remove_post(conn, id_post):
    with conn.cursor() as cursor:
        cursor.execute('UPDATE post SET ativo = False WHERE id_post = %s', (id_post))

def lista_posts_usuario(conn, id_usuario):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_post FROM post WHERE id_usuario=%s', (id_usuario))
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts

def lista_posts(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_post FROM post')
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts

def acha_post(conn, id_usuario, titulo):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_post FROM post WHERE id_usuario=%s AND titulo=%s', (id_usuario, titulo))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def adiciona_tags(conn, id_post):
    #Por enquanto só funciona quando as marcações tiverem espaço em seguida da marcação
    with conn.cursor() as cursor:
        ##Nao considerei que eh possivel add as tags no titulo, so add select texto AND titulo
        cursor.execute('SELECT texto FROM post WHERE id_post=%s', id_post)
        res = cursor.fetchone()
        ##Parsear o res, se tiver @ add ao tag_usuario, se tiver # add ao tag_passaro.
        try:
            texto = str(res[0])
            i = texto.find("@")
            if (i != -1):
                fim = texto.find(" ",i)#Acha o fim da tag
                tag_usuario = texto[i:fim]
            else:
                tag_usuario = None

            i = texto.find("#")
            if i != -1:
                fim = texto.find(" ",i)#Acha o fim da tag
                tag_passaro = texto[i:fim]
            else: 
                tag_passaro = None
        except Exception as e:
            return -1   
        
        if "@" in tag_usuario:
            usuario = tag_usuario[1:] #excluindo o @
            id_usuario = acha_usuario(conn, usuario)
        else:
            id_usuario = None
        if tag_passaro is not None:
            passaro = tag_passaro[1:] #excluindo o @
            id_passaro = acha_passaro(conn, passaro)
        else: 
            id_passaro = None

        if (id_usuario != None):
            try:
                cursor.execute('INSERT INTO tag_usuario (id_post, id_usuario) VALUES (%s, %s)', (id_post, id_usuario))
            except pymysql.err.IntegrityError as e:
                raise ValueError(f'Não posso adcionar {id_usuario} na tabela tag_usuario')

        if (id_passaro != None):
            try:
                cursor.execute('INSERT INTO tag_passaro (id_post, id_passaro) VALUES (%s, %s)', (id_post, id_passaro))
            except pymysql.err.IntegrityError as e:
                raise ValueError(f'Não posso adcionar {id_passaro} na tabela tag_passaro')

def lista_tags_usuario(conn, id_usuario): #lista todos os posts em que um usuario foi marcado
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_post FROM tag_usuario WHERE id_usuario=%s', id_usuario)
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts


def lista_tags_passaro(conn, id_passaro): #lista todos os posts em que um passaro foi marcado
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_post FROM tag_passaro WHERE id_passaro=%s', id_passaro)
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts
def adiciona_visualizacao(conn, id_usuario, id_post, aparelho, browser, ip):
  with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO visualizacao (id_usuario, id_post, aparelho, browser, ip) VALUES (%s, %s, %s, %s, %s)', (id_usuario, id_post, aparelho, browser, ip))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso adcionar {id_usuario} na tabela visualizacao')

def lista_visualizacao(conn, id_post):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario FROM visualizacao WHERE id_post=%s', id_post)
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts

def checa_ativo_post(conn, id_post):
    with conn.cursor() as cursor:
        cursor.execute('SELECT ativo FROM post WHERE id_post = %s', (id_post))
        res = cursor.fetchone()
        if res:
            return res[0] #Retorna se está 1 ou 0
        else:
            return -1
