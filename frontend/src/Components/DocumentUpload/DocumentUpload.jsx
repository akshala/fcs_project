import { Alert } from "@mui/material";
import React from "react"
import { withRouter } from 'react-router-dom';
import "./DocumentUpload.scss";

class DocumentUpload extends React.Component {

  constructor(props) {
    super(props)
    this.state = {}
    this.handleUpload = this.handleUpload.bind(this);
    this.username = '';
  }

  handleUpload() {
    // ev.preventDefault();

    const data = new FormData();
    data.append('file', this.uploadInput.files[0]);
    data.append('username', this.username);
    var axios = require('axios');
    axios.post('http://localhost:5000/upload', data).then((response) => {
      if(response.data == 'File Upload Successful') {
        this.setState({alert_severity: 'success', alert_message: response.data})
      } else {
        this.setState({alert_severity: 'error', alert_message: response.data})
      }
    });
    this.props.history.push("/Login");
    
  }

  render() {
    const { state } = this.props.location;
    this.username = this.props.location.state;
    return (
      <div className="Upload Verification Document">
        <h1>SignUp</h1>
        <div className="UploadBox">
          <div className="FileInput">
            <label>Upload Verification Document: </label>
            <input ref={(ref) => { this.uploadInput = ref; }} type="file" id="file" accept=".pdf" />
          </div>
          <input type="button" value="Submit" onClick={this.handleUpload} />
        </div>
        <p>
          Already a user?
        </p>
        <a href="/Login">Login Here</a>
        {this.state.alert_severity? 
          <Alert severity={this.state.alert_severity} variant="filled">{this.state.alert_message}</Alert>: ""
        }
      </div>
    );
  }

  }
  
  export default withRouter(DocumentUpload)
  