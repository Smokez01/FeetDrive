def ggt(a, b):
    while b != 0:
        r = a % b
        a = b
        b = r
    return a

# Beispiel:
a = int(input("Gib mir eine Zahl "))
b = int(input("Gib mir eine kleinere Zahl "))
print(f"Der größte gemeinsame Teiler von {a} und {b} ist: {ggt(a, b)}")