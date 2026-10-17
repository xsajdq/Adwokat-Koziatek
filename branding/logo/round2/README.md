# Runda 2: klasyczny, elegancki, prosty

## Research (10.2026)
- **Zieleń adwokatury.** Lamówki i żaboty tóg adwokackich są zielone. U radców prawnych są niebieskie, u sędziów fioletowe, u prokuratorów czerwone. Źródło: bezprawnik.pl/trzy-kolory-zabotow, rp.pl.
- **Znak „Adwokatura Polska”** (stylizowany orzeł z literami a i p, uchwała NRA 49/2009, regulamin 624/2025). Adwokat może go używać dobrowolnie. Dlatego nie używamy orła, żeby nie mylić własnego logo ze znakiem samorządu.
- **Kategoria:** waga Temidy, kolumny, młotek, granat ze złotem, szeryfowe monogramy. Dobre praktyki z przeglądów logo kancelarii (manypixels.co): monogram dla praktyki jednoosobowej, krój szeryfowy dla tradycji, ograniczona paleta (zieleń, granat, złoto), czytelność w małym rozmiarze, unikanie gołej wagi.
- **Imię i nazwisko.** W rejestrach występuje adw. Natalia Koziatek (Świnoujście). Do potwierdzenia, czy chodzi o tę kancelarię i czy imię ma być w logo.
- **Biblioteka skilla:** nie ma kategorii prawniczej. Dopracowane emblematy i litery: markdown, mozilla, pagekit, precursor. Znaleziony stylelint (przód smokingu) pokazuje, że „toga” z rundy 1 była bliska istniejącemu znakowi.

## Lista pomysłów (8–12 jednozdaniowych koncepcji) i ocena
Skala ocen 1–5 w kolejności: idea / wyróżnienie / prostota / trafność / mały rozmiar.

| # | Koncepcja | Ocena | |
|---|---|---|---|
| 1 | Kapitała K z wydłużoną nogą (subtelny róg, nawiązanie do nazwiska) | 4/4/5/4/5 | → wspólny detal |
| 2 | K w otwartym portalu na progu (wejście do kancelarii) | 4/4/4/4/3 | → A |
| 3 | Pieczęć z napisem w otoku i K (tajemnica adwokacka) | 4/3/3/5/2 | → B (z wersją małą) |
| 4 | Napis KOZIATEK z zieloną lamówką togi | 4/4/5/5/4 | → C |
| 5 | Ligatura AK ze wspólną diagonalą | 3/3/3/3/3 | |
| 6 | Paragraf § z liter K | 2/2/2/3/2 | |
| 7 | Kolumna jako pień K (runda 1) | 3/2/4/3/3 | |
| 8 | K w romb jak cecha złotnicza | 3/3/4/2/4 | |
| 9 | Napis Koziatek z ozdobną nogą K podkreślającą wyraz | 4/4/3/3/2 | |
| 10 | Kartusz z inicjałem i datą założenia | 3/2/3/4/2 | |

## Testy
- `svg_audit.py`: symbole A i C oraz wersje małe mają wynik 90/100. Pieczęć ma 75/100, bo napis w otoku dodaje ponad 800 punktów i drobne detale. Do małych rozmiarów służy `b-small.svg`.
- Ostrzeżenie „near-miss angle 118.7°” dotyczy krawędzi schowanej pod ramieniem K, której nie widać.
- `preview_sheet.py` (`preview.html`):
  - pieczęć jest nieczytelna przy 16–32 px, więc używamy wersji małej;
  - cienkie linie portalu słabną przy 16 px, więc używamy `a-small.svg` (samo K);
  - odbicie i obrót o 180° nie dają niechcianych skojarzeń;
  - ryzyko w A: łuk może kojarzyć się z nagrobkiem. Złagodzone otwarciem u dołu i progiem.
- Litery to krzywe. Krój Cinzel (licencja SIL OFL, wolno go użyć w logo), litera K narysowana od podstaw. Generator: `tools/build_r2.py`.
