# graphql-tabrak

Automatically generate and send query for graphql endpoint (based on enabled introspection query). Will help you find "misconfigured" graphql queries that unintentionally leak informations.



Usage:

```
1. pip install gql[all]
2. configure the data.yaml, add your variables
3. python3 tabrak.py
```
![image](https://github.com/user-attachments/assets/f93c6cd1-15ee-40a9-859f-b01296d04d92)

option 1: check mandatory variable

option 2: generate queries (in the form of request body so you can copy paste it direct to burpsuite) and automatically send it

option 3: generate mutation queries (in the form of request body so you can copy paste it direct to burpsuite)



**Example:**

*data.yaml*
```
# Sample YAML file

#general configuration
graphql_url: "http://localhost:4000/graphql"
cookies: ""
auth_token: ""
max_depth: 1


#enum configuration
id: 1
filter: "gra"
limit: 1
offset: 1
sort: null
pagination: null
queries: null
```
![image](https://github.com/user-attachments/assets/5b9acd5e-9b84-48b0-8a75-60e59bd6842c)

![image](https://github.com/user-attachments/assets/bd44af12-0aad-4488-995b-d110db1a0396)




