from xai_grok_sdk import XAI
import os
from dotenv import load_dotenv
from typing import List, Dict, Any
from database import init_db, get_customer_info as db_get_customer_info, get_order_details as db_get_order_details, cancel_order as db_cancel_order

load_dotenv()
init_db()  # Initialize the database

XAI_API_KEY = os.getenv("XAI_API_KEY", "")
# Initialize the client (do not provide tools when using streaming)

tool_definitions = [
    {
        "name": "get_customer_info",
        "description": "Retrieves customer information based on their customer ID. Returns the customer's name, email, and phone number.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The unique identifier for the customer.",
                }
            },
            "required": ["customer_id"],
        },
    },
    {
        "name": "get_order_details",
        "description": "Retrieves order details based on the order ID. Returns the order ID, product name, quantity, price and status.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The unique identifier for the order.",
                }
            },
            "required": ["order_id"],
        }
    },
    {
        "name": "cancel_order",
        "description": "Cancels an order based on the order ID. Returns a confirmation message if the cancellation is successful.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The unique identifier for the order.",
                }
            },
            "required": ["order_id"],
        }
    }
]



def get_customer_info(customer_id: str):
    result = db_get_customer_info(customer_id)
    return result if result else "Customer not found."

def get_order_details(order_id: str):
    result = db_get_order_details(order_id)
    return result if result else "Order not found."

def cancel_order(order_id: str):
    return db_cancel_order(order_id)

def process_tool_call(tool_name, tool_input):
    if tool_name == "get_customer_info":
        return get_customer_info(tool_input["customer_id"])
    elif tool_name == "get_order_details":
        return get_order_details(tool_input["order_id"])
    elif tool_name == "cancel_order":
        return cancel_order(tool_input["order_id"])

tool_call_llm = XAI(
    api_key=XAI_API_KEY,
    model="grok-2-1212",
    tools=tool_definitions,
    function_map={
        "get_customer_info": get_customer_info,
        "get_order_details": get_order_details,
        "cancel_order": cancel_order
    }
)

answer_llm = XAI(
    api_key=XAI_API_KEY,
    model="grok-2-1212",
)

def chatbot_interaction(messages: List[Dict[str, Any]]):

    response = tool_call_llm.invoke(messages=messages, tool_choice="auto")

    if response.choices[0].message.tool_results:
        for idx, tool_result in enumerate(response.choices[0].message.tool_results):
            print(f"Tool: {tool_result.name}")
            print(f"Content: {tool_result.content}")

            messages.append(
                {
                    "role": "tool",
                    "tool_id": response.choices[0].message.tool_calls[idx].id,
                    "content": str(tool_result.content)
                }
            )

    final_response = answer_llm.invoke(messages=messages)

    return (final_response.choices[0].message.content, messages)
