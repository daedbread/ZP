# Wymagane biblioteki:

    sys, numpy, math, PySide6.QtCore, PySide6.QtWidgets, matplotlib, fractions, scipy.signal

# Uruchamianie programu:

Program można uruchomić z terminala VSCode. Żeby program uruchomił się poprawnie pliki `projekt_laboratorium_fourierowskie.py` i `funkcje_fourier.py` muszą znajdować się w tym samym folderze. 

# Zaimplementowane funkcje:

Sygnał syntetyczny można dodać wpisując dane w formacie `amplituda, częstotliwość, faza` w pierwszym polu tekstowym. Można podać wielokrotność tego formatu np. `A1,f1,p1,A2,f2,p2`. Podane fazy są mnożone przez $\pi$. Wartości ułamkowe można wpisać w postaci ułamka dziesiętnego lub zwykłego (dzięki funkcji z biblioteki `fractions`). Na przykład wpisanie `1/3,4,1,5,1,0` jest równoważne funkcji `f(t) = (1/3) * sin(4 * 2 $\pi$ * t + 1 * $\pi$) + 5 * sin(1 * 2 $\pi$ * t + 0 * $\pi$)`.

Żeby wczytać pkili do programu, te pliki muszą znajdować się w tym samym folderze co folder z programem. Dane w pliku muszą być w formacie 2 kolumn: 1-sza z czasem, 2-ga z amplitudą sygnału.

Syganły syntetyczne i pobrane z pliku można do siebie dodawać, lub nadpisywać nowym sygnałem.

Program umożliwia dodania składowej stałej oraz białego szumu za pomocą suwaków, a także wyboru okna czasowego i filtra z listy. Filtry `low-pass` i `highpass` wymagają podania tylko wartości 1-szej częstotliwości (domyślnie ustawionej na 0), a filty `band-pass` i `band-stop` wymagają też podania 2-giej częstotliwości. Filty `band-pass` i `band-stop` filtrują dane w zakresie od mniejszej podanej częstotliwości do większej.

W przypadku wpisania błędnych danych program wyświetla odpowiedni błąd na dole okna.

Program wyświetla wczytany sygnał przed i po filtracji, a także Transformatę Fouriera obydwu z nich.

# Podział pracy:

## Ryszard Budzisz:

Tworzenie sygnału syntetycznego

Wczytywanie i zapis do pliku

Analiza Fouriera i wyświetlanie wykresów

## Jakub Machlarz:

GUI

Połączenie GUI z surowym kodem

Napisanie pliku readme

## Mateusz Knajp:

Filtry sygnału

Pomoc w pisaniu pliku readme