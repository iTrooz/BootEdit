import sys
import signal

from bootedit.logic.application import ApplicationLogic

def main():
    # Allow Ctrl+C
    signal.signal(signal.SIGINT, signal.SIG_DFL)
 
    app = ApplicationLogic(sys.argv)
    app.setStyle("fusion")
    app.init()
    sys.exit(app.run())

if __name__ == '__main__':
    main()
