import { Button } from "@material-ui/core";
import { Add, Delete} from "@material-ui/icons";
import React from "react";
import { withRouter } from 'react-router-dom';
import { Alert } from '@mui/material';


class NewProduct extends React.Component {
    constructor(props) {
        super(props);
        this.categories = ["Electronics", "Household", "Sports", "Fashion", "Entertainment"]
        this.state = {
            name: '',
            description: '',
            category: this.categories[0],
            price: 0,
            alert_severity: null,
            alert_message: null
        }
        this.create = this.create.bind(this);
        this.discard = this.discard.bind(this);
    }

    create() {
        this.setState({alert_severity: null, alert_message: null})
        var axios = require('axios');
        const data = new FormData();
        data.append('name', this.state.name);
        data.append('description', this.state.description); 
        data.append('category', this.state.category)
        data.append('price', this.state.price)
        data.append('image_1',  this.image1.files[0])
        data.append('image_2', this.image2.files[0])
        console.log(data)
        axios.post(`https://localhost:5000/products/new`, data,
        {
            headers: {
                Authorization: 'bearer ' + this.props.fetchLoginFromSessionStorage().token
            }
        }
        ).then((response) => {
            if(response.data == 'Product created successfully') {
                this.setState({
                    name: '',
                    description: '',
                    category: this.categories[0],
                    price: 0, 
                    alert_severity: 'success', 
                    alert_message: response.data})
            } else {
                this.setState({alert_severity: 'error', alert_message: response.data})
            }
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
            <div className="ProductText">
                <label>Image 1: </label>
                <input ref={(ref) => { this.image1 = ref; }} type="file" id="file" accept=".png, .jpg" />
            </div>
            <div className="ProductText">
                <label>Image 2: </label>
                <input ref={(ref) => { this.image2 = ref; }} type="file" id="file" accept=".png, .jpg" />
            </div>
            <div className="Controls">
            <Button disabled={!(this.state.name && this.categories.includes(this.state.category) && this.state.price > 0 && this.image1 && this.image2)} onClick = {this.create}>
                    <Add />
                    <span>Create</span>
                </Button>
                <Button onClick = {this.discard}>
                    <Delete />
                    <span>Discard</span>
                </Button>
            </div>
            {this.state.alert_severity? 
                <Alert severity={this.state.alert_severity} variant="filled">{this.state.alert_message}</Alert>: ""
            }
            
        </div>;
    }
}
 
export default withRouter(NewProduct);