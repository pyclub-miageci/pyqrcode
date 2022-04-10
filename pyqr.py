"""
auteur : ...
nom du programme : geerateur de qr code
description : programme permettant de generé un qr code contenat le nom et le matricule renseigné
date : 07/02/2021
"""

#importation
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import cv2
import sys,qrcode


#classe principale
class interface(QDialog):
    def __init__(self):
        super(interface, self).__init__()
        loadUi("interface.ui", self) #charge notre interface
        self.txt.clicked.connect(self.saveClicked)
        #cacher le label d'erreur et le label de succes
        self.error.hide()
        self.txt.hide()

        #afficher une image de qr code dans le label qr
        pixmap=QtGui.QPixmap("img/qr.png")
        self.qr.setStyleSheet("border-image: url(img/qr.png);")
        
        #lancer la fonction de generation de qr code lorsque le text change dans le champ name ou/et le champ matricue
        self.name.textChanged.connect(self.qr_code)
        self.id_card_2.textChanged.connect(self.qr_code)
        self.id_card_3.textChanged.connect(self.qr_code)
        self.save_dir = "img/lolipop.png" # lien ou sera stocké notre image qr generé
        self.color = "black"
        self.vert.clicked.connect(lambda : self.setColor("green"))
        self.jaune.clicked.connect(lambda : self.setColor("yellow"))
        self.bleu.clicked.connect(lambda : self.setColor("blue"))
        #initialisation du qr code
        
     
    def setColor(self, color):
        self.color = color
        self.qr_code()
    def add_color_and_save_qrcode(self, qr_code):
        try:
            #controle pour generé l'image du qr code avec des couleur differente 
            img = qr_code.make_image(fill_color=str(self.color), back_color="white")

            
            img.save(self.save_dir)
                #affichage de l'image generé dans le label qr
            pixmap=QtGui.QPixmap(self.save_dir) 
            self.qr.setStyleSheet("border-image: url("+self.save_dir+");")
        except Exception as e:
            print(e)
    def qr_code(self):
        """
           fonction qui genère un qr code en temps réel en fonction du matricule et du nom renseigné
        """
        try :
            name = self.name.text() #on recupere la valeur du champ name
            #matricule = self.id_card.text() #on recupere la valeur du champ matricule
            numero = self.id_card_2.text() #on recupere la valeur du champ numéro
            mail = self.id_card_3.text()
        
            if(len(name)>0 and len(numero)>0 and len(mail)>0): #verifie si les 2 champs ne sont pas vide
                if(len(numero)==10):
                    """
                    if self.checkBox.isChecked() == True:
                        b="blue"
                    elif self.checkBox_2.isChecked() == True:
                        b="yellow"
                    elif self.checkBox_3.isChecked() == True:
                        b="green"
                    else:
                        b="black"
                    """

                    #creation du qr code
                    qr_code = qrcode.QRCode(     
                        version=1,     
                        error_correction=qrcode.constants.ERROR_CORRECT_H,     
                        box_size=5,     
                        border=4, )
                    qr_code.add_data("Nom : "+name+"\nNuméro : "+numero+"\nMail : "+mail)
                    qr_code.make(fit=True)
                    
                    self.error.hide()
                    self.add_color_and_save_qrcode(qr_code)
                        
                        
                    self.txt.show()
                else :
                    self.error.show()
                    self.txt.hide()
            else:
                self.txt.hide()
        except Exception as e :
                print(e)
    
    def saveClicked(self):
        try:
            fname, filter = QFileDialog.getSaveFileName(self, 'Save File', 'C:\\', "Image Files (*.jpg)")
            if fname:
                image = cv2.imread(self.save_dir)
                
                cv2.imwrite(fname,image)
            else:
                print("error")
        except Exception as e:
            print(e)
            
        
if __name__ == "__main__":
    #lancer du programme
    app = QApplication(sys.argv)
    mainwindow = interface()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    widget.setFixedHeight(330)
    widget.setFixedWidth(527)
    widget.show()
app.exec_()
