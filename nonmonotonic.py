# Base de conocimientos inicial
hechos = {
    "en_escena": True,
    "huellas_en_arma": True,
    "coartada": False  # Inicialmente no hay coartada
}

# Regla deductiva
def es_culpable(hechos):
    if hechos["en_escena"] and hechos["huellas_en_arma"] and not hechos["coartada"]:
        return "Culpable"
    else:
        return "No culpable"

# Conclusión inicial
print("Conclusión inicial:", es_culpable(hechos))

# Nueva información: Coartada verificada
hechos["coartada"] = True

# Conclusión revisada
print("Conclusión revisada:", es_culpable(hechos))

class DefaultLogic:
    def __init__(self):
        self.facts = set()  # Conjunto de hechos conocidos
        self.exceptions = set()  # Conjunto de excepciones

    def add_fact(self, fact):
        """ Agrega un hecho al conocimiento """
        self.facts.add(fact)

    def add_exception(self, exception):
        """ Agrega una excepción a una regla """
        self.exceptions.add(exception)

    def infer(self, entity, default_rule):
        """ Realiza una inferencia usando lógica por defecto """
        prereq, assumption, conclusion = default_rule
        if prereq in self.facts and assumption not in self.exceptions:
            return conclusion
        return "No se puede inferir"

# ---- DEMOSTRACIÓN ----
logic = DefaultLogic()

# Hecho conocido: Tweety es un pájaro
logic.add_fact("es_pajaro_Tweety")

# Regla por defecto: Si es un pájaro y no hay evidencia de que no vuele, entonces puede volar.
default_rule = ("es_pajaro_Tweety", "no_vuela_Tweety", "vuela_Tweety")

# Inferimos si Tweety puede volar
print(logic.infer("Tweety", default_rule))  # Output: "vuela_Tweety"


# Ahora agregamos una excepción (descubrimos que es un pingüino)
logic.add_exception("no_vuela_Tweety")

# Volvemos a inferir
print(logic.infer("Tweety", default_rule))  # Output: "No se puede inferir"

class Circumscription:
    def __init__(self):
        self.evidence = {}  # Almacena hechos explícitos

    def add_fact(self, entity, property, value):
        """ Agrega un hecho explícito """
        if entity not in self.evidence:
            self.evidence[entity] = {}
        self.evidence[entity][property] = value

    def query(self, entity, property):
        """ Solo devuelve una conclusión si hay evidencia explícita """
        return self.evidence.get(entity, {}).get(property, "No se puede inferir")

# ---- DEMOSTRACIÓN ----
circ = Circumscription()

# No hay información sobre Juan
print(circ.query("Juan", "culpable"))  # Output: "No se puede inferir"
print(circ.query("Juan", "inocente"))  # Output: "No se puede inferir"

# Agregamos un hecho explícito: Juan es inocente
circ.add_fact("Juan", "inocente", True)

# Ahora podemos inferir que Juan es inocente
print(circ.query("Juan", "inocente"))  # Output: True
print(circ.query("Juan", "culpable"))  # Output: "No se puede inferir"

# Agregamos un hecho explícito de que María es culpable
circ.add_fact("Maria", "culpable", True)

# Podemos consultar sobre María
print(circ.query("Maria", "culpable"))  # Output: True
print(circ.query("Maria", "inocente"))  # Output: "No se puede inferir"

class AutoepistemicReasoning:
    def __init__(self):
        self.knowledge = set()  # Conjunto de hechos conocidos

    def add_knowledge(self, fact):
        """ Agrega un hecho explícito al conocimiento """
        self.knowledge.add(fact)

    def knows(self, fact):
        """ Retorna True si el agente SABE que el hecho es verdadero """
        return fact in self.knowledge

    def does_not_know(self, fact):
        """ Retorna True si el agente NO SABE que el hecho es verdadero """
        return fact not in self.knowledge

    def infer(self, fact, assumption):
        """
        Inferencia autoepistémica:
        Si NO sabemos que una negación es cierta, asumimos que el hecho es verdadero.
        """
        if self.does_not_know(f"not_{fact}"):
            return assumption
        return False

# ---- DEMOSTRACIÓN ----
agent = AutoepistemicReasoning()

# Preguntamos si sabe que NO hay taxis
print(agent.knows("not_taxis"))  # False (el agente no tiene evidencia de que no hay taxis)

# Aplicamos la regla: "Si NO sabe que no hay taxis, asume que hay taxis"
taxis_available = agent.infer("taxis", True)
print(f"¿Hay taxis disponibles?: {taxis_available}")  # True


# Ahora agregamos conocimiento explícito de que no hay taxis
agent.add_knowledge("not_taxis")

# Aplicamos la regla nuevamente
taxis_available = agent.infer("taxis", True)
print(f"¿Hay taxis disponibles?: {taxis_available}")  # False

class BeliefBase:
    def __init__(self):
        self.beliefs = set()

    def expand(self, belief):
        """Añade una nueva creencia sin modificar las anteriores"""
        self.beliefs.add(belief)

    def contract(self, belief):
        """Elimina una creencia"""
        if belief in self.beliefs:
            self.beliefs.remove(belief)

    def revise(self, new_belief):
        """Revisa las creencias, eliminando contradicciones si es necesario"""
        contradicciones = {b for b in self.beliefs if self.is_contradiction(b, new_belief)}

        if contradicciones:
            print(f"⚠️ Se encontraron contradicciones: {contradicciones}. Ajustando creencias...")
            self.beliefs -= contradicciones  # Eliminar creencias contradictorias

        self.beliefs.add(new_belief)

    def is_contradiction(self, belief1, belief2):
        """Define cuándo dos creencias son contradictorias"""
        return belief1 == f"¬{belief2}" or belief2 == f"¬{belief1}"

    def show_beliefs(self):
        """Muestra el conjunto actual de creencias"""
        print("📌 Creencias actuales:", self.beliefs)

# --- Ejemplo de uso ---
beliefs = BeliefBase()
beliefs.expand("Los pájaros vuelan")
beliefs.expand("Tweety es un pájaro")
beliefs.show_beliefs()


# Ahora aprendemos que "Tweety NO vuela" (porque es un pingüino)
beliefs.revise("¬(Tweety vuela)")
beliefs.show_beliefs()