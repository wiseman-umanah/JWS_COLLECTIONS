let inactivityTimeout;
const INACTIVITY_TIME_LIMIT = (10 - 5) * 60 * 1000;

function startInactivityTimer() {
  inactivityTimeout = setTimeout(logout, INACTIVITY_TIME_LIMIT);
}

function resetInactivityTimer() {
  clearTimeout(inactivityTimeout);
  startInactivityTimer();
}


function logout() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  deleteCookie('access_token');
  window.location.href = '/login';
}

function refreshToken() {
  const refreshToken = localStorage.getItem('refresh_token');
  if (refreshToken) {
    fetch('/refresh', {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + refreshToken
      }
    })
    .then(response => response.json())
    .then(data => {
      if (data.access_token) {
        localStorage.setItem('access_token', data.access_token);
      } else {
        logout();
      }
    })
    .catch(err => {
      console.error('Failed to refresh token:', err);
      logout();
    });
  } else {
    logout();
  }
}


['click', 'mousemove', 'keypress'].forEach(event => {
  document.addEventListener(event, resetInactivityTimer);
});

function isAuthenticated() {
    const accessToken = localStorage.getItem('access_token');
    return !!accessToken;
}

document.addEventListener('DOMContentLoaded', function() {
    const protectedRoutes = ['/store', '/checkout', '/order'];

    protectedRoutes.forEach(route => {
        if (window.location.pathname === route && !isAuthenticated()) {
            window.location.href = '/login';
        }
    });
});


startInactivityTimer();

setInterval(refreshToken, (10 - 1) * 60 * 1000);
