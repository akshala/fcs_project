import React from "react"
import { withRouter } from 'react-router-dom';
import sha256 from 'crypto-js/sha256';
import cryptoRandomString from 'crypto-random-string';
import "./Login.scss";

class Login extends React.Component {

  constructor(props) {
    super(props)
    this.saltAndHash = this.saltAndHash.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  saltAndHash(message, salt) {
    const hashDigest = sha256(message + salt);
    return hashDigest + "";
  }

  handleSubmit() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    var axios = require('axios');
    var response = axios.post('http://localhost:5000/login', 
      {'password': this.saltAndHash(password, username), 'username': username}).then((response) => {
        if (response.data == "True")
            this.props.history.push("/Home");
        else
            console.log("User not verified / Invalid credentials"); //Display on frontend
      });

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
          <input type="button" value="Submit" onClick={this.handleSubmit} />
        </div>
        <p>
          New to Amawon?
        </p>
        <a href="/SignUp">SignUp Here</a>
      </div>
    );
  }

  }
  
  export default withRouter(Login);
  