# Ugly hack to allow absolute import from the root folder
# whatever its name is. Please forgive the heresy.
import sys
import os
sys.path.insert(os.path.abspath('..'))
