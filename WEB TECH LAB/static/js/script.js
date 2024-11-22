document.addEventListener("DOMContentLoaded", () => {
    // Check the session state by making an API request to check if the user is logged in
    fetch('/check_login')
        .then(response => response.json())
        .then(data => {
            const isLoggedIn = data.logged_in;

            // Show/Hide login and logout links based on login state
            document.getElementById("login-link").style.display = isLoggedIn ? "none" : "block";
            document.getElementById("logout-link").style.display = isLoggedIn ? "block" : "none";

            // Fetch books and render them
            fetch('http://127.0.0.1:5000/books')
                .then(response => response.json())
                .then(data => {
                    const bookList = document.getElementById("book-list");
                    data.forEach(book => {
                        const bookDiv = document.createElement("div");
                        bookDiv.className = "book";
                        bookDiv.innerHTML = `
                            <h3>${book.title}</h3>
                            <p>Author: ${book.author}</p>
                            <p>Price: $${book.price}</p>
                            <button class="add-to-cart" onclick="addToCart('${book.title}')">Add to Cart</button>
                        `;
                        bookList.appendChild(bookDiv);
                    });

                    // Show "Add to Cart" buttons if the user is logged in
                    if (isLoggedIn) {
                        const cartButtons = document.querySelectorAll(".add-to-cart");
                        cartButtons.forEach((button) => {
                            button.style.display = "inline-block";
                        });
                    }
                })
                .catch(err => console.error("Error fetching books:", err));
        })
        .catch(err => console.error("Error checking login status:", err));
});

// Function to add a book to the cart
function addToCart(bookTitle) {
    alert(`${bookTitle} has been added to your cart!`);
    // Additional logic to save the cart state can go here
}
