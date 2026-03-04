from __future__ import annotations 
from pydantic import BaseModel, ValidationError
import abc
from enum import Enum
from typing import Any
from dataclasses import dataclass, field
from pathlib import Path
from pydantic.json_schema import model_json_schema
# define different types of tools
class Toolkind(str, Enum):
    READ = "read"
    WRITE = "write"
    SHELL = "shell"
    NETWORK = "network"
    MEMORY = "memory"
    MCP = "mcp"

@dataclass
class ToolResult:
     success: bool
     output: str
     error: str | None = None
     metadata: dict[str, Any] = field(default_factory=dict)
     truncated: bool =False
     @classmethod
     def error_result(cls, error: str, output: str = "",**kwargs: Any):
          return cls(
               success = False,
               output = output,
               error = error,
               **kwargs
          )
     @classmethod
     def success_result(cls, output: str = "",**kwargs: Any):
          return cls(
               success = True,
               output = output,
               error = None,
               **kwargs
          )
     
@dataclass
class ToolInvocation:
     params: dict[str, Any]
     cwd: Path
@dataclass
class ToolConfirmation:
     tool_name: str
     params: dict[str, Any]



#base class for all tools
class Tool(abc.ABC):
    name: str = "base_tool"
    description: str = "Base tool"
    kind: Toolkind = Toolkind.READ
    def __init__(self) -> None:
        pass
     
    #a error needs to be raised if schema is not implemented thats why we use property instead of creating a class attribute like name, description, kind
    @property
    def schema(self) -> dict[str, Any] | type["BaseModel"]: #dictionary is for mcp, BaseModel is for other tools
        raise NotImplementedError("Tool must define a schema property or class attribute")
    @abc.abstractmethod
    async def execute(self, invocation: ToolInvocation) -> ToolResult:
            pass
    def validate_params(self, params: dict[str, Any]) -> list[str]:
        schema = self.schema
        if isinstance(schema, type) and issubclass(schema, BaseModel):
            try:
                schema(**params) # if the params pass the validation error 
            except ValidationError as e:
                errors = []  #if it catches an error we give the list of errors to the model
                for error in e.errors():
                    field = ".".join(str(x) for x in error.get("loc",[]))
                    msg = error.get("msg", "Validation error")
                    errors.append(f"Parameter '{field}': {msg}")
                
                return errors
            except Exception as e: #worst case just send the string of error to the LLM
                 return [str(e)]
            
# if the schema is a dictionary its for mcp tool so we dont need to validate it here
        return []
    
    def is_mutating(self, params: dict[str, Any]) ->  bool: # a mutating state means it changes the state of the system
         return self.kind in {Toolkind.WRITE, Toolkind.SHELL, Toolkind.NETWORK, Toolkind.MEMORY}
    async def get_confirmation(self, invocation: ToolInvocation) -> ToolInvocation:
         if not self.is_mutating(invocation.params):
              return None
         return ToolConfirmation(
              tool_name=self.name,
              params = invocation.params,
              description = f"Execute {self.name}",
         )
    def to_openai_schema(self) -> dict[str, Any]:
        schema = self.schema
        if isinstance(schema, type) and issubclass(schema, BaseModel):
              json_schema = model_json_schema(schema, mode = "serialization")
              #this is the way openai expects the tool schema to be defined
              return {                     
                   "name": self.name,
                   "description": self.description,
                   "parameters":{
                        "type": "object",
                        "properties": json_schema.get("properties", {}),
                        "required": json_schema.get("required", [])
                   },
              }
        if isinstance(schema,dict):
              result = {"name": self.name, "description": self.description}
              if "parameters" in schema:
                   result["parameters"] = schema["parameters"]
              else:
                   result["parameters"] = schema
              return result
        raise ValueError(f"Invalid schema type for tool {self.name}: {type(schema)}")