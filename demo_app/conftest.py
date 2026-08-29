import os
import sys
import importlib.util

# Ensure hackathon root is in the Python path
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, base_dir)

# Map the demo_app directory to demo_app module name for imports to work
spec = importlib.util.spec_from_file_location("demo_app", os.path.join(base_dir, "demo_app", "__init__.py"))
demo_app = importlib.util.module_from_spec(spec)
sys.modules["demo_app"] = demo_app
spec.loader.exec_module(demo_app)

