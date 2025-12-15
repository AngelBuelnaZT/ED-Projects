using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using System.Threading;

namespace CalabozosX
{
    #region Game Core Classes
    public class GameBoard
    {
        private readonly int[,,] board;
        private readonly bool[,,] revealed;
        private readonly Random random = new Random();
        public const int Empty = 0; public const int Wall = 1; public const int TreasureNormal = 2;
        public const int Trap = 3; public const int Exit = 4; public const int Player = 5;
        public const int Key = 6; public const int TreasureEpic = 7; public const int TreasureLegendary = 8;
        public int Width { get; private set; }
        public int Height { get; private set; }
        public int Levels { get; private set; }

        public GameBoard(int width, int height, int levels)
        {
            Width = width; Height = height; Levels = levels;
            board = new int[width, height, levels];
            revealed = new bool[width, height, levels];
        }

        public void InitializeBoard()
        {
            for (int z = 0; z < Levels; z++) { GenerateLevel(z); }
        }

        private int ChooseTreasureType()
        {
            int chance = random.Next(1, 101);
            if (chance <= 5) return TreasureLegendary;
            if (chance <= 30) return TreasureEpic;
            return TreasureNormal;
        }

        private void GenerateLevel(int level)
        {
            for (int x = 0; x < Width; x++) { board[x, 0, level] = Wall; board[x, Height - 1, level] = Wall; }
            for (int y = 0; y < Height; y++) { board[0, y, level] = Wall; board[Width - 1, y, level] = Wall; }
            int mapArea = (Width - 2) * (Height - 2);
            int internal_walls = (int)(mapArea * 0.10) + level * 5;
            int trap_count = (int)(mapArea * 0.05) + level * 3;
            int treasure_count = (int)(mapArea * 0.08);

            for (int i = 0; i < internal_walls; i++) PlaceRandomElementInEmpty(Wall, level);
            for (int i = 0; i < treasure_count; i++) PlaceRandomElementInEmpty(ChooseTreasureType(), level);
            for (int i = 0; i < trap_count; i++) PlaceRandomElementInEmpty(Trap, level);
            PlaceRandomElementInEmpty(Exit, level);
            PlaceRandomElementInEmpty(Key, level);
        }

        private void PlaceRandomElementInEmpty(int element, int level)
        {
            int x, y;
            do { x = random.Next(1, Width - 1); y = random.Next(1, Height - 1); }
            while (board[x, y, level] != Empty);
            board[x, y, level] = element;
        }

        public int GetElement(int x, int y, int z) => board[x, y, z];
        public void SetElement(int x, int y, int z, int value) => board[x, y, z] = value;
        public bool IsRevealed(int x, int y, int z) => revealed[x, y, z];
        
        // CORRECCIÓN: Se añade el método que faltaba para la carga de partidas.
        public void SetRevealed(int x, int y, int z, bool value)
        {
            if (x >= 0 && x < Width && y >= 0 && y < Height && z >= 0 && z < Levels)
            {
                revealed[x, y, z] = value;
            }
        }

        public void RevealArea(int x, int y, int z)
        {
            revealed[x, y, z] = true;
            if (x > 0) revealed[x - 1, y, z] = true; if (x < Width - 1) revealed[x + 1, y, z] = true;
            if (y > 0) revealed[x, y - 1, z] = true; if (y < Height - 1) revealed[x, y + 1, z] = true;
        }
    }

