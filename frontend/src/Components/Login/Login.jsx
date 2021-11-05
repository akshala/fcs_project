import React from "react"
import { withRouter } from 'react-router-dom';
import sha256 from 'crypto-js/sha256';
import cryptoRandomString from 'crypto-random-string';
import "./Login.scss";
import { Alert } from "@mui/material";

class Login extends React.Component {

  constructor(props) {
    super(props)
    this.saltAndHash = this.saltAndHash.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.change = this.change.bind(this);
    this.state = {
      type: "",
    }
  }

  saltAndHash(message, salt) {
    const hashDigest = sha256(message + salt);
    return hashDigest + "";
  }

  handleSubmit() {
    this.setState({alert_severity: null, alert_message: null})

    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var role = document.getElementById('role').value;

    var axios = require('axios');
    var response = axios.post('http://localhost:5000/login', 
      {'password': this.saltAndHash(password, username), 'username': username, 'role': role}).then((response) => {

        if (response.data.slice(0, 5) == 'true ') {
          this.props.login(role, response.data.slice(5));
          this.props.history.push("/Home");
        }
        else
            this.setState({alert_severity: 'error', alert_message: response.data})
      });

  }
  change(event) {
    this.setState({...this.state, type: event.target.value});
  }

  render() {
    return (
      <div className="Login">
        <h1>Login</h1>
        <div className="LoginBox">
          <div className="TextInput">
            <label>Username: </label>
            <input type="text" id="username" />
          </div>
          <div className="TextInput">
            <label>Password: </label>
            <input type="text" id="password" />
          </div>
          <div>
          {/* <label>Role:</label> */}
          <select value="Role" id = "role" onChange={this.change} value={this.state.type}>
            <option value="User">User</option>
            <option value="Seller">Seller</option>
          </select>
          </div> 
          <input type="button" value="Submit" onClick={this.handleSubmit} />
        </div>
        <p>
          New to Amawon?
        </p>
        <a href="/SignUp">SignUp Here</a>
        {this.state.alert_severity? 
          <Alert severity={this.state.alert_severity} variant="filled">{this.state.alert_message}</Alert>: ""
        }
      </div>
    );
  }

  }
  
  export default withRouter(Login);
  