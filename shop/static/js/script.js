function getCSRFToken() {
    var name = 'csrftoken';
    var value = document.cookie.match('(^|;)\\s*' + name + '=([^;]*)');
    return value ? value.pop() : '';
}


let cart = JSON.parse(localStorage.getItem('cart')) || [];  // Load cart from localStorage if it exists, or initialize as an empty array

// Save cart to localStorage whenever it changes
function saveCartToLocalStorage() {
    localStorage.setItem('cart', JSON.stringify(cart));
}


// window.onload = function() {
//     // Clear the localStorage on page load
//     localStorage.removeItem('cart');
// };


window.addToCart= function(id, name, price, image) {

    if (image.startsWith('/static/static/')) {
        image = image.replace('/static/static/', '/static/');
    }
    console.log("Adding to cart", id, name, price, image); 
    updateCartCount();

    
    const existingItemIndex = cart.findIndex(item => item.id === id);

    if (!id || !name || !price || !image) {
        console.error('Error: Missing or invalid product data');
        return;
    }

    if (id === undefined || name === undefined || price === undefined || image === undefined) {
        console.error('Error: Missing product data');
        return;
    }
    // Check if the product already exists in the cart
    let product = cart.find(item => item.id === id);

    if (product) {
        // If the product already exists, increase its quantity
        product.quantity += 1;
    } else {
        // If the product doesn't exist, add it to the cart with quantity 1
        cart.push({ id: id, name: name, price: price, quantity: 1, image:image });
    }

    console.log(cart); // For testing purposes

    // Update the cart count and display the updated cart
    updateCartCount();
     // Save updated cart to localStorage
     saveCartToLocalStorage();
}

function updateCartCount() {
    // Get the current cart data from localStorage
    
    const cartCount = cart.reduce((total, item) => total + item.quantity, 0);

    // Update the cart count displayed on the page
    const cartCountElement = document.getElementById('cart-count');
    if (cartCountElement) {
        cartCountElement.innerText = cartCount;
    }
}



function saveChanges() {
    // Get all the rows from the table
    const rows = document.querySelectorAll('#productsTable tbody tr');
    const updatedData = [];

    // Iterate through each row to collect the data
    rows.forEach(row => {
        const product = {
            product_name: row.querySelector('.product_name').value,
            product_description: row.querySelector('.product_description').value,
            price: parseFloat(row.querySelector('.price').value),
            category_name: row.querySelector('.category_name').value,
            brand: row.querySelector('.brand').value,
            color: row.querySelector('.color').value,
            size: row.querySelector('.size').value,
            quantity: parseInt(row.querySelector('.quantity').value),
            availability: row.querySelector('.availability').checked,
            rating: parseFloat(row.querySelector('.rating').value),
            reviews: parseInt(row.querySelector('.reviews').value),
            expiry_date: row.querySelector('.expiry_date').value,
            shipping_cost: parseFloat(row.querySelector('.shipping_cost').value),
            seller_name: row.querySelector('.seller_name').value,
            seller_rating: parseFloat(row.querySelector('.seller_rating').value),
        };
        updatedData.push(product);
    });

    // Send data to the server
    fetch('', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ products_data: updatedData }),
    })
        .then(response => response.json())
        .then(data => {
            console.log("Server response:", data);
            alert(data.message);
            if (data.success) {
                location.reload();
            }
        })
        .catch(error => console.error('Error:', error));
}



function submitCart() {
    const cartData = JSON.parse(localStorage.getItem('cart')) || [];
    
    if (cartData.length === 0) {
        alert('Your cart is empty!');
        return;
    }

    const csrfToken = getCSRFToken();

    fetch('/checkout/', { // Adjust to your actual checkout URL
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ cart_items: cartData })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Server response:', data);
        if (data.success) {
            alert('Cart submitted successfully!');
            localStorage.removeItem('cart');  // Clear cart if submission is successful
            // Optionally redirect or refresh the page
        } else {
            alert('Failed to submit cart');
        }
    })
    .catch(error => {
        console.error('Error submitting cart:', error);
        alert('An error occurred while submitting the cart');
    });
}




function addProductRow() {
    const tableBody = document.querySelector('#productsTable tbody');

    const newRow = document.createElement('tr');
    newRow.innerHTML = `
        <td><input type="text" class="product_name" value=""></td>
        <td><input type="text" class="product_description" value=""></td>
        <td><input type="number" class="price" step="0.01" value=""></td>
        <td><input type="text" class="category_name" value=""></td>
        <td><input type="text" class="brand" value=""></td>
        <td><input type="text" class="color" value=""></td>
        <td><input type="text" class="size" value=""></td>
        <td><input type="number" class="quantity" value=""></td>
        <td><input type="checkbox" class="availability"></td>
        <td><input type="number" class="rating" step="0.1" value=""></td>
        <td><input type="number" class="reviews" value=""></td>
        <td><input type="text" class="expiry_date" value=""></td>
        <td><input type="number" class="shipping_cost" step="0.01" value=""></td>
        <td><input type="text" class="seller_name" value=""></td>
        <td><input type="number" class="seller_rating" step="0.1" value=""></td>
    `;
    tableBody.appendChild(newRow);
}