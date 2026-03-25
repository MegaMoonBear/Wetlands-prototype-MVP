# Object-Oriented Programming (OOP) in the Wetlands Prototype

This project demonstrates the 2 of the 4 pillars of Object-Oriented Programming (OOP): **Encapsulation**and **Abstraction**. The 2 other pillars **Inheritance** and **Polymorphism** are included with examples from other novice projects. See the simplified definitions and examples for each pillar. 

By understanding and applying these 4 pillars, this project ensures clean, reusable, and maintainable code.

## 1. Encapsulation (in this repo)
Encapsulation means keeping the details of how something works hidden, so you only need to know how to use it. This helps protect the data and makes the code easier to use.

- **Example**: In [backend/models.py](models.py#L18-L28), the `get_db_connection()` function hides the complex steps of connecting to the database and just gives you a connection to use.

## 2. Abstraction (in this repo)
Abstraction means showing only the important parts and hiding the unnecessary details. This simplifies how you interact with the code.

- **Example**: In [backend/routes.py](routes.py#L32), the `upload_image()` function simplifies the process of uploading an image, so you don’t need to know how the image is stored or processed.

## 3. Inheritance
Inheritance allows one class to use the properties and methods of another class. This helps reduce code duplication.

- **Example**: In a novice-level repository, a `Dog` class might inherit from an `Animal` class, reusing its `eat()` method while adding its own `bark()` method.

    ```python
    class Animal:
        def eat(self):
            print("This animal eats food.")

    class Dog(Animal):
        def bark(self):
            print("The dog barks.")
    ```

## 4. Polymorphism
Polymorphism allows the same method to behave differently depending on the object that calls it. This makes the code more flexible.

- **Example**: In a novice-level repository, both `Cat` and `Dog` classes might have their own version of a `speak()` method, but you can call `speak()` on any `Animal` object.

    ```python
    class Cat:
        def speak(self):
            print("Meow")

    class Dog:
        def speak(self):
            print("Woof")

    for animal in [Cat(), Dog()]:
        animal.speak()
    ```
