import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

class Pokedex:
    def __init__(self, root):
        self.root = root
        self.root.title("Pokedex")
        self.root.geometry("400x600")
        self.root.config(bg="#cc0000")

        self.current_id = 1

        # search bar
        search_frame = tk.Frame(root, bg="#cc0000")
        search_frame.pack(pady=10)

        self.entry = tk.Entry(search_frame, font=("Arial", 14), width=15)
        self.entry.grid(row=0, column=0, padx=5)

        tk.Button(search_frame, text="Search", font=("Arial", 12),
                  command=self.search_pokemon, bg="#FFDE00").grid(row=0, column=1, padx=5)

        tk.Button(search_frame, text="Random", font=("Arial", 12),
                  command=self.random_pokemon, bg="#FFDE00").grid(row=0, column=2, padx=5)

        # frame to display pokemon
        self.pokemon_frame = tk.Frame(root, bg="#3B4CCA", width=350, height=250, 
                                      highlightbackground="#FFDE00", highlightthickness=4)
        self.pokemon_frame.pack(pady=10)
        self.pokemon_frame.pack_propagate(False)

        self.image_label = tk.Label(self.pokemon_frame, bg="#3B4CCA")
        self.image_label.pack(expand=True)

        # frame for display info
        self.info_frame = tk.Frame(root, bg="#cc0000", highlightbackground="#FFDE00", highlightthickness=3)
        self.info_frame.pack(pady=10, fill="both", expand=True)

        self.info_text = tk.Label(self.info_frame, font=("Arial", 12), justify="left", bg="#cc0000", fg="#ffffff")
        self.info_text.pack(padx=10, pady=10)

        # navigation buttons for previous and next
        nav_frame = tk.Frame(root, bg="#cc0000")
        nav_frame.pack(pady=5)

        tk.Button(nav_frame, text="◀ Previous", font=("Arial", 12),
                  command=self.previous_pokemon, bg="#FFDE00").grid(row=0, column=0, padx=15)

        tk.Button(nav_frame, text="Next ▶", font=("Arial", 12),
                  command=self.next_pokemon, bg="#FFDE00").grid(row=0, column=1, padx=15)

        # Load first Pokémon
        self.load_by_id(1)

    #  api request
    def fetch_pokemon(self, name_or_id):
        url = f"https://pokeapi.co/api/v2/pokemon/{name_or_id.lower()}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except requests.exceptions.RequestException:
            messagebox.showerror("Error", "Network Error. Check your connection.")
            return None

    # error handling for search bar
    def search_pokemon(self):
        name = self.entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a Pokémon name.")
            return
        data = self.fetch_pokemon(name)
        if data:
            self.display_pokemon(data)
            self.current_id = data["id"]
        else:
            messagebox.showerror("Error", "Pokémon not found.")

    # gerate a random pokemon
    def random_pokemon(self):
        random_id = random.randint(1, 898)
        self.load_by_id(random_id)

    # navigation functions for next and previous
    def next_pokemon(self):
        self.current_id += 1
        if self.current_id > 898:
            self.current_id = 1
        self.load_by_id(self.current_id)

    def previous_pokemon(self):
        self.current_id -= 1
        if self.current_id < 1:
            self.current_id = 898
        self.load_by_id(self.current_id)

    # load pokemon by id
    def load_by_id(self, poke_id):
        data = self.fetch_pokemon(str(poke_id))
        if data:
            self.display_pokemon(data)

    # display pokemon to save and load image and info
    def display_pokemon(self, data):
        sprite_url = data["sprites"]["front_default"]
        if sprite_url:
            temp_path = "temp_sprite.png"

            with open(temp_path, "wb") as f:
                f.write(requests.get(sprite_url).content)
            img = Image.open(temp_path).resize((200, 200))
            img = ImageTk.PhotoImage(img)

            self.image_label.config(image=img)
            self.image_label.image = img

        # pokemon information
        name = data["name"].title()
        poke_id = data["id"]
        height = data["height"]
        weight = data["weight"]
        base_exp = data.get("base_experience", "N/A")
        types = ", ".join([t["type"]["name"].title() for t in data["types"]])
        abilities = "\n - ".join([a["ability"]["name"].title() for a in data["abilities"]])
        stats = data["stats"]
        hp = stats[0]["base_stat"]
        attack = stats[1]["base_stat"]
        defense = stats[2]["base_stat"]
        speed = stats[5]["base_stat"]

        self.info_text.config(text=f"""
Name: {name}
ID: {poke_id}
Type(s): {types}

Height: {height}
Weight: {weight}
Base Experience: {base_exp}

Stats:
 - HP: {hp}
 - Attack: {attack}
 - Defense: {defense}
 - Speed: {speed}

Abilities:
 - {abilities}
        """)


root = tk.Tk()
app = Pokedex(root)
root.mainloop()
