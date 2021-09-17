import "./SignUp.css";
import { useHistory } from 'react-router-dom';
import sha256 from 'crypto-js/sha256';
import cryptoRandomString from 'crypto-random-string';

function SignUp() {
  const history = useHistory();
  function handleSubmit() {
    history.push("/Home");
  }
   function saltAndHash() {
   	var message = document.getElementById("password").value;
  	const salt = cryptoRandomString({length: 10, type: 'alphanumeric'});
  	const hashDigest = sha256(message + salt);
  	console.log(hashDigest + "    " + salt);
  	return {'hash': hashDigest, 'salt': salt};
  }
    return (
      <div className="SignUp">
        <h1>SignUp</h1>
        <div className="SignUpBox">
          <div className="TextInput">
            <label>Username: </label>
            <input type="text" />
          </div>
          <div className="TextInput">
            <label>Name: </label>
            <input type="text" />
          </div>
          <div className="TextInput">
            <label>Email ID: </label>
            <input type="text" />
          </div>
          <div className="TextInput">
            <label>Password: </label>
            <input type="text" id = "password" />
          </div>
          <input type="button" value="Submit" onClick={saltAndHash} />
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
 