import { Button, IconButton, StepButton } from "@material-ui/core";
import { Delete, Save, SaveAlt, Share, Update } from "@material-ui/icons";
import { Alert } from "@mui/material";
import React from "react";
import './Products.scss'
import { withRouter } from 'react-router-dom';


class Products extends React.Component {
    constructor(props) {
        super(props);
        this.categories = ["Electronics", "Household", "Sports", "Fashion", "Entertainment"]
        this.state = {
            id: this.props.match.params.id,
            role: this.props.fetchLoginFromSessionStorage()['role'],
            alert_severity: null,
            alert_message: null,
            images: []
        }
        this.product = {
            id: this.props.match.params.id
        }
        this.update = this.update.bind(this)
        this.fetchProductDetails();
      }
    
      fetchProductDetails = () => {
        var axios = require('axios');
        axios.get(`http://localhost:5000/products/${this.state.id}`, {
            headers: {
              Authorization: 'bearer ' + this.props.fetchLoginFromSessionStorage()['token']
            }
          }).then((response) => {
              console.log(response.data)
            this.product = response.data
            this.setState({
                ...response.data
            })
        });
    }
    
    update =() => {
        this.setState({alert_severity: null, alert_message: null});
        var axios = require('axios');
        axios.post(`http://localhost:5000/products/${this.state.id}`, this.state, {
            headers: {
              Authorization: 'bearer ' + this.props.fetchLoginFromSessionStorage()['token']
            }
          }).then((response) => {
            if(response.data == 'update success') {
                this.props.history.push('/');
            } else {
                this.setState({alert_severity: 'error', alert_message: response.data});
            }        
        });
    }
    
    delete =() => {
        this.setState({alert_severity: null, alert_message: null});
        var axios = require('axios');
        axios.delete(`http://localhost:5000/products/${this.state.id}`, {
            headers: {
              Authorization: 'bearer ' + this.props.fetchLoginFromSessionStorage()['token']
            }
          }).then((response) => {
            if(response.data == 'delete success') {
                this.props.history.push('/');
            } else {
                this.setState({alert_severity: 'error', alert_message: response.data});
            }
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
                <h2>Seller ID: {this.state.seller_id}</h2>
                {this.state.role == 'User' ? '': <Button onClick = {this.delete}>
                    <Delete />
                    <span>Delete</span>
                </Button>}
                <IconButton onClick={() => {navigator.clipboard.writeText(window.location); this.setState({alert_severity: 'info', alert_message: 'Link copied to clipboard'})}}>
                    <Share />
                </IconButton>
            </div>

            <div className="ProductText">
                <span>Product Name: </span>
                {this.state.role == 'User' ? <span>{this.state.name}</span> : <input value={this.state.name} onChange={(event) => this.setState({name: event.target.value})} />}
            </div>
            <div className="ProductText">
                <span>Description: </span>
                {this.state.role == 'User' ? <span>{this.state.description}</span> : <input value={this.state.description} onChange={(event) => this.setState({description: event.target.value})} />}
            </div>
            <div className="ProductText">
                <span>Category: </span>
                {this.state.role == 'User' ? <span>{this.state.category}</span> : 
                <select value={this.state.category} onChange={(event) => this.setState({category: event.target.value})} >
                    {this.categories.map((category) => (<option value={category}>{category}</option>))}
                </select>}
            </div>
            <div className="ProductText">
                <span>Price: </span>
                {this.state.role == 'User' ? <span>{this.state.price}</span> :
                <input type="number" value={this.state.price} onChange={(event) => this.setState({price: event.target.value})} />}
            </div>
            {this.state.role == 'User' ? "":
                <div className="Controls">
                    <Button disabled={!(this.state.name && this.categories.includes(this.state.category) && this.state.price > 0)} onClick = {this.update}>
                        <Update />
                        <span>Update</span>
                    </Button>
                    <Button onClick = {this.discard}>
                        <Delete />
                        <span>Discard</span>
                    </Button>
                </div>}
                <div className="ProductImages">
                    {this.state.images.map((image) => <div className="ProductImageWrapper"> <img src={'http://localhost:5000/product_images/' + this.state.id +  '/' + image} className="ProductImage" /> </div>)}
                </div>
            {this.state.alert_severity? 
                <Alert severity={this.state.alert_severity} variant="filled">{this.state.alert_message}</Alert>: ""
            }
         </div>);
    }
}
 
export default withRouter(Products);