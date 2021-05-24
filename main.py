from store.wsgi import application
import os
import sys
# Add vendor directory to module search path
parent_dir = os.path.abspath(os.path.dirname(__file__))
vendor_dir = os.path.join(parent_dir, 'vendor')
sys.path.append(vendor_dir)
# Add Environment ariables
os.environ['DEBUG'] = 'False'

app = application