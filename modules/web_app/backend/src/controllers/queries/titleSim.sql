/**
@file titleSim.sql
@params: $1: a title string
@return: every articles that have the title

Given an article title, return a list of articles having
that title (with blocks if necessary).
*/

SELECT * 
FROM topdup_articles A
WHERE A.topic LIKE '$1'