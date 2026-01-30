import numpy as np
import pickle
import random
import os

class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.3):
        self.q_table = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        
    def get_state_key(self, board):
        """Convierte el tablero a una clave para la tabla Q"""
        return ''.join([''.join(row) for row in board])
    
    def get_available_actions(self, board):
        """Obtiene todas las acciones posibles (casillas vacías)"""
        actions = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    actions.append((i, j))
        return actions
    
    def choose_action(self, board, training=True):
        """Selecciona una acción usando estrategia epsilon-greedy"""
        state = self.get_state_key(board)
        available_actions = self.get_available_actions(board)
        
        if not available_actions:
            return None
        
        # Durante entrenamiento: usar epsilon-greedy
        if training:
            if random.random() < self.epsilon:
                return random.choice(available_actions)
        # Durante juego: solo explotar (mejor acción)
        
        # Inicializar valores si no existen en la tabla
        if state not in self.q_table:
            self.q_table[state] = {}
        
        best_action = None
        best_value = -float('inf')
        
        for action in available_actions:
            action_key = f"{action[0]},{action[1]}"
            if action_key not in self.q_table[state]:
                self.q_table[state][action_key] = 0
            
            if self.q_table[state][action_key] > best_value:
                best_value = self.q_table[state][action_key]
                best_action = action
        
        # Si no hay acción mejor, elegir aleatoria
        if best_action is None:
            return random.choice(available_actions)
        
        return best_action
    
    def update_q_value(self, board, action, reward, next_board, done):
        """Actualiza el valor Q usando la ecuación de Bellman"""
        state = self.get_state_key(board)
        next_state = self.get_state_key(next_board)
        action_key = f"{action[0]},{action[1]}"
        
        # Inicializar si no existen
        if state not in self.q_table:
            self.q_table[state] = {}
        if action_key not in self.q_table[state]:
            self.q_table[state][action_key] = 0
        
        # Obtener el mejor valor Q del siguiente estado
        if done:
            max_next_q = 0
        else:
            max_next_q = -float('inf')
            if next_state in self.q_table:
                for a_key in self.q_table[next_state]:
                    if self.q_table[next_state][a_key] > max_next_q:
                        max_next_q = self.q_table[next_state][a_key]
            else:
                max_next_q = 0
        
        # Ecuación de Bellman
        current_q = self.q_table[state][action_key]
        new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        self.q_table[state][action_key] = new_q
    
    def save_q_table(self, filename='q_table_20000.pkl'):
        """Guarda la tabla Q en un archivo"""
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)
        print(f"Tabla Q guardada en {filename} ({len(self.q_table)} estados)")
    
    def load_q_table(self, filename='q_table_20000.pkl'):
        """Carga la tabla Q desde un archivo"""
        try:
            with open(filename, 'rb') as f:
                self.q_table = pickle.load(f)
            print(f"Tabla Q cargada: {len(self.q_table)} estados")
            return True
        except:
            print(f"No se pudo cargar {filename}")
            return False

