import os
import sys

# So that we can do `import botfleet` in our tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import botfleet  # noqa: E402

botfleet.api_base = os.getenv("BOTFLEET_API_BASE")  # type: ignore
botfleet.api_key = os.getenv("BOTFLEET_API_KEY")  # type: ignore
