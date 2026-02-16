import random
import os

def load_jokes(filename="Jokes.txt"):
    jokes_list = []
    script_dir = os.path.dirname(__file__)
    candidates = [
        filename,
        os.path.join(script_dir, filename),
        os.path.join(script_dir, "resources", filename)
    ]
    found = None
    for path in candidates:
        if os.path.exists(path):
            found = path
            break

    with open(found, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if "?" in line:
                setup, punchline = line.split("?", 1)
                jokes_list.append((setup.strip() + "?", punchline.strip()))
    return jokes_list

def tell_joke(jokes):
    """Select and display a random joke."""
    joke = random.choice(jokes)
    setup, punchline = joke
    print("\nAlexa:", setup)
    input("\nPress ENTER to hear the punchline...")
    print("Alexa:", punchline)

def main():
    print("Alexa Tell Me a Joke")


    jokes = load_jokes("Jokes.txt")
    if not jokes:
        print("No jokes loaded. Please check your file.")
        return

    while True:
        command = input("\nType 'Alexa tell me a joke' or 'quit': ").strip().lower()
        if command == "alexa tell me a joke":
            tell_joke(jokes)
        elif command == "quit":
            print("\nAlexa: Goodbye!")
            break
        else:
            print("Alexa: I didn’t understand that. Try again!")

if __name__ == "__main__":
    main()
