USE p_megadados;

DROP VIEW IF EXISTS aparelho_browser;
CREATE VIEW aparelho_browser AS 
	SELECT aparelho, browser
    FROM visualizacao
    GROUP BY aparelho, browser;