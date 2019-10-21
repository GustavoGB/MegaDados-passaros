USE p_megadados;

CREATE TABLE passaro_url (
    id_passaro INT NOT NULL,
    url VARCHAR(200),
	CONSTRAINT fk3_passaro FOREIGN KEY (id_passaro)
		REFERENCES tag_passaro (id_passaro)
    ON DELETE CASCADE,
    PRIMARY KEY (id_passaro, url)
);
