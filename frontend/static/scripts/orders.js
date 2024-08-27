import { getOrder } from "./utils/place_order.js";

$(document).ready(() => {
    async function fetchOrders() {
        let accessToken = localStorage.getItem('access_token');
        let orderData = await getOrder(accessToken);
        
        return orderData;
    }
        
    
    function generateOrderHTML() {
        fetchOrders()
        .then(data => {
            if (!data) {
                return;
            }
    
            let orderHTML = '';
    
            const currentOrder = data;
            currentOrder.forEach((orderItem) => {
                orderHTML += `
                <div class="order-container">
                    <div class="order-header">
                        <div class="order-header-left-section">
                            <div class="order-date">
                                <div class="order-header-label">Order Placed:</div>
                                <div>${orderItem.created_at}</div>
                            </div>
                            <div class="order-total">
                                <div class="order-header-label">Total:</div>
                                <div>$${orderItem.total_price.toFixed(2)}</div>
                            </div>
                        </div>
                        <div class="order-header-right-section">
                            <div class="order-header-label">Order ID:</div>
                            <div>${orderItem.id}</div>
                        </div>
                    </div>
    
                    `;
                
                orderItem.items.forEach(cartItem => {
                    orderHTML += `
                    <div class="order-details-grid">
                        <div class="product-image-container">
                            <img src="${cartItem.shoe_image}" alt="${cartItem.shoe_name}">
                        </div>
                        <div class="product-details">
                            <div class="product-name">
                                ${cartItem.shoe_name}
                            </div>
                            <div class="product-quantity">
                                Quantity: ${cartItem.quantity}
                            </div>                    
                        </div>
                    </div>`;
                });
    
                // orderHTML += `</div>`;
            });
            $('.orders-grid').html(orderHTML);
    
        })
        .catch(error => {
            console.error('Error fetching order data:', error);
        });
    }

    generateOrderHTML();    
})