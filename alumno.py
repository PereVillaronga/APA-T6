import re

class Alumno:
    """
    Clase usada para el tratamiento de las notas de los alumnos. Cada uno
    incluye los atributos siguientes:

    numIden:   Número de identificación. Es un número entero que, en caso
               de no indicarse, toma el valor por defecto 'numIden=-1'.
    nombre:    Nombre completo del alumno.
    notas:     Lista de números reales con las distintas notas de cada alumno.
    """

    def __init__(self, nombre, numIden=-1, notas=[]):
        self.numIden = numIden
        self.nombre = nombre
        self.notas = [nota for nota in notas]

    def __add__(self, other):
        """
        Devuelve un nuevo objeto 'Alumno' con una lista de notas ampliada con
        el valor pasado como argumento. De este modo, añadir una nota a un
        Alumno se realiza con la orden 'alumno += nota'.
        """
        return Alumno(self.nombre, self.numIden, self.notas + [other])

    def media(self):
        """
        Devuelve la nota media del alumno.
        """
        return sum(self.notas) / len(self.notas) if self.notas else 0

    def __repr__(self):
        """
        Devuelve la representación 'oficial' del alumno. A partir de copia
        y pega de la cadena obtenida es posible crear un nuevo Alumno idéntico.
        """
        return f'Alumno("{self.nombre}", {self.numIden!r}, {self.notas!r})'

    def __str__(self):
        """
        Devuelve la representación 'bonita' del alumno. Visualiza en tres
        columnas separas por tabulador el número de identificación, el nombre
        completo y la nota media del alumno con un decimal.
        """
        return f'{self.numIden}\t{self.nombre}\t{self.media():.1f}'



def leeAlumnos(ficAlum):
    """
    Llegeix un fitxer de text amb les notes dels alumnes i retorna un
    diccionari amb el nom de cada alumne com a clau i l'objecte Alumno com a valor.

    >>> alumnos = leeAlumnos('alumnos.txt')
    >>> for alumno in alumnos:
    ...     print(alumnos[alumno])
    ...
    171	Blanca Agirrebarrenetse	9.5
    23	Carles Balcells de Lara	4.9
    68	David Garcia Fuster	7.0
    """
    dicc_alumnos = {}
    
    # Explicació de l'expressió regular:
    # ^(\d+)       -> Grup 1: L'identificador (números a l'inici de la línia)
    # \s+          -> Espais en blanc separadors
    # (.+?)        -> Grup 2: El nom (qualsevol caràcter, però perezós per aturar-se abans de les notes)
    # \s+          -> Espais en blanc separadors abans de les notes
    # ([\d\.\s]+)$ -> Grup 3: Les notes (combinació de números, punts decimals i espais fins al final)
    patron = re.compile(r"^(\d+)\s+(.+?)\s+([\d\.\s]+)$")

    with open(ficAlum, 'r', encoding='utf-8') as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
                
            match = patron.match(linea)
            if match:
                numIden = int(match.group(1))
                nombre = match.group(2).strip()
                notas_str = match.group(3).split()
                notas = [float(nota) for nota in notas_str]

                dicc_alumnos[nombre] = Alumno(nombre, numIden, notas)

    return dicc_alumnos

# tests del programa
if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE, verbose=True)
