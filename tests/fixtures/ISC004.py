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

# Unparenthesized concatenation of three or more strings triggers a single ISC004
facts = (
    "Lobsters have blue blood.",
    "Octopuses have three hearts."
    "Honey never spoils."
    "Or does it?",
)

# Non-ASCII text must not skew ISC004 detection or positions
facts = [
    "ロブスターの血は青い。",
    "肝臓は完全に再生できる唯一の人間の臓器です。",
    "クラリネットはほぼ全てムピンゴの木から作られている。"
    "1971年、宇宙飛行士アラン・シェパードは月でゴルフをした。",
]

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

# Parenthesized concatenation of three or more strings should not trigger ISC004
facts = (
    "Lobsters have blue blood.",
    "The liver is the only human organ that can fully regenerate itself.",
    (
        "Clarinets are made almost entirely out of wood from the mpingo tree."
        "In 1971, astronaut Alan Shepard played golf on the moon."
        "Or did he?"
    ),
)

facts = (
    "Lobsters have blue blood.\n"
    "The liver is the only human organ that can fully regenerate itself.\n"
    "Clarinets are made almost entirely out of wood from the mpingo tree.\n"
    "In 1971, astronaut Alan Shepard played golf on the moon.\n"
)

# A single f-string is not an implicit concatenation, even when its
# replacement fields contain string literals
facts = [f"{'Lobsters'} {'have'} {'blue blood.'}"]

# Implicit concatenation involving f-strings is flagged
facts = [
    f"Octopuses have {3} hearts."
    "Honey never spoils.",
]

# ...unless parenthesized
facts = [
    (
        f"Octopuses have {3} hearts."
        "Honey never spoils."
    ),
]

# Function calls should not trigger ISC004 (not a collection)
def func(*args, **kwargs) -> None: pass

functions = [
    print("Lobsters have " "blue blood"),
    func(1, "Honey " "never " "spoils", 3),
    func("Octopuses have " "three hearts"),
    func(arg="mpingo" "tree"),
]

# A collection nested inside other brackets is still a collection
functions = [
    func(["Lobsters have " "blue blood"]),
]
