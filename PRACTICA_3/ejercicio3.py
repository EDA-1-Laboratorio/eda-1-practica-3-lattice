import math
import numpy as np
import matplotlib.pyplot as plt

class Circulo:
    def __init__(self, x, y, r):
        if r <= 0:
            raise ValueError("El radio debe ser positivo")
        self.x = x
        self.y = y
        self.r = r

    def distancia(self, otro):
        return math.sqrt((self.x - otro.x)**2 + (self.y - otro.y)**2)

    def tipo_interseccion(self, otro):
        d = self.distancia(otro)

        if d > self.r + otro.r:
            return "No se intersectan"
        elif d == self.r + otro.r:
            return "Tangencia externa"
        elif d < abs(self.r - otro.r):
            return "Un círculo dentro del otro"
        elif d == abs(self.r - otro.r):
            return "Tangencia interna"
        else:
            return "Se intersectan en dos puntos"

    def area_interseccion(self, otro):
        d = self.distancia(otro)
        r1, r2 = self.r, otro.r

        if d >= r1 + r2:
            return 0

        if d <= abs(r1 - r2):
            return math.pi * min(r1, r2)**2

        def safe_acos(x):
            return math.acos(max(-1, min(1, x)))

        parte1 = r1**2 * safe_acos((d**2 + r1**2 - r2**2) / (2*d*r1)) 
        parte2 = r2**2 * safe_acos((d**2 + r2**2 - r1**2) / (2*d*r2)) 
        parte3 = 0.5 * math.sqrt(
            (-d+r1+r2)*(d+r1-r2)*(d-r1+r2)*(d+r1+r2)
        )

        return parte1 + parte2 - parte3


# ===== ENTRADA DEL USUARIO =====
print("Ingrese los datos del Círculo 1")
x1 = float(input("x1: "))
y1 = float(input("y1: "))
r1 = float(input("radio1: "))

print("\nIngrese los datos del Círculo 2")
x2 = float(input("x2: "))
y2 = float(input("y2: "))
r2 = float(input("radio2: "))

c1 = Circulo(x1, y1, r1)
c2 = Circulo(x2, y2, r2)

# ===== RESULTADOS =====
tipo = c1.tipo_interseccion(c2)
area = c1.area_interseccion(c2)

print("\nResultado:")
print("Tipo de intersección:", tipo)
print("Área de intersección:", round(area, 4))

# ===== GRÁFICA =====
fig, ax = plt.subplots()

circle1 = plt.Circle((c1.x, c1.y), c1.r, color='blue', alpha=0.3)
circle2 = plt.Circle((c2.x, c2.y), c2.r, color='red', alpha=0.3)

ax.add_patch(circle1)
ax.add_patch(circle2)

# Sombreado numérico
x = np.linspace(min(c1.x-c1.r, c2.x-c2.r),
                max(c1.x+c1.r, c2.x+c2.r), 500)

y = np.linspace(min(c1.y-c1.r, c2.y-c2.r),
                max(c1.y+c1.r, c2.y+c2.r), 500)

X, Y = np.meshgrid(x, y)

mask1 = (X - c1.x)**2 + (Y - c1.y)**2 <= c1.r**2
mask2 = (X - c2.x)**2 + (Y - c2.y)**2 <= c2.r**2

intersection = mask1 & mask2

ax.contourf(X, Y, intersection, levels=[0.5, 1], alpha=0.4)

ax.set_aspect('equal')
ax.grid(True)
plt.title("Intersección de Círculos")
plt.show()