import sys
import signal

from bootedit.main.ui import run_ui

def main():
    # Allow Ctrl+C
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    sys.exit(run_ui())

if __name__ == '__main__':
    main()
