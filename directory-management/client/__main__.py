import os
import sys
home_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if home_dir not in sys.path:
    sys.path.append(home_dir)

from client import Client
Client().run()
