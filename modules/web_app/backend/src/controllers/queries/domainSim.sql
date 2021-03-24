/**
@file domainSim.sql
@params: $1: a domain string
@return: every articles that have the domain

Given a domain, return a list of all articles having
that domain (with blocks if necessary).
*/

SELECT * 
FROM topdup_articles A
WHERE A.href LIKE '$1'