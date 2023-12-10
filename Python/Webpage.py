from flask import Flask, render_template, redirect, request, flash, jsonify
from flask_mysqldb import MySQL, MySQLdb
import os
from datetime import datetime

import MySQLdb    
app = Flask(__name__)

# Database configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'chessyeti'
app.config['MYSQL_DB'] = 'worldcup'


mysql = MySQL(app)
@app.route('/')
def index():   
    conn = mysql.connect
    if conn:
        cur = conn.cursor()

        # Call the stored procedure
        cur.callproc('GetAllWorldCupData')

        # Fetch the results from each SELECT statement in the procedure
        matches = cur.fetchall()
        cur.nextset()  # Move to the next result set
        players = cur.fetchall()
        cur.nextset()
        referees = cur.fetchall()
        cur.nextset()
        results = cur.fetchall()
        cur.nextset()
        worldcups = cur.fetchall()

        cur.close()

    return render_template('worldcup.html', worldcup=worldcups, matches=matches, players=players, referees=referees, results=results)

@app.route('/statistic')
def statistic():   # Changed function name to 'statistic'
    conn = mysql.connect
    
    # Set the isolation level
    conn.isolation_level = "REPEATABLE READ"
    
    if conn:
        cur = conn.cursor()
        
    cur.execute("SELECT Winner as Country, Count(*) as wins FROM worldcup GROUP BY Winner ORDER BY wins DESC LIMIT 10")
    winnter_counts = cur.fetchall()
    print(winnter_counts)
    cur.close()
    return render_template('dashboard.html', winnter_counts = winnter_counts)

@app.route('/get_country_data/<country_name>')
def get_country_data(country_name):
    conn = mysql.connect
    if conn:
        conn.isolation_level = "REPEATABLE READ"
        cur = conn.cursor()
        # Call the stored procedure
        cur.callproc('GetCountryStats', [country_name])
        
        # Fetch the results
        data = cur.fetchone()

        # Ensure data is in a serializable format
        result = {
            'totalworldWins': data[0],
            'totalMatches': data[1],
            'totalWins': data[2],
            'winRate': data[3]
        }

        cur.close()
        return jsonify(result)


