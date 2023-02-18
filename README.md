<h1>Differentially-Private-Queries</h1>


<h2>Description</h2>

This project aims to implement a querying system for a company that collects movie ratings, with the goal of securely disclosing this information. 
Instead of releasing a database with pseudonymized identifiers, this company aims to enable researchers to learn some useful information from their database while preserving the privacy of their users. 
The system allows researchers to send counting queries of a certain format, where they can obtain the number of people who have rated a given movie greater or equal than a certain level. 
The queries are answered in a differentially private way, using the Laplace mechanism. 
The class DpQuerySession contains a get_count method, which takes as input the movie name, rating threshold, and epsilon value and returns the count with differentially private noise added. It also has a remaining_budget method to calculate the remaining privacy budget. The implementation should ensure that the queries do not exceed the privacy budget. 

<h2>Languages Used</h2>

- <b>Python </b> 

<!--
 ```diff
- text in red
+ text in green
! text in orange
# text in gray
@@ text in purple (and bold)@@
```
--!>
