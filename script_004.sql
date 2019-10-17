USE p_megadados;

DROP PROCEDURE IF EXISTS consulta_posts;
DELIMITER //
CREATE PROCEDURE consulta_posts(IN id INT)
    BEGIN
	    SELECT id_post FROM post WHERE id_usuario = id ORDER BY instante DESC;
    END//   
DELIMITER ;

DROP VIEW IF EXISTS usuario_popular;
CREATE VIEW usuario_popular AS 
	SELECT id_usuario, COUNT(*) as cnt
    FROM tag_usuario
    GROUP BY id_usuario
    ORDER BY cnt
    LIMIT 1;

DROP FUNCTION IF EXISTS lista_referencias;
DELIMITER //
CREATE FUNCTION lista_referencias(id INT) RETURNS INT READS SQL DATA
BEGIN
	DECLARE usuario INT;
	SELECT id_usuario 
        INTO usuario 
    FROM post
    INNER JOIN tag_usuario USING(id_post)
    GROUP BY id_usuario;
    RETURN usuario;
END//
DELIMITER ;