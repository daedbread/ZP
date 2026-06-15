# Projekt: Mini-laboratorium fourierowskie

## Cel projektu

Celem projektu jest przygotowanie aplikacji pozwalającej na interaktywną analizę sygnałów jednowymiarowych przy pomocy transformaty Fouriera. Program powinien umożliwiać zarówno generowanie sygnałów syntetycznych, jak i wczytywanie sygnałów z plików. Użytkownik powinien móc obserwować sygnał w dziedzinie czasu, jego widmo w dziedzinie częstotliwości oraz efekty prostego przetwarzania sygnału.

Projekt powinien mieć graficzny interfejs użytkownika. Preferowane rozwiązanie to aplikacja desktopowa przygotowana z użyciem `PySide6`, z wykresami realizowanymi przy pomocy `matplotlib` albo `pyqtgraph`.

## Przykładowe biblioteki

W projekcie należy wykorzystać biblioteki wykraczające poza standardową bibliotekę Pythona. Przykładowy zestaw:

- `numpy` - reprezentacja sygnałów, obliczenia numeryczne, transformata Fouriera;
- `scipy.signal` - generowanie i przetwarzanie sygnałów, okna, filtry, spektrogramy;
- `matplotlib` albo `pyqtgraph` - wykresy;
- `PySide6` - graficzny interfejs użytkownika;
- `sounddevice` / `soundfile` - odtwarzanie lub zapis dźwięku;
- `librosa` - opcjonalnie, bardziej zaawansowana analiza sygnałów audio.

Nie trzeba używać wszystkich wymienionych bibliotek. Projekt powinien jednak wykorzystywać co najmniej jedną bibliotekę związaną z GUI oraz co najmniej jedną bibliotekę związaną z analizą lub przetwarzaniem sygnałów.

## Zakres projektu

Aplikacja powinna umożliwiać pracę z sygnałami jednowymiarowymi. W tym projekcie nie zajmujemy się obrazami 2D.

Program powinien obsługiwać dwa źródła sygnału:

1. generowanie sygnału syntetycznego,
2. wczytywanie sygnału z pliku.

## Generowanie sygnałów syntetycznych

Aplikacja powinna pozwalać użytkownikowi na wygenerowanie sygnału złożonego z kilku prostych składników. Przykładowo użytkownik powinien móc utworzyć sygnał będący sumą kilku sinusoid:

```text
x(t) = A_1 sin(2 pi f_1 t + phi_1) + A_2 sin(2 pi f_2 t + phi_2) + ...
```

Parametry możliwe do ustawienia:

- czas trwania sygnału;
- częstotliwość próbkowania;
- liczba składowych sinusoidalnych;
- amplitudy składowych;
- częstotliwości składowych;
- fazy początkowe;
- składowa stała;
- poziom szumu;
- typ szumu, np. biały szum gaussowski;
- opcjonalnie: sygnał prostokątny, piłokształtny, impuls, paczka falowa albo chirp.

W wersji podstawowej wystarczy możliwość wygenerowania sumy kilku sinusoid, dodania szumu oraz dodania składowej stałej.

## Wczytywanie sygnałów

Aplikacja powinna umożliwiać wczytanie sygnału z pliku. Minimalnie wystarczy obsługa pliku tekstowego lub CSV zawierającego próbki sygnału.

Przykładowe dopuszczalne formaty:

- jedna kolumna: wartości sygnału;
- dwie kolumny: czas i wartość sygnału;
- opcjonalnie plik `.wav`, jeżeli zespół zdecyduje się na pracę z sygnałami audio.

Po wczytaniu pliku program powinien pokazać podstawowe informacje o sygnale, np.:

- liczba próbek;
- czas trwania;
- częstotliwość próbkowania, jeżeli jest znana;
- wartość średnia;
- wartość minimalna i maksymalna;
- odchylenie standardowe.


## Analiza Fouriera

Program powinien obliczać dyskretną transformatę Fouriera sygnału i prezentować wyniki w czytelnej formie.

Aplikacja powinna pokazywać co najmniej:

- sygnał w dziedzinie czasu;
- widmo amplitudowe;
- opcjonalnie widmo fazowe;
- dominujące częstotliwości;
- wpływ składowej stałej na widmo;
- wpływ szumu na widmo.

W przypadku sygnałów rzeczywistych warto używać `numpy.fft.rfft` oraz `numpy.fft.rfftfreq`, aby wyświetlać tylko dodatnie częstotliwości.

## Okna czasowe

Aplikacja powinna umożliwiać zastosowanie wybranego okna przed obliczeniem transformaty Fouriera.

Wymagane okna:

- brak okna, czyli okno prostokątne;
- Hann;
- Hamming.

