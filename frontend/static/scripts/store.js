import { get_products } from './utils/products.js'


$(document).ready(() => {
  let productsHTML = '';
  let currentProducts = [];
  let currentPage = 1;
  let lastPage = 1;
  const itemsPerPage = 10;

  function renderProducts(products) {
    productsHTML = '';
    products.forEach((product) => {
      productsHTML += `
        <div class="product-container">
          <div class="product-image-container">
            <img class="product-image" src="${product._shoe_image}">
          </div>
          <div class="product-name limit-text-to-2-lines">
            ${product.shoe_name}
          </div>
          <div class="product-price">
            $ ${product._shoe_price}
          </div>
          <div class="product-quantity-container">
            <select class="product-quantity" id=product-quantity>
              <option selected value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
              <option value="5">5</option>
              <option value="6">6</option>
              <option value="7">7</option>
              <option value="8">8</option>
              <option value="9">9</option>
              <option value="10">10</option>
            </select>
          </div>
          <div class="product-spacer"></div>
          <div class="added-to-cart">
            <img src="static/images/icons/checkmark.png">
            Added
          </div>
          <button class="add-to-cart-button button-primary js-add-to-cart" data-product-id="${product.id}">
            Add to Cart
          </button>
        </div>
      `;
    });

    $('.js-products-grid').html(productsHTML);
  }
  
  function updatePages(page, totalPages) {
    $('.current-page').text(`Page ${page} of ${totalPages}`);
  }

  function queryProducts(category = '', brand = '', min_price = '', max_price = '', color = '') {
    get_products(currentPage, itemsPerPage, category, brand, min_price, max_price, color)
      .then(data => {
        currentProducts = data.products;
        currentPage = data.page;
        lastPage = data.total_pages;
        updatePages(currentPage, lastPage);
        renderProducts(currentProducts);
      })
      .catch(error => {
        console.error('Error fetching products:', error);
      });
  }

  function filterProducts(query) {
    const filtered = currentProducts.filter(product =>
      product.shoe_name.toLowerCase().includes(query.toLowerCase())
    );
    renderProducts(filtered);
  }

  queryProducts();

  $('.search-bar').on('input', function() {
    const query = $(this).val();
    filterProducts(query);
  });


  $('input[name="category"]').on('change', function() {
    const category = $(this).val();
    currentPage = 1;
    queryProducts(category, 
      $('input[name="brand"]:checked').val(), 
      $('input[name="min-price"]').val(), 
      $('input[name="max-price"]').val(), 
      $('input[name="color"]').val());
  });

  $('input[name="brand"]').on('change', function() {
    const brand = $(this).val();
    currentPage = 1;
    queryProducts($('input[name="category"]:checked').val(), 
    brand, $('input[name="min-price"]').val(), 
    $('input[name="max-price"]').val(), 
    $('input[name="color"]').val());
  });

  $('input[name="min-price"]').on('input', function() {
    const min_price = $(this).val();
    currentPage = 1;
    queryProducts($('input[name="category"]:checked').val(), 
    $('input[name="brand"]:checked').val(), 
    min_price, $('input[name="max-price"]').val(), 
    $('input[name="color"]').val());
  });

  $('input[name="max-price"]').on('input', function() {
    const max_price = $(this).val();
    currentPage = 1;
    queryProducts($('input[name="category"]:checked').val(), 
    $('input[name="brand"]:checked').val(), 
    $('input[name="min-price"]').val(), 
    max_price, $('input[name="color"]').val());
  });

  $('input[name="color"]').on('input', function() {
    const color = $(this).val();
    currentPage = 1;
    queryProducts($('input[name="category"]:checked').val(), 
    $('input[name="brand"]:checked').val(), 
    $('input[name="min-price"]').val(), 
    $('input[name="max-price"]').val(), color);
  });

  $('.next-page').on('click', function() {
    if (currentPage < lastPage) {
      currentPage++;
      queryProducts(
        $('input[name="category"]:checked').val(),
        $('input[name="brand"]:checked').val(),
        $('input[name="min-price"]').val(),
        $('input[name="max-price"]').val(),
        $('input[name="color"]').val()
      );
    }
  });

  $('.prev-page').on('click', function() {
    if (currentPage > 1) {
      currentPage--;
      queryProducts(
        $('input[name="category"]:checked').val(),
        $('input[name="brand"]:checked').val(),
        $('input[name="min-price"]').val(),
        $('input[name="max-price"]').val(),
        $('input[name="color"]').val()
      );
    }
  });
});

