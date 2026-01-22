import os
import sys

# Add the project directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
