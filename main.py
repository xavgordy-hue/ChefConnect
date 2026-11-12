from dataclasses import dataclass
from drafter import *

@dataclass
class Chef:
    name: str
    cuisine: str
    location: str
    price: int
    rating: float

@dataclass
class State:
    chefs: list[Chef]
    budget: int
    cuisine: str
    location: str
    selected_chef: str
    quantity: int
    status: str


@route
def index(state: State) -> Page:
    return Page(state, [
        Header("ChefConnect"),
        Text("Find a chef in your area!"),
        Button("Find Chefs", "preferences"),
        Button("Add a Chef", "add_chef"),
        Text(state.status)
    ])


@route
def preferences(state: State) -> Page:
    return Page(state, [
        Header("Your Preferences"),
        Text("Budget:"),
        TextBox("budget", state.budget, "number"),
        Text("Cuisine:"),
        SelectBox("cuisine", ["Jamaican", "Italian", "Mexican"], state.cuisine),
        Text("City:"),
        TextBox("location", state.location),
        Button("Search", "update_preferences")
    ])


@route
def update_preferences(state: State, budget: int, cuisine: str, location: str) -> Page:
    state.budget = budget
    state.cuisine = cuisine
    state.location = location
    state.status = ""
    return results(state)


@route
def results(state: State) -> Page:
    names = []
    for chef in state.chefs:
        if chef.price <= state.budget:
            if chef.cuisine == state.cuisine:
                if chef.location.lower() == state.location.lower():
                    names.append(chef.name)

    if len(names) == 0:
        state.status = "No chefs found. Try different preferences."
        return Page(state, [
            Header("Matching Chefs"),
            Text(state.status),
            Button("Try Again", "preferences")
        ])

    return Page(state, [
        Header("Matching Chefs"),
        Text("Choose a chef:"),
        SelectBox("name", names),
        Button("View Chef", "select_chef")
    ])


@route
def select_chef(state: State, name: str) -> Page:
    state.selected_chef = name
    return chef_profile(state)


@route
def chef_profile(state: State) -> Page:
    for chef in state.chefs:
        if chef.name == state.selected_chef:
            return Page(state, [
                Header(chef.name),
                Text("Cuisine: " + chef.cuisine),
                Text("City: " + chef.location),
                Text("Rating: " + str(chef.rating)),
                Text("Price per meal: $" + str(chef.price)),
                Text("Number of meals:"),
                TextBox("quantity", state.quantity, "number"),
                Button("Review Order", "order_summary")
            ])
    return results(state)


@route
def order_summary(state: State, quantity: int) -> Page:
    if quantity < 1:
        return Page(state, [Text("Enter at least one meal."), Button("Back", "chef_profile")])
    state.quantity = quantity
    for chef in state.chefs:
        if chef.name == state.selected_chef:
            total = chef.price * state.quantity
            return Page(state, [
                Header("Order Summary"),
                Text("Chef: " + chef.name),
                Text("Meals: " + str(state.quantity)),
                Text("Total: $" + str(total)),
                Button("Confirm", "confirm_order"),
                Button("Back", "chef_profile")
            ])
    return results(state)


@route
def confirm_order(state: State) -> Page:
    state.status = "Order confirmed with " + state.selected_chef
    return Page(state, [
        Header("Order Confirmed"),
        Text(state.status),
        Button("Home", "index")
    ])


@route
def add_chef(state: State) -> Page:
    return Page(state, [
        Header("Add a Chef"),
        Text("Name:"), TextBox("name"),
        Text("Cuisine:"), SelectBox("cuisine", ["Jamaican", "Italian", "Mexican"]),
        Text("City:"), TextBox("location"),
        Text("Price:"), TextBox("price", 0, "number"),
        Text("Rating:"), TextBox("rating", 0, "number"),
        Button("Save", "save_chef")
    ])


@route
def save_chef(state: State, name: str, cuisine: str,
              location: str, price: int, rating: float) -> Page:
    if name.strip() == "" or location.strip() == "" or price <= 0:
        state.status = "Please enter a name, city, and positive price."
    elif rating < 0 or rating > 5:
        state.status = "Rating must be between 0 and 5."
    else:
        state.chefs.append(Chef(name, cuisine, location, price, rating))
        state.status = "Added " + name + "!"
    return index(state)


chefs = [
    Chef("Marcus", "Jamaican", "Newark", 15, 4.8),
    Chef("Maya", "Italian", "Newark", 25, 4.7),
    Chef("Jordan", "Jamaican", "Wilmington", 20, 4.5),
    Chef("Olivia", "Mexican", "Newark", 18, 4.6)
]

start_server(State(chefs, 30, "Jamaican", "Newark", "", 1, ""))



