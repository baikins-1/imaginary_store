


from drafter import *
from dataclasses import dataclass


# -----------------------------
# DATACLASSES
# -----------------------------

@dataclass
class Product:
    name: str
    category: str
    price: float
    description: str
    stock: int


@dataclass
class CartItem:
    product: Product
    quantity: int


@dataclass
class State:
    products: list[Product]
    cart: list[CartItem]
    message: str


# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def pink_button(label, route_name, arguments=None):
    button = Button(label, route_name, arguments)
    return change_background_color(button, "#B76E88")


def product_card(product):
    return Div(
        Header(product.name, 3),
        Text("$" + str(product.price)),
        Text(product.description),
        Text("Category: " + product.category),
        pink_button(
            "Add to Cart",
            "add_to_cart",
            [Argument("product_name", product.name)]
        )
    )


def cart_total(state):
    total = 0

    for item in state.cart:
        total += item.product.price * item.quantity

    return round(total, 2)


# -----------------------------
# HOME PAGE
# -----------------------------

@route
def index(state: State) -> Page:
    return Page(state, [
        Header("Welcome!", 1),
        Text("Welcome to your fictional shopping experience!"),
        Text("Find something that makes you happy!"),
        Text(state.message),
        pink_button("Start Shopping", "shop"),
        pink_button("View Cart", "view_cart")
    ])


# -----------------------------
# SHOP PAGE
# -----------------------------

@route
def shop(state: State) -> Page:
    content = [
        Header("Shop", 1),
        Text("Browse all of our products!")
    ]

    for product in state.products:
        content.append(product_card(product))

    content.append(pink_button("View Cart", "view_cart"))
    content.append(pink_button("Home", "index"))

    return Page(state, content)


# -----------------------------
# ADD TO CART
# -----------------------------

@route
def add_to_cart(state: State, product_name: str) -> Page:

    selected_product = None

    for product in state.products:
        if product.name == product_name:
            selected_product = product

    if selected_product == None:
        state.message = "Product not found."

    elif selected_product.stock <= 0:
        state.message = "This product is out of stock."

    else:
        existing_item = None

        for item in state.cart:
            if item.product.name == product_name:
                existing_item = item

        if existing_item != None:
            if existing_item.quantity >= selected_product.stock:
                state.message = "No more stock available."
            else:
                existing_item.quantity += 1
                state.message = "Added another " + product_name + "!"

        else:
            state.cart.append(CartItem(selected_product, 1))
            state.message = product_name + " added to cart!"

    return shop(state)


# -----------------------------
# VIEW CART
# -----------------------------

@route
def view_cart(state: State) -> Page:
    content = [
        Header("Shopping Cart", 1),
        Text(state.message)
    ]

    if len(state.cart) == 0:
        content.append(Text("Your cart is empty!"))

    else:
        for item in state.cart:
            content.append(
                Div(
                    Header(item.product.name, 3),
                    Text("Price: $" + str(item.product.price)),
                    Text("Quantity: " + str(item.quantity)),
                    Text(
                        "Subtotal: $"
                        + str(round(
                            item.product.price * item.quantity, 2
                        ))
                    ),
                    pink_button(
                        "Remove",
                        "remove_from_cart",
                        [Argument("product_name", item.product.name)]
                    )
                )
            )

        content.append(
            Header("Total: $" + str(cart_total(state)), 2)
        )

        content.append(pink_button("Checkout", "checkout"))

    content.append(pink_button("Continue Shopping", "shop"))

    return Page(state, content)


# -----------------------------
# REMOVE FROM CART
# -----------------------------

@route
def remove_from_cart(state: State, product_name: str) -> Page:

    updated_cart = []

    for item in state.cart:
        if item.product.name != product_name:
            updated_cart.append(item)

    state.cart = updated_cart
    state.message = product_name + " removed from cart."

    return view_cart(state)


# -----------------------------
# CHECKOUT PAGE
# -----------------------------

@route
def checkout(state: State) -> Page:
    content = [
        Header("Checkout", 1),
        Text("This is a fictional shop. No real money is used!")
    ]

    if len(state.cart) == 0:
        content.append(Text("Your cart is empty."))
        content.append(pink_button("Return to Shop", "shop"))

    else:
        content.append(Header("Your Items", 2))

        for item in state.cart:
            content.append(
                Text(
                    item.product.name
                    + " x "
                    + str(item.quantity)
                )
            )

        content.append(
            Header("Total: $" + str(cart_total(state)), 2)
        )

        content.append(Text("Checkout is just a preview for now!"))
        content.append(pink_button("Back to Cart", "view_cart"))
        content.append(pink_button("Continue Shopping", "shop"))

    return Page(state, content)


# -----------------------------
# START WEBSITE
# -----------------------------

start_server(
    State(
        products=[
            Product(
                "Mystery Hoodie",
                "Clothing",
                45,
                "A surprise hoodie with a random design.",
                10
            ),
            Product(
                "Duck Night Light",
                "Room Decor",
                18,
                "A cute little lamp for your bedroom.",
                10
            ),
            Product(
                "Mini Projector",
                "Technology",
                70,
                "A mini projector for movie nights.",
                5
            ),
            Product(
                "Strawberry Matcha Kit",
                "Food & Drinks",
                32,
                "Everything for strawberry matcha.",
                10
            ),
            Product(
                "Plush Frog",
                "Random Finds",
                16,
                "A tiny frog plushie.",
                10
            )
        ],
        cart=[],
        message="Welcome to the shop!"
    )
)




