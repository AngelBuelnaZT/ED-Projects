import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class SnakeGame extends JPanel implements ActionListener, KeyListener {
    private final int WIDTH = 800;
    private final int HEIGHT = 800;
    private final int UNIT_SIZE = 25;
    private final int GAME_UNITS = (WIDTH * HEIGHT) / (UNIT_SIZE * UNIT_SIZE);
    
    private final int[] DELAYS = {100, 85, 70, 55, 40};
    
    private final int[] x = new int[GAME_UNITS];
    private final int[] y = new int[GAME_UNITS];

    private int bodyParts = 6;
    private int applesEaten = 0;
    private int trapsEaten = 0;
    private int level = 1;
    private int score = 0;
    private long startTime;
    private long pauseTime;
    private long totalPaused;
    private int appleX, appleY;
    private char direction = 'R';
    private boolean running = false;
    private boolean paused = false;
    private boolean showLeaderboard = false;
    private Timer timer;
    private Random random;

    private List<Trap> traps = new ArrayList<>();
    private static final int MAX_TRAPS = 15;
    private static final int TRAPS_PER_LEVEL = 2;

    private static final String LEADERBOARD_FILE = "snake_leaderboard.txt";
    private static final String SAVE_FILE = "snake_save.txt";
    private static final int MAX_SCORES = 10;

    private List<ScoreEntry> leaderboard = new ArrayList<>();

    public SnakeGame() {
        random = new Random();
        this.setPreferredSize(new Dimension(WIDTH, HEIGHT));
        this.setBackground(Color.BLACK);
        this.setFocusable(true);
        this.addKeyListener(this);
        loadLeaderboard();
        startGame();
    }

    public void startGame() {
        bodyParts = 6;
        applesEaten = 0;
        trapsEaten = 0;
        level = 1;
        score = 0;
        startTime = System.currentTimeMillis();
        pauseTime = 0;
        totalPaused = 0;
        direction = 'R';
        traps.clear();
        showLeaderboard = false;

        for (int i = 0; i < bodyParts; i++) {
            x[i] = UNIT_SIZE * 16 - i * UNIT_SIZE;
            y[i] = UNIT_SIZE * 16;
        }

        newApple();
        spawnTraps();

        if (timer != null && timer.isRunning()) {
            timer.stop();
        }

        timer = new Timer(DELAYS[0], this);
        running = true;
        paused = false;
        timer.start();

        repaint();
        requestFocusInWindow();
    }

    public void saveGame() {
        if (!running) return;
        try {
            PrintWriter pw = new PrintWriter(new FileWriter(SAVE_FILE));
            pw.println("bodyParts:" + bodyParts);
            pw.println("applesEaten:" + applesEaten);
            pw.println("trapsEaten:" + trapsEaten);
            pw.println("level:" + level);
            pw.println("score:" + score);
            pw.println("startTime:" + startTime);
            pw.println("totalPaused:" + totalPaused);
            pw.println("direction:" + direction);
            pw.println("appleX:" + appleX);
            pw.println("appleY:" + appleY);
            for (int i = 0; i < bodyParts; i++) {
                pw.println("snake:" + i + "," + x[i] + "," + y[i]);
            }
            for (Trap trap : traps) {
                pw.println("trap:" + trap.x + "," + trap.y);
            }
            pw.close();
            showMessage("💾 Partida guardada!");
        } catch (IOException e) {
            showMessage("❌ Error al guardar");
        }
    }

    public void loadGame() {
        try {
            BufferedReader br = new BufferedReader(new FileReader(SAVE_FILE));
            String line;
            traps.clear();
            while ((line = br.readLine()) != null) {
                String[] parts = line.split(":");
                if (parts.length < 2) continue;
                if (parts[0].equals("bodyParts")) bodyParts = Integer.parseInt(parts[1]);
                else if (parts[0].equals("applesEaten")) applesEaten = Integer.parseInt(parts[1]);
                else if (parts[0].equals("trapsEaten")) trapsEaten = Integer.parseInt(parts[1]);
                else if (parts[0].equals("level")) level = Integer.parseInt(parts[1]);
                else if (parts[0].equals("score")) score = Integer.parseInt(parts[1]);
                else if (parts[0].equals("startTime")) startTime = Long.parseLong(parts[1]);
                else if (parts[0].equals("totalPaused")) totalPaused = Long.parseLong(parts[1]);
                else if (parts[0].equals("direction")) direction = parts[1].charAt(0);
                else if (parts[0].equals("appleX")) appleX = Integer.parseInt(parts[1]);
                else if (parts[0].equals("appleY")) appleY = Integer.parseInt(parts[1]);
                else if (parts[0].equals("snake")) {
                    String[] pos = parts[1].split(",");
                    int idx = Integer.parseInt(pos[0]);
                    if (idx < x.length) { 
                        x[idx] = Integer.parseInt(pos[1]); 
                        y[idx] = Integer.parseInt(pos[2]); 
                    }
                } else if (parts[0].equals("trap")) {
                    String[] pos = parts[1].split(",");
                    traps.add(new Trap(Integer.parseInt(pos[0]), Integer.parseInt(pos[1])));
                }
            }
            br.close();
            
            // CORREGIDO: Configurar timer correctamente
            if (timer == null) {
                timer = new Timer(DELAYS[0], this);
            }
            if (level - 1 < DELAYS.length) {
                timer.setDelay(DELAYS[level - 1]);
            }
            
            running = true;
            paused = false;
            timer.start();
            showMessage("📁 Partida cargada!");
            repaint();
            requestFocusInWindow();
        } catch (Exception e) {
            showMessage("❌ No hay partida guardada");
        }
    }

    private void showMessage(String msg) {
        JOptionPane.showMessageDialog(this, msg, "Snake Pro", JOptionPane.INFORMATION_MESSAGE);
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        draw(g);
    }

    public void draw(Graphics g) {
        if (showLeaderboard) {
            drawLeaderboard(g);
            return;
        }

        if (running) {
            // Grilla
            g.setColor(new Color(30, 30, 30));
            for (int i = 0; i <= WIDTH / UNIT_SIZE; i++) {
                g.drawLine(i * UNIT_SIZE, 0, i * UNIT_SIZE, HEIGHT);
            }
            for (int i = 0; i <= HEIGHT / UNIT_SIZE; i++) {
                g.drawLine(0, i * UNIT_SIZE, WIDTH, i * UNIT_SIZE);
            }

            // Manzana
            g.setColor(Color.RED);
            g.fillOval(appleX, appleY, UNIT_SIZE, UNIT_SIZE);
            g.setColor(Color.ORANGE);
            g.fillOval(appleX + 5, appleY + 5, UNIT_SIZE - 10, UNIT_SIZE - 10);

            // Trampas
            for (int i = 0; i < traps.size(); i++) {
                Trap trap = traps.get(i);
                g.setColor(new Color(150, 0, 150));
                g.fillOval(trap.x, trap.y, UNIT_SIZE, UNIT_SIZE);
                g.setColor(Color.WHITE);
                g.fillOval(trap.x + 7, trap.y + 7, 5, 5);
                g.fillOval(trap.x + 13, trap.y + 7, 5, 5);
                g.setColor(Color.CYAN);
                g.setFont(new Font("Arial", Font.BOLD, 14));
                g.drawString((i+1)+"", trap.x + 9, trap.y + 20);
            }

            // Serpiente
            for (int i = 0; i < bodyParts; i++) {
                if (i == 0) {
                    g.setColor(Color.GREEN);
                    g.fillRect(x[i], y[i], UNIT_SIZE, UNIT_SIZE);
                    g.setColor(Color.WHITE);
                    g.fillOval(x[i] + 5, y[i] + 5, 4, 4);
                    g.fillOval(x[i] + 16, y[i] + 5, 4, 4);
                } else {
                    g.setColor(new Color(45, 180, 0));
                    g.fillRect(x[i], y[i], UNIT_SIZE, UNIT_SIZE);
                }
            }

            // INFO
            g.setColor(Color.WHITE);
            g.setFont(new Font("Arial", Font.BOLD, 22));
            g.drawString("Puntos: " + score, 20, 35);
            g.drawString("Tamaño: " + bodyParts, 20, 65);
            g.drawString("Nivel: " + level, 20, 95);
            g.drawString("Trampas: " + traps.size(), 20, 125);

            long elapsed = (System.currentTimeMillis() - startTime - totalPaused) / 1000;
            long minutes = elapsed / 60;
            long seconds = elapsed % 60;
            g.drawString("Tiempo: " + padZero(minutes) + ":" + padZero(seconds), WIDTH - 220, 35);
            g.drawString("Manzanas: " + applesEaten, WIDTH - 220, 65);

            // CONTROLES CENTRADOS
            g.setFont(new Font("Arial", Font.BOLD, 18));
            g.setColor(Color.CYAN);
            String controls = "Flechas = Mover | S = Guardar | C = Cargar | P = Pausa | L = Leaderboard";
            FontMetrics fm = getFontMetrics(g.getFont());
            g.drawString(controls, (WIDTH - fm.stringWidth(controls)) / 2, HEIGHT - 30);

            // PAUSA
            if (paused) {
                g.setColor(new Color(0, 0, 0, 200));
                g.fillRect(0, 0, WIDTH, HEIGHT);
                g.setColor(Color.YELLOW);
                g.setFont(new Font("Arial", Font.BOLD, 70));
                fm = getFontMetrics(g.getFont());
                g.drawString("PAUSADO", (WIDTH - fm.stringWidth("PAUSADO")) / 2, HEIGHT / 2);
                g.setFont(new Font("Arial", Font.BOLD, 28));
                g.setColor(Color.WHITE);
                g.drawString("P = Continuar | S = Guardar | C = Cargar | L = Leaderboard", 
                    (WIDTH - getFontMetrics(g.getFont()).stringWidth("P = Continuar | S = Guardar | C = Cargar | L = Leaderboard")) / 2, 
                    HEIGHT / 2 + 70);
            }

            if (bodyParts >= GAME_UNITS) {
                gameWin(g);
            }
        } else {
            gameOver(g);
        }
    }

    // 🆕 PANTALLA LEADERBOARD
    private void drawLeaderboard(Graphics g) {
        g.setColor(Color.BLACK);
        g.fillRect(0, 0, WIDTH, HEIGHT);

        // Título
        g.setColor(Color.YELLOW);
        g.setFont(new Font("Arial", Font.BOLD, 50));
        FontMetrics fmTitle = getFontMetrics(g.getFont());
        g.drawString("🏆 LEADERBOARD 🏆", (WIDTH - fmTitle.stringWidth("🏆 LEADERBOARD 🏆")) / 2, 80);

        // Headers
        g.setColor(Color.WHITE);
        g.setFont(new Font("Arial", Font.BOLD, 30));
        g.drawString("PTS", 50, 150);
        g.drawString("TAM", 150, 150);
        g.drawString("MANZ", 230, 150);
        g.drawString("NIV", 320, 150);
        g.drawString("TRP", 400, 150);
        g.drawString("TIEMPO", 460, 150);

        // Scores
        g.setFont(new Font("Arial", Font.PLAIN, 24));
        int yPos = 190;
        for (int i = 0; i < Math.min(10, leaderboard.size()); i++) {
            ScoreEntry entry = leaderboard.get(i);
            g.setColor(i == 0 ? Color.GOLD : i == 1 ? Color.SILVER : i == 2 ? Color.ORANGE : Color.WHITE);
            g.drawString((i+1) + ". " + entry.score, 20, yPos);
            g.drawString(entry.size + "", 150, yPos);
            g.drawString(entry.apples + "", 230, yPos);
            g.drawString(entry.level + "", 320, yPos);
            g.drawString(entry.traps + "", 400, yPos);
            g.drawString(padZero(entry.time / 60) + ":" + padZero(entry.time % 60), 460, yPos);
            yPos += 35;
        }

        // Instrucciones
        g.setColor(Color.CYAN);
        g.setFont(new Font("Arial", Font.BOLD, 28));
        FontMetrics fmInstr = getFontMetrics(g.getFont());
        g.drawString("Presiona L para volver al juego", 
                    (WIDTH - fmInstr.stringWidth("Presiona L para volver al juego")) / 2, 
                    HEIGHT - 80);
        g.drawString("ESPACIO = Nueva partida", 
                    (WIDTH - fmInstr.stringWidth("ESPACIO = Nueva partida")) / 2, 
                    HEIGHT - 40);
    }

    private String padZero(long num) {
        return num < 10 ? "0" + num : "" + num;
    }

    public void newApple() {
        boolean invalid;
        do {
            appleX = random.nextInt(WIDTH / UNIT_SIZE) * UNIT_SIZE;
            appleY = random.nextInt(HEIGHT / UNIT_SIZE) * UNIT_SIZE;
            invalid = false;
            for (int i = 0; i < bodyParts; i++) {
                if (x[i] == appleX && y[i] == appleY) { invalid = true; break; }
            }
            for (Trap trap : traps) {
                if (appleX == trap.x && appleY == trap.y) { invalid = true; break; }
            }
        } while (invalid);
    }

    public void spawnTraps() {
        traps.clear();
        int numTraps = Math.min(level * TRAPS_PER_LEVEL, MAX_TRAPS);
        for (int i = 0; i < numTraps; i++) {
            boolean valid;
            int tx, ty;
            do {
                tx = random.nextInt(WIDTH / UNIT_SIZE) * UNIT_SIZE;
                ty = random.nextInt(HEIGHT / UNIT_SIZE) * UNIT_SIZE;
                valid = true;
                for (int j = 0; j < bodyParts; j++) {
                    if (x[j] == tx && y[j] == ty) { valid = false; break; }
                }
                if (appleX == tx && appleY == ty) valid = false;
            } while (!valid);
            traps.add(new Trap(tx, ty));
        }
    }

    public void move() {
        for (int i = bodyParts; i > 0; i--) {
            x[i] = x[i - 1];
            y[i] = y[i - 1];
        }
        switch (direction) {
            case 'U': y[0] = (y[0] - UNIT_SIZE + HEIGHT) % HEIGHT; break;
            case 'D': y[0] = (y[0] + UNIT_SIZE) % HEIGHT; break;
            case 'L': x[0] = (x[0] - UNIT_SIZE + WIDTH) % WIDTH; break;
            case 'R': x[0] = (x[0] + UNIT_SIZE) % WIDTH; break;
        }
    }

    public void checkApple() {
        // 🆕 CORREGIDO: Subir nivel CADA 50 PUNTOS EXACTOS
        if (x[0] == appleX && y[0] == appleY) {
            bodyParts++;
            applesEaten++;
            int pointsPerApple = 10 + (level * 5);
            score += pointsPerApple;
            newApple();
            
            // VERIFICAR NIVEL DESPUÉS de sumar puntos
            if (score % 50 == 0 && score > 0 && level < DELAYS.length) {
                level++;
                timer.setDelay(DELAYS[level - 1]);
                spawnTraps();
                showMessage("🎉 NIVEL " + level + " DESBLOQUEADO!");
            }
            return;
        }
        
        for (Trap trap : traps) {
            if (x[0] == trap.x && y[0] == trap.y) {
                trapsEaten++;
                running = false;
                saveScore();
                return;
            }
        }
    }

    public void checkCollisions() {
        for (int i = bodyParts; i > 0; i--) {
            if (x[0] == x[i] && y[0] == y[i]) {
                running = false;
                saveScore();
                return;
            }
        }
    }

    private void saveScore() {
        long elapsed = (System.currentTimeMillis() - startTime - totalPaused) / 1000;
        ScoreEntry entry = new ScoreEntry(score, bodyParts, applesEaten, trapsEaten, level, (int)elapsed);
        leaderboard.add(entry);
        
        // Bubble sort
        for (int i = 0; i < leaderboard.size(); i++) {
            for (int j = i + 1; j < leaderboard.size(); j++) {
                if (leaderboard.get(i).score < leaderboard.get(j).score) {
                    ScoreEntry temp = leaderboard.get(i);
                    leaderboard.set(i, leaderboard.get(j));
                    leaderboard.set(j, temp);
                }
            }
        }
        
        if (leaderboard.size() > MAX_SCORES) {
            leaderboard = leaderboard.subList(0, MAX_SCORES);
        }
        saveLeaderboard();
    }

   private void loadLeaderboard() {
    try {
        File file = new File(LEADERBOARD_FILE);
        if (!file.exists()) {
            saveLeaderboard(); // Crear archivo vacío
            return;
        }
        BufferedReader br = new BufferedReader(new FileReader(LEADERBOARD_FILE));
        leaderboard.clear();
        String line;
        while ((line = br.readLine()) != null) {
            String[] p = line.split(",");
            if (p.length == 6) {
                try {
                    leaderboard.add(new ScoreEntry(
                            Integer.parseInt(p[0]), Integer.parseInt(p[1]),
                            Integer.parseInt(p[2]), Integer.parseInt(p[3]),
                            Integer.parseInt(p[4]), Integer.parseInt(p[5])
                    ));
                } catch (NumberFormatException e) {
                    // CORRECCIÓN: Informa sobre líneas corruptas
                    System.err.println("Error de formato en línea del leaderboard: " + line);
                }
            }
        }
        br.close();
    } catch (IOException e) {
        System.err.println("Error al cargar el leaderboard: " + e.getMessage());
        e.printStackTrace();
        leaderboard.clear();
    }
}

 private void saveLeaderboard() {
    try {
        PrintWriter pw = new PrintWriter(new FileWriter(LEADERBOARD_FILE));
        for (ScoreEntry e : leaderboard) {
            pw.println(e.score + "," + e.size + "," + e.apples + "," + e.traps + "," + e.level + "," + e.time);
        }
        pw.close();
    } catch (IOException e) {
        System.err.println("Error al guardar el leaderboard: " + e.getMessage());
        e.printStackTrace(); 
    }
}

    public void gameOver(Graphics g) {
        g.setColor(new Color(0, 0, 0, 200));
        g.fillRect(0, 0, WIDTH, HEIGHT);
        g.setColor(Color.RED);
        g.setFont(new Font("Arial", Font.BOLD, 90));
        FontMetrics fm = getFontMetrics(g.getFont());
        g.drawString("GAME OVER", (WIDTH - fm.stringWidth("GAME OVER")) / 2, HEIGHT / 2 - 30);
        g.setColor(Color.WHITE);
        g.setFont(new Font("Arial", Font.BOLD, 28));
        fm = getFontMetrics(g.getFont());
        String stats = "Puntos: " + score + " | Manzanas: " + applesEaten + " | Trampas: " + traps.size();
        g.drawString(stats, (WIDTH - fm.stringWidth(stats)) / 2, HEIGHT / 2 + 30);
        g.setFont(new Font("Arial", Font.BOLD, 32));
        g.drawString("ESPACIO = Reiniciar | L = Leaderboard | S = Guardar", 
                    (WIDTH - getFontMetrics(g.getFont()).stringWidth("ESPACIO = Reiniciar | L = Leaderboard | S = Guardar")) / 2, 
                    HEIGHT / 2 + 100);
    }

    public void gameWin(Graphics g) {
        running = false;
        timer.stop();
        saveScore();
        g.setColor(new Color(0, 0, 0, 200));
        g.fillRect(0, 0, WIDTH, HEIGHT);
        g.setColor(Color.YELLOW);
        g.setFont(new Font("Arial", Font.BOLD, 80));
        FontMetrics fm = getFontMetrics(g.getFont());
        g.drawString("VICTORIA TOTAL!", (WIDTH - fm.stringWidth("VICTORIA TOTAL!")) / 2, HEIGHT / 2);
        g.setColor(Color.WHITE);
        g.setFont(new Font("Arial", Font.BOLD, 30));
        g.drawString("¡Llenaste el tablero con " + score + " puntos!", 
                    (WIDTH - getFontMetrics(g.getFont()).stringWidth("¡Llenaste el tablero con " + score + " puntos!")) / 2, 
                    HEIGHT / 2 + 80);
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if (running && !paused) {
            move();
            checkApple();
            checkCollisions();
        }
        repaint();
    }

    @Override
    public void keyPressed(KeyEvent e) {
        int key = e.getKeyCode();
        
        if (showLeaderboard) {
            if (key == KeyEvent.VK_L || key == KeyEvent.VK_ESCAPE) {
                showLeaderboard = false;
                repaint();
            } else if (key == KeyEvent.VK_SPACE) {
                startGame();
            }
            return;
        }
        
        if (running && !paused) {
            if (key == KeyEvent.VK_LEFT && direction != 'R') direction = 'L';
            else if (key == KeyEvent.VK_RIGHT && direction != 'L') direction = 'R';
            else if (key == KeyEvent.VK_UP && direction != 'D') direction = 'U';
            else if (key == KeyEvent.VK_DOWN && direction != 'U') direction = 'D';
        }
        
        if (key == KeyEvent.VK_S) saveGame();
        else if (key == KeyEvent.VK_C) loadGame();
        else if (key == KeyEvent.VK_P) {
            if (running) {
                paused = !paused;
                if (paused) { pauseTime = System.currentTimeMillis(); timer.stop(); }
                else { totalPaused += System.currentTimeMillis() - pauseTime; timer.start(); }
            }
        } else if (key == KeyEvent.VK_L) {
            showLeaderboard = true;
            repaint();
        } else if (key == KeyEvent.VK_SPACE && !running) {
            startGame();
        }
    }

    @Override public void keyTyped(KeyEvent e) {}
    @Override public void keyReleased(KeyEvent e) {}

    private static class Trap { int x, y; Trap(int x, int y) { this.x = x; this.y = y; } }
    private static class ScoreEntry {
        int score, size, apples, traps, level, time;
        ScoreEntry(int s, int sz, int a, int tr, int l, int t) {
            score = s; size = sz; apples = a; traps = tr; level = l; time = t;
        }
    }

    public static void main(String[] args) {
        JFrame frame = new JFrame("Snake Pro - 800x800");
        SnakeGame game = new SnakeGame();
        frame.add(game);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setResizable(false);
        frame.pack();
        frame.setLocationRelativeTo(null);
        frame.setVisible(true);
        game.requestFocusInWindow();
    }
}