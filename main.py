from fastapi import FastAPI
from pydantic import BaseModel 
import pymysql

app = FastAPI()

#Adiciona Usuario
@app.post("/usuarios/{id_usuario}")
def adiciona_usuario(conn, nome, email, cidade):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO usuario (nome, EMAIL, cidade) VALUES (%s, %s, %s)', (nome, email, cidade))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {nome} na tabela perigo')

#Encontra Usuario
@app.get("/usuarios/{id_usuario}")
def acha_usuario(conn, nome):
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
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE usuario SET nome=%s where id_usuario=%s', (novo_nome, id_usuario))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso alterar nome do id {id} para {novo_nome} na tabela usuario')
#Remove usuario
@app.delete("/usuario/{id_usuario}")
def remove_usuario(conn, id_usuario):
    with conn.cursor() as cursor:
        try:
        	cursor.execute('UPDATE usuario SET ativo = False WHERE id_usuario=%s', (id_usuario))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso remover usuario de id {id} na tabela usuario')
#Lista usuarios
@app.get("/usuario/{id_usuario}")
def lista_usuarios(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario from usuario')
        res = cursor.fetchall()
        usuarios = tuple(x[0] for x in res)
        return usuarios

#Checa se usuario existe        
@app.get("/usuario/{id_usuario}")
def checa_ativo(conn, id_usuario):
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
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO passaro (especie) VALUES (%s)', (especie))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {especie} na tabela comida')
#Encontra um passaro especifico
@app.get("/passaros/{id_passaro}")
def acha_passaro(conn, especie):
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
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM passaro WHERE id_passaro=%s', (id_passaro))

#Lista todos os passaros
@app.get("/passaros/{id_passaro}")
def lista_passaros(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_passaro from passaro')
        res = cursor.fetchall()
        passaros = tuple(x[0] for x in res)
        return passaros




