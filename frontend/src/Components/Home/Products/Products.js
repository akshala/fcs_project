import React from "react";
import Product from "./Product"
import "./Products.css"

class Products extends React.Component {

    addToCart = (id) => {
        this.props.addToCart(id);
    }

    removeFromCart = (id) => {
        this.props.removeFromCart(id);
    }

    render() {
        return (
        <div className="ProductsWindow">
            {this.props.products.map((product) => 
            <Product product={product} addToCart={this.addToCart} removeFromCart={this.removeFromCart} />
            )}
        </div>
        );
    }
}

export default Products;