import React from 'react';

class Checkout extends React.Component {
    constructor(props) {
        super(props);
        this.state = { 
            cart: sessionStorage.getItem('cart') ? sessionStorage.getItem('cart').split(',') : []
         }
    }
    render() { 
        return ( 
        <div>
            <li>
                {this.state.cart.map((item) => (<ul>{item}</ul>))}
            </li>
        </div> );
    }
}
 
export default Checkout;