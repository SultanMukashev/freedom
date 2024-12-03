# PostgreSQL practice
## In this practice you will work with HR database
### To start:

1.Install postgresql
refer: http://w3resource.com/PostgreSQL/install-postgresql-on-linux-and-windows.php

2.In postgresql prompt
```sql
create database "dbname"
```
3.
```sql
\q
```
4.
```sh
psql -h ip -U postgres dbname < pgex_backup.pgsql
```
sqlex_backup.pgsql must be with proper path. For local machine ip is 127.0.0.1

5.
```
psql -h ip -U postgres dbname
```
6.
```sql
CREATE ROLE username WITH LOGIN ENCRYPTED PASSWORD 'password';
```
7.
```sql
GRANT CONNECT ON DATABASE dbname TO username;
```
8.
```sql
GRANT SELECT ON ALL TABLES IN SCHEMA public TO username;
```
9.
```
\q
```
10.
```
psql -h ip -U postgres dbname
```
supply password for username

### Observe HR Database, create table statements and draw Diagram of this database.

### Start executing SQL commands now

### Exercises
1. Write a query to display the names of employees with column aliases as “First Name" for `first_name` and "Last Name" for `last_name`.
```sql
SELECT first_name "First Name", last_name "Last Name" 
FROM employees;
```
2. Create a query that displays each employee's first and last name, salary, and calculates 15% of their salary, naming this amount "PF".
```sql
SELECT first_name, last_name, salary, salary*.15 PF 
FROM employees;
```
3. Write a query to find the average salary and the total number of employees.
```sql
SELECT AVG(salary), COUNT(*) 
FROM employees;
```
4. Create a query to find both the highest and lowest salaries paid to employees.
```sql
SELECT MAX(salary), MIN(salary) 
FROM employees;
```
5. Write a query to get the second-highest and second-lowest salaries in the company.
```sql
SELECT 
    MAX(salary) AS second_highest_salary
FROM 
    employees
WHERE 
    salary < (SELECT MAX(salary) FROM employees);
```
```sql
SELECT 
    MIN(salary) AS second_lowest_salary
FROM 
    employees
WHERE 
    salary > (SELECT MIN(salary) FROM employees);
```
6. List all employees' first names, converting each name to uppercase.
```sql
SELECT UPPER(first_name) 
FROM employees;
```
7. Write a query to get each employee's first name with all leading and trailing spaces removed.
```sql
SELECT TRIM(first_name) 
FROM employees;
```
8. Display each employee's first name, last name, and the combined length of both names.
```sql
SELECT first_name, last_name, 
LENGTH(first_name) + LENGTH(last_name) AS "Length of Names" 
FROM employees;
```
9. Write a query to identify if any employee's first name contains numeric characters.
```sql
SELECT * 
FROM employees 
WHERE first_name 
SIMILAR TO '%0|1|2|3|4|5|6|7|8|9%';
```
10. Find the number of distinct job positions in the employee data.
```sql
SELECT COUNT(DISTINCT job_id) 
FROM employees;
```
11. Write a query to get the maximum, minimum, total, and average salaries of all employees.
```sql
SELECT 
    MAX(salary) AS max_salary,
    MIN(salary) AS min_salary,
    SUM(salary) AS total_salary,
    AVG(salary) AS average_salary
FROM 
    employees;

```
12. Display the number of employees holding each job position.
```sql
SELECT job_id, COUNT(*) 
FROM employees
GROUP BY job_id;
```
13. Write a query to get the manager ID along with the lowest salary of employees reporting to that manager.
```sql
SELECT manager_id, MIN(salary)
FROM employees
WHERE manager_id IS NOT NULL 
GROUP BY manager_id 
ORDER BY MIN(salary) DESC;
```
14. List the address details (location_id, street_address, city, state_province, country_name) for all departments.
```sql
SELECT location_id, 
       street_address, 
       state_province, 
       country_name, 
       department_name 
FROM locations 
NATURAL JOIN countries 
NATURAL JOIN departments;
```
15. Join the `employees` and `departments` tables to display each employee's first and last name, department ID, and department name.
```sql
SELECT first_name, 
       last_name, 
       department_id,
       department_name
FROM employees 
JOIN departments USING (department_id);
```
16. Write a query to join the `employees`, `departments`, and `locations` tables to find the first name, last name, job title, department name, and department ID for employees based in London.
```sql
SELECT e.first_name, 
       e.last_name, 
       e.job_id, 
       e.department_id, 
       d.department_name
FROM employees e 
JOIN departments d 
ON (e.department_id = d.department_id) 
JOIN locations l ON
(d.location_id = l.location_id)
WHERE l.city = 'London';
```
17. Use a self-join on the `employees` table to display each employee's ID, last name as "Employee", along with their manager’s ID and last name as "Manager".
```sql
SELECT W1.employee_id as "Emp_id", 
       W1.last_name AS "Employee", 
       W2.employee_id AS "Manager ID",
       W2.last_name AS "Manager"
FROM employees W1 
JOIN employees W2 
ON W1.manager_id = W2.employee_id;
```
18. Join tables to find the employee ID, job title, and days worked by employees who were in the department with ID 90.
```sql
SELECT employee_id, 
       job_title, 
       end_date - start_date Days 
FROM job_history 
NATURAL JOIN jobs
WHERE department_id = 90;
```
19. Use a join to display the department name, manager's name, and the city of each department.
```sql
SELECT w1.department_name,
       w2.first_name, 
       w3.city 
FROM departments w1 
JOIN employees w2 
ON (w1.manager_id = w2.employee_id) 
JOIN locations w3 USING (location_id);
```
20. Join the `job_history` and `employees` tables to show the status of employees currently earning more than a salary of 10,000.
```sql
SELECT jh.* 
FROM job_history jh 
JOIN employees em 
ON (jh.employee_id = em.employee_id) 
WHERE em.salary > 10000;
```
21. Write a query to find the first and last names and salaries of employees who earn more than the salary of the employee with the last name "Bull".
```sql
SELECT first_name, 
       last_name, 
       salary 
FROM employees 
WHERE salary > 
      (SELECT salary 
       FROM employees 
       WHERE last_name = 'Bull');
```
22. Use a subquery to find the first and last names of employees working in the IT department.
```sql
SELECT first_name, 
       last_name 
FROM employees 
WHERE department_id 
      IN (SELECT department_id 
          FROM departments 
          WHERE department_name = 'IT');
```
23. Use a subquery to list the first and last names of employees who report to a manager working in a department based in the United States.
```sql
SELECT first_name, 
       last_name 
FROM employees 
WHERE manager_id IN (
        SELECT employee_id 
        FROM employees 
        WHERE department_id IN (
                SELECT department_id 
                FROM departments 
                WHERE location_id IN ( 
                        SELECT location_id 
                        FROM locations 
                        WHERE country_id = 'US' 
                    )
            )
    );
```
24. Write a subquery to find the first and last names of employees who hold a managerial position.
```sql

SELECT first_name, 
       last_name 
FROM employees 
WHERE (employee_id
        IN (SELECT manager_id
            FROM employees)
      );

```
25. Use a subquery to retrieve the first name, last name, and salary of each employee whose salary matches the minimum salary for their job position.
```sql
SELECT first_name,
       last_name, 
       salary 
FROM employees 
WHERE employees.salary = ( 
    SELECT min_salary
    FROM jobs 
    WHERE employees.job_id = jobs.job_id
);
```
26. Write a subquery to find the first name, last name, and salary of employees who earn above the average salary and work in any IT-related department.
```sql
SELECT first_name,
       last_name, 
       salary
FROM employees 
WHERE department_id IN (
    SELECT department_id 
    FROM departments 
    WHERE department_name LIKE 'IT%'
) 
AND salary >( 
    SELECT avg(salary)
    FROM employees
);
```
27. Use a subquery to find the first name, last name, job ID, and salary of employees who earn more than all "Shipping Clerks" (JOB_ID = 'SH_CLERK'), sorted by salary in ascending order.
```sql
SELECT first_name, 
       last_name, 
       job_id, 
salary 
FROM employees
WHERE salary > ALL ( 
    SELECT salary 
    FROM employees 
    WHERE job_id = 'SH_CLERK'
) 
ORDER BY salary;
```

