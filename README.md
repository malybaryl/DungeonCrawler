----------------------------------------------ENGLISH----------------------------------------------
# Dungeon Crawler

Dungeon Crawler is a simple game created in Python using the Pygame library. The game offers a classic dungeon crawl system where players explore dungeons, battle enemies, collect items, and gain experience.

## Features:

- **Player Character**: Control a character navigating through dungeons, utilizing ranged weapons.
- **Enemies**: The game includes various enemies, including orcs and powerful bosses.
- **Combat**: Combat system involves shooting enemies with a bow and avoiding enemy attacks.
- **Item Collection**: Players can acquire gold, health potions, and other items.
- **HUD (Heads-Up Display)**: Displays information about health, gold, and other player stats.
- **Main Menu**: Simple main menu handling, allowing for starting a new game and adjusting settings.
- **Saving Settings**: Your settings in the game will be saved even if you turn off the game.

## How to Run:

1. Install Python and Pygame.
2. Run the `main.py` file.

## Configuration:

You can customize game settings, such as screen resolution, sound, or fullscreen mode, in the game settings or by editing the `config/config.txt` file.

## Project Structure:

- **scripts**: Folder containing modules and classes, such as character, weapon, background, enemies, HUD, items, music, and menu.
- **levels**: Folder containing CSV files with level data.
- **assets**: Folder containing graphic and audio files used in the game.

## More About Scripts:

- **background.py**: Handles the background in the game.
- **changeResolution.py**: Handles resolution in the game.
- **character.py**: Handles player movement and all events related to the player.
- **constants.py**: A file with all constant values used in the game.
- **damageText.py**: Displays the amount of damage the player dealt to an enemy.
- **enemies.py**: Handles all types of enemies like Orcs or Bosses. Their movement and AI.
- **HUD.py**: Handles displaying information about health, gold, and other player stats.
- **items.py**: Handles interactions with players for all types of items like health potions or gold.
- **load.py**: Handles loading config, assets, and saving config.
- **menu.py**: Handles the main menu and settings.
- **music.py**: Handles the behavior of music and effects in the game.
- **weapon.py**: Handles the behavior of all types of weapons in the game.
- **world.py**: Loads and handles the world in the game from CSV files.
- **main.py**: The main file of the game.

## Game Versions:

- **0.0.1**: Working main menu, settings, credits. Short game level with a few Orcs and Shaman Orc Boss. No possibility to finish the game. It's a short demo to showcase the possibilities of the game.

## Authors:

- Kacper Baryłowicz "malybaryl"

## License:

The scripts are written by me, and you can use them freely. Of course, it would be nice if you mention me. Some of the assets are made by me, but not all of them. For more information, see credits/credits.txt.

----------------------------------------------POLSKI----------------------------------------------
# Dungeon Crawler

Dungeon Crawler to prosta gra stworzona w Pythonie przy użyciu biblioteki Pygame. Gra oferuje klasyczny system dungeon crawl, gdzie gracz eksploruje lochy, walczy z przeciwnikami, zbiera przedmioty i zdobywa doświadczenie.

## Funkcje:

- **Postać gracza**: Kontroluj postać poruszającą się po lochach i korzystającą z broni dystansowej.
- **Przeciwnicy**: Gra obejmuje różnorodnych przeciwników, w tym orków i potężnych bossów.
- **Walka**: System walki obejmuje strzelanie do wrogów za pomocą łuku i unikanie ataków przeciwników.
- **Zbieranie przedmiotów**: Gracz może zdobywać złoto, mikstury zdrowia i inne przedmioty.
- **HUD (Heads-Up Display)**: Wyświetla informacje na temat zdrowia, złota i innych statystyk gracza.
- **Menu główne**: Proste zarządzanie menu głównego, umożliwiające rozpoczęcie nowej gry i dostosowywanie ustawień.
- **Zapisywanie Ustawień**: Twoje ustawienia w grze zostaną zapisane nawet po wyłączeniu gry.

## Jak uruchomić:

1. Zainstaluj Pythona i Pygame.
2. Uruchom plik `main.py`.

## Konfiguracja:

Możesz dostosować ustawienia gry, takie jak rozdzielczość ekranu, dźwięk czy tryb pełnoekranowy, w ustawieniach gry lub edytując plik `config/config.txt`.

## Struktura projektu:

- **scripts**: Katalog zawiera moduły i klasy, takie jak postać, broń, tło, przeciwnicy, HUD, przedmioty, muzyka i menu.
- **levels**: Katalog zawiera pliki CSV z danymi poziomów.
- **assets**: Katalog zawiera pliki graficzne i dźwiękowe używane w grze.

## Więcej o Skryptach:

- **background.py**: Obsługuje tło w grze.
- **changeResolution.py**: Obsługuje rozdzielczość w grze.
- **character.py**: Obsługuje ruch gracza i wszystkie zdarzenia związane z graczem.
- **constants.py**: Plik zawiera wszystkie stałe wartości używane w grze.
- **damageText.py**: Wyświetla ilość zadanych obrażeń wrogowi przez gracza.
- **enemies.py**: Obsługuje wszystkie rodzaje wrogów, takie jak Orki czy Boski. Ich ruch i sztuczną inteligencję.
- **HUD.py**: Obsługuje wyświetlanie informacji o zdrowiu, złocie i innych statystykach gracza.
- **items.py**: Obsługuje interakcje z graczem dla wszystkich rodzajów przedmiotów, takich jak mikstury zdrowia czy złoto.
- **load.py**: Obsługuje ładowanie konfiguracji, zasobów i zapisywanie konfiguracji.
- **menu.py**: Obsługuje główne menu i ustawienia.
- **music.py**: Obsługuje zachowanie muzyki i efektów dźwiękowych w grze.
- **weapon.py**: Obsługuje zachowanie wszystkich rodzajów broni w grze.
- **world.py**: Ładuje i obsługuje świat w grze z pliku CSV.
- **main.py**: Główny plik gry.

## Wersje Gry:

- **0.0.1**: Działa główne menu, ustawienia, napisy końcowe. Krótki poziom gry z kilkoma Orkami i Szamanem - Bossem. Brak możliwości zakończenia gry. Jest to krótka wersja demonstracyjna, pokazująca możliwości gry.

## Autorzy:

- Kacper Baryłowicz "malybaryl"

## Licencja:

Skrypty są przeze mnie napisane, możesz z nich swobodnie korzystać. Oczywiście byłoby miło, gdybyś wspomniał o mnie. Niektóre zasoby są przeze mnie stworzone, ale nie wszystkie. Więcej informacji znajdziesz w credits/credits.txt.

