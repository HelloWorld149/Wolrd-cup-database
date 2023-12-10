DELIMITER //

DROP PROCEDURE IF EXISTS GetAllWorldCupData;

CREATE PROCEDURE GetAllWorldCupData()
BEGIN
    SELECT * FROM WorldCupMatch;
    SELECT * FROM Player;
    SELECT * FROM WorldCupReferee;
    SELECT * FROM WorldCupResult;
    SELECT * FROM worldcup;
END //

DELIMITER ;
