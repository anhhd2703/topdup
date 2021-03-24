/**
@file articleQueryDate.sql
@params: 
    $1: the title of the article needed to find.
    $2: the domain of the article needed to find.
    $3: start date string: In the form of `yyyy-mm-dd`. Eg: 2013-12-23
    $4: end date string: In the form of `yyyy-mm-dd`. Eg: 2022-12-23
@return: the found articles

Given parameters, return a list of query articles.
*/
SELECT * 
FROM topdup_articles A
WHERE LOWER(A.topic) LIKE LOWER('%$1%')
    AND LOWER(A.href) LIKE LOWER('%$2%')
    AND created_date::date >= '$3'
    AND created_date::date < '$4'