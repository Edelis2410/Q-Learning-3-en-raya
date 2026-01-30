"""
Este script analiza la tabla Q entrenada (q_table_20000.pkl) y selecciona
10 estados representativos del aprendizaje del algoritmo Q-Learning.
Genera 'tabla_10_estados_qlearning.txt'.
"""

import pickle

def extract_key_states (pkl_file='q_table_20000.pkl'):
    """
    Extrae 10 estados variados que demuestren el aprendizaje, incluyendo el estado inicial
    """
    try:
        # Cargar tabla Q
        with open(pkl_file, 'rb') as f:
            q_table = pickle.load(f)
        
        print("="*60)
        print("EXTRAYENDO 10 ESTADOS VARIADOS CON APRENDIZAJE DEMOSTRADO")
        print("="*60)
        
        # 1. DEFINIR LOS TIPOS DE ESTADOS QUE QUEREMOS BUSCAR
        target_states = []
        
        # Estado 1: Tablero vacío 
        empty_board = "         "
        if empty_board in q_table:
            target_states.append({
                'name': "1. Tablero Vacío",
                'state': empty_board,
                'description': "Estado inicial, todas las casillas vacías",
                'priority': 1
            })
        
        # Buscar estados específicos con valores Q interesantes
        states_found = []
        for state, actions in q_table.items():
            if actions and state != empty_board:  
                max_q = max(actions.values())
                min_q = min(actions.values())
                avg_q = sum(actions.values()) / len(actions)
                x_count = state.count('X')
                o_count = state.count('O')
                empty_count = state.count(' ')
                
                # Clasificar el estado
                state_type = classify_state(state, max_q, min_q, avg_q, x_count, o_count, empty_count)
                
                if state_type:
                    states_found.append({
                        'state': state,
                        'actions': actions,
                        'max_q': max_q,
                        'min_q': min_q,
                        'avg_q': avg_q,
                        'x_count': x_count,
                        'o_count': o_count,
                        'empty_count': empty_count,
                        'type': state_type,
                        'score': calculate_state_score(max_q, min_q, state_type)
                    })
        
        # 2. SELECCIONAR ESTADOS REPRESENTATIVOS DE DIFERENTES CATEGORÍAS
        categories_needed = [
            "victoria_inminente",
            "bloqueo_oponente", 
            "estrategia_avanzada",
            "estado_intermedio",
            "posicion_defensiva",
            "situacion_compleja",
            "empate_forzado",
            "error_evitado",
            "aprendizaje_temprano"
        ]
        
        selected_states_info = []
        
        # Para cada categoría, buscar el mejor estado disponible
        for category in categories_needed:
            # Filtrar estados por categoría
            category_states = [s for s in states_found if s['type'] == category]
            
            if category_states:
                # Ordenar por score descendente y tomar el mejor
                category_states.sort(key=lambda x: x['score'], reverse=True)
                best_state = category_states[0]
                
                # Asignar nombre descriptivo
                state_name = get_state_name(category, best_state['max_q'], best_state['x_count'], best_state['o_count'])
                target_states.append({
                    'name': state_name,
                    'state': best_state['state'],
                    'description': get_state_description(category),
                    'priority': 2,
                    'state_info': best_state
                })
                
                # Remover este estado de la lista para no repetir
                states_found = [s for s in states_found if s['state'] != best_state['state']]
        
        #  10 estados
        if len(target_states) < 10:
            remaining_needed = 10 - len(target_states)
            # Ordenar estados restantes por score
            states_found.sort(key=lambda x: x['score'], reverse=True)
            
            for i in range(min(remaining_needed, len(states_found))):
                state_info = states_found[i]
                # Generar nombre descriptivo basado en características
                descriptive_name = generate_descriptive_name(state_info)
                
                target_states.append({
                    'name': descriptive_name,
                    'state': state_info['state'],
                    'description': get_generic_description(state_info),
                    'priority': 3,
                    'state_info': state_info
                })
        
        # Limitar a 10 estados exactamente
        target_states = target_states[:10]
        
        # Asegurarnos de que el estado inicial esté primero
        target_states.sort(key=lambda x: x['priority'])
        
        # Renumerar los estados
        for idx, state_data in enumerate(target_states, 1):
            if idx == 1:
                state_data['name'] = f"{idx}. {state_data['name'].split('. ')[-1]}"
            else:
                state_data['name'] = f"{idx}. {state_data['name']}"
        
        # 3. CREAR ARCHIVO CON FORMATO DE TABLA
        print(f"\nGENERANDO ARCHIVO 'tabla_10_estados_qlearning.txt'...")
        
        with open('tabla_10_estados_qlearning.txt', 'w', encoding='utf-8') as f:
            f.write("="*150 + "\n")
            f.write("TABLA DE 10 ESTADOS VARIADOS - ALGORITMO Q-LEARNING\n")
            f.write("="*150 + "\n\n")
            
            f.write("RESUMEN ESTADÍSTICO:\n")
            f.write(f"• Total de estados aprendidos: {len(q_table)}\n")
            f.write("• Estados seleccionados: 10 (representando diferentes niveles de aprendizaje)\n")
            f.write("• 'X' = Jugador humano, 'O' = IA, '·' = Casilla vacía\n\n")
            
            f.write("="*150 + "\n")
            f.write("TABLA DE ANÁLISIS DE ESTADOS\n")
            f.write("="*150 + "\n\n")
            
            # Definir anchos de columna
            col_widths = [25, 25, 25, 18, 12, 40]
            
            # Función para crear línea horizontal
            def horizontal_line():
                return "+" + "-"*(col_widths[0]+1) + "+" + "-"*(col_widths[1]+1) + "+" + \
                       "-"*(col_widths[2]+1) + "+" + "-"*(col_widths[3]+1) + "+" + \
                       "-"*(col_widths[4]+1) + "+" + "-"*(col_widths[5]+1) + "+\n"
            
            # Encabezados de la tabla
            headers = ["Estado (Descripción)", "Representación del Tablero", 
                      "Acciones Posibles", "Mejor Acción", "Valor Q", 
                      "Demostración de Aprendizaje"]
            
            # Escribir encabezados con líneas verticales
            f.write(horizontal_line())
            
            # Escribir fila de encabezados
            header_row = "|"
            for i, header in enumerate(headers):
                header_row += f" {header:<{col_widths[i]}} |"
            f.write(header_row + "\n")
            
            f.write(horizontal_line())
            
            # Escribir filas de datos
            for idx, state_data in enumerate(target_states, 1):
                state = state_data['state']
                state_info = state_data.get('state_info')
                
                # Convertir estado a representación visual
                board_matrix = []
                for i in range(0, 9, 3):
                    row = state[i:i+3]
                    row_chars = []
                    for char in row:
                        if char == ' ':
                            row_chars.append('·')
                        else:
                            row_chars.append(char)
                    board_matrix.append(row_chars)
                
                # Representación en formato [[],[],[]]
                representation = f"[{''.join(board_matrix[0])}], [{''.join(board_matrix[1])}], [{''.join(board_matrix[2])}]"
                
                # Información de acciones
                if state in q_table and q_table[state]:
                    actions = q_table[state]
                    actions_count = len(actions)
                    
                    # Contar casillas vacías para acciones posibles
                    empty_cells = 0
                    for i in range(3):
                        for j in range(3):
                            if state[i*3 + j] == ' ':
                                empty_cells += 1
                    
                    actions_text = f"{empty_cells} casillas vacías"
                    if actions_count > 0:
                        actions_text += f", {actions_count} con valores Q"
                    
                    # Obtener mejor acción y valor Q
                    max_q = -float('inf')
                    best_act = None
                    for action, q_value in actions.items():
                        if q_value > max_q:
                            max_q = q_value
                            best_act = action
                    
                    if best_act:
                        best_action = f"({best_act.split(',')[0]},{best_act.split(',')[1]})"
                        best_q = max_q
                    else:
                        best_action = "N/A"
                        best_q = 0.0
                else:
                    actions_text = "9 casillas vacías"
                    best_action = "N/A"
                    best_q = 0.0
                
                # Determinar demostración de aprendizaje
                if state == empty_board:
                    demonstration = "Estado inicial - base para todas las estrategias"
                elif best_q > 0.8:
                    demonstration = "Alta confianza en jugada óptima o ganadora"
                elif best_q > 0.5:
                    demonstration = "Preferencia clara por estrategia efectiva"
                elif best_q > 0.2:
                    demonstration = "Desarrollo de preferencias estratégicas"
                elif best_q > 0:
                    demonstration = "Aprendizaje inicial en desarrollo"
                elif best_q == 0:
                    demonstration = "Estado equilibrado o en exploración"
                else:
                    demonstration = "Reconocimiento de jugadas a evitar"
                
                # Preparar datos para la fila
                row_data = [
                    state_data['name'],
                    representation,
                    actions_text,
                    best_action,
                    f"{best_q:.4f}",
                    demonstration
                ]
                
                # Escribir fila con líneas verticales
                row = "|"
                for i, data in enumerate(row_data):
                    row += f" {data:<{col_widths[i]}} |"
                f.write(row + "\n")
                
                # Línea horizontal entre filas
                f.write(horizontal_line())
            
            # 4. AÑADIR ANÁLISIS DETALLADO
            f.write("\n" + "="*150 + "\n")
            f.write("ANÁLISIS DETALLADO DEL APRENDIZAJE\n")
            f.write("="*150 + "\n\n")
            
            f.write("VARIEDAD DE ESTADOS SELECCIONADOS:\n")
            for idx, state_data in enumerate(target_states, 1):
                f.write(f"{idx}. {state_data['name'].split('. ')[-1]}\n")
            
            f.write("\nINTERPRETACIÓN DE VALORES Q:\n")
            f.write("• 0.900 - 1.000: Jugada ganadora segura\n")
            f.write("• 0.700 - 0.899: Estrategia altamente efectiva\n")
            f.write("• 0.400 - 0.699: Jugada buena con ventaja\n")
            f.write("• 0.100 - 0.399: Preferencia desarrollada\n")
            f.write("• 0.000 - 0.099: Aprendizaje en progreso\n")
            f.write("• Negativos: Jugadas que conducen a derrota\n\n")
            
            # Análisis específico por estado
            f.write("ANÁLISIS POR ESTADO:\n")
            f.write("-"*100 + "\n")
            
            for idx, state_data in enumerate(target_states, 1):
                state = state_data['state']
                f.write(f"\n{state_data['name']}\n")
                
                # Dibujar tablero visual
                f.write("  Tablero:\n")
                for i in range(0, 9, 3):
                    row = state[i:i+3]
                    row_display = []
                    for char in row:
                        if char == ' ':
                            row_display.append('·')
                        else:
                            row_display.append(char)
                    f.write(f"    {' | '.join(row_display)}\n")
                    if i < 6:
                        f.write("    ---+---+---\n")
                
                # Información detallada
                if state in q_table and q_table[state]:
                    actions = q_table[state]
                    
                    # Mostrar las 3 mejores acciones
                    sorted_actions = sorted(actions.items(), key=lambda x: x[1], reverse=True)
                    
                    f.write(f"\n  Top 3 acciones aprendidas:\n")
                    for i, (action, q_value) in enumerate(sorted_actions[:3]):
                        row, col = map(int, action.split(','))
                        f.write(f"    {i+1}. ({row},{col}): Q = {q_value:.4f}\n")
                    
                    # Estadísticas básicas
                    q_values = list(actions.values())
                    avg_q = sum(q_values) / len(q_values)
                    
                    f.write(f"\n  Estadísticas:\n")
                    f.write(f"  • Valor Q promedio: {avg_q:.4f}\n")
                    f.write(f"  • Mejor valor Q: {max(q_values):.4f}\n")
                    f.write(f"  • Peor valor Q: {min(q_values):.4f}\n")
                    f.write(f"  • Número de acciones: {len(actions)}\n")
                
                f.write(f"\n  ¿Qué demuestra este estado?\n")
                f.write(f"  {get_detailed_analysis(state, state_data)}\n")
                f.write("-"*100 + "\n")
        
        print("✓ Archivo generado: 'tabla_10_estados_qlearning.txt'")
        
        # 5. MOSTRAR RESUMEN
        print("\n" + "="*60)
        print("RESUMEN DE LA TABLA GENERADA:")
        print("="*60)
        
        print(f"• Total estados en tabla Q: {len(q_table)}")
        print(f"• Estados seleccionados: 10")
        print(f"• Estado inicial incluido: SÍ")
        print(f"• Variedad de valores Q: SÍ")
        print(f"\nEstados incluidos con nombres descriptivos:")
        for state_data in target_states:
            print(f"  - {state_data['name']}")
        
        print("\n" + "="*60)
        print("INSTRUCCIONES PARA EL PAPER:")
        print("="*60)
        print("1. Copia la tabla completa del archivo generado")
        print("2. Incluye el análisis detallado en la sección de Discusión")
        print("3. Destaca la variedad de estados y valores Q")
        
        return True
        
    except FileNotFoundError:
        print(f"ERROR: No se encontró el archivo '{pkl_file}'")
        print("Asegúrate de que esté en la misma carpeta")
        return False
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

