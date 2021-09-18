import React from "react";
import { Add, AddShoppingCart, Remove } from "@material-ui/icons";
import { IconButton } from "@material-ui/core";

class Product extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            count: 0,
        }
    }

    addToCart = () => {
        this.props.addToCart(this.props.product)
        this.setState({count: this.state.count + 1})
    }

    removeFromCart = () => {
        this.props.removeFromCart(this.props.product)
        this.setState({count: this.state.count - 1})
    }

    render() {
        return (
        <div className="ProductCard">
            <img src={this.props.product.image} className="ProductImage" />
            <div className="ProductName">{this.props.product.name}</div>
            <div className="ProductDescription">{this.props.product.description}</div>
            {this.state.count == 0 ? (
            <IconButton onClick={this.addToCart}>
                <AddShoppingCart />
            </IconButton>) : (
            <div>
                <IconButton onClick={this.addToCart}>
                    <Add />
                </IconButton>
                <span>{this.state.count}</span>
                <IconButton onClick={this.removeFromCart}>
                    <Remove />
                </IconButton>
            </div>
                

            )}
            
        </div>
        );
    }
}

export default Product;