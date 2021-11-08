import "./Home.scss"
import "./ProductCard/ProductCard.scss"
import React from "react"
import ProductCard from "./ProductCard/ProductCard"
import { Button } from "@material-ui/core";
import { Add } from "@material-ui/icons";
import { withRouter } from 'react-router-dom';


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
    }
    this.fetchProducts();
  }

  fetchProducts = () => {
    var axios = require('axios');
    axios.get('https://192.168.2.239:5000/products', { 
      headers: { 
        Authorization: 'bearer ' + this.props.fetchLoginFromSessionStorage()['token']
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
      var isResult = (this.state.selectedCategory == 'All' || product.category == this.state.selectedCategory) && product.name.toLowerCase().includes(this.state.query.toLowerCase());
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
            {this.props.role == 'Seller' ? (
              <div className="ProductCard">
                <Button onClick={() => {this.props.history.push('/Products/New')}}> 
                  <Add /> Add product
                </Button>
              </div>
            ): ""}
            {this.state.filteredProducts.map((product) => 
            <ProductCard role={this.props.role} product={product} addToCart={this.addToCart} removeFromCart={this.removeFromCart} />
            )}
        </div>
      </div>
    );
  }
}

export default withRouter(Home);
