import React from "react"
import { withRouter } from 'react-router-dom';
import "./SignUpSeller.scss";
import sha256 from 'crypto-js/sha256';
import cryptoRandomString from 'crypto-random-string';

class SignUpSeller extends React.Component {

  constructor(props) {
    super(props)
    this.saltAndHash = this.saltAndHash.bind(this);
    this.checkPassword = this.checkPassword.bind(this);
    this.checkEmailAvailibility = this.checkEmailAvailibility.bind(this);
    this.checkUsernameAvailibility = this.checkUsernameAvailibility.bind(this);
    this.retrieveSignUpDetails = this.retrieveSignUpDetails.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
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

  checkEmailAvailibility(email){
    let regexEmail = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    if (email.match(regexEmail)){
      return true;
    }else{
      return false;
    }
    // checkAvailibilityWithBackend();
  }

  checkUsernameAvailibility(username){
    //checkUsernameAvailibilityWithBackend();
    return true;
  }

  retrieveSignUpDetails() {
    var username = document.getElementById('username').value;
    var name = document.getElementById('name').value;
    var password = document.getElementById('password').value;
    var email = document.getElementById('email').value;

    if (this.checkPassword(password)){
      password = this.saltAndHash(password, username);
    }else{
      // showPasswordError()
      console.log('Oh no');
    }
    if(!this.checkEmailAvailibility(email)) {
      // showEmailError();
    }
    if(!this.checkUsernameAvailibility(username)){
      // showUsernameError();
    }
    const files: FileList = this.fileInput.nativeElement.files;
    if (files.length === 0) {
      return;
    };
    
    var axios = require('axios');
    const response = axios.post('http://localhost:5000/signup', 
      {'password': password, 'username': username, 'email': email, 'name': name}).then(response => response.data.id);

    const formData: FormData = new FormData();
    formData.append('file', files[0], files[0].name);
    formData.append('username', username);

    const response2 = axios.post('http://localhost:5000/upload_file', 
      formData).then(response => response.data.id);
    return {'password': password, 'username': username, 'email': email, 'name': name}
  }

  handleSubmit() {
    var details = this.retrieveSignUpDetails();
    this.props.history.push("/Verify");
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
            <input type="text" id = "password" />
          </div>
          <div className="FileInput">
            <label>Upload Verification Document: </label>
            <input type="file" id="file" accept=".pdf"/>
          </div>
          <input type="button" value="Submit" onClick={this.handleSubmit} />
        </div>
        <p>
          Already a user?
        </p>
        <a href="/Login">Login Here</a>
      </div>
    );
  }

  }
  
  export default withRouter(SignUpSeller);
  