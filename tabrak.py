import requests
from graphql import build_client_schema, get_introspection_query, GraphQLObjectType
import json
import yaml


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


with open('data.yaml', 'r') as file:
    data = yaml.safe_load(file)


def fetch_schema(url, headers=None):
    query = get_introspection_query()
    response = requests.post(url, json={'query': query}, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data['data']

def build_schema(introspection_data):
    return build_client_schema(introspection_data)

def get_full_type(type_obj):
    """ Recursively unwraps nested GraphQL types to get the full type. """
    while hasattr(type_obj, 'of_type'):
        type_obj = type_obj.of_type
    return type_obj

def generate_field_string(field_type, depth, max_depth=1):
    if depth > max_depth:
        return "__typename"  # Prevents deep nesting beyond max_depth

    """ Recursively generate fields for nested GraphQLObjectTypes. """
    if isinstance(field_type, GraphQLObjectType):
        fields = field_type.fields
        field_strings = []
        for field_name, field in fields.items():
            sub_field_type = get_full_type(field.type)
            if isinstance(sub_field_type, GraphQLObjectType):
                sub_fields = generate_field_string(sub_field_type, depth+1, max_depth)
                field_strings.append(f"{field_name} {{ {sub_fields} }}")
            else:
                field_strings.append(field_name)
        return " ".join(field_strings)
    return ""



def generate_query_string(query_name, query_info):
    global_arg_list = []
    args_list = []
    variables = {}

    for arg in query_info.args:
        global_arg_list.append(f'${arg}: {query_info.args[arg].type}')
        variables[arg] = data[str(arg)]
        args_list.append(f'{arg}: ${arg}')

    global_arg_str = ", ".join(global_arg_list)
    args_str = ", ".join(args_list)
    vars_str = ", ".join([f"{arg.name}: ${arg.name}" for arg in query_info.args if hasattr(arg, 'type')])

    return_type = get_full_type(query_info.type)
    field_string = generate_field_string(return_type, 0)
    if field_string:
        if args_str:
            query = f"query ({global_arg_str}) {{ {query_name}({args_str}) {{ {field_string} }} }} "
        else:
            query = f"{{ {query_name} {{ {field_string} }} }}"
    else:
        if args_str:
            query = f"query ({global_arg_str}) {{ {query_name}({args_str}) }}"
        else:
            query = f"{{ {query_name} }}"
    return query, variables, global_arg_str

def send_query(query, variables, url, headers=None):
    """ Send the query to the GraphQL API and return the response. """
    response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
    response.raise_for_status()
    return response.json()

def generate_and_send_queries(schema, url, headers=None):
    query_type = schema.query_type
    queries = query_type.fields
    for query_name, query_info in queries.items():
        print(bcolors.OKBLUE + bcolors.BOLD + f"Processing Query: {query_name}" + bcolors.ENDC)
        print("")
        query_string, variables, global_arg_str = generate_query_string(query_name, query_info)
        print(bcolors.BOLD + "Variables Required:" + bcolors.ENDC)
        print(f'{global_arg_str}')
        print("")
        print(bcolors.BOLD + "Generated Query String:" + bcolors.ENDC)
        print(f"{query_string}")
        print("")
        print(bcolors.BOLD + "Variables supplied:" + bcolors.ENDC)
        print(f"{json.dumps(variables)}")
        print("")

        
        try:
            response = send_query(query_string, variables, url, headers)
            print(bcolors.BOLD + "Response:" + bcolors.ENDC)
            print(json.dumps(response, sort_keys=True, indent=4))
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred while processing {query_name}: {http_err}")
        except Exception as err:
            print(f"An error occurred while processing {query_name}: {err}")
        
        print("")  # Newline for better readability

# Example usage
if __name__ == "__main__":
    graphql_url = 'http://localhost:4000/graphql'  # Replace with your GraphQL endpoint
    
    # If authentication is required, include the token
    headers = {
        'Authorization': 'Bearer YOUR_ACCESS_TOKEN'
    }
    
    try:
        introspection_data = fetch_schema(graphql_url, headers=headers)
        schema = build_schema(introspection_data)
        generate_and_send_queries(schema, graphql_url, headers)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except KeyError as key_err:
        print(f"Key error: {key_err}. Check if the schema returned correctly.")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")
