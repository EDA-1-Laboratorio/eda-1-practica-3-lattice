class Pizza:
    def __init__(self, tamaño, toppings):  # tamaño en radio, toppings en cantidad
        self.tamaño = tamaño
        self.toppings = toppings
        self.precio = self.calcular_precio()

    def calcular_precio(self):
        base_price = 100
        topping_price = 20
        return base_price + (topping_price * self.toppings)


def main():
    pizzas = []
    num_pizzas = int(input("¿Cuántas pizzas quieres ordenar? "))

    for i in range(num_pizzas):
        tamaño = float(input(f"¿Cuál es el tamaño (radio) de la pizza {i+1}? "))
        toppings = int(input(f"¿Cuántos toppings quieres en la pizza {i+1}? "))
        pizza = Pizza(tamaño, toppings)
        pizzas.append(pizza)

    # Calcular total sin descuento
    total_price = sum(p.precio for p in pizzas)

    # Agrupar pizzas por tamaño
    pizzas_por_tamaño = {}

    for pizza in pizzas:
        if pizza.tamaño not in pizzas_por_tamaño:
            pizzas_por_tamaño[pizza.tamaño] = []
        pizzas_por_tamaño[pizza.tamaño].append(pizza)

    descuento = 0

    # Aplicar 2x1 por cada par de pizzas del mismo tamaño
    for tamaño, lista in pizzas_por_tamaño.items():
        # Ordenar por precio (de menor a mayor)
        lista.sort(key=lambda p: p.precio)

        # Por cada par, la más barata es gratis
        for i in range(0, len(lista) - 1, 2):
            descuento += lista[i].precio

    total_final = total_price - descuento

    # Ticket
    print("\n--- Ticket de Orden ---")
    for i, pizza in enumerate(pizzas):
        print(f"Pizza {i+1}: Tamaño: {pizza.tamaño}, "
              f"Toppings: {pizza.toppings}, "
              f"Precio: ${pizza.precio}")

    if descuento > 0:
        print(f"Descuento 2x1 aplicado: -${descuento}")

    print(f"Precio Total Final: ${total_final}")


if __name__ == "__main__":
    main()

