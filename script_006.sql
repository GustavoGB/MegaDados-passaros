DROP VIEW IF EXISTS aparelho_browser;
CREATE VIEW aparelho_browser AS 
	SELECT COUNT(*), aparelho, browser
    FROM visualizacao
    GROUP BY aparelho, browser;

DROP VIEW IF EXISTS url_passaros;
CREATE VIEW url_passaros AS
    SELECT url, passaro.especie
    FROM passaro_url
    INNER JOIN tag_passaro USING(id_passaro)
    INNER JOIN passaro USING(id_passaro)
    GROUP BY passaro.especie
    ORDER BY COUNT(*) DESC;
    