    public class Player
    {
        public int X { get; set; } public int Y { get; set; } public int Level { get; set; }
        public int Lives { get; set; } = 3; public int Score { get; set; } = 0;
        public bool HasKey { get; set; } = false; public int Energy { get; set; } = 5;
        public const int DefaultEnergy = 5; public const int MaxEnergy = 5;
        private int successfulMovesCounter = 0;
        public const int MaxInventory = 5;
        private Dictionary<int, int> treasureInventory = new Dictionary<int, int>();
        public void LoseLife() => Lives--; public void AddScore(int points) => Score += points;
        public void UseKey() => HasKey = false;
        public void LoseEnergyOnCollision() { if (Energy > 0) Energy--; successfulMovesCounter = 0; }
        public void RegisterSuccessfulMove()
        {
            successfulMovesCounter++;
            if (successfulMovesCounter >= 3) { if (Energy < MaxEnergy) Energy++; successfulMovesCounter = 0; }
        }
        public void ResetEnergy() { Energy = DefaultEnergy; }
        public bool AddTreasure(int treasureType)
        {
            if (InventoryCount < MaxInventory)
            {
                if (!treasureInventory.ContainsKey(treasureType)) treasureInventory[treasureType] = 0;
                treasureInventory[treasureType]++; return true;
            }
            return false;
        }
        public int InventoryCount => treasureInventory.Values.Sum();
        public int InventoryScore
        {
            get
            {
                int score = 0;
                if (treasureInventory.ContainsKey(GameBoard.TreasureNormal)) score += treasureInventory[GameBoard.TreasureNormal] * 100;
                if (treasureInventory.ContainsKey(GameBoard.TreasureEpic)) score += treasureInventory[GameBoard.TreasureEpic] * 250;
                if (treasureInventory.ContainsKey(GameBoard.TreasureLegendary)) score += treasureInventory[GameBoard.TreasureLegendary] * 500;
                return score;
            }
        }
        public Dictionary<int, int> GetTreasureInventory() => treasureInventory;
        public void SetTreasureInventory(Dictionary<int, int> loadedInventory) => treasureInventory = loadedInventory;
    }

    public class Leaderboard
    {
        private readonly List<ScoreEntry> entries = new List<ScoreEntry>();
        private const string FilePath = "leaderboard.txt"; private const int MaxEntries = 10;
        private class ScoreEntry { public string Name { get; set; } public int Score { get; set; } }
        public void Load()
        {
            entries.Clear(); if (!File.Exists(FilePath)) return;
            try
            {
                string[] lines = File.ReadAllLines(FilePath);
                foreach (string line in lines)
                {
                    string[] parts = line.Split(':');
                    if (parts.Length == 2 && int.TryParse(parts[1].Trim(), out int score))
                        entries.Add(new ScoreEntry { Name = parts[0].Trim(), Score = score });
                }
            }
            catch (Exception ex) { Console.WriteLine($"Error al cargar la tabla de clasificación: {ex.Message}"); }
        }
        public void Save()
        {
            try
            {
                var lines = entries.Select(e => $"{e.Name}:{e.Score}");
                File.WriteAllLines(FilePath, lines);
            }
            catch (Exception ex) { Console.WriteLine($"Error al guardar la tabla de clasificación: {ex.Message}"); }
        }
        public void AddEntry(string name, int score)
        {
            entries.Add(new ScoreEntry { Name = name, Score = score });
            entries.Sort((a, b) => b.Score.CompareTo(a.Score));
            if (entries.Count > MaxEntries) entries.RemoveRange(MaxEntries, entries.Count - MaxEntries);
            Save();
        }
        public void Display()
        {
            Console.WriteLine("\n=== Tabla de Clasificación ===");
            if (entries.Count == 0) { Console.WriteLine("No hay puntuaciones registradas."); return; }
            for (int i = 0; i < entries.Count; i++)
                Console.WriteLine($"{i + 1}. {entries[i].Name}: {entries[i].Score} puntos");
        }
    }
    #endregion

    public class TreasureHuntGame
    {
        private readonly GameBoard board;
        private readonly Player player;
        private readonly Leaderboard leaderboard;
        private const int Width = 25, Height = 25, Levels = 3;
        private string gameMessage = "";
        private int elementUnderPlayer = GameBoard.Empty;
        private readonly Dictionary<int, char> symbol_map = new Dictionary<int, char>
        {
            { GameBoard.Empty, '.' }, { GameBoard.Wall, '#' }, { GameBoard.TreasureNormal, '$' },
            { GameBoard.TreasureEpic, '$' }, { GameBoard.TreasureLegendary, '$' }, { GameBoard.Trap, '!' },
            { GameBoard.Exit, 'E' }, { GameBoard.Player, '@' }, { GameBoard.Key, 'K' }
        };