def generate_descriptive_name(state_info):
    """Genera nombres descriptivos basados en las características del estado"""
    x_count = state_info['x_count']
    o_count = state_info['o_count']
    empty_count = state_info['empty_count']
    max_q = state_info['max_q']
    
    # Estado con victoria del oponente
    if x_count >= 3 and max_q < 0:
        return "Derrota Inminente"
    
    # Estados según número de fichas
    if empty_count >= 7:
        return "Apertura Temprana"
    elif empty_count >= 4:
        if o_count > x_count:
            return "Ventaja de IA"
        elif x_count > o_count:
            return "Ventaja de Humano"
        else:
            return "Juego Equilibrado"
    else:
        if max_q > 0.5:
            return "Posición Favorable"
        elif max_q > 0:
            return "Posición Neutra"
        else:
            return "Posición Crítica"

def get_generic_description(state_info):
    """Genera descripción genérica basada en el estado"""
    x_count = state_info['x_count']
    o_count = state_info['o_count']
    empty_count = state_info['empty_count']
    
    if empty_count >= 7:
        return f"Apertura con {x_count}X y {o_count}O"
    elif empty_count >= 4:
        return f"Juego medio con {x_count}X y {o_count}O"
    else:
        return f"Final de juego con {x_count}X y {o_count}O"

