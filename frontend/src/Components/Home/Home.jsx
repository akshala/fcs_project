import "./Home.scss"
import React from "react"
import Product from "./ProductCard/ProductCard"


class Home extends React.Component {

  constructor(props) {
    super(props);
    this.categories = ["All", "Electronics", "Household", "Sports", "Fashion", "Entertainment"]
    this.state = {
      selectedCategory: this.categories[0],
      products: [],
      query: "",
      filteredProducts: [],
      cart: sessionStorage.getItem('cart') ? sessionStorage.getItem('cart').split(',') : [],
      showCart: false,
      isAdmin: this.props.admin
    }
    this.fetchProducts();
  }

  fetchProducts = () => {
    var axios = require('axios');
    axios.get('http://localhost:5000/products', { 
      headers: { 
        Authorization: `Bearer ${data.token}`
      }
    }).then((response) => {
      this.setState({...this.state, products: response.data, filteredProducts: response.data})
    });
  } 

  updateCategory = (event) => {
    this.setState({...this.state, selectedCategory: event.target.value}, () => {
      this.filterProducts();
    })
  }

  filterProducts = () => {
    var filtered = this.state.products.filter((product) => {
      var isResult = (this.state.selectedCategory == 'All' || product.category == this.state.selectedCategory) && this.state.query.toLowerCase() == product.name.substring(0, this.state.query.length).toLowerCase();
      return isResult;
    })
    this.setState({filteredProducts: filtered})
  }

  handleSearchQueryChange = (event) => {
    this.setState({...this.state, query: event.target.value}, () => {
      this.filterProducts()
    })
  }

  addToCart = (id) => {
    sessionStorage.setItem('cart', [...this.state.cart, id])
    this.setState({cart: [...this.state.cart, id]}, () => console.log(this.state.cart));
  }

  removeFromCart = (id) => {
    var tempCart = []
    var deleted = false;
    for(var i in this.state.cart) {
      if(id == this.state.cart[i].id || !deleted) {
        deleted = true;
        continue;
      } else {
        tempCart.push(this.state.cart[i])
      }
    }
    sessionStorage.setItem('cart', tempCart)
    this.setState({cart: tempCart}, () => console.log(this.state.cart));
  }

  render() {
    return (
      <div className="Home">
        <div className="Categories">
          {this.categories.map((category) => <input aria-selected={this.state.selectedCategory==category} type="button" value={category} onClick={this.updateCategory} />)}
        </div>
        <div className="Search">
          <input value={this.state.query} onChange={this.handleSearchQueryChange} type="text" className="Sarch" placeholder="Search for product name, description etc" />
        </div>
        <div className="ProductsWindow">
            {this.state.filteredProducts.map((product) => 
            <Product admin={this.props.admin} product={product} addToCart={this.addToCart} removeFromCart={this.removeFromCart} />
            )}
        </div>
      </div>
    );
  }
}

export default Home;
