
import sys
import os

# Add our user-python directory to path
user_python = os.path.join(os.path.dirname(__file__), '.python-user', 'Python314', 'site-packages')
sys.path.insert(0, user_python)

# Now import streamlit and run
from streamlit.web import cli as stcli

if __name__ == '__main__':
    sys.argv = ['streamlit', 'run', 'ENHANCED_PANEL.py', '--server.headless', 'true', '--server.port', '8501']
    stcli.main()
