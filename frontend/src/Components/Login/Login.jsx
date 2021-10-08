import React from "react"
import { withRouter } from 'react-router-dom';
import "./Login.css";

class Login extends React.Component {

  constructor(props) {
    super(props)
    this.handleSubmit = this.handleSubmit.bind(this);
  }


  handleSubmit() {
    this.props.history.push("/Home");
  }

  render() {
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
  