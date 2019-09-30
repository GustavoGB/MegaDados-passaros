# MegaDados Rede Social passaros

O projeto é uma pequena rede social que envolve pássaros, em que os usuários podem comentar entre eles e marcar diferentes tipos de pássaros.

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