Opcjonalnie:

- Blackman;
- Tukey;
- Kaiser.

Użytkownik powinien móc porównać, jak wybór okna wpływa na widmo sygnału.

## Filtrowanie częstotliwości

Aplikacja powinna pozwalać na proste filtrowanie sygnału. Minimalnie należy zaimplementować jeden typ filtru, np. filtr dolnoprzepustowy.

Przykładowe filtry:

- dolnoprzepustowy;
- górnoprzepustowy;
- pasmowoprzepustowy;
- pasmowozaporowy.

Filtr może być zrealizowany na dwa sposoby:

1. przez modyfikację widma FFT i wykonanie transformaty odwrotnej,
2. przez użycie funkcji z `scipy.signal`.

Po filtracji program powinien pokazywać:

- sygnał przed filtracją;
- sygnał po filtracji;
- widmo przed filtracją;
- widmo po filtracji.

## Spektrogram

W wersji rozszerzonej aplikacja może pokazywać spektrogram sygnału, czyli zmianę widma w czasie.

Jest to szczególnie przydatne dla sygnałów niestacjonarnych, np.:

- chirp, czyli sygnał o zmieniającej się częstotliwości;
- krótki impuls;
- paczka falowa;
- sygnał audio.

Do wykonania spektrogramu można użyć `scipy.signal.spectrogram`.

## Interfejs użytkownika

Aplikacja powinna mieć graficzny interfejs użytkownika pozwalający na wygodną zmianę parametrów i obserwację wyników.

Minimalne elementy GUI:

- wybór źródła sygnału: sygnał syntetyczny albo plik;
- pola lub suwaki do ustawiania parametrów sygnału;
- przycisk generowania/wczytywania sygnału;
- wybór okna czasowego;
- wybór typu filtru i jego parametrów;
- przycisk wykonania analizy;
- wykres sygnału w czasie;
- wykres widma amplitudowego;
- wykres sygnału po filtracji;
- komunikaty o błędach, np. niepoprawny format pliku.

Interfejs nie musi być bardzo rozbudowany graficznie, ale powinien być czytelny i używalny.

## Wymagania podstawowe

Projekt powinien zawierać:

1. Graficzny interfejs użytkownika.
2. Możliwość wygenerowania sygnału syntetycznego.
3. Możliwość dodania do sygnału szumu.
4. Możliwość dodania składowej stałej.
5. Możliwość wczytania sygnału z pliku.
6. Wykres sygnału w dziedzinie czasu.
7. Obliczenie transformaty Fouriera.
8. Wykres widma amplitudowego.
9. Możliwość zastosowania co najmniej dwóch różnych okien czasowych.
10. Proste filtrowanie częstotliwości.
11. Porównanie sygnału przed i po filtracji.
12. Czytelny podział kodu na moduły.
13. Krótką instrukcję uruchomienia programu.

## Wymagania rozszerzone

Dodatkowe elementy, które mogą podnieść ocenę projektu:

- obsługa plików `.wav`;
- odtwarzanie sygnału audio;
- zapis przefiltrowanego sygnału;
- spektrogram;
- porównanie kilku sygnałów na jednym wykresie;
- automatyczne wykrywanie dominujących częstotliwości;
- widmo fazowe;
- eksport wyników do CSV;
- zapisywanie i wczytywanie konfiguracji analizy;
- testy jednostkowe dla funkcji obliczeniowych;
- użycie `librosa` do bardziej zaawansowanej analizy audio.

## Uwagi implementacyjne

W projekcie warto oddzielić logikę obliczeniową od interfejsu graficznego. Funkcje generujące sygnały, liczące FFT i wykonujące filtrację powinny dać się uruchomić niezależnie od GUI. Dzięki temu łatwiej je testować i łatwiej podzielić pracę w zespole.

Przykładowo funkcja licząca widmo nie powinna bezpośrednio rysować wykresu. Powinna zwracać dane, które potem zostaną narysowane przez część odpowiedzialną za GUI.

## Efekt końcowy

Efektem końcowym projektu powinna być działająca aplikacja, która pozwala użytkownikowi wygenerować lub wczytać sygnał, obejrzeć go w dziedzinie czasu, przeanalizować jego widmo Fouriera, zastosować proste przetwarzanie częstotliwościowe i zobaczyć wynik.

Projekt powinien być oddany razem z krótkim plikiem `README.md`, w którym należy opisać:

- jak zainstalować wymagane biblioteki;
- jak uruchomić program;
- jakie funkcje zostały zaimplementowane;
- jak podzielono pracę w zespole;
- przykładowe dane wejściowe lub scenariusze demonstracyjne.
