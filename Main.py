import sys

from PyQt5.QtWidgets import QApplication

from MainWindow import MyWindow
def main():
    App=QApplication(sys.argv)
    MainWindow=MyWindow()
    sys.exit(App.exec())
if __name__ == '__main__':
    main()
