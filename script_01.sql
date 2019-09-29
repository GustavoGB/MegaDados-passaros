DROP DATABASE IF EXISTS p_megadados;
CREATE DATABASE p_megadados;
USE p_megadados;

CREATE TABLE usuario (
	id_usuario INT NOT NULL auto_increment,
    nome VARCHAR(80),
    EMAIL VARCHAR(80),
    cidade VARCHAR(80),
    ativo BOOLEAN DEFAULT TRUE,
    PRIMARY KEY(id_usuario)
);

CREATE TABLE passaro (
	id_passaro INT NOT NULL auto_increment,
    especie VARCHAR(80),
    especie VARCHAR(80) UNIQUE,
    PRIMARY KEY (id_passaro)
);

CREATE TABLE usuario_passaro (
	id_usuario INT NOT NULL,
    id_passaro INT NOT NULL,
    FOREIGN KEY (id_usuario)
		REFERENCES usuario (id_usuario),
	FOREIGN KEY (id_passaro)
		REFERENCES passaro (id_passaro),
	PRIMARY KEY (id_usuario, id_passaro)
);

CREATE TABLE post (
	id_post INT NOT NULL auto_increment,
    id_usuario INT NOT NULL,
    titulo VARCHAR(80) NOT NULL,
    texto VARCHAR(300),
    url VARCHAR(200),
    ativo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_usuario)
		REFERENCES usuario (id_usuario),
    PRIMARY KEY (id_post, id_usuario)
);

CREATE TABLE visualizacao (
	id_usuario INT NOT NULL,
    id_post INT NOT NULL,
    aparelho VARCHAR(80),
    browser VARCHAR(80),
    ip VARCHAR(80),
    instante TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario)
		REFERENCES usuario (id_usuario),
	FOREIGN KEY (id_post)
		REFERENCES post (id_post),
	PRIMARY KEY (id_usuario, id_post)
);

CREATE TABLE tag_passaro (
	id_post INT NOT NULL,
    id_passaro INT NOT NULL,
    FOREIGN KEY (id_post)
		REFERENCES post (id_post),
	FOREIGN KEY (id_passaro)
		REFERENCES passaro (id_passaro),
	PRIMARY KEY (id_post, id_passaro)
);

CREATE TABLE tag_usuario (
	id_post INT NOT NULL,
    id_usuario INT NOT NULL,
    FOREIGN KEY (id_post)
		REFERENCES post (id_post),
	FOREIGN KEY (id_usuario)
		REFERENCES usuario (id_usuario),
	PRIMARY KEY (id_post, id_usuario)
);



