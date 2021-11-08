import React from "react";
import { Add, AddShoppingCart, Edit, Remove } from "@material-ui/icons";
import { IconButton } from "@material-ui/core";
import { withRouter } from 'react-router-dom';
import "./ProductCard.scss"

class ProductCard extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            count: (sessionStorage.getItem('cart') ? sessionStorage.getItem('cart').split(',') : []).filter(id => id == this.props.product.id).length,
        }
    }

    addToCart = () => {
        this.props.addToCart(this.props.product.id)
        this.setState({count: this.state.count + 1})
    }

    removeFromCart = () => {
        this.props.removeFromCart(this.props.product.id)
        this.setState({count: this.state.count - 1})
    }

    render() {
        return (
        <div className="ProductCard">
            <img src={'https://192.168.2.239:5000/product_images/' + this.props.product.id +  '/' + this.props.product.images[0]} className="ProductImage" />
            <a href={'/products/' + this.props.product.id} className="ProductName">{this.props.product.name}</a>
            <div className="ProductDescription">{this.props.product.description}</div>
            <div className="ProductDescription">Rs.{this.props.product.price}</div>
            {this.props.role == 'Admin' || this.props.role == 'Seller' ? (
                    <IconButton onClick={() => {this.props.history.push(`/Products/${this.props.product.id}`)}}> 
                        <Edit /> 
                    </IconButton>) : 
            (this.props.role == 'User' ?
                (this.state.count == 0 ? (
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
            )): 
            (<div />))}
            
        </div>
        );
    }
}

export default withRouter(ProductCard);