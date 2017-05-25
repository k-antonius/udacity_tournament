***************************
Udacity Tournament Project
***************************

Overview: A library of python functions implementing the back-end of
a swiss-style tournament system using PostgreSQL.

A swiss-style tournament system is one in which each player plays in each
round and is paired against a player with a similar win/loss record.  The
advantage of the swiss-style tournament is that a definitive winner is found
and a better player will not be knocked out of a tournament by a single loss
to a less successful player, as in a single-elimination tournament.

Limitations: This library assumes that the number of players is even and
that matches do not produce ties.

Dependencies: Python 2.7, PostgreSQL, psycopg2 python module.

To run:
(1) Clone this repository or download the source files.
(2) Install the dependencies as necessary.
(3) Open your terminal or command line program and
    navigate to the directory where the repository/files are located. All the
    next steps require that the directory not be changed.
(4) Launch PostgresSQL from the terminal using "psql" command.
(5) In the psql command line prompt, type "\i tournament.sql", which will
    run the SQL commands in that file, creating the appropriate schema for
    the tournament program.
(6) Quit the psql command line with "\q"
(7) Test everything is working. Run the test suite in the command line by
    typing "python tournament_test.py"
*************************
