import "./Admin_seller.css"
import React from "react"
import Sellers from "./Sellers"

class Admin_seller extends React.Component {

  constructor(props) {
    super(props);
    this.fetchSellers();
    this.state = {
      sellers: []
    }
  }

  fetchSellers = () => {
    var axios = require('axios');
    axios.get('http://localhost:5000/sellers').then((response) => {
      this.setState({...this.state, sellers: response.data})
    });
  } 

    render() {
        return (
          <div className="Admin">
            <h1>Welcome Admin!</h1>
            <Sellers sellers={this.state.sellers}/>
          </div>
        );
      }
      
}

export default Admin_seller;