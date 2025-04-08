from collections import Counter, defaultdict

class ClasificadorEmocion:
    def __init__(self):
        # Emociones a clasificar
        self.emociones = ["felicidad", "tristeza", "enojo", "miedo", "sorpresa"]
        
        # Contadores para palabras por emoción
        self.palabras_por_emocion = {
            emocion: Counter() for emocion in self.emociones
        }
        
        # Contador de mensajes por emoción
        self.mensajes_por_emocion = Counter()
        
        # Total de mensajes de entrenamiento
        self.total_mensajes = 0
        
        # Vocabulario completo
        self.vocabulario = set()
    
    def procesar_texto(self, texto):
        """Convierte texto a minúsculas y separa palabras"""
        return texto.lower().split()
    
    def entrenar(self, mensajes, emociones):
        """Entrena el clasificador con mensajes y sus emociones"""
        for mensaje, emocion in zip(mensajes, emociones):
            # Incrementar contadores
            self.mensajes_por_emocion[emocion] += 1
            self.total_mensajes += 1
            
            # Procesar palabras
            palabras = self.procesar_texto(mensaje)
            for palabra in palabras:
                self.palabras_por_emocion[emocion][palabra] += 1
                self.vocabulario.add(palabra)
    
    def tabla_frecuencias(self):
        """Genera tabla de frecuencias de palabras por emoción"""
        tabla = {}
        for emocion in self.emociones:
            total_palabras = sum(self.palabras_por_emocion[emocion].values())
            if total_palabras > 0:
                tabla[emocion] = {
                    palabra: count / total_palabras 
                    for palabra, count in self.palabras_por_emocion[emocion].items()
                }
        return tabla
    
    def prob_previa(self):
        """Calcula P(E) para cada emoción"""
        return {
            emocion: self.mensajes_por_emocion[emocion] / self.total_mensajes 
            for emocion in self.emociones
        }
    
    def prob_condicional(self, palabra):
        """Calcula P(W|E) para una palabra"""
        probs = {}
        suavizado = 1  # Suavizado de Laplace
        tamano_vocab = len(self.vocabulario)
        
        for emocion in self.emociones:
            total_palabras = sum(self.palabras_por_emocion[emocion].values())
            count = self.palabras_por_emocion[emocion][palabra] if palabra in self.palabras_por_emocion[emocion] else 0
            # Aplicar suavizado de Laplace
            probs[emocion] = (count + suavizado) / (total_palabras + suavizado * (tamano_vocab + 1))
        
        return probs
    
    def clasificar(self, mensaje):
        """Clasifica un mensaje calculando P(E|W)"""
        palabras = self.procesar_texto(mensaje)
        
        # Obtener probabilidades previas P(E)
        probs_previas = self.prob_previa()
        
        # Inicializar probabilidades para cada emoción
        probs = {emocion: prob for emocion, prob in probs_previas.items()}
        
        # Multiplicar por P(W|E) para cada palabra
        for palabra in palabras:
            cond_probs = self.prob_condicional(palabra)
            for emocion in self.emociones:
                probs[emocion] *= cond_probs[emocion]
        
        # Normalizar las probabilidades
        total = sum(probs.values())
        if total > 0:
            for emocion in probs:
                probs[emocion] /= total
        
        # Obtener la emoción más probable
        emocion_detectada = max(probs, key=probs.get)
        
        return emocion_detectada, probs


# Ejemplo de uso
if __name__ == "__main__":
    # Crear el clasificador
    clasificador = ClasificadorEmocion()
    
    # Datos de entrenamiento
    mensajes = [
        "estoy muy feliz hoy",
        "me siento genial",
        "qué día tan bonito",
        "estoy triste",
        "me siento mal",
        "todo salió mal",
        "estoy enojado contigo",
        "me irrita esto",
        "qué rabia",
        "tengo miedo",
        "estoy asustado",
        "me preocupa esto",
        "me sorprendió mucho",
        "qué sorpresa",
        "no me lo esperaba"
    ]
    
    emociones = [
        "felicidad", "felicidad", "felicidad",
        "tristeza", "tristeza", "tristeza",
        "enojo", "enojo", "enojo",
        "miedo", "miedo", "miedo",
        "sorpresa", "sorpresa", "sorpresa"
    ]
    
    # Entrenar el clasificador
    clasificador.entrenar(mensajes, emociones)
    
    # Mostrar tabla de frecuencias
    print("FRECUENCIAS DE PALABRAS POR EMOCIÓN:")
    tabla = clasificador.tabla_frecuencias()
    for emocion, palabras in tabla.items():
        print(f"\n{emocion.upper()}:")
        for palabra, freq in sorted(palabras.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {palabra}: {freq:.2f}")
    
    # Mostrar probabilidades previas
    print("\nPROBABILIDADES PREVIAS P(E):")
    previas = clasificador.prob_previa()
    for emocion, prob in previas.items():
        print(f"  P({emocion}) = {prob:.2f}")
    
    # Probar el clasificador
    while True:
        mensaje = input("\nEscribe un mensaje (o 'salir' para terminar): ")
        if mensaje.lower() == 'salir':
            break
        
        emocion, probabilidades = clasificador.clasificar(mensaje)
        
        print(f"\nEmoción detectada: {emocion}")
        print("\nProbabilidades P(E|W):")
        for e, p in sorted(probabilidades.items(), key=lambda x: x[1], reverse=True):
            print(f"  P({e}|mensaje) = {p:.4f}")