import { Button } from "@material-ui/core";
import { Alert } from "@mui/material";
import React, { useState, useEffect } from "react";
import ProductCard from "../Home/ProductCard/ProductCard";

// import React from 'react';

class Checkout extends React.Component {
    constructor(props) {
        super(props);
        var query = new URLSearchParams(window.location.search);
        if(query.get('success')) {
          sessionStorage.setItem('cart', [])
        }
        this.state = { 
            cart: sessionStorage.getItem('cart') ? sessionStorage.getItem('cart').split(',') : [],
            products: [],
            alert_severity: query.get('success') ? 'success' : query.get('cancelled') ? 'error': null,
            alert_message: query.get('success') ? 'Your order has been placed' : query.get('cancelled') ? 'Failed to place the order': null
         }
        this.state.cart.forEach(element => {
          this.fetchProductDetails(element)
        });

    }

    fetchProductDetails = (x) => {
      var axios = require('axios');
      axios.get(`http://localhost:5000/products/${x}`, {
          headers: {
            Authorization: 'bearer ' + this.props.fetchLoginFromSessionStorage()['token']
          }
        }).then((response) => {
          this.product = response.data
          this.setState({
              products: [...this.state.products, response.data]
          })
          console.log(response.data);
      });
    }

    sendCartToBackend = () => {
      var axios = require('axios');
      // const data = new FormData();
      // this.state.products.forEach(element => {
      //   data.append(element.id)
      // });
      // console.log(data)
      axios.post(`http://localhost:5000/create-checkout-session`, this.state.cart, {
        headers: {
          "Content-Type": 'application/json',
          Authorization: 'bearer ' + this.props.fetchLoginFromSessionStorage()['token']
        }
      }).then((response) => {
        console.log(this.state);
        console.log(response.data)
        window.location.href = response.data
    });
    }

    render() { 
        return ( 
        <div>
            {this.state.products.map((product) => 
              <ProductCard product={product}/>
            )}
         <Button onClick={this.sendCartToBackend} type ="submit">
           Checkout
         </Button>
         {this.state.alert_severity? 
          <Alert severity={this.state.alert_severity} variant="filled">{this.state.alert_message}</Alert>: ""
        }
       </div> );
    }
}
 
export default Checkout;