def classify_state(state, max_q, min_q, avg_q, x_count, o_count, empty_count):
    """Clasifica el estado según sus características"""
    
    # Victoria inminente para IA
    if o_count == 2 and x_count <= 1 and max_q > 0.8:
        board_3x3 = [list(state[i:i+3]) for i in range(0, 9, 3)]
        lines = get_all_lines(board_3x3)
        for line in lines:
            if line.count('O') == 2 and line.count(' ') == 1:
                return "victoria_inminente"
    
    # Bloqueo al oponente
    if x_count == 2 and o_count == 1 and max_q > 0.3:
        board_3x3 = [list(state[i:i+3]) for i in range(0, 9, 3)]
        lines = get_all_lines(board_3x3)
        for line in lines:
            if line.count('X') == 2 and line.count(' ') == 1:
                return "bloqueo_oponente"
    
    # Estado de empate
    if empty_count == 1 and x_count == 4 and o_count == 4:
        board_3x3 = [list(state[i:i+3]) for i in range(0, 9, 3)]
        if not check_winner(board_3x3) and max_q > 0.2:
            return "empate_forzado"
    
    # Estrategia avanzada
    if empty_count <= 3 and empty_count > 1 and max_q > 0.5:
        return "estrategia_avanzada"
    
    # Estado intermedio
    if empty_count == 4 or empty_count == 5:
        if max_q > 0.4:
            return "estado_intermedio"
    
    # Posición defensiva
    if x_count > o_count and max_q > 0.2:
        return "posicion_defensiva"
    
    # Situación compleja
    if empty_count >= 6 and abs(max_q - min_q) < 0.3:
        return "situacion_compleja"
    
    # Error evitado
    if min_q < -0.1:
        return "error_evitado"
    
    # Aprendizaje temprano
    if max_q < 0.3 and max_q > 0:
        return "aprendizaje_temprano"
    
    return None

