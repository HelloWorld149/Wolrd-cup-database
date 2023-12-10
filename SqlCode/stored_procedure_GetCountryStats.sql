DELIMITER //

DROP PROCEDURE IF EXISTS GetCountryStats;

CREATE PROCEDURE GetCountryStats(IN countryInput VARCHAR(255))
BEGIN
    DECLARE totalworldWins INT DEFAULT 0;
    DECLARE totalMatches INT;
    DECLARE totalWins INT;
    DECLARE winRate DECIMAL(5,2);
	
    -- Calculate total world cup wins
    SELECT COUNT(*) INTO totalworldWins
    FROM worldcup
    WHERE Winner = countryInput;
    
    -- Calculate total matches
    SELECT COUNT(DISTINCT MatchID) INTO totalMatches
    FROM worldcupmatch 
    WHERE HomeTeamName = countryInput OR AwayTeamName = countryInput;

    -- Calculate total wins
    SELECT 
        (SELECT COUNT(DISTINCT m.MatchID) 
         FROM worldcupmatch m 
         JOIN Worldcupresult r ON m.MatchID = r.MatchID
         WHERE m.HomeTeamName = countryInput AND r.HomeTeamGoals > r.AwayTeamGoals) 
        +
        (SELECT COUNT(DISTINCT m.MatchID)
         FROM worldcupmatch m 
         JOIN Worldcupresult r ON m.MatchID = r.MatchID
         WHERE m.AwayTeamName = countryInput AND r.AwayTeamGoals > r.HomeTeamGoals) 
    INTO totalWins;

    -- Calculate win rate
    IF totalMatches > 0 THEN
        SET winRate = (totalWins / totalMatches) * 100;
    ELSE
        SET winRate = 0;
    END IF;

    -- Return results
    SELECT totalworldWins, totalMatches, totalWins, winRate;
END //

DELIMITER ;



