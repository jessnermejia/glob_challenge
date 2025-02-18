WITH HIRES AS (
SELECT 
	tdp.idtbl_department as id
	, tdp.department
	, COUNT(tdp.department) as hired
FROM glob_challenge.tbl_hired_employee the
LEFT JOIN glob_challenge.tbl_department tdp
ON the.tbl_department_idtbl_department = tdp.idtbl_department
WHERE
	YEAR(hire_datetime)=@year
GROUP BY 1,2
ORDER BY 3 DESC
)
SELECT *
FROM HIRES
HAVING hired > (SELECT AVG(hired) FROM HIRES)