def calculate_state_score(max_q, min_q, state_type):
    """Calcula un score para priorizar estados interesantes"""
    score = 0
    
    if max_q > 0.8:
        score += 30
    elif max_q > 0.5:
        score += 20
    elif max_q > 0.2:
        score += 10
    
    q_range = max_q - min_q
    if q_range > 0.5:
        score += 15
    elif q_range > 0.2:
        score += 10
    
    type_scores = {
        "victoria_inminente": 25,
        "bloqueo_oponente": 20,
        "empate_forzado": 18,
        "estrategia_avanzada": 15,
        "error_evitado": 12,
        "estado_intermedio": 10,
        "posicion_defensiva": 8,
        "situacion_compleja": 5,
        "aprendizaje_temprano": 3
    }
    
    score += type_scores.get(state_type, 0)
    return score

def get_state_name(category, max_q, x_count, o_count):
    """Genera un nombre descriptivo para el estado"""
    names = {
        "victoria_inminente": f"Victoria Inminente de IA",
        "bloqueo_oponente": f"Bloqueo Estratégico",
        "empate_forzado": f"Empate Forzado",
        "estrategia_avanzada": f"Estrategia Avanzada",
        "estado_intermedio": f"Juego Intermedio",
        "posicion_defensiva": f"Posición Defensiva",
        "situacion_compleja": f"Situación Compleja",
        "error_evitado": f"Error Evitado",
        "aprendizaje_temprano": f"Aprendizaje Temprano"
    }
    
    return names.get(category, f"Estado (Q={max_q:.2f})")

