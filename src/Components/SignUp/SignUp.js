import "./SignUp.css";

function SignUp() {
    return (
      <div className="SignUp">
        <h1>SignUp</h1>
        <div className="SignUpBox">
          <div className="TextInput">
            <label>Username: </label>
            <input type="text" />
          </div>
          <div className="TextInput">
            <label>Password: </label>
            <input type="text" />
          </div>
          <input type="button" value="Submit" />
        </div>
        <p>
          Already a user?
        </p>
        <a href="/Login">Login Here</a>
      </div>
    );
  }
  
  export default SignUp;
  