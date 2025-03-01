import requests
from graphql import build_client_schema, get_introspection_query, GraphQLObjectType, GraphQLInputObjectType
import json
import yaml
from http.cookies import SimpleCookie
import argparse
import os


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


max_depth = 0

def fetch_schema(url, headers=None, cookies=None):
    query = get_introspection_query()
    response = requests.post(url, json={'query': query}, headers=headers, cookies=json_cookies, verify=False)
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

def generate_field_string(field_type, depth):
    if depth > max_depth:
        return "__typename"  # Prevents deep nesting beyond max_depth

    """ Recursively generate fields for nested GraphQLObjectTypes. """
    if isinstance(field_type, GraphQLObjectType):
        fields = field_type.fields
        field_strings = []
        for field_name, field in fields.items():
            sub_field_type = get_full_type(field.type)
            if isinstance(sub_field_type, GraphQLObjectType):
                sub_fields = generate_field_string(sub_field_type, depth+1)
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
        variables[arg] = config[str(arg)]
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

def generate_mutation_string(mutation_name, mutation_info):
    global_arg_list = []
    args_list = []
    variables = {}

    for arg in mutation_info.args:
        global_arg_list.append(f'${arg}: {mutation_info.args[arg].type}')
        variables[arg] = config[str(arg)]
        args_list.append(f'{arg}: ${arg}')

    global_arg_str = ", ".join(global_arg_list)
    args_str = ", ".join(args_list)
    vars_str = ", ".join([f"{arg.name}: ${arg.name}" for arg in mutation_info.args if hasattr(arg, 'type')])

    return_type = get_full_type(mutation_info.type)
    field_string = generate_field_string(return_type, 0)
    if field_string:
        if args_str:
            mutation = f"mutation ({global_arg_str}) {{ {mutation_name}({args_str}) {{ {field_string} }} }} "
        else:
            mutation = f"{{ {mutation_name} {{ {field_string} }} }}"
    else:
        if args_str:
            mutation = f"mutation ({global_arg_str}) {{ {mutation_name}({args_str}) }}"
        else:
            mutation = f"{{ {mutation_name} }}"
    return mutation, variables, global_arg_str


def send_query(query, variables, url, headers=None):
    """ Send the query to the GraphQL API and return the response. """
    jsons = {'query': query, 'variables': variables}
    print(bcolors.BOLD + "Request Body (copy to burpsuite):" + bcolors.ENDC)
    print(f'{json.dumps(jsons)}')
    print("")
    response = requests.post(url, json=jsons, headers=headers, cookies=json_cookies, verify=False)
    response.raise_for_status()
    return response.json()

def get_var_requirements(operations, schema):
    def get_input_fields(input_type, depth):
        if depth > max_depth:
            return ""  # Prevents deep nesting beyond max_depth
        """Recursively retrieves input object fields."""
        fields = []
        if hasattr(input_type, 'fields'):
            for field_name, field in input_type.fields.items():
                field_type = get_full_type(field.type)
                if isinstance(field_type, GraphQLInputObjectType):
                    sub_fields = get_input_fields(field_type, depth+1)
                    fields.append(f"{field_name}: {{ {', '.join(sub_fields)} }}")
                else:
                    fields.append(f"{field_name}: {field_type}")
        return fields

    var_reqs = {}
    
    for operation_name, operation_info in operations.items():
        for arg in operation_info.args:
            arg_type = get_full_type(operation_info.args[arg].type)
            input_fields = get_input_fields(arg_type, 1)
            var_reqs[arg] = arg_type.name + " { " + ", ".join(input_fields) + " }"

    sorted_dict = dict(sorted(var_reqs.items()))
    
    for var, type_desc in sorted_dict.items():
        print(f'{var}: {type_desc}')


def generate_and_send_queries(schema, url, headers=None, cookies=None):
    query_type = schema.query_type
    queries = query_type.fields

    mutation_type = schema.mutation_type
    if mutation_type:
        mutations = mutation_type.fields
    else:
        mutations = None

    print("1. see all args requirements")
    print("2. generate and send queries")
    print("3. generate mutations (mutations is dangerous so we are not gonna send it)")
    opt = input(">> ")
    if opt == "1":
        print("\n" + bcolors.BOLD + "Queries Variables Required:" + bcolors.ENDC + "\n")
        get_var_requirements(queries, schema)
        print("")
        print("\n" + bcolors.BOLD + "Mutations Variables Required:" + bcolors.ENDC + "\n")
        if mutations:
            get_var_requirements(mutations, schema)
        else:
            print("[!] Seems like graphql doesn't have mutation") 
    elif opt == "2":
        for query_name, query_info in queries.items():
            print(bcolors.OKBLUE + bcolors.BOLD + f"Processing Query: {query_name}" + bcolors.ENDC)
            print("")
            query_string, variables, global_arg_str = generate_query_string(query_name, query_info)
            print(bcolors.BOLD + "Variables Required:" + bcolors.ENDC)
            print(f'{global_arg_str}')
            print("")
            # print(bcolors.BOLD + "Generated Query String:" + bcolors.ENDC)
            # print(f"{query_string}")
            # print("")
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
    elif opt == "3":
        if mutations:
            for mutation_name, mutation_info in mutations.items():
                print(mutation_name, mutation_info)
                print(bcolors.OKBLUE + bcolors.BOLD + f"Processing Query: {mutation_name}" + bcolors.ENDC)
                print("")
                mutation_string, variables, global_arg_str = generate_mutation_string(mutation_name, mutation_info)
                print(bcolors.BOLD + "Variables Required:" + bcolors.ENDC)
                print(f'{global_arg_str}')
                print("")
                print(bcolors.BOLD + "Generated Query String:" + bcolors.ENDC)
                print(f"{mutation_string}")
                print("")
                print(bcolors.BOLD + "Variables supplied:" + bcolors.ENDC)
                print(f"{json.dumps(variables)}")
                print("")
                jsons = {'query': mutation_string, 'variables': variables}
                print(bcolors.BOLD + "Request Body (copy to burpsuite):" + bcolors.ENDC)
                print(f'{json.dumps(jsons)}')
                print("")
        else:
            print("[!] Seems like graphql doesn't have mutation") 
    else:
        print("[!] Error")



def read_file(file_path):
    """Reads and returns the content of the file."""
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return None
    
    with open(file_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)

        return config

# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a file and a URL.")
    parser.add_argument("file", type=str, help="Path to the file")
    parser.add_argument("url", type=str, help="URL to process")

    args = parser.parse_args()
    config = read_file(args.file)
    max_depth = config["max_depth"]

    graphql_url = args.url
    
    # If authentication is required, include the token
    headers = {
        'Authorization': config['auth_token'],
        'X-Csrf-Token': config['auth_token']
    }

    cookie = SimpleCookie()
    cookie.load(config['cookies'])
    json_cookies = {}
    for key, morsel in cookie.items():
        json_cookies[key] = morsel.value
    print(json_cookies)
    
    try:
        introspection_data = fetch_schema(graphql_url, headers=headers, cookies=json_cookies)
        schema = build_schema(introspection_data)
        generate_and_send_queries(schema, graphql_url, headers=headers, cookies=json_cookies)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except KeyError as key_err:
        print(f"Key error: {key_err}. Check if the schema returned correctly.")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")

