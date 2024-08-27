export async function placeOrder(access_token) {
    try {
        const response = await fetch('https://jws-collections-gi44.vercel.app/api/v1/checkout', {
          headers: {
            'Authorization': `Bearer ${access_token}`,
            'Content-Type': 'application/json'
          },
          method: 'POST',
          credentials: 'include'
        });
        
        const data = await response.json();
        return data;
      } catch (error) {
        throw new Error('Error while checking out')
      }
}


export async function getOrder(access_token) {
  try {
      const response = await fetch('https://jws-collections-gi44.vercel.app/api/v1/order', {
        headers: {
          'Authorization': `Bearer ${access_token}`,
          'Content-Type': 'application/json'
        },
        method: 'GET',
        credentials: 'include'
      });
  
      const data = await response.json();
      return data;
    } catch (error) {
      throw new Error('Error while checking out')
    }
}
