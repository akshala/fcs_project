import { Button, IconButton, StepButton } from "@material-ui/core";
import { Delete, Save, SaveAlt, Update } from "@material-ui/icons";
import React from "react";
import './Products.scss'

class Products extends React.Component {
    constructor(props) {
        super(props);
        this.categories = ["Electronics", "Household", "Sports", "Fashion", "Entertainment"]
        this.state = {
            id: this.props.match.params.id,
        }
        this.product = {
            id: this.props.match.params.id
        }
        this.update = this.update.bind(this)
        this.fetchProductDetails();
      }
    
      fetchProductDetails = () => {
        var axios = require('axios');
        axios.get(`http://localhost:5000/products/${this.state.id}`).then((response) => {
            this.product = response.data
            this.setState({
                ...response.data
            })
        });
    }
    
    update =() => {
        console.log(this.product)
        console.log(this.state)
        // console.log(`update from ${this.product} to ${this.state}`)
        var axios = require('axios');
        axios.post(`http://localhost:5000/products/${this.state.id}`, this.state).then((response) => {
            console.log(response.data)
        });
    }
    
    delete =() => {
        console.log(`delete`)
        var axios = require('axios');
        axios.delete(`http://localhost:5000/products/${this.state.id}`).then((response) => {
            console.log(response.data)
        });
    }
    
    discard =() => {
        this.setState({...this.product})
    }
    
    
    render() {
        return (
        <div>
            <div className="Heading">
                <h2>Product ID: {this.state.id}</h2>
                <h2>Seller ID: {this.state.seller}</h2>
                <Button onClick = {this.delete}>
                    <Delete />
                    <span>Delete</span>
                </Button>
            </div>
            
            <div className="ProductText">
                <span>Product Name: </span>
                <input value={this.state.name} onChange={(event) => this.setState({name: event.target.value})} />
            </div>
            <div className="ProductText">
                <span>Description: </span>
                <input value={this.state.description} onChange={(event) => this.setState({description: event.target.value})} />
            </div>
            <div className="ProductText">
                <span>Category: </span>
                <select value={this.state.category} onChange={(event) => this.setState({category: event.target.value})} >
                    {this.categories.map((category) => (<option value={category}>{category}</option>))}
                </select>
            </div>
            <div className="ProductText">
                <span>Price: </span>
                <input type="number" value={this.state.price} onChange={(event) => this.setState({price: event.target.value})} />
            </div>
            <div className="Controls">
            <Button disabled={!(this.state.name && this.categories.includes(this.state.category) && this.state.price > 0)} onClick = {this.update}>
                    <Update />
                    <span>Update</span>
                </Button>
                <Button onClick = {this.discard}>
                    <Delete />
                    <span>Discard</span>
                </Button>
            </div>
        </div>);
    }
}
 
export default Products;