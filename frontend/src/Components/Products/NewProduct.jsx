import { Button } from "@material-ui/core";
import { Add, Create, Delete, Update } from "@material-ui/icons";
import React from "react";

class NewProduct extends React.Component {
    constructor(props) {
        super(props);
        this.categories = ["Electronics", "Household", "Sports", "Fashion", "Entertainment"]
        this.state = {
            name: '',
            description: '',
            category: this.categories[0],
            price: 0,
        }
        this.create = this.create.bind(this);
        this.discard = this.discard.bind(this);
    }

    create() {
        var axios = require('axios');
        axios.post(`http://localhost:5000/products/new`, this.state).then((response) => {
            console.log(this.state);
            console.log(response.data)
        });
    }

    discard() {
        this.setState({name: '', category: '', price: ''});
    }
    render() { 
        return <div>
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
            <Button disabled={!(this.state.name && this.categories.includes(this.state.category) && this.state.price > 0)} onClick = {this.create}>
                    <Add />
                    <span>Create</span>
                </Button>
                <Button onClick = {this.discard}>
                    <Delete />
                    <span>Discard</span>
                </Button>
            </div>
        </div>;
    }
}
 
export default NewProduct;