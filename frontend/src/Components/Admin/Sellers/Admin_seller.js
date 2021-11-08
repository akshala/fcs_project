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
    axios.get('https://192.168.2.239:5000/sellers', {
      headers: {
        Authorization: 'bearer ' + this.props.fetchLoginFromSessionStorage()['token']
      }
    }).then((response) => {
      this.setState({...this.state, sellers: response.data})
    });
  } 

    render() {
        return (
          <div className="Admin">
            <h1>Welcome Admin!</h1>
            <Sellers fetchLoginFromSessionStorage={this.props.fetchLoginFromSessionStorage} sellers={this.state.sellers}/>
          </div>
        );
      }
      
}

export default Admin_seller;