class Dog:
    def __init__(self, name):
        self.name = name
    
    def bark(self):
        print(f"{self.name} says woof!")
        

# this 'Dog' is an instance of the Python class Dog
dog = Dog("Bob")

print(dog.name)

# now with the method:

print("Barking!!!!")
dog.bark()