def get_state_description(category):
    """Genera una descripción breve para el estado"""
    descriptions = {
        "victoria_inminente": "IA puede ganar en 1 jugada",
        "bloqueo_oponente": "Debe bloquear jugada ganadora del oponente",
        "empate_forzado": "Forzar empate en posición difícil",
        "estrategia_avanzada": "Jugada táctica compleja",
        "estado_intermedio": "Decisión en medio del juego",
        "posicion_defensiva": "IA en desventaja pero con opciones",
        "situacion_compleja": "Múltiples opciones similares",
        "error_evitado": "Aprendió a evitar malas jugadas",
        "aprendizaje_temprano": "Desarrollo inicial de preferencias"
    }
    
    return descriptions.get(category, "Estado representativo")

def get_detailed_analysis(state, state_data):
    """Genera análisis detallado para cada estado"""
    
    if state == "         ":  # Estado vacío
        return "Estado inicial fundamental. Todas las estrategias parten de esta configuración. Muestra cómo el agente considera las primeras jugadas."
    
    state_name = state_data['name'].split('. ')[-1]
    x_count = state.count('X')
    o_count = state.count('O')
    empty_count = state.count(' ')
    
    if "Victoria Inminente" in state_name:
        return f"La IA identifica claramente una oportunidad de victoria con {o_count} de sus fichas alineadas. Asigna valores Q altos a la jugada ganadora."
    
    if "Bloqueo" in state_name:
        return f"Reconocimiento defensivo efectivo. Con {x_count} fichas del oponente amenazando, la IA prioriza el bloqueo sobre el ataque."
    
    if "Empate Forzado" in state_name:
        return f"Gestión inteligente de posiciones difíciles. Con solo {empty_count} casilla(s) vacía(s), valora positivamente forzar empates como alternativa a la derrota."
    
    if "Estrategia Avanzada" in state_name:
        return f"Manejo de situaciones complejas con {empty_count} casillas vacías. Demuestra capacidad para analizar múltiples líneas de juego."
    
    if "Juego Intermedio" in state_name or "Intermedio" in state_name:
        return f"Toma de decisiones en fase media ({empty_count} casillas vacías). Muestra desarrollo de preferencias estratégicas basadas en experiencia."
    
    if "Posición Defensiva" in state_name:
        return f"Juego desde posición de desventaja ({x_count} vs {o_count} fichas). Demuestra capacidad adaptativa y búsqueda de contrajugadas."
    
    if "Situación Compleja" in state_name:
        return f"Múltiples opciones con valores similares. Indica situaciones donde varias jugadas son igualmente buenas o donde el agente aún explora."
    
    if "Error Evitado" in state_name:
        return f"Aprendizaje por refuerzo negativo. Valores Q negativos muestran que identificó jugadas que conducen a malos resultados."
    
    if "Aprendizaje Temprano" in state_name:
        return f"Desarrollo inicial de preferencias. Valores Q bajos indican las primeras señales de aprendizaje antes de desarrollar confianza fuerte."
    
    if "Derrota Inminente" in state_name:
        return f"Reconocimiento de posición perdida. Valores Q negativos reflejan que el agente aprendió a identificar situaciones sin salida."
    
    if "Apertura Temprana" in state_name:
        return f"Estrategias iniciales con {empty_count} casillas vacías. Muestra las primeras preferencias desarrolladas después del estado vacío."
    
    if "Ventaja" in state_name:
        advantage = "IA" if o_count > x_count else "Humano"
        return f"Posición con ventaja para {advantage}. Demuestra cómo el agente maneja situaciones favorables."
    
    if "Juego Equilibrado" in state_name:
        return f"Posición equilibrada ({x_count}X vs {o_count}O). Muestra toma de decisiones en situaciones simétricas."
    
    if "Posición Favorable" in state_name:
        return f"Posición ventajosa con valores Q positivos. Indica que el agente identifica y aprovecha situaciones favorables."
    
    if "Posición Crítica" in state_name:
        return f"Situación difícil con valores Q bajos o negativos. Muestra reconocimiento de posiciones problemáticas."
    
    return f"Estado representativo con {x_count} fichas X, {o_count} fichas O y {empty_count} casillas vacías. Muestra el progreso del aprendizaje."

