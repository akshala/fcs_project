import React from "react"
import { withRouter } from 'react-router-dom';
import "./DocumentUpload.scss";

class DocumentUpload extends React.Component {

  constructor(props) {
    super(props)
    this.handleUpload = this.handleUpload.bind(this);
    this.username = '';
  }

  handleUpload() {
    // ev.preventDefault();

    const data = new FormData();
    data.append('file', this.uploadInput.files[0]);
    data.append('username', this.username);

    fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: data,
    }).then((response) => {
      response.json().then((body) => {
        console.log(response.data) });
    });
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
      </div>
    );
  }

  }
  
  export default withRouter(DocumentUpload)
  