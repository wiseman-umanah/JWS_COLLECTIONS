export async function loginUser(email, password) {
    const response = await fetch('https://jws-collections-gi44.vercel.app/api/v1/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });
    
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Login failed');
    }

    const data = await response.json();
    return data;
}

export async function SignupUser(firstname, lastname, username, email, password) {
    const response = await fetch('https://jws-collections-gi44.vercel.app/api/v1/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password, firstname, lastname, username })
    });
    
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Signup failed');
    }
}

  