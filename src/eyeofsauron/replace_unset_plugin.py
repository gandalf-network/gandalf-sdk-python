from ariadne_codegen.plugins.base import Plugin

class ReplaceUnsetPlugin(Plugin):
    def __init__(self, schema, config_dict):
        super().__init__(schema, config_dict)
    
    def copy_code(self, copied_code: str) -> str:
        if 'UNSET = UnsetType()' in copied_code:
            copied_code = copied_code.replace('UNSET = UnsetType()', 'UNSET = None')
        return copied_code
