import java.util.Scanner;
import java.io.IOException;

public class BattleshipGame {
    private BattleshipPlayer player1;
    private BattleshipPlayer player2;
    private Scanner scanner;
    private boolean gameOver = false;
    private String winner = "";

    private int[] shipSizes = {4, 3, 3, 2, 2, 1, 1}; // Tamaños de los barcos
    private int totalShipCells = 16; // Suma de todos los tamaños

    public BattleshipGame() {
        scanner = new Scanner(System.in);
        player1 = new BattleshipPlayer("Jugador 1");
        player2 = new BattleshipPlayer("Jugador 2");
    }

    // Muestra las reglas del juego
    private void displayRules() {
        System.out.println("\n=====================================");
        System.out.println("           REGLAS DE BATALLA NAVAL   ");
        System.out.println("=====================================");
        System.out.println("1. Tablero: 7x8 (filas A-G, columnas 0-7).");
        System.out.println("2. Barcos: 7 barcos (tamaños 4,3,3,2,2,1,1). Total 16 celdas ocupadas.");
        System.out.println("3. Colocación: Cada jugador coloca sus barcos sin superposiciones.");
        System.out.println("4. Juego: Turnos alternos (empieza Jugador 1). Dispara al tablero enemigo.");
        System.out.println("   - Hit ('X'): Impacta un barco. Si hunde todos (16 hits), ganas.");
        System.out.println("   - Miss ('O'): Agua. ");
        System.out.println("5. Victoria: Hundir todos los barcos del enemigo.");
        System.out.println("6. Empate: Si ambos jugadores hunden todos los barcos simultáneamente.");
        System.out.println("7. El tablero enemigo muestra solo disparos; el tuyo es visible.");
        System.out.println("=====================================\n");
    }

    // Fase de colocación para un jugador
    private void placementPhase(BattleshipPlayer player) {
        System.out.println("\n--- Fase de Colocación para " + player.getName() + " ---");
        System.out.println("Coloca tus barcos uno por uno. No se pueden mover después.");
        for (int size : shipSizes) {
            boolean placed = false;
            while (!placed) {
                player.displayOwnBoard(); // Muestra su propio tablero
                System.out.println("Colocando barco de tamaño " + size);
                System.out.print("Fila (A-G): ");
                char rowChar = scanner.next().charAt(0);
                System.out.print("Columna (0-7): ");
                int col = scanner.nextInt();
                System.out.print("Horizontal? (s/n): ");
                boolean isHorizontal = scanner.next().toLowerCase().charAt(0) == 's';

                int row = player.convertRow(rowChar);
                if (row >= 0 && row < player.getRows() && col >= 0 && col < player.getCols()) {
                    if (player.isValidPosition(row, col, size, isHorizontal)) {
                        player.placeShip(row, col, size, isHorizontal);
                        placed = true;
                        System.out.println("Barco colocado exitosamente.");
                    } else {
                        System.out.println("¡Posición inválida! (Fuera de tablero o superposición). Intenta de nuevo.");
                    }
                } else {
                    System.out.println("¡Coordenadas fuera del tablero! Intenta de nuevo.");
                }
            }
        }
        System.out.println("¡Todos los barcos colocados para " + player.getName() + "!");
        player.displayOwnBoard();
        pauseForNextPlayer();
    }

    // Pausa para que el otro jugador no vea la pantalla
    private void pauseForNextPlayer() {
        System.out.println("\nPresiona Enter para continuar...");
        try {
            System.in.read();
        } catch (IOException e) {
            e.printStackTrace();
        }
        // Limpia la consola (aproximado, depende del SO)
        System.out.print("\033[H\033[2J");
    }

    // Fase de juego principal
    private void playGame() {
        System.out.println("\n--- ¡Comienza el juego! ---");
        boolean player1Turn = true;
        BattleshipPlayer currentPlayer = player1;
        BattleshipPlayer opponent = player2;

        while (!gameOver) {
            currentPlayer.displayBoards(); // Muestra propio y enemigo (parcial)
            System.out.println(currentPlayer.getName() + ", es tu turno. Dispara al tablero enemigo.");
            System.out.print("Fila (A-G): ");
            char rowChar = scanner.next().charAt(0);
            System.out.print("Columna (0-7): ");
            int col = scanner.nextInt();

            int row = currentPlayer.convertRow(rowChar);
            if (row < 0 || row >= currentPlayer.getRows() || col < 0 || col >= currentPlayer.getCols()) {
                System.out.println("¡Coordenadas inválidas! Pierdes tu turno.");
                player1Turn = !player1Turn;
                continue;
            }

            // Disparo
            char result = opponent.shoot(row, col);
            if (result == 'X') {
                System.out.println("¡Impacto! ('X')");
                if (opponent.getHits() >= totalShipCells) {
                    checkWin(currentPlayer, opponent);
                    break;
                }
            } else if (result == 'O') {
                System.out.println("¡Fallaste! ('O')");
            } else {
                System.out.println("¡Ya disparaste ahí! Pierdes tu turno.");
            }

            player1Turn = !player1Turn;
            currentPlayer = player1Turn ? player1 : player2;
            opponent = player1Turn ? player2 : player1;

            pauseForNextPlayer();
        }

        displayFinalResult();
    }