28. List the first and last names of employees who do not manage other employees.
```sql
SELECT b.first_name, 
       b.last_name 
FROM employees b 
WHERE NOT EXISTS ( 
    SELECT 'X' 
    FROM employees a 
    WHERE a.manager_id = b.employee_id 
);
```
29. Use a subquery to display employee ID, first name, last name, and department name for all employees.
```sql
SELECT employee_id, 
       first_name, 
       last_name, 
       (SELECT department_name 
        FROM departments d 
        WHERE e.department_id = d.department_id)
       AS department 
FROM employees e 
ORDER BY department;
```
30. Write a subquery to get the fourth-lowest salary among all employees' salaries.
```sql
SELECT DISTINCT salary 
FROM employees e1 
WHERE 4 = ( 
    SELECT COUNT(DISTINCT salary)
    FROM employees e2 
    WHERE e1.salary >= e2.salary
);
```
31. Find the department numbers and names of departments with no current employees.
```sql
SELECT * 
FROM departments 
WHERE department_id NOT IN (
    SELECT department_id 
    FROM employees
);
```
32. Write a query to retrieve the top three highest unique salaries.
```sql
SELECT DISTINCT salary 
FROM employees a
WHERE 3 >= ( 
    SELECT COUNT(DISTINCT salary) 
    FROM employees b 
    WHERE a.salary <= b.salary 
) 
ORDER BY a.salary DESC;
```
33. Change the `email` field of employees whose department_id is 80 and commission rate is below 20% to 'not available'.
```sql
UPDATE employees 
SET email='not available'
WHERE department_id=80 
AND commission_pct<0.20;
```
34. Update the salary to 8,000 for the employee with ID 105, but only if their current salary is below 5,000.
```sql
UPDATE employees 
SET SALARY = 8000 
WHERE employee_id = 105 
AND salary < 5000;
```
35. Change the job ID of the employee with ID 118 to 'SH_CLERK' if they work in department 30 and their current job ID does not start with 'SH'.
```sql
UPDATE employees 
SET JOB_ID = 'SH_CLERK' 
WHERE employee_id = 118 
AND department_id = 30 
AND NOT JOB_ID LIKE 'SH%';
```
36. Increase the salaries of employees in departments 40, 90, and 110 as follows: 25% for department 40, 15% for department 90, and 10% for department 110. Salaries in other departments remain the same.
```sql
UPDATE employees 
SET salary = CASE department_id 
                WHEN 40 THEN salary + (salary * 0.25) 
                WHEN 90 THEN salary + (salary * 0.15) 
                WHEN 110 THEN salary + (salary * 0.10)
                ELSE salary 
            END
WHERE department_id IN (40,50,50,60,70,80,90,110);
```
37. Write a query to find the last name, job title, and salary of employees who have not worked as "Programmer" or "Shipping Clerk" and do not have a salary of 4,500, 10,000, or 15,000.
```sql
SELECT last_name, job_id, salary 
FROM employees 
WHERE job_id NOT IN ('IT_PROG', 'SH_CLERK') 
AND salary NOT IN (4500,10000, 15000);
```
38. Write a query to list the employee ID, job title, and the length of service in days for all employees who have worked in a department with ID 100.
```sql
SELECT 
    employee_id, 
    job_title, 
    (CURRENT_DATE - hire_date) AS length_of_service_in_days
FROM 
    employees
NATURAL JOIN jobs
WHERE 
    department_id = 100;
```

39. Write a query to display the first name, last name, department name, and location ID for employees working in departments located in the city "New York."
```sql
SELECT 
    e.first_name, 
    e.last_name, 
    d.department_name, 
    d.location_id
FROM 
    employees e
JOIN 
    departments d ON e.department_id = d.department_id
JOIN 
    locations l ON d.location_id = l.location_id
WHERE 
    l.city = 'New York';

```

40. Create a query to show each department’s ID, name, and the number of employees in that department, only for departments with more than five employees.
```sql
SELECT 
    d.department_id, 
    d.department_name, 
    COUNT(e.employee_id) AS number_of_employees
FROM 
    departments d
JOIN 
    employees e ON d.department_id = e.department_id
GROUP BY 
    d.department_id, d.department_name
HAVING 
    COUNT(e.employee_id) > 5;
```

### Submission
#### You should send `.sql` or `.md` file with all queries and comments with describing your query.