        public TreasureHuntGame(bool load = false)
        {
            board = new GameBoard(Width, Height, Levels);
            player = new Player();
            leaderboard = new Leaderboard();
            leaderboard.Load();
            
            if (load && File.Exists("savegame.txt"))
            {
                LoadGame("savegame.txt");
            }
            else
            {
                board.InitializeBoard();
                player.X = Width / 2;
                player.Y = Height / 2;
                player.Level = 0;
                board.SetElement(player.X, player.Y, player.Level, GameBoard.Player);
                board.RevealArea(player.X, player.Y, player.Level);
            }
        }

        #region Game Loop and Display
        
        public void Play()
        {
            bool gameIsActive = true;
            while (gameIsActive)
            {
                Display();
                ConsoleKeyInfo key = Console.ReadKey(true);
                HandleInput(key, ref gameIsActive);
            }
        }
        
        private void HandleInput(ConsoleKeyInfo key, ref bool gameIsActive)
        {
            int dx = 0, dy = 0;
            switch (key.Key)
            {
                case ConsoleKey.UpArrow: dy = -1; break;
                case ConsoleKey.DownArrow: dy = 1; break;
                case ConsoleKey.LeftArrow: dx = -1; break;
                case ConsoleKey.RightArrow: dx = 1; break;
                case ConsoleKey.I: ShowInventoryScreen(); break;
                case ConsoleKey.R: ShowLeaderboardScreen(); break;
                case ConsoleKey.G:
                    SaveGame("savegame.txt");
                    gameMessage = "¡Partida guardada!";
                    Display();
                    Thread.Sleep(1000);
                    gameIsActive = false;
                    break;
                case ConsoleKey.Q:
                    gameMessage = "¿Salir sin guardar? (S/N)";
                    Display();
                    if (Console.ReadKey(true).Key == ConsoleKey.S) gameIsActive = false;
                    break;
            }

            if (dx != 0 || dy != 0)
            {
                MovePlayer(dx, dy);
            }
        }
        
        private void MovePlayer(int dx, int dy)
        {
            int new_x = player.X + dx;
            int new_y = player.Y + dy;

            if (new_x >= 0 && new_x < Width && new_y >= 0 && new_y < Height && board.GetElement(new_x, new_y, player.Level) != GameBoard.Wall)
            {
                player.RegisterSuccessfulMove();
                board.SetElement(player.X, player.Y, player.Level, elementUnderPlayer);
                int previousLevel = player.Level;
                player.X = new_x; player.Y = new_y;
                elementUnderPlayer = board.GetElement(player.X, player.Y, player.Level);
                ProcessCell(player.X, player.Y);
                if (player.Level != previousLevel) elementUnderPlayer = GameBoard.Empty;
                else if (elementUnderPlayer != GameBoard.Exit && elementUnderPlayer != GameBoard.Empty) elementUnderPlayer = GameBoard.Empty;
                board.SetElement(player.X, player.Y, player.Level, GameBoard.Player);
                board.RevealArea(player.X, player.Y, player.Level);
            }
            else
            {
                player.LoseEnergyOnCollision();
                gameMessage += $"¡Chocaste! Pierdes 1 de energía.\n";
                if (player.Energy <= 0)
                {
                    player.LoseLife();
                    gameMessage += "¡Te quedaste sin energía y pierdes una vida!\n";
                    if (player.Lives <= 0) { EndGame(false); return; }
                    player.ResetEnergy();
                    gameMessage += "Tu energía ha sido restaurada.\n";
                }
            }
        }
        