@app.route("/ajax_add",methods=["POST","GET"])
def ajax_add():
    conn = mysql.connect
    conn.isolation_level = "REPEATABLE READ"
    
    if conn:
        cur = conn.cursor()
    print(request.method)
    if request.method == 'POST':
        if request.form['tableName'] == 'matches':
            RoundID= request.form['RoundID']
            MatchID= request.form['MatchID']
            ResultID= request.form['ResultID']
            Year= request.form['Year']
            Datetime= request.form['Datetime']
            Stage= request.form['Stage']
            Stadium= request.form['Stadium']
            City= request.form['City']
            HomeTeamName= request.form['HomeTeamName']
            AwayTeamName= request.form['AwayTeamName']
            Attendance= request.form['Attendance']
            HomeTeamInitials= request.form['HomeTeamInitials']
            AwayTeamInitials= request.form['AwayTeamInitials']
            if not RoundID:
                msg = 'Please input RoundID'
            elif not MatchID:
                msg = 'Please input MatchID'
            elif not ResultID:
                msg = 'Please input ResultID'
            elif not Datetime:
                msg = 'Please input Datetime'
            elif not Stage:
                msg = 'Please input Stage'
            elif not Year:
                msg = 'Please input Year'
            elif not Stadium:
                msg = 'Please input Stadium'
            elif not HomeTeamName:
                msg = 'Please input HomeTeamName'
            elif not HomeTeamInitials:
                msg = 'Please input HomeTeamInitials'
            elif not Attendance:
                msg = 'Please input Attendance'
            elif not AwayTeamName:
                msg = 'Please input AwayTeamName'
            elif not AwayTeamInitials:
                msg = 'Please input AwayTeamInitials'
            else:      
                cur.execute("""
                    INSERT INTO worldcupmatch
                    (RoundID, MatchID, ResultID, _Year, _Datetime, Stage, Stadium, City, HomeTeamName, AwayTeamName, Attendance, HomeTeamInitials, AwayTeamInitials) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, 
                    [RoundID, MatchID, ResultID, Year, Datetime, Stage, Stadium, City, HomeTeamName, AwayTeamName, Attendance, HomeTeamInitials, AwayTeamInitials])

                conn.commit()       
                cur.close()
                msg = 'New record created successfully'   
        else:
            _Year = request.form['_Year']
            Country = request.form['Country']
            Winner = request.form['Winner']
            RunnersUp = request.form['RunnersUp']
            Third = request.form['Third']
            Fourth = request.form['Fourth']
            GoalsScored = request.form['GoalsScored']
            QualifiedTeams = request.form['QualifiedTeams']
            MatchesPlayed = request.form['MatchesPlayed']
            Attendance = request.form['Attendance']

            if not _Year:
                msg = 'Please input Year'
            elif not Country:
                msg = 'Please input Country'
            elif not Winner:
                msg = 'Please input Winner'
            elif not RunnersUp:
                msg = 'Please input RunnersUp'
            elif not Third:
                msg = 'Please input Third'
            elif not Fourth:
                msg = 'Please input Fourth'
            elif not GoalsScored:
                msg = 'Please input GoalsScored'
            elif not QualifiedTeams:
                msg = 'Please input QualifiedTeams'
            elif not MatchesPlayed:
                msg = 'Please input MatchesPlayed'
            elif not Attendance:
                msg = 'Please input Attendance'
            else:      
                print()  
                cur.execute("INSERT INTO WorldCup (_Year, Country, Winner, RunnersUp, Third, Fourth, GoalsScored, QualifiedTeams, MatchesPlayed, Attendance) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", [_Year, Country, Winner, RunnersUp, Third, Fourth, GoalsScored, QualifiedTeams, MatchesPlayed, Attendance])
                conn.commit()       
                cur.close()
                msg = 'New record created successfully'   
    
    return jsonify(msg)

@app.route("/ajax_update",methods=["POST","GET"])
def ajax_update():
    conn = mysql.connect

    conn.isolation_level = "REPEATABLE READ"
    if conn:
        cur = conn.cursor()
    if request.method == 'POST':
        print(request.form)
        if request.form['tableName'] == "matches":
            print(request.form)
            RoundID= request.form['RoundID']
            MatchID= request.form['MatchID']
            ResultID= request.form['ResultID']
            Year= request.form['Year']
            Datetime= request.form['Datetime']
            print(Datetime)
            Datetime = datetime.strptime(Datetime, "%Y-%m-%d").strftime("%Y-%m-%d %H:%M:%S")
            Stage= request.form['Stage']
            Stadium= request.form['Stadium']
            City= request.form['City']
            HomeTeamName= request.form['HomeTeamName']
            AwayTeamName= request.form['AwayTeamName']
            Attendance= request.form['Attendance']
            HomeTeamInitials= request.form['HomeTeamInitials']
            AwayTeamInitials= request.form['AwayTeamInitials']
            cur.execute("""
                UPDATE WorldCupMatch
                SET _Year = %s, _Datetime = %s, Stage = %s, Stadium = %s, City = %s, 
                    HomeTeamName = %s, AwayTeamName = %s, Attendance = %s, 
                    HomeTeamInitials = %s, AwayTeamInitials = %s, ResultID = %s
                WHERE RoundID = %s AND MatchID = %s
                """, 
                [Year, Datetime, Stage, Stadium, City, HomeTeamName, AwayTeamName, Attendance, 
                HomeTeamInitials, AwayTeamInitials, ResultID, RoundID, MatchID])
        else:
            _Year = request.form['_Year']
            Country = request.form['Country']
            Winner = request.form['Winner']
            RunnersUp = request.form['RunnersUp']
            Third = request.form['Third']
            Fourth = request.form['Fourth']
            GoalsScored = request.form['GoalsScored']
            QualifiedTeams = request.form['QualifiedTeams']
            MatchesPlayed = request.form['MatchesPlayed']
            Attendance = request.form['Attendance']
            cur.execute("""
                UPDATE WorldCup 
                SET Country = %s, Winner = %s, RunnersUp = %s, Third = %s, Fourth = %s, 
                    GoalsScored = %s, QualifiedTeams = %s, MatchesPlayed = %s, Attendance = %s
                WHERE _Year = %s
                """, [Country, Winner, RunnersUp, Third, Fourth, GoalsScored, QualifiedTeams, MatchesPlayed, Attendance, _Year])
        
        
        conn.commit()       
        cur.close()
        msg = 'Record successfully Updated'   
    return jsonify(msg)    
 
@app.route("/ajax_delete",methods=["POST","GET"])
def ajax_delete():
    conn = mysql.connect
    
    conn.isolation_level = "REPEATABLE READ"
    if conn:
        cur = conn.cursor()
    if request.method == 'POST':
        print("Delete: ",request.form)
        getid = request.form['string']
        if request.form['tableName'] == "matches":
            cur.execute('DELETE FROM worldcupmatch WHERE matchID = {0}'.format(getid))
        else:
            cur.execute('DELETE FROM worldcup WHERE _Year = {0}'.format(getid))
        conn.commit()       
        cur.close()
        msg = 'Record deleted successfully'   
    return jsonify(msg) 
 
if __name__ == "__main__":
    app.run(debug=True)