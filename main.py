import sys
import signal

from application import MyApplication

def main():
    # Allow Ctrl+C
    signal.signal(signal.SIGINT, signal.SIG_DFL)
 
    app = MyApplication(sys.argv)
    app.init()
    sys.exit(app.run())

if __name__ == '__main__':
    main()
