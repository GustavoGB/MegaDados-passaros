USE p_megadados;

CREATE TABLE joinha (
	id_usuario INT NOT NULL,
    id_post INT NOT NULL,
    estado BOOLEAN,
    FOREIGN KEY (id_usuario)
        REFERENCES usuario (id_usuario),
	FOREIGN KEY (id_post)
		REFERENCES post (id_post),
    PRIMARY KEY (id_usuario, id_post)
);
