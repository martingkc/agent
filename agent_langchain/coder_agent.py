from typing import Any, Dict, Union
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
import coder_config
import requests
import yaml
from difflib import unified_diff
from langchain_core.tools import tool

@tool
def diff(source: str, destination: str) -> str:
    """
    Return a unified diff between two text strings.
    """
    return "\n".join(
        unified_diff(
            source.splitlines(),
            destination.splitlines(),
            fromfile="original",
            tofile="updated",
            lineterm="",
        )
    )


@tool
def write_file(file_path: str, content: str):
    """Writes content to a file."""
    with open(file_path, "w") as f:
        f.write(content)


@tool
def read_file(file_path: str):
    """Reads the contents of a file. Pass as argument the path to the file that you want to read."""
    with open(file_path, "r") as f:
        return f.read()


@tool
def get_api_spec() -> str:
    """
    Fetches a list of your available tools on the API.
    If the tools that you need are not available you can create them using the create_tools function.
    """
    base_url = "http://localhost:5000/tools"

    try:
        response = requests.get(base_url)
        openapi_spec = response.json()
    except requests.RequestException as e:
        return f"Error fetching OpenAPI specification: {e}"

    return yaml.dump(openapi_spec, sort_keys=False)



prompt = """
**You are a helpful assistant that can execute only read_file(), write_file(), and diff operations.**
- Your task is to add only the necessary functions and define a new endpoint within the existing code in a Flask server.
- First call `read_file("../app/tools/routes/routes.py")` to fetch current contents, then use diff to preview any changes.
- You must *not* replace the entire file; insert or append only the minimal code required for the new endpoint and also append the openAPI description of the endpoint to `openapi_spec`.
- After crafting edits, call `diff(**{{'source': original, 'destination': updated}})` to verify minimal changes.
- Finally, call `write_file("../app/tools/routes/routes.py", updated_content)`.
- Add the OpenAPI spec under `openapi_spec` and any needed imports in `../app/tools/routes/imports.py` using patch-based edits.
- Only use Flask for routing.
- After having saved the changes check if the changes you made have caused any errors by running `docker compose logs api`

`../app/tools/routes/imports.py`
```python
{imports_py}
```
`../app/tools/routes/routes.py`
``` python
{routes_py}
```
"""

coder_tools = [write_file, read_file, get_api_spec, diff]

coder_agent = create_react_agent(
    "openai:gpt-4o-mini",
    coder_tools,
    prompt=prompt.format(
        imports_py=read_file("../app/tools/routes/imports.py"),
        routes_py=read_file("../app/tools/routes/routes.py"),
    ),
)


@tool
def create_tools(user_msg: str) -> None:
    """
    Creates tools and endpoints based on user instructions, and logs diffs before writing.
    Always fetch the updated OpenAPI spec afterwards.
    """
    input_message = [
        {"role": "user", "content": user_msg},
    ]

    for step in coder_agent.stream(
        {"messages": input_message},
        stream_mode="values",
    ):
        if step.get("tool_calls"):
            for tc in step["tool_calls"]:
                print(f">>> tool call: {tc}")
        step["messages"][-1].pretty_print()
    return