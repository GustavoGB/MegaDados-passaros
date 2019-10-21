from fastapi import FastAPI
import pymysql

app = FastAPI()

def connect_db(host='localhost',user='root',password='vlm1998',database='p_megadados'):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='vlm1998',
        database='p_megadados')
    return conn

#Adiciona Usuario
@app.put("/usuarios")
def adiciona_usuario(nome: str, email: str, cidade: str):
    conn = connect_db()
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO usuario (nome, EMAIL, cidade) VALUES (%s, %s, %s)', (nome, email, cidade))
            cursor.execute('''COMMIT''')
            conn.close()
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {nome} na tabela perigo')
            conn.close()

#Encontra Usuario
@app.get("/usuarios")
def acha_usuario(nome:str):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario FROM usuario WHERE nome = %s', (nome))
        res = cursor.fetchone()
        if res:
            conn.close()
            return res[0]
        else:
            conn.close()
            return None		
#Muda nome do Usuario
@app.put("/usuario")
def muda_nome_usuario(id_usuario, novo_nome):
    conn = connect_db()
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE usuario SET nome=%s where id_usuario=%s', (novo_nome, id_usuario))
            cursor.execute('''COMMIT''')
            conn.close()
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso alterar nome do id {id} para {novo_nome} na tabela usuario')
            conn.close()
#Remove usuario
@app.delete("/usuario")
def remove_usuario(id_usuario):
    conn = connect_db()    
    with conn.cursor() as cursor:
        try:
        	cursor.execute('UPDATE usuario SET ativo = False WHERE id_usuario=%s', (id_usuario))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso remover usuario de id {id} na tabela usuario')
        conn.commit()
        conn.close()

#Adiciona Passaros
@app.post("/passaros")
def adiciona_passaro(especie):
    conn = connect_db()
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO passaro (especie) VALUES (%s)', (especie))
            conn.commit()
            conn.close()
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {especie} na tabela comida')
            conn.close()

#Encontra um passaro especifico
@app.get("/passaros")
def acha_passaro(especie):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_passaro FROM passaro WHERE especie = %s', (especie))
        res = cursor.fetchone()
        if res:
            conn.close()
            return res[0]
        else:
            conn.close()
            return None
#Deleta passaros            
@app.delete("/passaros")
def remove_passaro(id_passaro):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM passaro WHERE id_passaro=%s', (id_passaro))
        conn.commit()
        conn.close()

#Lista todos os passaros
@app.get("/passaros")
def lista_passaros():
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_passaro from passaro')
        res = cursor.fetchall()
        passaros = tuple(x[0] for x in res)
        conn.close()
        return passaros

#Adiciona preferencia de um passaro para um usuario
@app.post("/preferencias")
def adiciona_preferencia_a_usuario(id_usuario, id_passaro):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO usuario_passaro VALUES (%s, %s)', (id_usuario, id_passaro))
        conn.commit()
        conn.close()
#Remove preferencia de um passaro para um usuario
@app.delete("/preferencias")
def remove_preferencia_de_usuario(id_usuario, id_passaro):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM usuario_passaro WHERE id_usuario=%s AND id_passaro=%s',(id_usuario, id_passaro))
        conn.commit()
        conn.close()
#Lista todas as preferencias de um usuario
@app.get("/preferencias")
def lista_prefenrecias_de_usuario(id_usuario):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_passaro FROM usuario_passaro WHERE id_usuario=%s', (id_usuario))
        res = cursor.fetchall()
        preferencias = tuple(x[0] for x in res)
        conn.close()
        return preferencias

#Lista todas as preferencias(id_usuarios) de um certo passaro 
@app.get("/preferencias")
def lista_preferencias_de_passaro(id_passaro):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario FROM usuario_passaro WHERE id_passaro=%s', (id_passaro))
        res = cursor.fetchall()
        usuarios = tuple(x[0] for x in res)
        conn.close()
        return usuarios

#Adiciona post na rede social
@app.post("/posts")
def adiciona_post(titulo, id_usuario, texto, url):
    conn = connect_db()
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO post (titulo, id_usuario, texto, url) VALUES (%s, %s, %s, %s)', (titulo, id_usuario, texto, url))
            conn.commit()
            conn.close()
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso adcionar {titulo} na tabela post')
            conn.close()
#Remove post da rede social
@app.delete("/posts")
def remove_post(id_post):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('UPDATE post SET ativo = False WHERE id_post = %s', (id_post))
        conn.commit()
        conn.close()
#Lista posts de usuario
@app.get("/posts")
def lista_posts_usuario(id_usuario):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_post FROM post WHERE id_usuario=%s', (id_usuario))
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        conn.close()
        return posts

#Lista todos os posts
@app.get("/posts")
def lista_posts():
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_post FROM post')
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        conn.close()
        return posts

