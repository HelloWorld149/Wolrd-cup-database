USE worldcup;

CREATE TABLE WorldCup (
    _Year INT PRIMARY KEY,
    Country VARCHAR(255),
    Winner VARCHAR(255),
    RunnersUp VARCHAR(255),
    Third VARCHAR(255),
    Fourth VARCHAR(255),
    GoalsScored INT,
    QualifiedTeams INT,
    MatchesPlayed INT,
    Attendance INT
);

CREATE TABLE WorldCupMatch (
    RoundID INT,
    MatchID INT PRIMARY KEY,
    ResultID VARCHAR(20),
    _Year INT,
    _Datetime DATETIME,
    Stage VARCHAR(255),
    Stadium VARCHAR(255),
    City VARCHAR(255),
    HomeTeamName VARCHAR(255),
    AwayTeamName VARCHAR(255),
    Attendance INT,
    HomeTeamInitials VARCHAR(5),
    AwayTeamInitials VARCHAR(5),
    FOREIGN KEY (_Year) REFERENCES WorldCup(_Year)
);

CREATE TABLE WorldCupResult (
    ResultID VARCHAR(20) PRIMARY KEY,
    RoundID INT,
    MatchID INT,
    HomeTeamName VARCHAR(255),
    HomeTeamGoals INT,
    AwayTeamGoals INT,
    AwayTeamName VARCHAR(255),
    WinConditions VARCHAR(255),
    HomeTeamInitials VARCHAR(50),
    AwayTeamInitials VARCHAR(50),
    HalfTimeHomeGoals INT,
    HalfTimeAwayGoals INT,
    FOREIGN KEY (MatchID) REFERENCES WorldCupMatch(MatchID)
);

CREATE TABLE Player (
    PlayerID INT PRIMARY KEY,
    RoundID INT,
    MatchID INT,
    TeamInitials VARCHAR(3),
    CoachName VARCHAR(255),
    LineUp VARCHAR(255),
    ShirtNumber INT,
    PlayerName VARCHAR(255),
    Position VARCHAR(255),
    FOREIGN KEY (MatchID) REFERENCES WorldCupMatch(MatchID)
);

CREATE TABLE WorldCupReferee (
    RoundID INT,
    MatchID INT,
    Referee VARCHAR(255),
    Assistant1 VARCHAR(255),
    Assistant2 VARCHAR(255),
    PRIMARY KEY (MatchID),
    FOREIGN KEY (MatchID) REFERENCES WorldCupMatch(MatchID)
);