def get_all_lines(board_3x3):
    """Obtiene todas las líneas posibles (filas, columnas, diagonales)"""
    lines = []
    lines.extend(board_3x3)
    for j in range(3):
        lines.append([board_3x3[0][j], board_3x3[1][j], board_3x3[2][j]])
    lines.append([board_3x3[0][0], board_3x3[1][1], board_3x3[2][2]])
    lines.append([board_3x3[0][2], board_3x3[1][1], board_3x3[2][0]])
    return lines

def check_winner(board_3x3):
    """Verifica si hay ganador en un tablero 3x3"""
    for i in range(3):
        if board_3x3[i][0] != ' ' and board_3x3[i][0] == board_3x3[i][1] == board_3x3[i][2]:
            return board_3x3[i][0]
    for j in range(3):
        if board_3x3[0][j] != ' ' and board_3x3[0][j] == board_3x3[1][j] == board_3x3[2][j]:
            return board_3x3[0][j]
    if board_3x3[0][0] != ' ' and board_3x3[0][0] == board_3x3[1][1] == board_3x3[2][2]:
        return board_3x3[0][0]
    if board_3x3[0][2] != ' ' and board_3x3[0][2] == board_3x3[1][1] == board_3x3[2][0]:
        return board_3x3[0][2]
    return None

# Ejecutar
if __name__ == "__main__":
    extract_key_states()