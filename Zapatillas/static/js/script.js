// Carrusel de imágenes
const slides = document.querySelector('.slides');
const slideCount = document.querySelectorAll('.slide').length;
let currentIndex = 0;

function changeSlide() {
  currentIndex = (currentIndex + 1) % slideCount;
  const offset = -currentIndex * 100;
  slides.style.transform = `translateX(${offset}%)`;
}

// Cambiar la imagen cada 3 segundos
setInterval(changeSlide, 3000);

// Botón de navegación
document.querySelector('.toggle_btn').addEventListener('click', function () {
  const navbar = document.querySelector('.navbar');
  const menu = document.querySelector('ul');
  navbar.classList.toggle('expanded');
  menu.classList.toggle('show');
  
  // Ocultar el botón de toggle cuando el menú se expande
  if (navbar.classList.contains('expanded')) {
    document.querySelector('.toggle_btn').style.display = 'none';
  } else {
    document.querySelector('.toggle_btn').style.display = 'block';
  }
});

// OpenAI Chat
document.getElementById('chat-popup').style.display = 'block';

document.getElementById('close-popup').addEventListener('click', function() {
    document.getElementById('chat-popup').style.display = 'none';
});

document.getElementById('send-btn').addEventListener('click', function() {
    const userInput = document.getElementById('user-input').value;
    if (userInput) {
        const chatBody = document.querySelector('.chat-body');
        const newMessage = document.createElement('p');
        newMessage.textContent = userInput;
        chatBody.appendChild(newMessage);
        document.getElementById('user-input').value = ''; // Limpiar el input
    }
});

// Carrito de Compras: Añadir al carrito
function addToCart(productId, productName, productPrice) {
    fetch('/add_to_cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'product_id': productId,
            'product_name': productName,
            'product_price': productPrice,
            'quantity': 1  // Puedes ajustar la cantidad según lo necesario
        })
    }).then(response => {
        if (response.ok) {
            alert('Producto agregado al carrito');
        } else {
            alert('Hubo un problema al agregar el producto al carrito.');
        }
    });
}

// Carrito de Compras: Actualizar cantidad de productos
function updateQuantity(index, change) {
    const cartItem = document.querySelector(`#price-${index}`).closest('.cart-item');
    let quantity = parseInt(cartItem.querySelector('.quantity-input').value);

    // Actualizar la cantidad
    quantity += change;

    // Prevenir que la cantidad sea menor que 1
    if (quantity < 1) {
        quantity = 1;
    }

    cartItem.querySelector('.quantity-input').value = quantity;

    // Actualizar el precio en la interfaz
    const priceElement = cartItem.querySelector('.price');
    const productPrice = parseFloat(priceElement.getAttribute('data-price'));
    const newPrice = (productPrice * quantity).toFixed(2);
    priceElement.textContent = `$${newPrice}`;

    // Enviar solicitud al servidor para actualizar la cantidad en la sesión
    fetch('/update_cart_quantity', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ index: index, quantity: quantity })
    }).then(response => {
        if (!response.ok) {
            alert('Hubo un problema al actualizar la cantidad.');
        }
    });
}

// Carrito de Compras: Eliminar un artículo
function removeItem(index) {
    const cartItem = document.querySelector(`#price-${index}`).closest('.cart-item');
    cartItem.remove();

    // Enviar solicitud al servidor para eliminar el artículo del carrito
    fetch('/remove_from_cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ index: index })
    }).then(response => {
        if (!response.ok) {
            alert('Hubo un problema al eliminar el artículo.');
        }
    });
}

function addToCart(id, nombre, precio) {
    // Código para agregar el producto al carrito
    console.log("Agregando al carrito:", id, nombre, precio);
}

document.querySelectorAll('.card__button').forEach(button => {
    button.addEventListener('click', function(event) {
        event.preventDefault(); // Prevenir el comportamiento por defecto del enlace
        const productId = this.getAttribute('data-id');
        const productName = this.getAttribute('data-name');
        const productPrice = parseFloat(this.getAttribute('data-price'));

        addToCart(productId, productName, productPrice);
    });
});
