# MegaDados Rede Social passaros

O projeto é uma pequena rede social que envolve pássaros, em que os usuários podem comentar entre eles e marcar diferentes tipos de pássaros.

# Dicionário de Dados 
Para explicar o nosso modelo foi necessário criar entidades(tabelas) para conseguir ter controle dos testes a serem feitos passados no enunciado, resultando em 7 entidades. Contando com o fato de que uma das entidades é uma view. 

## Pássaro
| passaro | tipo |
| --- | --- |
| id_passaro | INT(11) |
| especie | VARCHAR(80) |

A entidade pássaros será responsável por guardar o id dos mesmos e qual é o tipo da espécie. 


## Usuário_pássaro
| usuario_passaro | tipo |
| --- | --- |
| id_usuario | INT(11) |
| id_passaro | INT(11) |

A entidade usuario_passaro é uma tabela relacional entre a entidade Pássaros e a entidade Usuário. 

## Usuário
| usuario | tipo |
| --- | --- |
| id_usuario | INT(11) |
| nome | VARCHAR(80) |
| EMAIL| VARCHAR(80)|
| cidade| VARCHAR(80)|
| ativo | TINYINT(1)|

A entidade usuário é responsável por guardar informações importantes do usuário, além de saber se o usuário está ativo na rede ou não.

## Visualização


# Schema

A partir do enunciado e da ideia de modelos relacionais, foi possível montar as tabelas no MySql workbench que se relacionam para ajudar na nossa modelagem.

![Diagrama](diagramaPassaros.png)


# Testes

Para verificar se os scripts SQL estão corretos, utilizaremos o unittest e o subprocess. O primeiro irá facilitar na criação de testes, enquanto o subprocess será responsável por nos ajudar a automatizar nossa aplicação. 

Isso pois é possível utilizar o o subprocess para criar uma conexão do mysql utilizando um script.py como segue o exemplo:

```python
import subprocess
import unittest

class TestCase(unittest.TestCase):
    def test_meu_teste(self):
        pass
    @classmethod
    def setUpClass(TestCase):
        with open ('script.sql', 'rb') as f:
            res = subprocess.run('mysql -u root -proot'.split(),stdin =f)
            print(res)        

if __name__ = '__main__':
    unittest.main()

```







