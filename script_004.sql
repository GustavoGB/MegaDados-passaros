USE p_megadados;

DROP PROCEDURE IF EXISTS consulta_posts;
DELIMITER //
CREATE PROCEDURE consulta_posts(IN id INT)
    BEGIN
	    SELECT id_post FROM post WHERE id_usuario = id ORDER BY instante DESC;
    END//   
DELIMITER ;

DROP PROCEDURE IF EXISTS usuario_popular;
DELIMITER //
CREATE PROCEDURE usuario_popular(IN num_cidades INT)
    BEGIN      
        SELECT nome, cidade
        FROM usuario
        LEFT OUTER JOIN post USING(id_usuario)
        RIGHT OUTER JOIN tag_usuario USING(id_usuario)
        GROUP BY cidade
        ORDER BY COUNT(*) DESC
        LIMIT num_cidades;
    END//   
DELIMITER ;


DROP PROCEDURE IF EXISTS lista_referencias;
DELIMITER //
CREATE PROCEDURE lista_referencias(IN id INT)
    BEGIN
        SELECT DISTINCT post.id_usuario
        FROM post
        INNER JOIN tag_usuario USING(id_post)
        WHERE tag_usuario.id_usuario = id;
    END//   
DELIMITER ;
