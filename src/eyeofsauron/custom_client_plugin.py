import ast
from typing import Dict

from ariadne_codegen.plugins.base import Plugin
from graphql import GraphQLSchema

class CustomClientPlugin(Plugin):
    def __init__(self, schema: GraphQLSchema, config_dict: Dict) -> None:
        super().__init__(schema=schema, config_dict=config_dict)
    
    def generate_client_module(self, module: ast.Module) -> ast.Module:
        # Add necessary imports
        module.body.insert(0, self._generate_import("json"))
        module.body.insert(1, self._generate_import_from("typing", ["Optional", "Any", "Dict"]))
        module.body.insert(2, self._generate_import_from("graphqlclient", ["GraphQLClient"]))
        module.body.insert(2, self._generate_import_from("pydantic_core", ["to_jsonable_python"]))
        module.body.insert(3, self._generate_import_from("ecdsa", ["SigningKey", "VerifyingKey", "SECP256k1", "BadSignatureError"]))
        module.body.insert(4, self._generate_import("base64"))
        module.body.insert(5, self._generate_import("hashlib"))
        module.body.insert(6, self._generate_import("ecdsa"))
        
        # Add standalone function
        standalone_function = self._generate_standalone_function()
        module.body.append(standalone_function)
        return module

    def _generate_import(self, module: str) -> ast.Import:
        return ast.Import(names=[ast.alias(name=module)])

    def _generate_import_from(self, module: str, names: list) -> ast.ImportFrom:
        return ast.ImportFrom(module=module, names=[ast.alias(name=name) for name in names], level=0)
    
    def _generate_standalone_function(self) -> ast.FunctionDef:
        # Define a standalone function
        standalone_function = ast.parse(
            """
    # Step 1: Prepare the signature
def prepare_signature(private_key_hex, message):
    sk = SigningKey.from_string(bytes.fromhex(private_key_hex), curve=SECP256k1)
    message_hash = hashlib.sha256(message).digest()
    signature_der = sk.sign_digest(message_hash, sigencode=ecdsa.util.sigencode_der)

    # Encode the signature in base64
    signature_base64 = encode_signature(signature_der)
    return signature_base64

# Step 2: Encode the signature
def encode_signature(signature):
    return base64.b64encode(signature).decode('utf-8')
"""
    )
        return standalone_function
    
    def generate_client_class(self, class_def: ast.ClassDef) -> ast.ClassDef:
        # Add custom __init__ method
        init_method = self._generate_init_method()
        class_def.body.insert(0, init_method)
        
        # Add custom execute method
        execute_method = self._generate_execute_method()
        class_def.body.insert(1, execute_method)
        
        return ast.fix_missing_locations(class_def)
    
    def _generate_init_method(self) -> ast.FunctionDef:
        # Define the __init__ method
        init_method = ast.parse(
            """
def __init__(self, secret_key, *args, **kwargs):
        super().__init__(url="https://sauron.gandalf.network/public/gql", *args, **kwargs)
        if secret_key.lower().startswith('0x'):
            secret_key = secret_key[2:]
        self.secret_key = secret_key
"""
        )
        return init_method

    def _generate_execute_method(self) -> ast.AsyncFunctionDef:
        # Define the execute method
        execute_method = ast.parse(
            """
async def execute(
        self,
        query: str,
        operation_name: Optional[str] = None,
        variables: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ):
        # Prepare the request body
        request_body = {
            "query": query,
            "operationName": operation_name,
            "variables": variables,
        }
        
        request_body_str = json.dumps(request_body).encode('utf-8')

        # Generate the signature based on the request body
        signature = prepare_signature(self.secret_key, request_body_str)

        headers: Dict[str, str] = {"Content-Type": "application/json"}
        headers.update({"X-Gandalf-Signature": signature})

        merged_kwargs: Dict[str, Any] = kwargs.copy()
        merged_kwargs["headers"] = headers
        
        return await self.http_client.post(
            url=self.url,
            content=json.dumps(
                {
                    "query": query,
                    "operationName": operation_name,
                    "variables": variables,
                },
                default=to_jsonable_python,
            ),
            **merged_kwargs,
        )
"""
        )
                
        return execute_method
