import logging
from plugin.llm_tool_plugin import LLMToolMetadata, LLMToolPlugin


class EchoPlugin(LLMToolPlugin):
    """
    A sample LLM tool plugin that echoes the input text.
    """
    _version_ = "1.0.0"

    @classmethod
    def get_metadata(cls) -> LLMToolMetadata:
        return {
            "name": "echo",
            "displayName": "Echo Tool",
            "description": "A tool to echo the input text",
            "displayDescription": "This tool simply echoes the input text you provide",
            "parameters": {
                "text": {
                    "type": "string",
                    "description": "The text to echo",
                    "displayDescription": "The text that will be echoed back",
                    "required": True
                },
                "prefix": {
                    "type": "string",
                    "description": "A prefix to add before the text",
                    "displayDescription": "Optional prefix to add before the echoed text",
                    "required": False
                }
            }
        }

    def invoke(self, text: str, prefix: str = "") -> str:
        logging.info(f"Echo tool was called with text: {text} and prefix: {prefix}")
        result = prefix + text if prefix else text
        return result