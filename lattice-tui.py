import sys
from tui.app import LatticeApp

def main():
    workspace = sys.argv[1] if len(sys.argv) > 1 else "."
    app = LatticeApp(workspace)
    app.run()

if __name__ == "__main__":
    main()
