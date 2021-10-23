import "./Verify.scss";
import React from "react"

class Verify extends React.Component {

  constructor(props) {
    super(props)
    this.handleSubmit = this.handleSubmit.bind(this);
    this.state = {
        verification_status: false
    }
  }

  retrieveVerificationDetails() {
    var otp = document.getElementById('otp').value;

    var axios = require('axios');
    axios.get('http://localhost:5000/verify', { params: { user_otp: otp } }).then((response) => {
        this.setState({...this.state, verification_status: response.data})
      });

  }

  handleSubmit() {
    // this.props.history.push("/Home");
    var details = this.retrieveVerificationDetails();
    if (this.state) {
        this.props.history.push("/Home");
    }
  }

  render() {
    return (
      <div className="Verification">
        <h1>Email Verification</h1>
        <div className="VerificationBox">
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