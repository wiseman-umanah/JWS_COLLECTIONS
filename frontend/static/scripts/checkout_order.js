import { placeOrder } from "./utils/place_order.js";


$(document).ready(() => {
    $(document).on('click', '.place-order-button', async function() {
        console.log('hello')
        let accessToken = localStorage.getItem('access_token');

        let response = await placeOrder(accessToken);

        console.log(response.message);
        localStorage.setItem('order_id', response.order_id);
        })
});
