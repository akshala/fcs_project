import React from "react";

class Product extends React.Component {

    render() {
        return (
        <div className="ProductCard">
            <img src={this.props.product.image} className="ProductImage" />
            <div className="ProductName">{this.props.product.name}</div>
            <div className="ProductDescription">{this.props.product.description}</div>
        </div>
        );
    }
}

export default Product;