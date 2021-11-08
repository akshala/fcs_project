import { Button } from "@material-ui/core";
import { Alert } from "@mui/material";
import React, { useState, useEffect } from "react";
import ProductCard from "../Home/ProductCard/ProductCard";
import './Checkout.scss'

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
            alert_message: query.get('success') ? 'Your order has been placed' : query.get('cancelled') ? 'Failed to place the order': null,
            loading: false
        }
        this.fetchProductDetails()

    }

    fetchProductDetails = () => {
      this.setState({loading: true});
      var axios = require('axios');
      axios.post(`https://192.168.2.239:5000/products/cart`, {cart: this.state.cart}, {
          headers: {
            Authorization: 'bearer ' + this.props.fetchLoginFromSessionStorage()['token']
          }
        }).then((response) => {
          this.setState({
              products: response.data,
              loading: false
          })
      });
    }

    sendCartToBackend = () => {

      this.setState({alert_severity: null, alert_message: null, loading: true})

      var axios = require('axios');

      axios.get('https://192.168.2.239:5000/get_certificate').then((response) => {
        var data = response.data
        
        if(!data['cert']) {
          this.setState({alert_severity: 'error', alert_message: 'Server certificate is invalid', loading: false});
          return;
        }

        axios.get('http://192.168.2.239:7000/get_public_key').then((response) => {
          var data2 = response.data
          var bigInt = require("big-integer")
          
          if(!bigInt(data['enc_m']).modPow(65537, bigInt(data['public_key'])).equals(bigInt(data['enc_m_CA']).modPow(65537, bigInt(data2['public_key_CA'])))) {
            this.setState({alert_severity: 'error', alert_message: 'Server certificate is invalid', lodaing: false});
            return;
          }
          var axios = require('axios');

          axios.post(`https://192.168.2.239:5000/create-checkout-session`, this.state.cart, {
            headers: {
              "Content-Type": 'application/json',
              Authorization: 'bearer ' + this.props.fetchLoginFromSessionStorage()['token']
            }
          }).then((response) => {
            window.location.href = response.data
            this.setState({loading: false});
        })

      })

      
    });
    }

    render() { 
        return ( 
        <div className="Cart">
            <div>
              {
                console.log(this.state.products)
              }
              {this.state.products.map((product) => 
                <ProductCard product={product}/>
              )}
            </div>
            {this.state.cart.length == 0? <div>No Items to show in cart!</div> : ""}
            {this.state.loading? <div>Loading...</div> : ""}
            <Button disabled={this.state.cart.length == 0} onClick={this.sendCartToBackend} type ="submit">
              Checkout
            </Button>
            {this.state.alert_severity? 
              <Alert severity={this.state.alert_severity} variant="filled">{this.state.alert_message}</Alert>: ""
            }
       </div> );
    }
}
 
export default Checkout;