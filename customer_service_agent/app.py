from fasthtml.common import *
from customer_service_agent import chatbot_interaction

hdrs = (
    Script(src="https://cdn.tailwindcss.com"),
    MarkdownJS()
)
app = FastHTML(hdrs=hdrs, cls="p-4 max-w-lg mx-auto")

def ChatMessage(msg: str, user: bool = False):
    bubble_class = "bg-blue-500 text-white" if user else "bg-gray-200 text-gray-800"
    chat_class = "justify-end" if user else "justify-start"
    return Div(
        Div(
            P(msg, cls="marked"),
            cls=f"max-w-[70%] p-3 rounded-lg {bubble_class}"
        ),
        cls=f"flex {chat_class} mb-4"
    )

def ChatInput():
    return Input(
        name="msg",
        id="msg-input",
        placeholder="Type a message...",
        cls="w-full p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500",
        hx_swap_oob='true'
    )


@app.get
def index():
    page = Form(
        hx_post="/send",
        hx_target="#chatlist",
        hx_swap="beforeend"
    )(
        Div(id="chatlist", cls="h-[73vh] overflow-y-auto mb-4"),
        Div(cls="flex space-x-2")(
            ChatInput(),
            Button("Send", cls="p-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none")
        )
    )
    return Titled('Customer Service Bot', page)

@app.post
def send(msg: str, messages: List[str] = None):
    if not messages:
        messages = []

    messages.append(
        {
            "role": "user",
            "content": msg.rstrip()
        }
    )

    r, messages = chatbot_interaction(messages)
    return (
        ChatMessage(msg, True),
        ChatMessage(r.rstrip(), False),
        ChatInput()
    )
