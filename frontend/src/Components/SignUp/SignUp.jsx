import "./SignUp.scss";
import React from "react"
import { withRouter } from 'react-router-dom';
import sha256 from 'crypto-js/sha256';
import cryptoRandomString from 'crypto-random-string';
import { Alert } from "@mui/material";
import ReCAPTCHA from "react-google-recaptcha";

class SignUp extends React.Component {

  constructor(props) {
    super(props)
    this.saltAndHash = this.saltAndHash.bind(this);
    this.checkPassword = this.checkPassword.bind(this);
    this.checkEmail = this.checkEmail.bind(this);
    this.retrieveSignUpDetails = this.retrieveSignUpDetails.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.change = this.change.bind(this);
    this.username = ''
    this.onChange = this.onChange.bind(this);
    this.state = {
      type: "",
      alert_severity: null,
      alert_message: null,
      captcha: null,
      loading: false
    }
  }

  onChange(value) {
    this.setState({...this.state, captcha: value});
}

 
  saltAndHash(message, salt) {
    const hashDigest = sha256(message + salt);
    return hashDigest + "";
  }

  checkPassword(s) {
    if (s.length < 8){
      return false;
    }
    var c1 = 0, c2 = 0, c3 = 0;
    for (var i = 0;i < s.length; i++){
      if (s[i] >= 'A' && s[i] <= 'Z'){
        c1 = 1;
      }
      if (s[i] >= 'a' && s[i] <= 'z'){
        c2 = 1;
      }
      if (s[i] >= '0' && s[i] <= '9'){
        c3 = 1;
      }
    }
    if (c1 === 1 && c2 === 1 && c3 === 1){
      return true;
    }
    return false;
  }

  checkEmail(email){
    let regexEmail = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    if (email.match(regexEmail)){
      return true;
    }else{
      return false;
    }
  }

  retrieveSignUpDetails() {
    var username = document.getElementById('username').value;
    var name = document.getElementById('name').value;
    var password = document.getElementById('password').value;
    var email = document.getElementById('email').value;
    var type = document.getElementById('role').value;
    

    this.username = username;

    if (this.checkPassword(password)){
      password = this.saltAndHash(password, username);
    }else{
      this.setState({alert_severity: 'error', alert_message: 'Password does not meet the requirements of length 8, atleast one capital, atleast one small letter, atleast one number'})
      return;
    }
    if(!this.checkEmail(email)) {
      this.setState({alert_severity: 'error', alert_message: 'Invalid Email Address'})
      return;
    }
    var axios = require('axios');
    axios.post('https://localhost:5000/signup', 
      {'password': password, 'username': username, 'email': email, 'name': name, 'type': type, 'captcha': this.state.captcha}).then((response) => {
        this.setState({loading: false});
        if(response.data == 'success') {
          sessionStorage.setItem('role', type);
          this.props.history.push({pathname: "/Verify", state: this.username});  
        } else {
          this.setState({alert_severity: 'error', alert_message: response.data});
        }
      });
    return type;
  }

  handleSubmit() {
    this.setState({alert_severity: null, alert_message: null, loading: true})
    var type = this.retrieveSignUpDetails();
  }

  change(event) {
    this.setState({...this.state, type: event.target.value});
  }

  render() {
    return (
      <div className="SignUp">
        <h1>SignUp</h1>
        <div className="SignUpBox">
          <div className="TextInput">
            <label>Username: </label>
            <input type="text" id = "username" />
          </div>
          <div className="TextInput">
            <label>Name: </label>
            <input type="text" id = "name" />
          </div>
          <div className="TextInput">
            <label>Email ID: </label>
            <input type="text" id = "email" />
          </div>
          <div className="TextInput">
            <label>Password: </label>
            <input type="password" id = "password" />
          </div>
          <div className="TextInput">
            <select value="Role" id = "role" onChange={this.change} value={this.state.type}>
              <option value="User">User</option>
              <option value="Seller">Seller</option>
            </select>
          </div> 
          <ReCAPTCHA
            sitekey="6LeE2RodAAAAAI5vXnGOLTPz4Leg0RnLCJ6CK2GU"
            onChange={this.onChange}
            />
          <input type="button" value="Submit" onClick={this.handleSubmit} />
          {this.state.loading? <div className="Loading"> loading... </div>: ""}
        </div>
        <p>
          Already a user?
        </p>
        <a href="/Login">Login Here</a>
        {this.state.alert_severity? 
          <Alert severity={this.state.alert_severity} variant="filled">{this.state.alert_message}</Alert>: ""
        }
 
      </div>
    );
  }
}
  
export default SignUp;