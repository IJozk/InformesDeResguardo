from datetime import time
from typing import List, Dict


def identify_safeguards(engine_events: List[Dict]) -> List[Dict]:
    """
    Identifica resguardos: eventos de motor apagado fuera del horario de turno.
    
    Horario de turno: 08:30 - 19:30
    Resguardo válido si motor apagado y hora < 08:30 o hora >= 19:30
    
    Args:
        engine_events: Lista de eventos con timestamp e is_running
    
    Returns:
        Lista de eventos de resguardo (solo apagados fuera de horario)
    """
    SHIFT_START = time(8, 30)   # 08:30
    SHIFT_END = time(19, 30)    # 19:30
    
    safeguards = []
    
    for event in engine_events:
        # Solo eventos de motor apagado
        if not event['is_running']:
            event_time = event['timestamp'].time()
            
            # Verificar si está fuera del horario de turno
            if event_time < SHIFT_START or event_time >= SHIFT_END:
                safeguards.append({
                    'timestamp': event['timestamp'],
                    'machine_serial': '844585'  # Hardcodeado por ahora
                })
    
    return safeguards