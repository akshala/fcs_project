import "./Admin_user.css"
import React from "react"
import Users from "./Users"

class Admin_user extends React.Component {

  constructor(props) {
    super(props);
    this.fetchUsers();
    this.state = {
      users: []
    }
  }

  fetchUsers = () => {
    var axios = require('axios');
    axios.get('https://192.168.2.239:5000/users', {
      headers: {
        Authorization: 'bearer ' + this.props.fetchLoginFromSessionStorage()['token']
      }
    }).then((response) => {
      this.setState({...this.state, users: response.data})
    });
  } 

    render() {
        return (
          <div className="Admin_user">
            <h1>Welcome Admin!</h1>
            <Users fetchLoginFromSessionStorage={this.props.fetchLoginFromSessionStorage} users={this.state.users}/>
          </div>
        );
      }
      
}

export default Admin_user;