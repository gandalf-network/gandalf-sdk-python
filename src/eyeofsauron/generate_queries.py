from graphql import build_client_schema, get_introspection_query, get_named_type, is_interface_type, is_object_type, is_union_type, print_ast, parse, print_ast

import requests

def fetch_schema(url):
    response = requests.post(
        url,
        json={'query': get_introspection_query()}
    )
    response.raise_for_status()
    return build_client_schema(response.json()['data'])

def format_arguments(args):
    arg_strings = [f"${arg_name}: {arg.type}" for arg_name, arg in args.items()]
    return ", ".join(arg_strings)

def format_arguments_in_query(args):
    arg_strings = [f"{arg_name}: ${arg_name}" for arg_name in args.keys()]
    return f"({', '.join(arg_strings)})" if arg_strings else ""

def get_query_fields(type_, current_depth, max_depth, schema, alias_counter, global_field_aliases):
    if current_depth > max_depth:
        return ""

    fields = type_.fields
    field_strings = []

    for field_name, field in fields.items():
        field_type = get_named_type(field.type)
        field_args = format_arguments_in_query(field.args)

        if field_name in global_field_aliases and global_field_aliases[field_name] != field_type:
            alias = f"{field_name}Alias{alias_counter[field_name]}:{field_name}"
            alias_counter[field_name] += 1
        else:
            alias = field_name
            if field_name not in global_field_aliases:
                alias_counter[field_name] = 1  # Initialize counter if not present
            global_field_aliases[field_name] = field_type

        if is_object_type(field_type) or is_interface_type(field_type) or is_union_type(field_type):
            nested_fields = get_query_fields(field_type, current_depth + 1, max_depth, schema, alias_counter, global_field_aliases)
            if is_interface_type(field_type) or is_union_type(field_type):
                possible_types = schema.get_possible_types(field_type)
                inline_fragments = []
                for possible_type in possible_types:
                    nested_possible_fields = get_query_fields(possible_type, current_depth + 1, max_depth, schema, alias_counter, global_field_aliases)
                    inline_fragments.append(f"... on {possible_type.name} {{\n{nested_possible_fields}\n}}")
                field_strings.append(f"{alias}{field_args} {{\n__typename\n{nested_fields}\n{' '.join(inline_fragments)}\n}}")
            else:
                field_strings.append(f"{alias}{field_args} {{\n__typename\n{nested_fields}\n}}")
        else:
            field_strings.append(f"{alias}{field_args}")

    return " ".join(field_strings)

def generate_query_for_field(type_name, field_name, schema, depth=1, alias_counter=None, global_field_aliases=None):
    if alias_counter is None:
        alias_counter = {}
    if global_field_aliases is None:
        global_field_aliases = {}

    type_ = schema.get_type(type_name)
    if not type_:
        raise ValueError(f"Type '{type_name}' not found in the schema.")

    field = type_.fields.get(field_name)
    if not field:
        raise ValueError(f"Field '{field_name}' not found in type '{type_name}'.")

    scope_field_types = global_field_aliases.copy()
    field_type = get_named_type(field.type)
    field_args = format_arguments_in_query(field.args)
    query_fields = get_query_fields(field_type, 1, depth, schema, alias_counter, scope_field_types)
    query = f"{field_name}{field_args} {{\n{query_fields}\n__typename\n}}"
    return query, field.args

def generate_queries_for_type(type_name, schema, depth=1):
    alias_counter = {}
    global_field_aliases = {}

    type_ = schema.get_type(type_name)
    if not type_:
        raise ValueError(f"Type '{type_name}' not found in the schema.")

    queries = []
    all_args = {}

    for field_name in type_.fields.keys():
        query, args = generate_query_for_field(type_name, field_name, schema, depth, alias_counter, global_field_aliases)
        all_args.update(args)
        formatted_args = format_arguments(args)
        queries.append(f"{type_name.lower()} {field_name} ({formatted_args}) {{ {query} }}")

    return queries, all_args


def generate_queries(url):
    schema = fetch_schema(url)
    queries, _ = generate_queries_for_type('Query', schema, depth=20)

    query_list = "\n".join(queries)
    ast = parse(query_list)
    return print_ast(ast)