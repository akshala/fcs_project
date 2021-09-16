import "./SignUp.css";
import { useHistory } from 'react-router-dom';

function SignUp() {
  const history = useHistory();
  function handleSubmit() {
    history.push("/Home");
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
            <input type="text" />
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
  