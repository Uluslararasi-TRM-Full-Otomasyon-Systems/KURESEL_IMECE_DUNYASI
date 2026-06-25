
import sys
import os

# Add the streamlit_env directory to the path
env_path = os.path.join(os.path.dirname(__file__), 'streamlit_env')
sys.path.insert(0, env_path)

# Now import and run streamlit
from streamlit.web import cli as stcli

if __name__ == '__main__':
    sys.argv = ['streamlit', 'run', 'ENHANCED_PANEL.py', '--server.headless', 'true', '--server.port', '8501']
    stcli.main()
