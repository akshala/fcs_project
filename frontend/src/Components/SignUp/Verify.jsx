import "./Verify.scss";
import React from "react"
import { Alert } from "@mui/material";
import { withRouter } from 'react-router-dom';
import Keyboard from 'react-virtual-keyboard';

class Verify extends React.Component {

  constructor(props) {
    super(props)
    this.handleSubmit = this.handleSubmit.bind(this);
    this.state = {}
  }


  onInputChanged = (data) => {
    this.setState({ input: data });
  }
  
  onInputSubmitted = (data) => {
    console.log("Input submitted:", data);
  }

  handleSubmit() {
    var username = document.getElementById('username').value;
    var otp = this.state.input;
    console.log('otp: ', otp);
    var role = sessionStorage.getItem('role');
    var axios = require('axios');
    axios.post('https://localhost:5000/verify', 
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
            {/* <input type="text" id = "otp" /> */}
            <Keyboard 
            value={this.state.input}
            name='keyboard'
            options={{
              type:"input",
              layout: "qwerty",
              alwaysOpen: false,
              usePreview: false,
              useWheel: false,
              stickyShift: false,
              appendLocally: true,
              color: "light",
              updateOnChange: true,
              initialFocus: true,
              lockInput: true,
              display: {
                "accept" : "Submit"
              }
            }}
            onChange={this.onInputChanged}
            onAccepted={this.onInputSubmitted}
            ref={k => this.keyboard = k}
          />
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