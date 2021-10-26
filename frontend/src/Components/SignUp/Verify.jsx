import "./Verify.scss";
import React from "react"

class Verify extends React.Component {

  constructor(props) {
    super(props)
    this.handleSubmit = this.handleSubmit.bind(this);
    this.username = '';
    this.state = {
      verify_status: "Abc",
    }
  }

  handleSubmit() {
    // var username = document.getElementById('username').value;
    console.log(this.username);
    var otp = document.getElementById('otp').value;
    var axios = require('axios');
    var response = axios.post('http://localhost:5000/verify', 
      {'otp': otp, 'username': this.username}).then((response) => {
        this.setState({...this.state, verify_status: response.data});
        if (this.state.verify_status == "True")
            this.props.history.push("/Login");
        else
            console.log("Invalid OTP"); //Display on frontend
      });
  }

  render() {
    const { state } = this.props.location;
    this.username = this.props.location.state;
    return (
      <div className="Verification">
        <h1>Email Verification</h1>
        <div className="VerificationBox">
          {/* <div className="TextInput">
            <label>Enter Username: </label>
            <input type="text" id = "username" />
          </div> */}
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