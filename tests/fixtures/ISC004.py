facts = (
    "Lobsters have blue blood.",
    "The liver is the only human organ that can fully regenerate itself.",
    "Clarinets are made almost entirely out of wood from the mpingo tree."
    "In 1971, astronaut Alan Shepard played golf on the moon.",
)

facts = [
    "Lobsters have blue blood.",
    "The liver is the only human organ that can fully regenerate itself.",
    "Clarinets are made almost entirely out of wood from the mpingo tree."
    "In 1971, astronaut Alan Shepard played golf on the moon.",
]

facts = {
    "Lobsters have blue blood.",
    "The liver is the only human organ that can fully regenerate itself.",
    "Clarinets are made almost entirely out of wood from the mpingo tree."
    "In 1971, astronaut Alan Shepard played golf on the moon.",
}

facts = {
    (
        "Clarinets are made almost entirely out of wood from the mpingo tree."
        "In 1971, astronaut Alan Shepard played golf on the moon."
    ),
}

facts = (
    "Octopuses have three hearts."
    # Missing comma here.
    "Honey never spoils.",
)

facts = [
    "Octopuses have three hearts."
    # Missing comma here.
    "Honey never spoils.",
]

facts = {
    "Octopuses have three hearts."
    # Missing comma here.
    "Honey never spoils.",
}

facts = (
    (
        "Clarinets are made almost entirely out of wood from the mpingo tree."
        "In 1971, astronaut Alan Shepard played golf on the moon."
    ),
)

facts = [
    (
        "Clarinets are made almost entirely out of wood from the mpingo tree."
        "In 1971, astronaut Alan Shepard played golf on the moon."
    ),
]

facts = (
    "Lobsters have blue blood.\n"
    "The liver is the only human organ that can fully regenerate itself.\n"
    "Clarinets are made almost entirely out of wood from the mpingo tree.\n"
    "In 1971, astronaut Alan Shepard played golf on the moon.\n"
)

# Function calls should not trigger ISC004 (not a collection)
def func(*args, **kwargs) -> None: pass

functions = [
    print("Lobsters have " "blue blood"),
    func(1, "Honey " "never " "spoils", 3),
    func("Octopuses have " "three hearts"),
    func(arg="mpingo" "tree"),
]
