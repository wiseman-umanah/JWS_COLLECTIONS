import { email_validation } from "./utils/utils.js";
import { loginUser, SignupUser } from "./utils/auth.js";

function flippage(event) {
  event.preventDefault();
  const $flipCardInner = $('.flip-card-inner');
  const $flipButton = $('#flipButton');

  $flipCardInner.toggleClass('flip');
  
  if ($flipCardInner.hasClass('flip')) {
      $flipButton.text('Switch to Login');
      $("title").text("Signup");
  } else {
      $flipButton.text('Switch to Signup');
      $("title").text("Login");
  }
}

function email_valid() {
  const email = $(this).val();
    if (email_validation(email)) {
      $(this).css('border-color', 'green');
    } else {
      $(this).css('border-color', 'red');
    }
}

function show_hide_password(input) {
  if (input.attr('type') === 'password') {
    console.log(true)
      input.attr('type', 'text');
  } else {
      input.attr('type', 'password');
  }
}


$(document).ready(function() {
  const $flipButton = $('#flipButton');
  const $loginForm = $('#loginForm');
  const $signupForm = $('#signupForm');

  $flipButton.on('click', flippage)

  $('#email').on('input', email_valid)
  $('#signup_email').on('input', email_valid)

  $('#signup_show_password').on('click', function() {
    show_hide_password($('input[id="signup_password"]'));
  });

  $('#login_show_password').on('click', function() {
    show_hide_password($('input[id="password"]'));
  });

  $loginForm.on('submit', async function(event) {
    event.preventDefault();
    
    const email = $('input[id="email"]').val();
    const password = $('input[id="password"]').val();

    if (!email_validation(email)) {
        alert('Invalid email address -- user@gmail.com');
        return;
    }
    
    try {
        const { access_token, refresh_token } = await loginUser(email, password);
        
        if (access_token && refresh_token) {
            localStorage.setItem('access_token', access_token);
            localStorage.setItem('refresh_token', refresh_token);
            document.cookie = `access_token=${access_token}; path=/; Secure; SameSite=None`;
            window.location.href = '/store';
        } else {
            alert('Invalid credentials. Please try again.');
        }
    } catch (e) {
        alert(e.message || 'An error occurred during login.');
    }
});


  $signupForm.on('submit', async function(event) {
    event.preventDefault();

    const email = $('input[id="signup_email"]').val();
    const password = $('input[id="signup_password"]').val();
    const firstname = $('input[name="firstname"]').val();
    const lastname = $('input[name="lastname"]').val();    
    const username = $('input[name="username"]').val();

    if (!email_validation(email)) {
        alert('Invalid email address -- user@gmail.com');
        return;
    }
    
    try {
      await SignupUser(firstname, lastname, username, email, password);
      flippage(event)
    } catch (e) {
      alert(e.message || 'An error occurred during login.');
  }
  });
});