#Encontra post baseado no titulo e no usuario
@app.get("/posts")
def acha_post(id_usuario, titulo):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_post FROM post WHERE id_usuario=%s AND titulo=%s', (id_usuario, titulo))
        res = cursor.fetchone()
        if res:
            conn.close()
            return res[0] 
        else:
            conn.close()
            return None
        
#Adiciona tag usuario e tag passaros
@app.post("/tags")
def adiciona_tags(id_post):
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
        conn.commit()
        conn.close()
#Lista tags do usuarios baseado em marcacoes de post
@app.get("/tags_usuario")
def lista_tags_usuario(id_usuario):
    conn = connect_db() 
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_post FROM tag_usuario WHERE id_usuario=%s', id_usuario)
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        conn.close()
        return posts

#Lista tags de passaros basedo em marcacoes de post
@app.get("/tags_passaro")
def lista_tags_passaro(id_passaro):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_post FROM tag_passaro WHERE id_passaro=%s', id_passaro)
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        conn.close()
        return posts

#Adiciona uma view
@app.post("/view") 
def adiciona_visualizacao(id_usuario, id_post, aparelho, browser, ip):
      conn = connect_db()
      with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO visualizacao (id_usuario, id_post, aparelho, browser, ip) VALUES (%s, %s, %s, %s, %s)', (id_usuario, id_post, aparelho, browser, ip))
            conn.commit()
            conn.close()
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso adcionar {id_usuario} na tabela visualizacao')
            conn.close()

#Lista os valores de uma visulizacao
@app.get("/view")
def lista_visualizacao(id_post):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario FROM visualizacao WHERE id_post=%s', id_post)
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        conn.close()
        return posts
#Lista os posts que estao ativos
@app.get("/posts")
def checa_ativo_post(id_post):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('SELECT ativo FROM post WHERE id_post = %s', (id_post))
        res = cursor.fetchone()
        if res:
            conn.close()
            return res[0] #Retorna se está 1 ou 0
        else:
            conn.close()
            return -1
#Adiciona Joinha nos posts            
@app.post("/posts")
def adiciona_joinha(id_usuario, id_post, joinha):
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
                conn.commit()
                conn.close()
            else:
                #Cria um novo joinha
                if(joinha == 1):
                    cursor.execute('INSERT INTO joinha (id_usuario, id_post, estado) VALUES (%s, %s, True)', (id_usuario, id_post))
                if(joinha == 0):
                    cursor.execute('INSERT INTO joinha (id_usuario, id_post, estado) VALUES (%s, %s, False)', (id_usuario, id_post))
                conn.commit()
                conn.close()
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso adcionar {joinha} na tabela joinha')
            conn.close()

#Remove algum joinha
@app.delete("/posts")
def remove_joinha(id_usuario, id_post):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM joinha WHERE id_usuario=%s AND id_post=%s', (id_usuario, id_post))
        conn.commit()
        conn.close()
#Lista os joinhas em um post
@app.get("/posts")
def lista_joinhas_post(conn, id_post):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario FROM joinha WHERE id_post = %s', (id_post))
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        conn.close()
        return posts

#Lista joinhas de um post de um usuario especifico
@app.get("/posts")
def lista_joinhas_usuario(id_usuario):
     conn = connect_db()
     with conn.cursor() as cursor:
        cursor.execute('SELECT id_post FROM joinha WHERE id_usuario = %s', (id_usuario))
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        conn.close()
        return posts

#Lista joinha unico de um post para cada usuario(estado joinha ou anti-joinha)
@app.get("/posts")
def lista_joinha_unico(id_usuario, id_post):
     conn = connect_db()
     with conn.cursor() as cursor:
        cursor.execute('SELECT estado FROM joinha WHERE id_usuario=%s AND id_post=%s', (id_usuario, id_post))
        res = cursor.fetchone()
        if res:
            conn.close()
            return res[0] #Retorna se está 1 ou 0
        else:
            conn.close()
            return -1

#lista as views
@app.get("/view")
def view_aparelho_browser():
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM aparelho_browser')
        res = cursor.fetchall()
        conn.close()
        return res

#Lista posts
@app.get("/posts")
def procedure_consulta_posts(id_usuario):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('CALL consulta_posts(%s)', (id_usuario))
        res = cursor.fetchall()
        ret = tuple(x[0] for x in res)
        conn.commit()
        conn.close()
        return ret

#Lista usuarios mais comentados em sua cidade
@app.get("/nomes/cidades") 
def procedure_usuario_popular(num):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('CALL usuario_popular(%s)', (num) )
        res = cursor.fetchall()
        conn.commit()
        conn.close()
        return res
#Lista as referencias de usuarios em posts
@app.get("/referencias")
def procedure_lista_referencias(id_usuario):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute('CALL lista_referencias(%s)', (id_usuario) )
        res = cursor.fetchall()
        ret = tuple(x[0] for x in res)
        conn.commit()
        conn.close()
        return ret
                