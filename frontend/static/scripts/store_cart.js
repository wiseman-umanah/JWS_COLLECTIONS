import { getCartQuantity, addToCart } from './utils/cart.js';


$(document).ready(() => {
    $(document).on('click', '.js-add-to-cart', async function() {
        const productId = $(this).data('product-id');
        const quantity = $(this).closest('.product-container')
                              .find('.product-quantity')
                              .val();

        try {
            let access_token = localStorage.getItem('access_token');
            let success = await addToCart(productId, quantity, access_token);

            if (success) {
                let cart_quantity = await getCartQuantity(localStorage.getItem('access_token'));
                if (cart_quantity) {
                    $('.js-cart-quantity').text(cart_quantity);
                } else {
                    console.error('Cart number not updated');
                }
            } else {
                console.error("Failed to add product after token refresh");
            }
        } catch (error) {
            console.error('Error:', error.message);
        }
    });
});
