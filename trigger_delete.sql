USE p_megadados;
DROP TRIGGER IF EXISTS delete_posts;

DELIMITER //
CREATE TRIGGER delete_posts AFTER UPDATE ON usuario FOR EACH ROW
BEGIN
		UPDATE post 
			INNER JOIN Inserted I USING(id_usuario)
        SET ativo = 0
		WHERE id_usuario = I.ID AND I.ativo = 0;
END// 

DELIMITER ;
