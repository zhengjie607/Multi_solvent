from PyQt5.QtWidgets import QApplication
import sys
from main import myform

app=QApplication(sys.argv)
form=myform()
form.show()
app.exec_()
sys.exit()