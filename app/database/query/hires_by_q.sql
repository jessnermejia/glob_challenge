SELECT 
	tdp.department
    , tjo.name_job as job
    , the.name as employee
    , DATE(the.hire_datetime) as date_hire
    , CONCAT('Q',QUARTER(DATE(the.hire_datetime))) as q
FROM 
	glob_challenge.tbl_hired_employee as the
LEFT JOIN glob_challenge.tbl_department as tdp
	ON the.tbl_department_idtbl_department = tdp.idtbl_department
LEFT JOIN glob_challenge.tbl_job as tjo
	ON the.tbl_job_idtbl_job = tjo.idtbl_job
WHERE 
	YEAR(the.hire_datetime) = @year
ORDER BY
	tdp.department
    , tjo.name_job