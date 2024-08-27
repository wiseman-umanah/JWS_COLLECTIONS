import { getCart } from "./utils/cart.js";

$(document).ready(() => {
    async function fetchCartItems() {
        const accessToken = localStorage.getItem('access_token');
        if (!accessToken) {
            console.error('Access token not found. Redirecting to login.');
            window.location.href = '/login';  // Redirect if no access token
            return null;
        }

        try {
            const cartData = await getCart(accessToken);
            return cartData;
        } catch (error) {
            console.error('Error while getting cart data:', error);
            return null;
        }
    }

    function cartItem() {
        const shippingHandling = 4.99;
        const estimatedTaxRate = 0.10;

        let cartHTML = '';

        fetchCartItems()
        .then(data => {
            if (!data || !data.length) {
                console.error('No cart data found or cart is empty.');
                return;
            }

            const currentCart = data;
            const numCart = currentCart.length;
            let total_price = 0;

            currentCart.forEach((item) => {
                total_price += item.total_price;
                cartHTML += `
                <div class="cart-item-container">
                    <div class="cart-item-details-grid">
                        <img class="product-image" src="${item.shoe_image}" alt="${item.shoe_name}">
                        <div class="cart-item-details">
                            <div class="product-name">
                                ${item.shoe_name}
                            </div>
                            <div class="product-price">
                                $${item.price.toFixed(2)}
                            </div>
                            <div class="product-quantity">
                                <span>
                                    Quantity: <span class="quantity-label">${item.quantity}</span>
                                </span>
                            </div>
                        </div>
                    </div>
                </div>`;
            });

            $('.return-to-home-link').text(numCart);
            $('.order-summary').html(cartHTML);

            const estimatedTax = total_price * estimatedTaxRate;
            const totalBeforeTax = total_price + shippingHandling;
            const orderTotal = totalBeforeTax + estimatedTax;

            const paymentSummaryHTML = `
            <div class="payment-summary-title">
                Order Summary
            </div>
            <div class="payment-summary-row">
                <div>Items (${numCart}):</div>
                <div class="payment-summary-money">$${total_price.toFixed(2)}</div>
            </div>
    
            <div class="payment-summary-row">
                <div>Shipping &amp; handling:</div>
                <div class="payment-summary-money">$${shippingHandling.toFixed(2)}</div>
            </div>
    
            <div class="payment-summary-row subtotal-row">
                <div>Total before tax:</div>
                <div class="payment-summary-money">$${totalBeforeTax.toFixed(2)}</div>
            </div>
    
            <div class="payment-summary-row">
                <div>Estimated tax (${(estimatedTaxRate * 100).toFixed(0)}%):</div>
                <div class="payment-summary-money">$${estimatedTax.toFixed(2)}</div>
            </div>
    
            <div class="payment-summary-row total-row">
                <div>Order total:</div>
                <div class="payment-summary-money">$${orderTotal.toFixed(2)}</div>
            </div>
    
            <button class="place-order-button button-primary">
                Place your order
            </button>
        `;
    
        $('.payment-summary').html(paymentSummaryHTML);
        }).catch(error => {
            console.error('Error fetching cart data:', error);
        });
    }
        
    cartItem();
});
