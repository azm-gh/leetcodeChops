# Design Patterns

**Source:** [NeetCode — 8 Design Patterns Every Programmer Should Know](https://neetcode.io/courses/lessons/8-design-patterns) · [YouTube Video](https://www.youtube.com/watch?v=tAuRQs_d9F8)

Design patterns are reusable, tested solutions to commonly occurring problems in software engineering. They fall into three categories:

| Category | Purpose |
|----------|---------|
| **Creational** | Object creation mechanisms |
| **Structural** | Object composition and relationships |
| **Behavioral** | Object communication and responsibility |

---

## 1. Factory Method

**Category:** Creational

**Intuition:** Instead of calling `ClassName()` directly, you delegate object creation to a factory method. The client code doesn't know the concrete class — it only knows the interface. This decouples the "what" from the "how."

```python
from abc import ABC, abstractmethod

class Logger(ABC):
    @abstractmethod
    def log(self, message: str): ...

class ConsoleLogger(Logger):
    def log(self, message: str):
        print(f"Console: {message}")

class FileLogger(Logger):
    def log(self, message: str):
        with open("log.txt", "a") as f:
            f.write(f"{message}\n")

class LoggerFactory(ABC):
    @abstractmethod
    def create_logger(self) -> Logger: ...

class ConsoleLoggerFactory(LoggerFactory):
    def create_logger(self) -> Logger:
        return ConsoleLogger()

class FileLoggerFactory(LoggerFactory):
    def create_logger(self) -> Logger:
        return FileLogger()

# Usage
factory = ConsoleLoggerFactory() if config == "dev" else FileLoggerFactory()
logger = factory.create_logger()
logger.log("Application started")
```

**Used in practice:** Django's object-relational mapping (ORM) uses factory methods to create different database backends (PostgreSQL, MySQL, SQLite) from a single interface. GUI frameworks use factories to generate platform-specific buttons and windows while keeping client code cross-platform.

**External links:**
- [Refactoring Guru — Factory Method](https://refactoring.guru/design-patterns/factory-method)
- [SourceMaking — Factory Method](https://sourcemaking.com/design_patterns/factory_method)

---

## 2. Singleton

**Category:** Creational

**Intuition:** Ensures a class has exactly **one instance** and provides a global point of access to it. Useful when exactly one object is needed to coordinate actions across the system — like a single database connection pool or a centralized configuration manager.

```python
class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connected = False
        return cls._instance

    def connect(self):
        if not self._connected:
            print("Connecting to database...")
            self._connected = True

    def query(self, sql: str):
        if not self._connected:
            raise RuntimeError("Not connected")
        print(f"Executing: {sql}")

# Usage — both variables point to the same instance
db1 = DatabaseConnection()
db2 = DatabaseConnection()
assert db1 is db2  # True
```

**Used in practice:** Logging frameworks typically use a singleton logger so all parts of an application write to the same destination. Configuration managers (reading from a single config file) and thread pools are common real-world singletons.

**External links:**
- [Refactoring Guru — Singleton](https://refactoring.guru/design-patterns/singleton)
- [SourceMaking — Singleton](https://sourcemaking.com/design_patterns/singleton)

---

## 3. Builder

**Category:** Creational

**Intuition:** When an object requires many optional parameters or a multi-step construction process, the Builder pattern separates construction from representation. Instead of a constructor with 15 parameters, you chain method calls, each setting one piece, then call `build()` to get the final object.

```python
class Pizza:
    def __init__(self):
        self.size = None
        self.cheese = False
        self.pepperoni = False
        self.mushrooms = False
        self.olives = False

    def __str__(self):
        toppings = []
        if self.cheese: toppings.append("cheese")
        if self.pepperoni: toppings.append("pepperoni")
        if self.mushrooms: toppings.append("mushrooms")
        if self.olives: toppings.append("olives")
        return f"Pizza({self.size}) with {', '.join(toppings)}"

class PizzaBuilder:
    def __init__(self):
        self._pizza = Pizza()

    def set_size(self, size: str):
        self._pizza.size = size
        return self

    def add_cheese(self):
        self._pizza.cheese = True
        return self

    def add_pepperoni(self):
        self._pizza.pepperoni = True
        return self

    def add_mushrooms(self):
        self._pizza.mushrooms = True
        return self

    def add_olives(self):
        self._pizza.olives = True
        return self

    def build(self) -> Pizza:
        return self._pizza

# Usage
pizza = PizzaBuilder() \
    .set_size("large") \
    .add_cheese() \
    .add_pepperoni() \
    .build()
print(pizza)
```

**Used in practice:** Building SQL query strings (e.g., SQLAlchemy's `select().where().order_by()`), constructing HTTP requests in libraries like `requests` or `httpx`, and generating complex HTML documents programmatically.

**External links:**
- [Refactoring Guru — Builder](https://refactoring.guru/design-patterns/builder)
- [SourceMaking — Builder](https://sourcemaking.com/design_patterns/builder)

---

## 4. Adapter

**Category:** Structural

**Intuition:** Allows incompatible interfaces to work together. The adapter wraps an existing class with a new interface the client expects — like a power plug adapter that lets a US device work in a European outlet. You don't modify the existing class; you write a wrapper.

```python
from abc import ABC, abstractmethod

# Target interface the client expects
class JSONAnalyzer(ABC):
    @abstractmethod
    def analyze(self, json_data: dict): ...

# Existing class with a different interface
class XMLProcessor:
    def process_xml(self, xml_string: str):
        print(f"Processing XML: {xml_string[:50]}...")

# Adapter makes XMLProcessor work with JSONAnalyzer
class XMLToJSONAdapter(JSONAnalyzer):
    def __init__(self, xml_processor: XMLProcessor):
        self._processor = xml_processor

    def analyze(self, json_data: dict):
        # Convert JSON to XML, then delegate
        xml_string = self._json_to_xml(json_data)
        self._processor.process_xml(xml_string)

    def _json_to_xml(self, data: dict) -> str:
        parts = [f"<{k}>{v}</{k}>" for k, v in data.items()]
        return "<root>" + "".join(parts) + "</root>"

# Usage
processor = XMLProcessor()
adapter = XMLToJSONAdapter(processor)
adapter.analyze({"name": "Alice", "age": 30})
```

**Used in practice:** Database drivers (e.g., `psycopg2` adapts Python types to PostgreSQL wire protocol), caching layers that wrap different cache backends (Redis, Memcached, in-memory) behind a unified interface, and UI component wrappers that make third-party libraries conform to an application's rendering API.

**External links:**
- [Refactoring Guru — Adapter](https://refactoring.guru/design-patterns/adapter)
- [SourceMaking — Adapter](https://sourcemaking.com/design_patterns/adapter)

---

## 5. Decorator

**Category:** Structural

**Intuition:** Attaches additional responsibilities to an object **dynamically** without modifying its class. Decorators provide a flexible alternative to subclassing for extending functionality. Each decorator wraps the original object and can add behavior before or after delegating to it.

```python
from abc import ABC, abstractmethod

class Coffee(ABC):
    @abstractmethod
    def cost(self) -> float: ...

    @abstractmethod
    def description(self) -> str: ...

class SimpleCoffee(Coffee):
    def cost(self) -> float:
        return 5.0

    def description(self) -> str:
        return "Simple coffee"

class CoffeeDecorator(Coffee, ABC):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee

class MilkDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 1.5

    def description(self) -> str:
        return self._coffee.description() + " + milk"

class WhippedCreamDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 2.0

    def description(self) -> str:
        return self._coffee.description() + " + whipped cream"

# Usage
coffee = SimpleCoffee()
coffee = MilkDecorator(coffee)
coffee = WhippedCreamDecorator(coffee)
print(f"{coffee.description()} = ${coffee.cost():.2f}")
# Simple coffee + milk + whipped cream = $8.50
```

**Used in practice:** Python's `@property`, `@staticmethod`, and `@functools.lru_cache` are decorators in the language itself. Web frameworks like FastAPI use decorators for route registration (`@app.get("/")`). Java's `java.io.BufferedInputStream` wraps an `InputStream` to add buffering.

**External links:**
- [Refactoring Guru — Decorator](https://refactoring.guru/design-patterns/decorator)
- [SourceMaking — Decorator](https://sourcemaking.com/design_patterns/decorator)

---

## 6. Facade

**Category:** Structural

**Intuition:** Provides a **simplified, unified interface** to a larger body of code — a library, framework, or complex subsystem. Instead of calling 15 classes in the right order, the client calls one method on the facade. This reduces dependencies and makes the subsystem easier to use.

```python
class Amplifier:
    def on(self): print("Amplifier on")
    def set_volume(self, vol: int): print(f"Volume set to {vol}")

class BluRayPlayer:
    def on(self): print("BluRay on")
    def play(self, movie: str): print(f"Playing {movie}")

class Projector:
    def on(self): print("Projector on")
    def set_input(self, source: str): print(f"Input set to {source}")

class TheaterLights:
    def dim(self, level: int): print(f"Lights dimmed to {level}%")

class HomeTheaterFacade:
    def __init__(self):
        self._amp = Amplifier()
        self._bluray = BluRayPlayer()
        self._projector = Projector()
        self._lights = TheaterLights()

    def watch_movie(self, movie: str):
        print("Starting movie...")
        self._lights.dim(10)
        self._projector.on()
        self._projector.set_input("BluRay")
        self._amp.on()
        self._amp.set_volume(30)
        self._bluray.on()
        self._bluray.play(movie)

# Usage — one call instead of seven
theater = HomeTheaterFacade()
theater.watch_movie("Inception")
```

**Used in practice:** Web framework routers (a single `app.router` facade that internally manages middleware, route matching, and handler dispatch). ORM session objects that wrap transaction management, query building, and connection pooling behind a simple `session.query()` or `session.commit()` interface.

**External links:**
- [Refactoring Guru — Facade](https://refactoring.guru/design-patterns/facade)
- [SourceMaking — Facade](https://sourcemaking.com/design_patterns/facade)

---

## 7. Strategy

**Category:** Behavioral

**Intuition:** Defines a family of interchangeable algorithms, encapsulates each one, and makes them swappable at runtime. The client delegates to a strategy object rather than implementing the algorithm directly or using a large conditional chain. This is the "has-a" alternative to subclassing.

```python
from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float): ...

class CreditCardPayment(PaymentStrategy):
    def pay(self, amount: float):
        print(f"Paid ${amount:.2f} with credit card")

class PayPalPayment(PaymentStrategy):
    def pay(self, amount: float):
        print(f"Paid ${amount:.2f} with PayPal")

class CryptoPayment(PaymentStrategy):
    def pay(self, amount: float):
        print(f"Paid ${amount:.2f} with cryptocurrency")

class ShoppingCart:
    def __init__(self, strategy: PaymentStrategy):
        self._items = []
        self._strategy = strategy

    def add_item(self, item: str, price: float):
        self._items.append((item, price))

    def checkout(self):
        total = sum(price for _, price in self._items)
        self._strategy.pay(total)

# Usage
cart = ShoppingCart(PayPalPayment())
cart.add_item("Book", 15.99)
cart.add_item("Pen", 2.50)
cart.checkout()  # Paid $18.49 with PayPal
```

**Used in practice:** Authentication backends in Django (different strategies for session-based, token-based, or OAuth authentication). Compression algorithms (`gzip` vs `brotli`) and output formatters (JSON vs XML vs YAML) are classic strategy applications.

**External links:**
- [Refactoring Guru — Strategy](https://refactoring.guru/design-patterns/strategy)
- [SourceMaking — Strategy](https://sourcemaking.com/design_patterns/strategy)

---

## 8. Observer

**Category:** Behavioral

**Intuition:** Defines a **one-to-many** dependency between objects so that when one object (the subject) changes state, all its dependents (observers) are notified automatically. This is the publish–subscribe pattern that decouples the source of an event from the consumers.

```python
from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, temperature: float): ...

class WeatherStation:
    def __init__(self):
        self._observers = []
        self._temperature = 0.0

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def set_temperature(self, temp: float):
        self._temperature = temp
        self._notify_all()

    def _notify_all(self):
        for obs in self._observers:
            obs.update(self._temperature)

class PhoneDisplay(Observer):
    def update(self, temperature: float):
        print(f"Phone display: {temperature}°F")

class WindowDisplay(Observer):
    def update(self, temperature: float):
        print(f"Window display: {temperature}°F")

# Usage
station = WeatherStation()
phone = PhoneDisplay()
window = WindowDisplay()
station.attach(phone)
station.attach(window)
station.set_temperature(72.5)
# Phone display: 72.5°F
# Window display: 72.5°F
```

**Used in practice:** Frontend frameworks (React's `useEffect` observes state changes, Vue's reactive system observes data properties). Message queues and event buses (Redis Pub/Sub, Kafka consumer groups). GUI event listeners (button clicks, mouse movements) are textbook observer pattern implementations.

**External links:**
- [Refactoring Guru — Observer](https://refactoring.guru/design-patterns/observer)
- [SourceMaking — Observer](https://sourcemaking.com/design_patterns/observer)

---

## Summary

| Pattern | Category | Problem Solved |
|---------|----------|---------------|
| Factory Method | Creational | Decouple object creation from client code |
| Singleton | Creational | Single instance, global access |
| Builder | Creational | Step-by-step construction of complex objects |
| Adapter | Structural | Make incompatible interfaces work together |
| Decorator | Structural | Add responsibilities dynamically |
| Facade | Structural | Simplify a complex subsystem |
| Strategy | Behavioral | Swap algorithms at runtime |
| Observer | Behavioral | One-to-many change notification |

---

## References

- [NeetCode — 8 Design Patterns Every Programmer Should Know](https://neetcode.io/courses/lessons/8-design-patterns)
- [Refactoring Guru — Design Patterns](https://refactoring.guru/design-patterns)
- [SourceMaking — Design Patterns](https://sourcemaking.com/design_patterns)
- [Python Docs — `abc` module (abstract base classes)](https://docs.python.org/3/library/abc.html)
