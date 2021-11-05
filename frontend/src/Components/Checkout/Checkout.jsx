import { Button } from "@material-ui/core";
import React, { useState, useEffect } from "react";
import ProductCard from "../Home/ProductCard/ProductCard";

// import React from 'react';

class Checkout extends React.Component {
    constructor(props) {
        super(props);
        this.state = { 
            cart: sessionStorage.getItem('cart') ? sessionStorage.getItem('cart').split(',') : [],
            products: []
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
        </div> );
    }
}

// const ProductDisplay = () => (
//     <section>
//       <div className="product">
//         <img
//           src="https://i.imgur.com/EHyR2nP.png"
//           alt="The cover of Stubborn Attachments"
//         />
//         <div className="description">
//         <h3>Stubborn Attachments</h3>
//         <h5>$20.00</h5>
//         </div>
//       </div>
//       <form action="/create-checkout-session" method="POST">
//         <button type="submit">
//           Checkout
//         </button>
//       </form>
//     </section>
//   );

//   export default function App() {
//     const [message, setMessage] = useState("");
  
//     useEffect(() => {
//       // Check to see if this is a redirect back from Checkout
//       const query = new URLSearchParams(window.location.search);
  
//       if (query.get("success")) {
//         setMessage("Order placed! You will receive an email confirmation.");
//       }
  
//       if (query.get("canceled")) {
//         setMessage(
//           "Order canceled -- continue to shop around and checkout when you're ready."
//         );
//       }
//     }, []);

//     const Message = ({ message }) => (
//         <section>
//           <p>{message}</p>
//         </section>
//       );
      
  
//     return message ? (
//       <Message message={message} />
//     ) : (
//       <ProductDisplay />
//     );
//   }
  
 
export default Checkout;