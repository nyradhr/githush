import re
from githush.config import load_config 

#paths = ["/home/nyradhr/githush/.venv/lib/python3.12/site-packages/mypyc/irbuild/builder.py", "/home/nyradhr/githush/.venv/lib/python3.12/site-packages/mypyc/irbuild/ll_builder.py"]
path = "/home/nyradhr/githush/.venv/lib/python3.12/site-packages/mypyc/irbuild/ll_builder.py"
#pattern = r"(?:^|[\\/])\.[^\\/]+(?:[\\/][^\\/]+)*"
#patterns = [r"(?:^|[\\/])\.[^\\/]+(?:[\\/][^\\/]+)*", r"(?:^|\/|\\)(?:node_modules|vendor|githush|tests)(\/|\\)"]
config = load_config(None)
exclude_extensions = config.get("exclude_extensions", [])
exclude_paths = config.get("exclude_paths", [])
print(any(re.search(pattern, path) for pattern in exclude_paths))