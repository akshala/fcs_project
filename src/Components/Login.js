function Login() {
  return (
    <div className="SignUp">
      <h1>Login</h1>
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
        New to Amawon?
      </p>
      <a href="/SignUp">SignUp Here</a>
    </div>
  );

  }
  
  export default Login;
  