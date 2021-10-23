import "./Verify.scss";
import React from "react"

class Verify extends React.Component {

  constructor(props) {
    super(props)
    this.retrieveVerificationDetails = this.retrieveVerificationDetails.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  retrieveVerificationDetails() {
    var username = document.getElementById('username').value;
    var otp = document.getElementById('otp').value;

    // var axios = require('axios');
    // const response = axios.post('http://localhost:5000/verify', 
    //   {'otp': otp, 'username': username}).then(response => response.data.id);
    // return response

  }

  handleSubmit() {
    // this.props.history.push("/Home");
    var details = this.retrieveVerificationDetails();
    // if (details) {
    //     this.props.history.push("/Home");
    // }
  }

  render() {
    // const { state } = this.props.location;
    // var username = this.props.location.state;
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
      </div>
    );
  }
}
  
export default Verify;