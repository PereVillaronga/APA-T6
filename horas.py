import re

def normalizaHoras(ficText, ficNorm):
    """
    Lee el fichero ficText, busca expresiones horarias válidas y las escribe
    normalizadas en formato HH:MM en el fichero ficNorm. Las expresiones
    incorrectas se mantienen intactas.
    """
    # 1. Patrón estándar: tipo 18:30 o 4:45 (excluye un solo dígito en minutos como 17:5)
    patron_estandar = re.compile(r'\b(\d{1,2}):(\d{2})\b')
    
    # 2. Patrón formato h / hm: tipo 8h, 10h30m, 17h5m
    patron_h_m = re.compile(r'\b(\d{1,2})h(?:(\d{1,2})m)?\b')
    
    # 3. Patrones para expresiones complejas en lenguaje hablado
    patron_noche = re.compile(r'\b12\s+de\s+la\s+noche\b')
    patron_y_media_tarde = re.compile(r'\b(\d{1,2})\s+y\s+media\s+de\s+la\s+tarde\b')
    patron_h_manana = re.compile(r'\b(\d{1,2})h\s+de\s+la\s+mañana\b')
    patron_menos_cuarto = re.compile(r'\b(\d{1,2})\s+menos\s+cuarto\b')

    def procesar_linea(linea):
        # Procesamos primero las formas textuales para evitar que patron_h_m o patron_estandar las rompan
        
        # "12 de la noche" -> 00:00
        linea = patron_noche.sub("00:00", linea)
        
        # "4 y media de la tarde" -> 16:30 (Rango válido de la tarde: 3 a 8)
        def repl_tarde(m):
            h = int(m.group(1))
            if 3 <= h <= 8:
                return f"{h + 12:02d}:30"
            return m.group(0) # Expresiones incorrectas como "17 de la tarde" no se modifican
        linea = patron_y_media_tarde.sub(repl_tarde, linea)
        
        # "7h de la mañana" -> 07:00 (Rango válido de la mañana: 4 a 12)
        def repl_manana(m):
            h = int(m.group(1))
            if 4 <= h <= 12:
                return f"{h:02d}:00"
            return m.group(0)
        linea = patron_h_manana.sub(repl_manana, linea)
        
        # "5 menos cuarto" -> 04:45 (Se devuelve siempre en el rango de 00:00 a 11:59)
        def repl_menos_cuarto(m):
            h = int(m.group(1))
            if 1 <= h <= 12:
                h_real = 11 if h == 12 else h - 1
                return f"{h_real:02d}:45"
            return m.group(0)
        linea = patron_menos_cuarto.sub(repl_menos_cuarto, linea)
        
        # Formato h / hm (ej: 8h -> 08:00, 10h30m -> 10:30, 17h5m -> 17:05)
        def repl_h_m(m):
            h = int(m.group(1))
            m_val = m.group(2)
            minutos = int(m_val) if m_val else 0
            if h <= 23 and minutos <= 59:
                return f"{h:02d}:{minutos:02d}"
            return m.group(0) # Filtra horas incorrectes como 32h31m o 1h78m
        linea = patron_h_m.sub(repl_h_m, linea)
        
        # Formato estándar (ej: 18:30 -> 18:30, 4:45 -> 04:45)
        def repl_est(m):
            h = int(m.group(1))
            minutos = int(m.group(2))
            if h <= 23 and minutos <= 59:
                return f"{h:02d}:{minutos:02d}"
            return m.group(0)
        linea = patron_estandar.sub(repl_est, linea)
        
        return linea

    with open(ficText, 'r', encoding='utf-8') as f_in, open(ficNorm, 'w', encoding='utf-8') as f_out:
        for linea in f_in:
            f_out.write(procesar_linea(linea))


if __name__ == '__main__':
    normalizaHoras('horas.txt', 'horas_norm.txt')
    print("Normalització completada! Revisa el fitxer horas_norm.txt")