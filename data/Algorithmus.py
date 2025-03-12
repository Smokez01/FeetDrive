def ggt(a, b):
    while b != 0:
        r = a % b  # Berechne den Rest
        a = b      # Setze a auf den Wert von b
        b = r      # Setze b auf den Rest
    return a      # Wenn b 0 ist, ist a der GGT

# Beispiel:
a = int(input("Gib mir eine Zahl "))
b = int(input("Gib mir eine kleinere Zahl "))
print(f"Der größte gemeinsame Teiler von {a} und {b} ist: {ggt(a, b)}")