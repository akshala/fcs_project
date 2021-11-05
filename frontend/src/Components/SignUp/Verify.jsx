import "./Verify.scss";
import React from "react"
import { Alert } from "@mui/material";
import { withRouter } from 'react-router-dom';

class Verify extends React.Component {

  constructor(props) {
    super(props)
    this.handleSubmit = this.handleSubmit.bind(this);
    this.state = {}
  }

  handleSubmit() {
    var username = document.getElementById('username').value;
    var otp = document.getElementById('otp').value;
    var role = sessionStorage.getItem('role');
    var axios = require('axios');
    axios.post('http://localhost:5000/verify', 
      {'otp': otp, 'username': username}).then((response) => {
        if (response.data.slice(0, 5) == "true ") {
          this.props.login(role, response.data.slice(5));
          if(role == "Seller"){
            this.props.history.push({pathname: "/DocumentUpload", state: this.username});
          }
          else {
            this.props.history.push("/");
          }
        }
        else {
          this.setState({alert_severity: 'error', alert_message: response.data})
        }
      });
  }

  render() {
    return (
      <div className="Verification">
        <h1>Email Verification</h1>
        <div className="VerificationBox">
          <div className="TextInput">
            <label>Enter Username: </label>
            <input type="text" id = "username" />
          </div>
          <div className="TextInput">
            <label>Enter OTP: </label>
            <input type="text" id = "otp" />
          </div>
          <input type="button" value="Submit" onClick={this.handleSubmit} />
        </div>
        {this.state.alert_severity? 
          <Alert severity={this.state.alert_severity} variant="filled">{this.state.alert_message}</Alert>: ""
        }
      </div>
    );
  }
}
  
export default withRouter(Verify);