        public void Display()
        {
            Console.Clear();
            Console.WriteLine("=== CalabozosX ===");
            Console.WriteLine($"Nivel: {player.Level + 1} | Vidas: {player.Lives} | Energía: {player.Energy} | Puntuación: {player.Score} (+{player.InventoryScore}) | Llave: {(player.HasKey ? "Sí" : "No")}");
            Console.WriteLine($"Espacio en Inventario: {player.InventoryCount}/{Player.MaxInventory}");
            if (player.InventoryCount > 0)
            {
                var inv = player.GetTreasureInventory();
                int n = inv.GetValueOrDefault(GameBoard.TreasureNormal, 0);
                int e = inv.GetValueOrDefault(GameBoard.TreasureEpic, 0);
                int l = inv.GetValueOrDefault(GameBoard.TreasureLegendary, 0);
                Console.WriteLine($"Tesoros: Normal (x{n}), Épico (x{e}), Legendario (x{l})");
            } else { Console.WriteLine("Inventario vacío"); }
            
            Console.WriteLine();
            for (int y = 0; y < Height; y++)
            {
                Console.Write("|");
                for (int x = 0; x < Width; x++)
                {
                    char symbol = board.IsRevealed(x, y, player.Level) ? symbol_map.GetValueOrDefault(board.GetElement(x, y, player.Level), '?') : '*';
                    Console.Write($" {symbol}");
                }
                Console.WriteLine(" |");
            }
            Console.WriteLine(new string('-', Width * 2 + 3));
            if (!string.IsNullOrEmpty(gameMessage)) { Console.WriteLine(gameMessage.Trim()); gameMessage = ""; }
            
            Console.WriteLine("\nControles: Flechas (Mover), I (Inventario), R (Clasificación), G (Guardar y Salir), Q (Salir)");
        }
        #endregion

        #region Game Logic
        private void ProcessCell(int x, int y)
        {
            int cell = board.GetElement(x, y, player.Level);
            switch (cell)
            {
                case GameBoard.TreasureNormal: case GameBoard.TreasureEpic: case GameBoard.TreasureLegendary:
                    HandleTreasureCollection(cell); board.SetElement(x, y, player.Level, GameBoard.Empty); break;
                case GameBoard.Trap:
                    player.LoseLife(); gameMessage += $"¡Caíste en una trampa! Vidas restantes: {player.Lives}\n";
                    board.SetElement(x, y, player.Level, GameBoard.Empty); if (player.Lives <= 0) EndGame(false); break;
                case GameBoard.Key:
                    player.HasKey = true; gameMessage += "¡Has encontrado la llave para la salida!\n";
                    board.SetElement(x, y, player.Level, GameBoard.Empty); break;
                case GameBoard.Exit:
                    if (player.HasKey)
                    {
                        if (player.Level < Levels - 1)
                        {
                            int bonus = 500 * (player.Level + 1); player.AddScore(bonus);
                            gameMessage += $"¡Nivel {player.Level + 1} completado! Bonificación: {bonus} puntos\n";
                            board.SetElement(player.X, player.Y, player.Level, GameBoard.Empty);
                            player.Level++; player.UseKey(); player.X = Width / 2; player.Y = Height / 2;
                        }
                        else EndGame(true);
                    }
                    else gameMessage += "La puerta está cerrada. ¡Necesitas encontrar la llave (K)!\n";
                    break;
            }
        }

        private void HandleTreasureCollection(int treasureType)
        {
            if (player.AddTreasure(treasureType))
            {
                string r = ""; int p = 0;
                switch (treasureType)
                {
                    case GameBoard.TreasureNormal: r = "Normal"; p = 100; break;
                    case GameBoard.TreasureEpic: r = "Épico"; p = 250; break;
                    case GameBoard.TreasureLegendary: r = "Legendario"; p = 500; break;
                }
                gameMessage += $"¡Recolectaste un tesoro {r} (+{p} puntos)!\n";
            }
            else gameMessage += "¡Inventario lleno!\n";
        }
        
        private void ShowInventoryScreen()
        {
            Console.Clear();
            Console.WriteLine("=== Inventario Detallado ===");
            var inv = player.GetTreasureInventory();
            int n = inv.GetValueOrDefault(GameBoard.TreasureNormal, 0);
            int e = inv.GetValueOrDefault(GameBoard.TreasureEpic, 0);
            int l = inv.GetValueOrDefault(GameBoard.TreasureLegendary, 0);
            Console.WriteLine($"Tesoros: Normal (x{n}), Épico (x{e}), Legendario (x{l})");
            Console.WriteLine($"\nValor total de tesoros: {player.InventoryScore} puntos");
            Console.WriteLine("\nPresiona cualquier tecla para volver al juego...");
            Console.ReadKey(true);
        }

