USE p_megadados;

CREATE TABLE passaro_url (
    id_passaro INT NOT NULL,
    url VARCHAR(200),
	FOREIGN KEY (id_passaro)
		REFERENCES passaro (id_passaro),
    PRIMARY KEY (id_passaro, url)
);
