export async function getCartQuantity(access_token) {
  try {
    const response = await fetch('https://jws-collections-gi44.vercel.app/api/v1/cart', {
      headers: {
        'Authorization': `Bearer ${access_token}`,
        'Content-Type': 'application/json'
      },
      method: 'GET',
    });
    if (!response.ok) {
      throw new Error('Failed to fetch cart quantity');
    }

    const data = await response.json();
    return data.items.length;
  } catch (error) {
    console.error('Error while getting cart quantity:', error);
    throw new Error('Error while getting cart quantity');
  }
}


export async function addToCart(shoe_id, quantity, access_token) {
    try {
        const response = await fetch('https://jws-collections-gi44.vercel.app/api/v1/cart/add', {
          headers: {
            'Authorization': `Bearer ${access_token}`,
            'Content-Type': 'application/json'
          },
          method: 'POST',
          body: JSON.stringify({ shoe_id, quantity }),
          credentials: 'include'
        });
        
        const data = await response.json();
        console.log(data);
        return true;
      } catch (error) {
        throw new Error('Error while adding to cart')
      }
}

export async function getCart(access_token) {
  try {
    const response = await fetch('https://jws-collections-gi44.vercel.app/api/v1/cart', {
      headers: {
        'Authorization': `Bearer ${access_token}`,
        'Content-Type': 'application/json'
      },
      method: 'GET',
    });
    if (!response.ok) {
      throw new Error('Failed to fetch cart');
    }

    const data = await response.json();
    return data.items;
  } catch (error) {
    console.error('Error while getting cart quantity:', error);
    throw new Error('Error while getting cart quantity');
  }
}
