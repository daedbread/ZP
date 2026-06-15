# Zadania wprowadzające do programowania obiektowego w Pythonie

Poniżej znajduje się zestaw zadań, których celem jest stopniowe wprowadzenie do programowania obiektowego w Pythonie. Zadania obejmują tworzenie własnych klas, użycie `dataclass`, metody specjalne, obiekty funkcyjne, dziedziczenie oraz wykorzystanie `super()`.

---

## Zadanie 1. Licznik laboratoryjny - pierwsza własna klasa

### Cel
Pierwsze spotkanie z klasą, obiektami, atrybutami i metodami.

### Treść
Napisz klasę `Counter`, która reprezentuje prosty licznik całkowity. Obiekt tej klasy powinien:

- przechowywać aktualną wartość licznika,
- pozwalać zwiększyć wartość o 1,
- pozwalać zmniejszyć wartość o 1,
- pozwalać wyzerować licznik,
- pozwalać odczytać aktualną wartość.

Na końcu napisz krótki program testujący, który tworzy licznik i wykonuje na nim kilka operacji.

### Można się nauczyć
- `class`
- `__init__`
- `self`
- metody instancyjne

---

## Zadanie 2. Punkt pomiarowy - pierwsza `dataclass`

### Cel
Pokazać, do czego służy `dataclass` i czym różni się od zwykłej klasy.

### Treść
Napisz `dataclass` o nazwie `Measurement`, która przechowuje informacje o pojedynczym pomiarze:

- czas pomiaru,
- wartość,
- jednostkę.

Następnie napisz program, który:

- tworzy kilka obiektów tej klasy,
- przechowuje je w liście,
- wypisuje wszystkie pomiary,
- znajduje pomiar o największej wartości.

### Można się nauczyć
- dekorator `@dataclass`
- obiekt jako prosty rekord danych
- różnica między klasą „aktywną” a klasą służącą głównie do przechowywania danych


---

## Zadanie 3. Wektor 2D - metody specjalne i czytelny zapis obiektu

### Cel
Dodać sensowne zachowanie obiektu i pokazać przeciążanie operatorów.

### Treść
Napisz klasę `Vector2D`, która przechowuje współrzędne `x` i `y`.

Klasa powinna umożliwiać:

- utworzenie wektora o zadanych współrzędnych,
- wypisanie go w czytelnej postaci,
- dodawanie dwóch wektorów operatorem `+`,
- obliczenie długości wektora,
- mnożenie wektora przez liczbę.

### Można się nauczyć
- `__str__` lub `__repr__`
- `__add__`
- `__mul__` (hint: sprawdźcie też `__rmul__`)
- sens metod specjalnych

### Rozszerzenie
Dodać metodę obliczającą iloczyn skalarny dwóch wektorów.

---

## Zadanie 4. Pojemnik na wyniki pomiarów - indeksowanie i iteracja

### Cel
Pokazać, że własny obiekt może działać jak kolekcja.

### Treść
Napisz klasę `MeasurementSeries`, która przechowuje serię wyników pomiarowych.

Klasa powinna:

- przyjmować listę liczb przy tworzeniu obiektu,
- pozwalać pobierać elementy przez `[]`,
- pozwalać zmieniać elementy przez `[]`,
- zwracać liczbę elementów przez `len(...)`,
- umożliwiać iterację w pętli `for`,
- mieć metodę liczącą średnią arytmetyczną.

### Można się nauczyć
- `__getitem__`
- `__setitem__`
- `__len__`
- `__iter__`

### Rozszerzenie
Dodać metodę zwracającą największy i najmniejszy pomiar.

---

## Zadanie 5. Funkcja wielomianowa - obiekt funkcyjny

### Cel
Implementacja `__call__`.

### Treść
Napisz klasę `Polynomial`, która reprezentuje wielomian jednej zmiennej. Współczynniki wielomianu powinny być przekazywane przy tworzeniu obiektu w postaci listy.

Przykład: lista `[1, 0, 3]` oznacza wielomian:

$$1 + 0x + 3x^2$$

Klasa powinna:

- przechowywać współczynniki,
- pozwalać wypisać wielomian w czytelnej postaci,
- umożliwiać wywołanie obiektu jak funkcji, np. `p(2)`,
- mieć metodę zwracającą stopień wielomianu.

### Można się nauczyć
- `__call__`
- obiekt funkcyjny

### Rozszerzenie
Dodać metodę zwracającą wartość pochodnej wielomianu w punkcie.

---

## Zadanie 6. Konto punktowe gracza - dziedziczenie i `super()`

### Cel
Pierwsze sensowne dziedziczenie.

### Treść
Napisz klasę bazową `Account`, która reprezentuje konto użytkownika. Powinna przechowywać nazwę użytkownika i liczbę punktów.

Klasa powinna mieć metody:
- dodawania punktów,
- odejmowania punktów,
- wypisywania informacji o koncie.

Następnie napisz klasę `PremiumAccount`, dziedziczącą po `Account`, która dodatkowo:

- przechowuje współczynnik premii,
- przy dodawaniu punktów dolicza bonus,
- korzysta z `super()` tam, gdzie ma to sens.

### Można się nauczyć
- dziedziczenie
- nadpisywanie metod
- `super()`

### Rozszerzenie
Dodać trzeci typ konta, np. `PenaltyAccount`, które przy każdej operacji pobiera niewielką opłatę w punktach.

---

## Zadanie 7. Zwierzęta na planszy - polimorfizm

### Cel
Pokazać wspólny interfejs i różne implementacje.

### Treść
Napisz klasę bazową `Animal`, która przechowuje imię oraz pozycję zwierzęcia na planszy (`x`, `y`).

Klasa powinna mieć metody:
- `move()`
- `sound()`
- `info()`

Następnie napisz co najmniej dwie klasy dziedziczące, np.:
- `Dog`
- `Bird`

Każda z nich powinna:
- inaczej implementować metodę `sound()`,
- inaczej implementować metodę `move()`,
- korzystać z konstruktora klasy bazowej przez `super()`.

Na końcu napisz program, który tworzy listę różnych zwierząt i wywołuje na nich te same metody.

### Można się nauczyć
- polimorfizm
- wspólny interfejs
- praktyczny sens klasy bazowej

### Rozszerzenie
Niech klasa `Animal` będzie zaimplementowana jako abstrakcyjna.