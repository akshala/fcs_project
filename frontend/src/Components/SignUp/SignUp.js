import "./SignUp.css";
import { useHistory } from 'react-router-dom';
import sha256 from 'crypto-js/sha256';
import cryptoRandomString from 'crypto-random-string';

function SignUp() {
  const history = useHistory();
 
   function saltAndHash(message, salt) {
  	const hashDigest = sha256(message + salt);
  	return {'hash': hashDigest};
  }

  function checkPassword(s) {
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

  function checkEmailAvailibility(email){
    let regexEmail = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    if (email.match(regexEmail)){
      return true;
    }else{
      return false;
    }
    // checkAvailibilityWithBackend();
  }

  function checkUsernameAvailibility(username){
    //checkUsernameAvailibilityWithBackend();
    return true;
  }

  function retrieveSignUpDetails() {
    var username = document.getElementById('username').value;
    var name = document.getElementById('name').value;
    var password = document.getElementById('password').value;
    var email = document.getElementById('email').value;

    if (checkPassword(password)){
      password = saltAndHash(password, username);
    }else{
      //showPasswordError()
      console.log('Oh no');
    }
    if(!checkEmailAvailibility(email)) {
      // showEmailError();
    }
    if(!checkUsernameAvailibility(username)){
      // showUsernameError();
    }
    return {'password': password, 'username': username, 'email': email, 'name': name}
  }
  function handleSubmit() {
    // history.push("/Home");
    var details = retrieveSignUpDetails();
  }
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
          <input type="button" value="Submit" onClick={handleSubmit} />
        </div>
        <p>
          Already a user?
        </p>
        <a href="/Login">Login Here</a>
      </div>
    );
  }

  function signup() {
    
  }
  
  export default SignUp;
 