## LeetCode Problemset database

### Problemset ID & Name: 175. Combine Two Tables

Table: `Person`

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| PersonId    | int     |
| FirstName   | varchar |
| LastName    | varchar |
+-------------+---------+
PersonId is the primary key column for this table.
```

Table: `Address`

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| AddressId   | int     |
| PersonId    | int     |
| City        | varchar |
| State       | varchar |
+-------------+---------+
AddressId is the primary key column for this table.
``` 

Write a SQL query for a report that provides the following information for each person in the Person table, regardless if there is an address for each of those people:
```
FirstName, LastName, City, State
```

#### solution:
```
SELECT a.FirstName, a.LastName, b.City, b.State FROM Person as a
LEFT JOIN Address as b ON a.PersonId = b.PersonId
```

### Problemset ID & Name: 176. Second Highest Salary

Write a SQL query to get the second highest salary from the Employee table.

```
+----+--------+
| Id | Salary |
+----+--------+
| 1  | 100    |
| 2  | 200    |
| 3  | 300    |
+----+--------+
```

For example, given the above Employee table, the query should return 200 as the second highest salary. If there is no second highest salary, then the query should return null.

```
+---------------------+
| SecondHighestSalary |
+---------------------+
| 200                 |
+---------------------+
```

#### solution
```sql
/* Write your T-SQL query statement below */

--not commom solution
SELECT MAX(Salary) AS SecondHighestSalary FROM Employee
WHERE Salary < 
(
SELECT MAX(Salary) AS Salary FROM Employee
)
```

```sql
/* Write your T-SQL query statement below */

--commom solution
SELECT MAX(Salary) AS SecondHighestSalary FROM 
(SELECT *, DENSE_RANK() OVER(ORDER BY Salary DESC) AS rn FROM Employee
) AS mn
WHERE mn.rn = 2
```
**attention:** If there is no second highest salary, then the query should return null.

### Problemset ID & Name: 177. Nth Highest Salary
Write a SQL query to get the n^th highest salary from the Employee table.

```
+----+--------+
| Id | Salary |
+----+--------+
| 1  | 100    |
| 2  | 200    |
| 3  | 300    |
+----+--------+
```

For example, given the above Employee table, the nth highest salary where n = 2 is 200. If there is no nth highest salary, then the query should return null.

```
+------------------------+
| getNthHighestSalary(2) |
+------------------------+
| 200                    |
+------------------------+
```

#### solution
```sql
CREATE FUNCTION getNthHighestSalary(@N INT) RETURNS INT AS
BEGIN
    RETURN (
        /* Write your T-SQL query statement below. */
        SELECT MAX(mn.Salary) AS [getNthHighestSalary(@N)] FROM
        (
        SELECT *, DENSE_RANK() OVER(ORDER BY Salary DESC) AS rn FROM Employee
        ) AS mn
        WHERE mn.rn = @N
        );
END
```
**attention:** If there is no second highest salary, then the query should return null.

### Problemset ID & Name: 178. Rank Scores

Write a SQL query to rank scores. If there is a tie between two scores, both should have the same ranking. Note that after a tie, the next ranking number should be the next consecutive integer value. In other words, there should be no "holes" between ranks.

```
+----+-------+
| Id | Score |
+----+-------+
| 1  | 3.50  |
| 2  | 3.65  |
| 3  | 4.00  |
| 4  | 3.85  |
| 5  | 4.00  |
| 6  | 3.65  |
+----+-------+
```

For example, given the above Scores table, your query should generate the following report (order by highest score):

```
+-------+---------+
| score | Rank    |
+-------+---------+
| 4.00  | 1       |
| 4.00  | 1       |
| 3.85  | 2       |
| 3.65  | 3       |
| 3.65  | 3       |
| 3.50  | 4       |
+-------+---------+
```

Important Note: For MySQL solutions, to escape reserved words used as column Names, you can use an apostrophe before and after the keyword. For example `Rank`.

#### solution
```sql
/* Write your T-SQL query statement below */

SELECT score, Rank FROM (
SELECT *, DENSE_RANK() OVER(ORDER BY score DESC) as Rank FROM Scores
) AS mn
ORDER BY Rank
```

### Problemset ID & Name: 180. Consecutive Numbers

Write a SQL query to find all numbers that appear at least three times consecutively.

```
+----+-----+
| Id | Num |
+----+-----+
| 1  |  1  |
| 2  |  1  |
| 3  |  1  |
| 4  |  2  |
| 5  |  1  |
| 6  |  2  |
| 7  |  2  |
+----+-----+
```

For example, given the above Logs table, 1 is the only number that appears consecutively for at least three times.

```
+-----------------+
| ConsecutiveNums |
+-----------------+
| 1               |
+-----------------+
```

#### solution

