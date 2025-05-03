import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from interfaz.interfaz import InterfazApp

if __name__ == "__main__":
    app = InterfazApp()
