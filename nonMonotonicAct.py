libros = {
    "science_fiction": ["Dune", "Neuromancer", "Foundation"],
    "romance": ["Pride and Prejudice", "Me Before You", "The Notebook"],
    "mystery": ["Gone Girl", "Sherlock Holmes", "The Girl with the Dragon Tattoo"]
}

def libros_favoritos(preferencias):

#Determina los géneros que le gustan al usuario según sus preferencias.

    if preferencias["romance"] and preferencias["mystery"] and preferencias["science_fiction"]:
        return "Al usuario le gustan todo tipo de libros"
    
    elif preferencias["romance"] and preferencias["mystery"]:
        return "Al usuario le gustan los libros de romance y misterio"
    
    elif preferencias["romance"] and preferencias["science_fiction"]:
        return "Al usuario le gustan los libros de romance y ciencia ficción"
    
    elif preferencias["mystery"] and preferencias["science_fiction"]:
        return "Al usuario le gustan los libros de misterio y ciencia ficción"
    
    elif preferencias["romance"]:
        return "Al usuario le gustan los libros de romance"
    
    elif preferencias["mystery"]:
        return "Al usuario le gustan los libros de misterio"
    
    elif preferencias["science_fiction"]:
        return "Al usuario le gustan los libros de ciencia ficción"
    
    else:
        return "No le gustan los libros"

# Preferencias iniciales del usuario
libros_usuario = {
    "mystery": True,
    "romance": True,
    "science_fiction": False
}

print(libros_favoritos(libros_usuario))  # Output esperado: "Al usuario le gustan los libros de romance y misterio"

# Actualización de preferencias del usuario
libros_usuario.update({
    "mystery": False,
    "romance": False,
    "science_fiction": True
})

print(libros_favoritos(libros_usuario))  # Output esperado: "Al usuario le gustan los libros de ciencia ficción"

class DefaultLogic:
    def __init__(self):
        self.facts = set()
        self.exceptions = set()
    
    def add_fact(self, fact):
        self.facts.add(fact)
        
    def add_exception(self, exception):
        self.exception.add(exception)
    
    def infer(self, entity, default_rule):
        prereq, assumption, conclusion = default_rule
        if prereq in self.facts and assumption not in self.exceptions:
            return conclusion
        return "imposible inferir"
            
logic = DefaultLogic()

logic.add_fact("Es_un_Libro")

default_rule = ("Es_un_Libro", "Libros_son_buenos","Los_libros_te_hacen_mas_inteligente" )

print(logic.infer("Libros", default_rule))

class Circumpscription:
    def __init__(self):
        self.evidence = {}

    def add_fact(self, entity, property, value):
        if entity not in self.evidence:
            self.evidence[entity] = {}
    
            self.evidence[entity][property] = value
    
    def query(self, entity, property):
        return self.evidence.get(entity, {}).get(property, "no se puede inferir")

circ = Circumpscription()

print(circ.query("Santiago", "science_fiction"))  # Output: "No se puede inferir"
print(circ.query("Mariana", "mystery")) 
circ.add_fact("Juan", "science_fiction", True)