        private void ShowLeaderboardScreen()
        {
            Console.Clear();
            leaderboard.Display();
            Console.WriteLine("\nPresiona cualquier tecla para volver al juego...");
            Console.ReadKey(true);
        }
        
        private void EndGame(bool won)
        {
            int final_score = player.Score + player.InventoryScore; Console.Clear();
            Console.WriteLine("\n" + new string('=', 40));
            if (won) Console.WriteLine("|       ¡FELICIDADES, HAS GANADO!      |");
            else Console.WriteLine("|            FIN DEL JUEGO             |");
            Console.WriteLine(new string('-', 40));
            Console.WriteLine($"| Puntuación Final: {final_score,-18} |");
            Console.WriteLine(new string('=', 40));
            if (final_score > 0)
            {
                Console.WriteLine("\n¿Guardar puntuación en la tabla de clasificación? (S/N)");
                if (Console.ReadLine().ToUpper().StartsWith("S"))
                {
                    Console.Write("Ingresa tu nombre (letras/números, máx 20 carac.): ");
                    string name = Console.ReadLine().Trim();
                    if (Regex.IsMatch(name, @"^[a-zA-Z0-9\s]{1,20}$"))
                    {
                        leaderboard.AddEntry(name, final_score); Console.WriteLine("¡Puntuación guardada!"); leaderboard.Display();
                    } else { Console.WriteLine("Nombre inválido. La puntuación no se guardó."); }
                }
            }
            Console.WriteLine("\nPresiona cualquier tecla para salir..."); Console.ReadKey(true); Environment.Exit(0);
        }
        #endregion

        #region Save and Load Logic
        public void SaveGame(string filePath)
        {
            try
            {
                using (StreamWriter writer = new StreamWriter(filePath))
                {
                    writer.WriteLine("[PLAYER]");
                    writer.WriteLine($"X:{player.X}"); writer.WriteLine($"Y:{player.Y}"); writer.WriteLine($"Level:{player.Level}");
                    writer.WriteLine($"Lives:{player.Lives}"); writer.WriteLine($"Score:{player.Score}");
                    writer.WriteLine($"HasKey:{player.HasKey}"); writer.WriteLine($"Energy:{player.Energy}");
                    writer.WriteLine($"ElementUnderPlayer:{elementUnderPlayer}");
                    writer.WriteLine("[INVENTORY]");
                    foreach (var item in player.GetTreasureInventory()) writer.WriteLine($"{item.Key}:{item.Value}");
                    writer.WriteLine("[BOARD]");
                    for (int z = 0; z < Levels; z++)
                    {
                        string line = string.Join(",", from y in Enumerable.Range(0, Height) from x in Enumerable.Range(0, Width) select board.GetElement(x, y, z));
                        writer.WriteLine(line);
                    }
                    writer.WriteLine("[REVEALED]");
                    for (int z = 0; z < Levels; z++)
                    {
                        string line = string.Join(",", from y in Enumerable.Range(0, Height) from x in Enumerable.Range(0, Width) select board.IsRevealed(x, y, z));
                        writer.WriteLine(line);
                    }
                }
            } catch (Exception ex) { gameMessage = $"Error al guardar: {ex.Message}"; }
        }

