class City:
    def __init__(self, name, country, population):
        self.name = name
        self.country = country
        self.population = population


    def __repr__(self):
        return f"{self.name},{self.country}, {self.population}"
