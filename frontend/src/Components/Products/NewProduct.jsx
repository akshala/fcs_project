import { Button, IconButton } from "@material-ui/core";
import { Add, AddAPhoto, Delete, Remove} from "@material-ui/icons";
import React from "react";
import { withRouter } from 'react-router-dom';
import { Alert } from '@mui/material';
import ReCAPTCHA from "react-google-recaptcha";


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
            alert_message: null, 
            captcha: null,
            number_of_images: 2
        }
        this.images = [null, null]
        this.create = this.create.bind(this);
        this.discard = this.discard.bind(this);
        this.onChange = this.onChange.bind(this);
    }

    onChange(value) {
        this.setState({...this.state, captcha: value});
      }

    create() {
        this.setState({alert_severity: null, alert_message: null})
        var axios = require('axios');
        const data = new FormData();
        this.images.forEach((image, id) => {
            if(image?.files[0]) {
                data.append(`image_${id}`, image.files[0]);
            }
        })
        data.append('name', this.state.name);
        data.append('description', this.state.description); 
        data.append('category', this.state.category)
        data.append('price', this.state.price)
        data.append('captcha', this.state.captcha)
        axios.post(`https://192.168.2.239:5000/products/new`, data,
        {
            headers: {
                Authorization: 'bearer ' + this.props.fetchLoginFromSessionStorage().token
            }
        }
        ).then((response) => {
            if(response.data == 'success') {
                this.setState({
                    name: '',
                    description: '',
                    category: this.categories[0],
                    price: 0, 
                    alert_severity: 'success', 
                    alert_message: 'Product created successfully!'})
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
            {Array.from(Array(this.state.number_of_images).keys()).map((id) => <div className="ProductText">
                <label>Image {id + 1}: </label>
                <input ref={(ref) => { this.images[id] = ref; }} type="file" id="file" accept=".png, .jpg" />
            </div>)}
            <Button onClick={() => {this.setState({number_of_images: this.state.number_of_images + 1}, () => this.images.push(null));}} >
                <AddAPhoto /> 
                <span> Add more</span>
            </Button>
            <Button disabled={this.state.number_of_images <= 2} onClick={() => {this.setState({number_of_images: this.state.number_of_images - 1}, () => this.images.pop());}} >
                <Remove /> 
                <span> Remove</span>
            </Button>
            <ReCAPTCHA
            sitekey="6LeC2RodAAAAAH0Ujxo7YdsISfdqnJ1F48sZQXdy"
            onChange={this.onChange}
            />
            <div className="Controls">
            <Button disabled={!(this.state.name && this.categories.includes(this.state.category) && this.state.price > 0 && this.state.number_of_images >= 2)} onClick = {this.create}>
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