    // Verifica victoria o empate
    private void checkWin(BattleshipPlayer winnerPlayer, BattleshipPlayer loserPlayer) {
        if (loserPlayer.getHits() >= totalShipCells && winnerPlayer.getHits() >= totalShipCells) {
            winner = "¡Empate! Ambos jugadores hundieron todos los barcos.";
        } else {
            this.winner = winnerPlayer.getName() + " gana!";
        }
        gameOver = true;
    }

    // Muestra resultado final
    private void displayFinalResult() {
        System.out.println("\n=====================================");
        System.out.println(winner);
        System.out.println("=====================================");
        System.out.println("Tablero de " + player1.getName() + ":");
        player1.displayOwnBoard();
        System.out.println("Tablero de " + player2.getName() + ":");
        player2.displayOwnBoard();
    }

    // Método principal del juego
    public void startGame() {
        displayRules();
        placementPhase(player1);
        placementPhase(player2);
        playGame();
    }

    public static void main(String[] args) {
        BattleshipGame game = new BattleshipGame();
        game.startGame();
    }
}

// Clase para un jugador individual
class BattleshipPlayer {
    private char[][] ownBoard; // Tablero propio (con 'S' para barcos, '~' agua)
    private char[][] enemyBoard; // Tablero enemigo (para disparos: '~' no disparado, 'X' hit, 'O' miss)
    private String name;
    private int rows = 7;
    private int cols = 8;
    private int hits = 0; // Contador de hits en el tablero enemigo

    public BattleshipPlayer(String name) {
        this.name = name;
        ownBoard = new char[rows][cols];
        enemyBoard = new char[rows][cols];
        initializeBoards();
    }

    private void initializeBoards() {
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                ownBoard[i][j] = '~';
                enemyBoard[i][j] = '~';
            }
        }
    }

    public int getRows() { return rows; }
    public int getCols() { return cols; }
    public String getName() { return name; }
    public int getHits() { return hits; }

    // Muestra el tablero propio completo
    public void displayOwnBoard() {
        System.out.println("\nTu tablero (" + name + "):");
        displayBoard(ownBoard);
    }

    // Muestra ambos tableros (propio completo, enemigo parcial)
    public void displayBoards() {
        displayOwnBoard();
        System.out.println("Tablero enemigo:");
        displayBoard(enemyBoard);
    }

    // Muestra un tablero genérico (con colores ANSI si soportado)
    private void displayBoard(char[][] board) {
        System.out.print("  ");
        for (int j = 0; j < cols; j++) {
            System.out.print(j + " ");
        }
        System.out.println();
        for (int i = 0; i < rows; i++) {
            System.out.print((char)('A' + i) + " ");
            for (int j = 0; j < cols; j++) {
                char cell = board[i][j];
                String color = "";
                String displayChar = String.valueOf(cell);
                if (cell == '~') {
                    color = "\u001B[34m"; // Azul para agua
                    displayChar = "~";
                } else if (cell == 'S') {
                    color = "\u001B[32m"; // Verde para barco
                    displayChar = "■"; // Símbolo ASCII cuadrado
                } else if (cell == 'X') {
                    color = "\u001B[31m"; // Rojo para hit
                    displayChar = "X";
                } else if (cell == 'O') {
                    color = "\u001B[37m"; // Blanco para miss
                    displayChar = "O";
                }
                System.out.print(color + displayChar + " \u001B[0m");
            }
            System.out.println();
        }
    }

    // Convierte fila de letra a índice
    public int convertRow(char rowChar) {
        return Character.toUpperCase(rowChar) - 'A';
    }

    // Verifica posición válida para colocar barco
    public boolean isValidPosition(int row, int col, int size, boolean isHorizontal) {
        if (isHorizontal) {
            if (col + size > cols) return false;
            for (int j = col; j < col + size; j++) {
                if (ownBoard[row][j] != '~') return false;
            }
        } else {
            if (row + size > rows) return false;
            for (int i = row; i < row + size; i++) {
                if (ownBoard[i][col] != '~') return false;
            }
        }
        return true;
    }

    // Coloca un barco en el tablero propio
    public void placeShip(int row, int col, int size, boolean isHorizontal) {
        for (int i = 0; i < size; i++) {
            if (isHorizontal) {
                ownBoard[row][col + i] = 'S';
            } else {
                ownBoard[row + i][col] = 'S';
            }
        }
    }

    // Procesa un disparo en este tablero (llamado por el oponente)
    public char shoot(int row, int col) {
        if (enemyBoard[row][col] != '~') {
            return ' '; // Ya disparado
        }

        if (ownBoard[row][col] == 'S') {
            ownBoard[row][col] = 'X'; // Marca como hit en propio (para tracking)
            enemyBoard[row][col] = 'X';
            hits++; // El oponente aumenta sus hits
            return 'X';
        } else {
            enemyBoard[row][col] = 'O';
            return 'O';
        }
    }
}