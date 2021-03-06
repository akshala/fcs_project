import React from "react"
import { withRouter } from 'react-router-dom';
import sha256 from 'crypto-js/sha256';
import cryptoRandomString from 'crypto-random-string';
import "./Login.scss";
import { Alert } from "@mui/material";
import ReCAPTCHA from "react-google-recaptcha";

class Login extends React.Component {

  constructor(props) {
    super(props)
    this.saltAndHash = this.saltAndHash.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.change = this.change.bind(this);
    this.onChange = this.onChange.bind(this);
    this.state = {
      type: "",
      loading: false,
      captcha: null
    }
  }

  onChange(value) {
    this.setState({captcha: value});
  }

  saltAndHash(message, salt) {
    const hashDigest = sha256(message + salt);
    return hashDigest + "";
  }

  handleSubmit() {
    this.setState({alert_severity: null, alert_message: null, loading: true})

    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var role = document.getElementById('role').value;

    var axios = require('axios');

    axios.get('https://192.168.2.239:5000/get_certificate').then((response) => {
      var data = response.data
      
      if(!data['cert']) {
        this.setState({alert_severity: 'error', alert_message: 'Server certificate is invalid'});
        return;
      }

      axios.get('https://192.168.2.239:3001/get_public_key').then((response) => {
        var data2 = response.data
        var bigInt = require("big-integer")
        
        if(!bigInt(data['enc_m']).modPow(65537, bigInt(data['public_key'])).equals(bigInt(data['enc_m_CA']).modPow(65537, bigInt(data2['public_key_CA'])))) {
          this.setState({alert_severity: 'error', alert_message: 'Server certificate is invalid'});
          return;
        }

        console.log(this.state)

        axios.post('https://192.168.2.239:5000/login', 
        {'password': this.saltAndHash(password, username), 'username': username, 'role': role, 'captcha': this.state.captcha}).then((response) => {
          var data = response.data
          if (role == "Admin") {
            if (data.slice(0, 5) == 'true '){
              sessionStorage.setItem('role', role);
              this.props.history.push({pathname: "/Verify", state: username});
            }
            else {
              this.setState({alert_severity: 'error', alert_message: response.data})
            }
          } else {
            if (data.slice(0, 5) == 'true '){
              this.props.login(role, response.data.slice(5));
              this.props.history.push("/Home");
            }
            else {
              this.setState({alert_severity: 'error', alert_message: response.data})
            }
          }
          this.setState({loading:false});
        });
      })

    })
  }

  change(event) {
    this.setState({...this.state, type: event.target.value});
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
            <input type="password" id="password" />
          </div>
          <div>
          {/* <label>Role:</label> */}
          <select value="Role" id = "role" onChange={this.change} value={this.state.type}>
            <option value="User">User</option>
            <option value="Seller">Seller</option>
            <option value="Admin">Admin</option>
          </select>
          </div> 
          <ReCAPTCHA
            sitekey="6LeC2RodAAAAAH0Ujxo7YdsISfdqnJ1F48sZQXdy"
            onChange={this.onChange}
            />
          <input type="button" value="Submit" onClick={this.handleSubmit} />
          {this.state.loading? <div className="Loading"> loading... </div>: ""}
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
  