class TicTacToeGame:
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reinicia el juego"""
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.done = False
        self.winner = None
        return self.board.copy()
    
    def make_move(self, row, col, player):
        """Realiza un movimiento"""
        if self.board[row][col] == ' ' and not self.done:
            self.board[row][col] = player
            return True
        return False
    
    def check_winner(self):
        """Verifica si hay ganador"""
        # Filas
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return self.board[i][0]
        
        # Columnas
        for i in range(3):
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                return self.board[0][i]
        
        # Diagonales
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]
        
        # Empate
        if all(self.board[i][j] != ' ' for i in range(3) for j in range(3)):
            return 'Tie'
        
        return None
    
    def get_available_moves(self):
        """Obtiene movimientos disponibles"""
        moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    moves.append((i, j))
        return moves
    
    def step(self, row, col, player):
        """Ejecuta un paso del juego"""
        success = self.make_move(row, col, player)
        
        if not success:
            return self.board.copy(), -10, True
        
        # Verificar estado del juego
        winner = self.check_winner()
        reward = 0
        done = False
        
        if winner is not None:
            done = True
            if winner == 'O':  # Agente gana
                reward = 1
            elif winner == 'X':  # Agente pierde
                reward = -1
            elif winner == 'Tie':  # Empate
                reward = 0.5  # Recompensa positiva por empate
        
        # Cambiar jugador
        self.current_player = 'O' if player == 'X' else 'X'
        
        return self.board.copy(), reward, done

def get_opponent_move(board):
    """Movimiento del oponente (aleatorio pero inteligente)"""
    available = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                available.append((i, j))
    
    # Priorizar centro y esquinas
    if (1, 1) in available:
        return (1, 1)
    
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    for corner in corners:
        if corner in available:
            return corner
    
    return random.choice(available) if available else None

def train_agent_with_progress(episodes=20000):
    """Entrena el agente Q-Learning con barra de progreso"""
    agent = QLearningAgent(alpha=0.1, gamma=0.9, epsilon=0.3)
    game = TicTacToeGame()
    
    print("\n" + "="*60)
    print("ENTRENAMIENTO Q-LEARNING - 20,000 EPISODIOS")
    print("="*60)
    
    wins = 0
    losses = 0
    ties = 0
    
    for episode in range(episodes):
        board = game.reset()
        done = False
        total_reward = 0
        
        # Reducir epsilon gradualmente (0.3 -> 0.01)
        agent.epsilon = max(0.01, 0.3 * (1 - episode / episodes))
        
        while not done:
            # Turno del agente (O)
            action = agent.choose_action(board, training=True)
            if action is None:
                break
            
            # Guardar estado actual
            old_board = [row[:] for row in board]
            
            # Realizar movimiento
            board, reward, done = game.step(action[0], action[1], 'O')
            total_reward += reward
            
            # Actualizar Q-value
            agent.update_q_value(old_board, action, reward, board, done)
            
            if done:
                winner = game.check_winner()
                if winner == 'O':
                    wins += 1
                elif winner == 'X':
                    losses += 1
                elif winner == 'Tie':
                    ties += 1
                break
            
            # Turno del oponente (X) - más inteligente
            opponent_action = get_opponent_move(board)
            if opponent_action:
                board, reward, done = game.step(opponent_action[0], opponent_action[1], 'X')
        
        # Mostrar barra de progreso cada 100 episodios
        if (episode + 1) % 100 == 0:
            progress = (episode + 1) / episodes * 100
            bar_length = 50
            filled = int(bar_length * progress / 100)
            bar = '█' * filled + '░' * (bar_length - filled)
            
            win_rate = wins / (episode + 1) * 100 if (episode + 1) > 0 else 0
            loss_rate = losses / (episode + 1) * 100 if (episode + 1) > 0 else 0
            tie_rate = ties / (episode + 1) * 100 if (episode + 1) > 0 else 0
            
            print(f"\rProgreso: |{bar}| {progress:.1f}% ({episode + 1}/{episodes}) | "
                  f"Victorias: {win_rate:.1f}% | Derrotas: {loss_rate:.1f}% | Empates: {tie_rate:.1f}%", end="")
    
    # Guardar la tabla Q entrenada
    agent.save_q_table('q_table_20000.pkl')
    
    print(f"\n\n{'='*60}")
    print("ENTRENAMIENTO COMPLETADO")
    print(f"{'='*60}")
    print(f"Total episodios: {episodes}")
    print(f"Tamaño tabla Q: {len(agent.q_table)} estados")
    print(f"Estados finales aprendidos: {len(agent.q_table)}")
    print(f"Victorias finales: {wins} ({wins/episodes*100:.1f}%)")
    print(f"Derrotas finales: {losses} ({losses/episodes*100:.1f}%)")
    print(f"Empates finales: {ties} ({ties/episodes*100:.1f}%)")
    
    return agent

def test_agent_comprehensively(agent, num_games=1000):
    """Prueba del agente entrenado"""
    print(f"\n{'='*60}")
    print("PRUEBA DEL AGENTE")
    print(f"{'='*60}")
    
    game = TicTacToeGame()
    
    # Diferentes tipos de oponentes
    opponents = [
        ("Aleatorio", lambda board: random.choice([(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']) 
         if any(board[i][j] == ' ' for i in range(3) for j in range(3)) else None),
        
        ("Inteligente", get_opponent_move),
        
        ("Centro-Primero", lambda board: 
         (1, 1) if board[1][1] == ' ' else 
         random.choice([(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']) 
         if any(board[i][j] == ' ' for i in range(3) for j in range(3)) else None),
    ]
    
    for opponent_name, opponent_func in opponents:
        print(f"\nProbando contra: {opponent_name}")
        
        wins = 0
        losses = 0
        ties = 0
        
        for _ in range(num_games):
            board = game.reset()
            done = False
            
            # El agente siempre juega como 'O'
            while not done:
                # Turno del agente (O)
                action = agent.choose_action(board, training=False)
                if action is None:
                    break
                
                board, _, done = game.step(action[0], action[1], 'O')
                
                if done:
                    winner = game.check_winner()
                    if winner == 'O':
                        wins += 1
                    elif winner == 'X':
                        losses += 1
                    elif winner == 'Tie':
                        ties += 1
                    break
                
                # Turno del oponente (X)
                opponent_action = opponent_func(board)
                if opponent_action:
                    board, _, done = game.step(opponent_action[0], opponent_action[1], 'X')
                
                if done:
                    winner = game.check_winner()
                    if winner == 'O':
                        wins += 1
                    elif winner == 'X':
                        losses += 1
                    elif winner == 'Tie':
                        ties += 1
                    break
        
        print(f"  Victorias: {wins} ({wins/num_games*100:.1f}%)")
        print(f"  Derrotas: {losses} ({losses/num_games*100:.1f}%)")
        print(f"  Empates: {ties} ({ties/num_games*100:.1f}%)")

def main():
    """Función principal del entrenamiento"""
    print("\n" + "="*60)
    print("SISTEMA DE APRENDIZAJE POR REFUERZO - TRES EN RAYA")
    print("="*60)
    
    # Verificar si ya existe un modelo entrenado
    if os.path.exists('q_table_20000.pkl'):
        print("\n⚠️  Ya existe un modelo entrenado (q_table_20000.pkl)")
        response = input("¿Deseas reentrenar desde cero? (s/n): ").lower()
        
        if response != 's':
            print("Cargando modelo existente...")
            agent = QLearningAgent()
            if agent.load_q_table('q_table_20000.pkl'):
                test_agent_comprehensively(agent)
                return
        else:
            print("Iniciando entrenamiento desde cero...")
    
    # Entrenar el agente
    trained_agent = train_agent_with_progress(episodes=20000)
    
    # Probar el agente
    test_agent_comprehensively(trained_agent, num_games=1000)
    
    print(f"\n{'='*60}")
    print("INSTRUCCIONES PARA JUGAR:")
    print(f"{'='*60}")
    print("1. El agente ha sido entrenado con 20,000 episodios")
    print("2. Para jugar contra él, ejecuta 'interfaz.py'")
    print("3. El archivo 'q_table_20000.pkl' contiene el conocimiento")
    print("4. El agente juega como 'O', tú juegas como 'X'")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()