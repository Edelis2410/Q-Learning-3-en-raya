
import pickle
import random

class QLearningAgent:
    def __init__(self):
        self.q_table = {}
        self.stats = {
            'total_games': 0,
            'wins': 0,
            'losses': 0,
            'ties': 0,
            'states_learned': 0
        }
        
    def load_q_table(self, filename='q_table_20000.pkl'):
        """Carga la tabla Q entrenada"""
        try:
            with open(filename, 'rb') as f:
                self.q_table = pickle.load(f)
            self.stats['states_learned'] = len(self.q_table)
            return True
        except:
            return False
    
    def get_state_key(self, board):
        """Convierte el tablero a una clave para la tabla Q"""
        return ''.join([''.join(row) for row in board])
    
    def get_best_move(self, board):
        """Obtiene el mejor movimiento según la tabla Q"""
        state = self.get_state_key(board)
        
        if state not in self.q_table or not self.q_table[state]:
            return self.get_fallback_move(board)
        
        best_action = None
        best_value = -float('inf')
        
        for action_key in self.q_table[state]:
            value = self.q_table[state][action_key]
            if value > best_value:
                best_value = value
                try:
                    row, col = map(int, action_key.split(','))
                    if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == ' ':
                        best_action = (row, col)
                except:
                    continue
        
        if best_action is None:
            return self.get_fallback_move(board)
        
        return best_action
    
    def get_fallback_move(self, board):
        """Movimiento de respaldo si no hay datos en Q-table"""
        # Intentar ganar
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    if self.check_winner(board) == 'O':
                        board[i][j] = ' '
                        return (i, j)
                    board[i][j] = ' '
        
        # Intentar bloquear
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    if self.check_winner(board) == 'X':
                        board[i][j] = ' '
                        return (i, j)
                    board[i][j] = ' '
        
        # Centro
        if board[1][1] == ' ':
            return (1, 1)
        
        # Esquinas
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        random.shuffle(corners)
        for corner in corners:
            if board[corner[0]][corner[1]] == ' ':
                return corner
        
        # Cualquier movimiento
        available = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    available.append((i, j))
        
        return random.choice(available) if available else None
    
    def check_winner(self, board):
        """Verifica si hay ganador"""
        # Filas
        for i in range(3):
            if board[i][0] != ' ' and board[i][0] == board[i][1] == board[i][2]:
                return board[i][0]
        
        # Columnas
        for j in range(3):
            if board[0][j] != ' ' and board[0][j] == board[1][j] == board[2][j]:
                return board[0][j]
        
        # Diagonales
        if board[0][0] != ' ' and board[0][0] == board[1][1] == board[2][2]:
            return board[0][0]
        if board[0][2] != ' ' and board[0][2] == board[1][1] == board[2][0]:
            return board[0][2]
        
        # Empate
        if all(board[i][j] != ' ' for i in range(3) for j in range(3)):
            return 'Tie'
        
        return None
    
    def update_stats(self, result):
        """Actualiza estadísticas del juego"""
        self.stats['total_games'] += 1
        if result == 'O':
            self.stats['wins'] += 1
        elif result == 'X':
            self.stats['losses'] += 1
        elif result == 'Tie':
            self.stats['ties'] += 1

class GameState:
    """Maneja el estado del juego y coordina con el agente"""
    def __init__(self):
        self.reset()
        self.agent = QLearningAgent()
        
    def reset(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.moves_made = 0
        self.ia_thinking = False
    
    def make_move(self, row, col, player):
        if self.board[row][col] == ' ' and not self.game_over:
            self.board[row][col] = player
            self.moves_made += 1
            return True
        return False
    
    def check_winner(self):
        return self.agent.check_winner(self.board)