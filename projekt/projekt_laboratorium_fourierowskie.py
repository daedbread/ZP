import sys
import numpy as np
import funkcje_fourier as ry
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from fractions import Fraction

# klasa wykresu
class PlotWidget(FigureCanvasQTAgg): 
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)

    def plot(self, x1, y1, x2 = [], y2 = [], xlabel = '', ylabel = '', t = ''):
        self.ax.clear()
        self.ax.set_title(t)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.ax.plot(x1, y1, label = 'Sygnał', alpha = 0.67)
        if len(x2) == len(y2):
            self.ax.plot(x2, y2, label = 'Sygnał po filtracji', color = 'red')
        self.ax.legend()
        self.ax.grid(True)
        self.draw()

    def stem(self, x1, y1, x2 = [], y2 = [], xlabel = '', ylabel = '', t = ''):
        self.ax.clear()
        self.ax.set_title(t)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.ax.stem(x1, y1, basefmt=" ", label = 'Częstotliwości dominujące')
        if len(x2) == len(y2):
            self.ax.stem(x2, y2, basefmt=" ", linefmt='r-', markerfmt='ro', label = 'Częstotliwości dominujące po filtracji')
        self.ax.legend()
        self.ax.grid(True)
        self.draw()

# klasa okna aplikacji
class MainWindow(QMainWindow): 
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Laboratorium Fourierowskie')

        self.signal_saved = []
        self.signal_synth = ''
        self.signal_file = ''
        self.t = ry.czas(1024, 1)
        self.const = 0
        self.noise = 0
        self.win = 'none'
        self.signal_filtered = []
        self.filter = 'none'
        self.f1 = 0
        self.f2 = 0
        self.error_message = ''
        self.label_err = QLabel()
        self.error_msg()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# LAYOUT 2 (sygnał syntetyczny)

        # tworzenie layout2 jako poziome pudełko na widgety
        layout2 = QHBoxLayout()
        
        # okno do wpisywania
        self.lineedit2 = QLineEdit()
        self.lineedit2.setPlaceholderText('Sygnał syntetyczny (np. A1, f1, phi1, A2, f2, phi2 ...)')
        self.lineedit2.textEdited.connect(self.text_edited2)

        # przyciski
        button21 = QPushButton('Dodaj sygnał')
        button21.clicked.connect(self.the_button_was_clicked21)

        button22 = QPushButton('Nadpisz sygnał')
        button22.clicked.connect(self.the_button_was_clicked22)

        # dodanie widgetów do layout2
        layout2.addWidget(self.lineedit2)
        layout2.addWidget(button21)
        layout2.addWidget(button22)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# LAYOUT 3 (sygnał z pliku)

        # wszystko analogicznie do layout2
        layout3 = QHBoxLayout()        

        self.lineedit3 = QLineEdit()
        self.lineedit3.setPlaceholderText('Sygnał z pliku (np. plik.txt)')
        self.lineedit3.textEdited.connect(self.text_edited3)

        button31 = QPushButton('Dodaj sygnał')
        button31.clicked.connect(self.the_button_was_clicked31)

        button32 = QPushButton('Nadpisz sygnał')
        button32.clicked.connect(self.the_button_was_clicked32)

        layout3.addWidget(self.lineedit3)
        layout3.addWidget(button31)
        layout3.addWidget(button32)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# LAYOUT 4 (wykresy)

        layout4 = QHBoxLayout()

        # tworzenie widgetów
        self.plot41 = PlotWidget()
        self.plot42 = PlotWidget()

        # tworzenie wykresów i wrzucanie ich od widgetów
        self.wykres()
        
        layout4.addWidget(self.plot41)
        layout4.addWidget(self.plot42)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# LAYOUT 5 (szum)

        layout5 = QHBoxLayout()

        # pole z tekstem
        label1 = QLabel('Dodaj szum:')
        font = label1.font()
        font.setPointSize(10)
        label1.setFont(font)
        label1.setFixedSize(100,20)

        # suwak z wartościami [0,100]
        slider1 = QSlider(Qt.Orientation.Horizontal)
        slider1.setMinimum(0)
        slider1.setMaximum(100)
        slider1.valueChanged.connect(self.value_changed1)

        layout5.addWidget(label1)
        layout5.addWidget(slider1)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# LAYOUT 6 (stała)

        # analogicznie do layout5
        layout6 = QHBoxLayout()

        label2 = QLabel('Dodaj stałą:')
        font = label2.font()
        font.setPointSize(10)
        label2.setFont(font)
        label2.setFixedSize(100,20)

        slider2 = QSlider(Qt.Orientation.Horizontal)
        slider2.setMinimum(0)
        slider2.setMaximum(100)
        slider2.valueChanged.connect(self.value_changed2)

        layout6.addWidget(label2)
        layout6.addWidget(slider2)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# LAYOUT 7 (okna czasowe + filtry)

        layout7 = QHBoxLayout()

        label3 = QLabel('Wybierz okno czasowe:')
        font = label3.font()
        font.setPointSize(10)
        label3.setFont(font)
        label3.setFixedWidth(140)

        # pole wyboru okna czasowego
        combobox1 = QComboBox()
        combobox1.addItems(['None', 'Hann', 'Hamming', 'Blackman', 'Tukey', 'Kaiser'])
        combobox1.setFixedWidth(200)

        # wysyłanie wartości wybranego pola jako string
        combobox1.currentTextChanged.connect(self.text_changed1)
        
        label4 = QLabel('Wybierz filtr:')
        font = label4.font()
        font.setPointSize(10)
        label4.setFont(font)
        label4.setFixedWidth(80)

        # pole wyboru filtra
        combobox2 = QComboBox()
        combobox2.addItems(['None', 'Low-pass', 'High-pass', 'Band-pass', 'Band-stop'])
        combobox2.setFixedWidth(200)

        # wysyłanie wartości wybranego pola jako string
        combobox2.currentTextChanged.connect(self.text_changed2)

        label5 = QLabel('Podaj f1:')
        font = label5.font()
        font.setPointSize(10)
        label5.setFont(font)

        # pole do wpisania f1
        self.lineedit4 = QLineEdit()
        self.lineedit4.textEdited.connect(self.text_changed4)

        label6 = QLabel('Podaj f2 (tylko do Band-pass i Band-stop):')
        font = label4.font()
        font.setPointSize(10)
        label6.setFont(font)       

        # pole do wpisywania f2 
        self.lineedit5 = QLineEdit()
        self.lineedit5.textEdited.connect(self.text_changed5)      

        layout7.addWidget(label3)
        layout7.addWidget(combobox1)
        layout7.addWidget(label4)
        layout7.addWidget(combobox2)
        layout7.addWidget(label5)
        layout7.addWidget(self.lineedit4)
        layout7.addWidget(label6)
        layout7.addWidget(self.lineedit5)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# LAYOUT 1 (pozostałe layouty)

        layout1 = QVBoxLayout()

        # dodanie pozostałym layoutów do pierwszego
        layout1.addLayout(layout2)
        layout1.addLayout(layout3)
        layout1.addLayout(layout4)
        layout1.addLayout(layout5)
        layout1.addLayout(layout6)
        layout1.addLayout(layout7)

        # okienko wyświetlające ostatni błąd
        
        font = self.label_err.font()
        font.setPointSize(10)
        self.label_err.setFont(font)

        layout1.addWidget(self.label_err)

        # ustawienie layout1 jako ten główny, który jest wyświetlany
        central_widget = QWidget()
        central_widget.setLayout(layout1)

        self.setCentralWidget(central_widget)
        self.setFixedSize(1500,650)       

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# FUNKCJE

    # zbiera aktualny tekst z pole tekstowego do zmiennej
    def text_edited2(self, text = 0): 
        self.signal_synth = text

    # dopisuje dane do tablicy
    def the_button_was_clicked21(self): 
        temp = self.signal_synth.split(',')
        try:
            for i in range(len(temp)):
                self.signal_saved.append(float(Fraction(temp[i]))) # Fraction interpretuje string 'int/int' jako ułamek np.: '1/2' => '0.5'
            self.wykres()
        except ValueError:
            self.error_message = f'Dane zostały podane w złym formacie'
            self.error_msg()        

    # nadpisuje dane w tablicy
    def the_button_was_clicked22(self): 
        self.signal_saved = []
        temp = self.signal_synth.split(',')
        try:
            for i in range(len(temp)):
                self.signal_saved.append(float(Fraction(temp[i]))) # Fraction interpretuje string 'int/int' jako ułamek np.: '1/2' => '0.5'
            self.wykres()
        except ValueError:
            self.error_message = f'Dane zostały podane w złym formacie'
            self.error_msg()

    # zbiera aktualny tekst z pole tekstowego do zmiennej
    def text_edited3(self, text = ''):
        self.signal_file = text

    # otwiera plik o danej nazwie i dopisuje dane do tablicy
    def the_button_was_clicked31(self):
        try:
            with open(self.signal_file, "r") as f:
                for linia in f:
                    temp = linia.split(',')
                for i in range(len(temp)):
                    self.signal_saved.append(float(Fraction(temp[i])))
            self.wykres()         
        except FileNotFoundError:
            self.error_message = f'Nie znaleziono pliku {self.signal_file}'
            self.error_msg()
        except ValueError:
            self.error_message = f'Plik {self.signal_file} zawiera dane w złym formacie'
            self.error_msg()

    # otwiera plik o danej nazwie i nadpisuje dane w tablicy
    def the_button_was_clicked32(self):
        self.signal_saved = []
        try:
            with open(self.signal_file, "r") as f:
                for linia in f:
                    temp = linia.split(',')
                for i in range(len(temp)):
                    self.signal_saved.append(float(Fraction(temp[i])))
            self.wykres()
        except FileNotFoundError:
            self.error_message = f'Nie znaleziono pliku {self.signal_file}'
            self.error_msg()
        except ValueError:
            self.error_message = f'Plik {self.signal_file} zawiera dane w złym formacie'
            self.error_msg()

    # rysuje wykresy i dodaje go do widgetów w layout4, domyślnie (gdy nie ma podanych żadnych danych) rysuje wykres f(x) = 0 + szum + stała
    def wykres(self):
        if len(self.signal_saved) == 0:
            self.test = ry.create_sig(*[0,0,0], t=self.t, const=self.const, noise_lvl=self.noise)
        else:
            self.test = ry.create_sig(*self.signal_saved, t=self.t, const=self.const, noise_lvl=self.noise)

        # wykres A(t)
        self.signal_filtered = ry.filtr(self.test, self.f1, self.f2, self.filter)
        self.plot41.plot(self.t, self.test, self.t, self.signal_filtered, 'Czas [s]', 'Amplituda', 'Charakterystyka czasowa')

        # wykres A(f)
        self.amp, self.dod, self.faz = ry.fourier(self.test*ry.okno(self.test, self.win))
        self.amp2, self.dod2, self.faz2 = ry.fourier(self.signal_filtered*ry.okno(self.signal_filtered, self.win))
        self.plot42.stem(self.dod, self.amp, self.dod2, self.amp2, 'Częstotliwość [Hz]', 'Amplituda', 'Charakterystyka częstotliwościowa')

        self.error_message = ''
        self.error_msg()  

    # zbiera wartość szumu z suwaka i przeskalowuje z [0,100] => [0,1]
    def value_changed1(self, value):
        self.noise = value/100
        if self.error_message == '':
            self.wykres()

    # zbiera wartość stałej z suwaka i przeskalowuje z [0,100] => [0,10]
    def value_changed2(self, value):
        self.const = value/10
        if self.error_message == '':
            self.wykres()

    # zapisanie wybranej wartości okna jako string
    def text_changed1(self, text): 
        self.win = text.lower()
        if self.error_message == '':
            self.wykres()

    # zapisanie wybranej wartości filtra jako string
    def text_changed2(self, text): 
        self.filter = text.lower().replace('-', '')
        if self.error_message == '':
            self.wykres()

    # zbiera wartość f1
    def text_changed4(self, text):
        if len(text) == 0:
            text = 0
        try:
            self.f1 = float(text)
            if self.f1 >= 0:
                self.wykres()
            else:
                self.error_message = 'Częstotliwość musi być >= 0'
                self.error_msg()
        except ValueError:
            self.error_message = 'Niepoprawny format częstotliwości'
            self.error_msg()        

    # zbiera wartość f2
    def text_changed5(self, text):
        if len(text) == 0:
            text = 0
        try:
            self.f2 = float(text)
            if self.f2 >= 0:
                self.wykres()
            else:
                self.error_message = 'Częstotliwość musi być >= 0'
                self.error_msg()
        except ValueError:
            self.error_message = 'Niepoprawny format częstotliwości'
            self.error_msg()   

    def error_msg(self):
        self.label_err.setText(f'Błąd: {self.error_message}')

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()