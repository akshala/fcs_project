import React, { useState, useEffect } from "react";

// import React from 'react';

// class Checkout extends React.Component {
//     constructor(props) {
//         super(props);
//         this.state = { 
//             cart: sessionStorage.getItem('cart') ? sessionStorage.getItem('cart').split(',') : []
//          }
//     }
//     render() { 
//         return ( 
//         <div>
//             <li>
//                 {this.state.cart.map((item) => (<ul>{item}</ul>))}
//             </li>
//         </div> );
//     }
// }

const ProductDisplay = () => (
    <section>
      <div className="product">
        <img
          src="https://i.imgur.com/EHyR2nP.png"
          alt="The cover of Stubborn Attachments"
        />
        <div className="description">
        <h3>Stubborn Attachments</h3>
        <h5>$20.00</h5>
        </div>
      </div>
      <form action="/create-checkout-session" method="POST">
        <button type="submit">
          Checkout
        </button>
      </form>
    </section>
  );

  export default function App() {
    const [message, setMessage] = useState("");
  
    useEffect(() => {
      // Check to see if this is a redirect back from Checkout
      const query = new URLSearchParams(window.location.search);
  
      if (query.get("success")) {
        setMessage("Order placed! You will receive an email confirmation.");
      }
  
      if (query.get("canceled")) {
        setMessage(
          "Order canceled -- continue to shop around and checkout when you're ready."
        );
      }
    }, []);

    const Message = ({ message }) => (
        <section>
          <p>{message}</p>
        </section>
      );
      
  
    return message ? (
      <Message message={message} />
    ) : (
      <ProductDisplay />
    );
  }
  
 
// export default Checkout;