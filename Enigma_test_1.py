#Engigma machine Basic Functions by Eric Richardson
#13 April 2023

import string

class Rotor:
    def __init__(self, wiring, turnover):
        self.wiring = wiring
        self.turnover = turnover
        self.position = 0

    def set_position(self, position):
        self.position = position

    def rotate(self):
        self.position = (self.position + 1) % 26
        return self.position == self.turnover

    def forward(self, char):
        shifted = (ord(char) - 65 + self.position) % 26
        return self.wiring[shifted]

    def backward(self, char):
        index = (self.wiring.index(char) - self.position) % 26
        return chr(index + 65)

class Reflector:
    def __init__(self, wiring):
        self.wiring = wiring

    def reflect(self, char):
        return self.wiring[ord(char) - 65]

class Enigma:
    def __init__(self, rotors, reflector):
        self.rotors = rotors
        self.reflector = reflector

    def set_rotor_positions(self, positions):
        for rotor, position in zip(self.rotors, positions):
            rotor.set_position(position)

    def encrypt(self, text):
        encrypted = []
        for char in text:
            if char in string.ascii_letters:
                char = char.upper()
                for rotor in self.rotors:
                    if rotor.rotate():
                        break
                for rotor in self.rotors:
                    char = rotor.forward(char)
                char = self.reflector.reflect(char)
                for rotor in reversed(self.rotors):
                    char = rotor.backward(char)
            encrypted.append(char)
        return "".join(encrypted)

# Example configuration
rotor1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 17)  # turnover = Q
rotor2 = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", 5)   # turnover = E
rotor3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", 22)  # turnover = V

reflector = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")

enigma = Enigma([rotor1, rotor2, rotor3], reflector)
enigma.set_rotor_positions([0, 0, 0])

message = "HELLO WORLD"
encrypted = enigma.encrypt(message)
print(f"Encrypted: {encrypted}")

enigma.set_rotor_positions([0, 0, 0])
decrypted = enigma.encrypt(encrypted)
print(f"Decrypted: {decrypted}")


# output should be as follows:
#Encrypted: MIJPJ BNWYL
#Decrypted: HELLO WORLD
