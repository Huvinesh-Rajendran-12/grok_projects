from xai_grok_sdk import XAI
from xai_grok_sdk.xai import ChatCompletionResponse
from dotenv import load_dotenv
import os
load_dotenv()

XAI_API_KEY = os.getenv("XAI_API_KEY", "")

xai: XAI = XAI(
    api_key=XAI_API_KEY,
    model="grok-2-1212"
)

# basic chat completion
response: ChatCompletionResponse = xai.invoke(
    messages=[
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ],
    stream=True
)

msg = response.choices[0].message
print(msg)

# implement function calling

tool_definitions = [
    {
        "name": "get_weather",
        "description": "Get the weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g., San Francisco, CA",
                }
            },
            "required": ["location"],
        },
    }
]

def get_weather(location: str)  -> str:
    return f"The weather in {location} is 75 degrees and sunny."

xai_tool = XAI(
    api_key=XAI_API_KEY,
    model="grok-2-1212",
    tools=tool_definitions,
    function_map={"get_weather": get_weather}
)

tool_response = xai_tool.invoke(
    messages=[
        {
            "role": "user",
            "content": "What is the weather in New York ?"
        }
    ],
    tool_choice="auto"
)
print(tool_response.choices[0].message)
print(response.choices[0].message.tool_results[0].content if response.choices[0].message.tool_results else None)
