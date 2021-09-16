import React from "react";
import Product from "./Product"
import "./Products.css"

class Products extends React.Component {

    render() {
        return (
        <div className="ProductsWindow">
            {this.props.products.map((product) => 
            <Product product={product} />
            )}
        </div>
        );
    }
}

export default Products;