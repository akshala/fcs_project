import { useHistory } from 'react-router-dom';
import "./Login.css";

function Login() {
  const history = useHistory();

  function handleSubmit() {
    history.push("/Home");
  }

  return (
    <div className="Login">
      <h1>Login</h1>
      <div className="LoginBox">
        <div className="TextInput">
          <label>Username: </label>
          <input type="text" />
        </div>
        <div className="TextInput">
          <label>Password: </label>
          <input type="text" />
        </div>
        <input type="button" value="Submit" onClick={handleSubmit} />
      </div>
      <p>
        New to Amawon?
      </p>
      <a href="/SignUp">SignUp Here</a>
    </div>
  );

  }
  
  export default Login;
  