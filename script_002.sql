USE p_megadados;

DROP TRIGGER IF EXISTS delete_posts;

DELIMITER //
CREATE TRIGGER delete_posts
	BEFORE UPDATE ON usuario
	FOR EACH ROW
BEGIN
	IF NEW.ativo = 0 THEN
		UPDATE post
			SET ativo = False
			WHERE id_usuario = NEW.id_usuario;
	END IF;
END//
DELIMITER ;