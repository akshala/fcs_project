import React from "react"
import { withRouter } from 'react-router-dom';
import "./Login.scss";

class Login extends React.Component {

  constructor(props) {
    super(props)
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  verifyLogin() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    var axios = require('axios');
    const response = axios.post('http://localhost:5000/login', 
      {'password': password, 'username': username}).then(response => response.data.id).then((response) => {
        console.log(response.data);
        this.props.history.push("/Home");
      })
  }


  handleSubmit() {
    this.verifyLogin();
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
  