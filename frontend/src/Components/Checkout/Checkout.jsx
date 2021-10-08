import React from 'react';

class Checkout extends React.Component {
    constructor(props) {
        super(props);
        this.state = { 
            cart: sessionStorage.getItem('cart') ? sessionStorage.getItem('cart').split(',') : []
         }
         console.log(`cart: ${this.state.cart}`)
    }
    render() { 
        console.log(`cart: ${this.state.cart}`)
        return ( 
        <div>
            <li>
                {this.state.cart.map((item) => (<ul>{item}</ul>))}
            </li>
        </div> );
    }
}
 
export default Checkout;