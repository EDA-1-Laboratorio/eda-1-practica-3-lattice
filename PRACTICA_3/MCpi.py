import random

puntos_dentro_circulo = 0
total_puntos = 1000000

for _ in range(total_puntos): # Repetimos el proceso para un gran número de puntos
    x = random.uniform(-1, 1) # Generamos un número aleatorio entre -1 y 1 para la coordenada x y y
    y = random.uniform(-1, 1)
    
    if x**2 + y**2 <= 1: # Verificamos si el punto (x, y) está dentro del círculo de radio 1
        puntos_dentro_circulo += 1
pi_estimado = (puntos_dentro_circulo / total_puntos) * 4 # La proporción de puntos dentro del círculo multiplicada por 4 nos da una estimación de π
print(f"Estimación de π: {pi_estimado}")    

