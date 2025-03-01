# graphql-tabrak

Automatically generate and send query for graphql endpoint (based on enabled introspection query). Will help you find "misconfigured" graphql queries that unintentionally leak informations.



Usage:

```
1. pip install gql[all]
2. configure the data.yaml, add your variables
3. python3 tabrak.py data.yaml.example http://localhost:4000/graphql

```
![image](https://github.com/user-attachments/assets/f43fb77f-c2b6-4e9c-a7c6-a37039322fb3)

option 1: check mandatory variable

option 2: generate queries (in the form of request body so you can copy paste it direct to burpsuite) and automatically send it

option 3: generate mutation queries (in the form of request body so you can copy paste it direct to burpsuite)



**Example:**

*data.yaml*
```
# Sample YAML file

#general configuration
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
![image](https://github.com/user-attachments/assets/a79109df-ec4e-45ea-809f-4e1aa4414c3e)


![image](https://github.com/user-attachments/assets/1e489ba9-013f-4982-a321-85baade2c30d)