        public void LoadGame(string filePath)
        {
            try
            {
                string[] lines = File.ReadAllLines(filePath); string section = "";
                Dictionary<int, int> loadedInventory = new Dictionary<int, int>(); int levelIndex = 0;
                foreach (var line in lines)
                {
                    if (line.StartsWith("[")) { section = line; if(section == "[BOARD]") levelIndex = 0; if(section == "[REVEALED]") levelIndex = 0; continue; }
                    switch (section)
                    {
                        case "[PLAYER]":
                            var p = line.Split(':'); if(p.Length < 2) continue;
                            if (p[0] == "X") player.X = int.Parse(p[1]); if (p[0] == "Y") player.Y = int.Parse(p[1]);
                            if (p[0] == "Level") player.Level = int.Parse(p[1]); if (p[0] == "Lives") player.Lives = int.Parse(p[1]);
                            if (p[0] == "Score") player.Score = int.Parse(p[1]); if (p[0] == "HasKey") player.HasKey = bool.Parse(p[1]);
                            if (p[0] == "Energy") player.Energy = int.Parse(p[1]); if (p[0] == "ElementUnderPlayer") elementUnderPlayer = int.Parse(p[1]);
                            break;
                        case "[INVENTORY]":
                             var i = line.Split(':'); if(i.Length < 2) continue;
                             loadedInventory[int.Parse(i[0])] = int.Parse(i[1]);
                             break;
                        case "[BOARD]":
                             var boardValues = line.Split(','); int boardIndex = 0;
                             for (int y = 0; y < Height; y++) for (int x = 0; x < Width; x++)
                                { board.SetElement(x, y, levelIndex, int.Parse(boardValues[boardIndex++])); }
                             levelIndex++; break;
                        case "[REVEALED]":
                             var revealedValues = line.Split(','); int revealedIndex = 0;
                             for (int y = 0; y < Height; y++) for (int x = 0; x < Width; x++)
                                { board.SetRevealed(x, y, levelIndex, bool.Parse(revealedValues[revealedIndex++])); }
                             levelIndex++; break;
                    }
                }
                player.SetTreasureInventory(loadedInventory);
            } catch (Exception ex) { gameMessage = $"Error al cargar: {ex.Message}"; }
        }
        #endregion
    }

    class Program
    {
        static void Main()
        {
            Console.CursorVisible = false;
            ShowMainMenu();
        }

        static void ShowMainMenu()
        {
            Leaderboard leaderboard = new Leaderboard();
            while (true)
            {
                Console.Clear();
                Console.Title = "CalabozosX - Menú";
                Console.WriteLine(@"
         
 ____              ___             __                                         __   __     
/\  _`\           /\_ \           /\ \                                       /\ \ /\ \    
\ \ \/\_\     __  \//\ \      __  \ \ \____    ___   ____     ___     ____   \ `\`\/'/'   
 \ \ \/_/_  /'__`\  \ \ \   /'__`\ \ \ '__`\  / __`\/\_ ,`\  / __`\  /',__\   `\/ > <     
  \ \ \L\ \/\ \L\.\_ \_\ \_/\ \L\.\_\ \ \L\ \/\ \L\ \/_/  /_/\ \L\ \/\__, `\     \/'/\`\  
   \ \____/\ \__/.\_\/\____\ \__/.\_\\ \_,__/\ \____/ /\____\ \____/\/\____/     /\_\\ \_\
    \/___/  \/__/\/_/\/____/\/__/\/_/ \/___/  \/___/  \/____/\/___/  \/___/      \/_/ \/_/
                                                                                          
                                                                                          
                                                                 
                                                                 ");
                Console.WriteLine("                1. Nueva Partida");
                Console.WriteLine("                2. Cargar Partida");
                Console.WriteLine("                3. Tabla de Clasificación");
                Console.WriteLine("                4. Salir");
                Console.Write("\n                Elige una opción: ");

                char choice = Console.ReadKey(true).KeyChar;
                switch (choice)
                {
                    case '1': new TreasureHuntGame().Play(); break;
                    case '2':
                        if (File.Exists("savegame.txt")) new TreasureHuntGame(true).Play();
                        else
                        {
                            Console.WriteLine("\n\n                No se encontró ninguna partida guardada. Presiona una tecla...");
                            Console.ReadKey(true);
                        }
                        break;
                    case '3':
                        Console.Clear(); leaderboard.Load(); leaderboard.Display();
                        Console.WriteLine("\n                Presiona una tecla para volver al menú...");
                        Console.ReadKey(true);
                        break;
                    case '4': Environment.Exit(0); break;
                }
            }
        }
    }
}