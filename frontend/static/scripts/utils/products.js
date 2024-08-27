
let api_url = "https://jws-collections-gi44.vercel.app/api/v1/products"

export function get_products(page=1,
  per_page=30, category="", brand="",
min_price=undefined, max_price=undefined, color="") {
  const url = new URL(api_url);

  if (page) {
    url.searchParams.append('page', page)
  }
  if (per_page) {
    url.searchParams.append('per_page', per_page)
  }
  if (category) {
    url.searchParams.append('category', category)
  }
  if (brand) {
    url.searchParams.append('brand', brand)
  }
  if (min_price) {
    url.searchParams.append('min_price', min_price)
  }
  if (max_price) {
    url.searchParams.append('max_price', max_price)
  }
  if (color) {
    url.searchParams.append('color', color)
  }

  return fetch(url)
    .then(response => response.json())
    .then(data => data);
}

