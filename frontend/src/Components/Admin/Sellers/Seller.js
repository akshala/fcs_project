import React from "react";
import { ThumbUp } from "@material-ui/icons";
import { IconButton } from "@material-ui/core";

class Seller extends React.Component {

    constructor(props) {
        super(props);
        if(this.props.seller.approved == 1)
            this.state = {
                display: "none"
            }
        else
            this.state = {
                display: "unset"
            }
        this.delete = this.delete.bind(this);
        this.approve = this.approve.bind(this);
          
    }

    delete = () => {
        var axios = require('axios');
        axios.post('http://localhost:5000/delete_seller', {username: this.props.seller.username}).then((response) => {
            window.location.reload(false);
          });
    }

    approve = () => {
        var axios = require('axios');
        axios.post('http://localhost:5000/approve_seller', {username: this.props.seller.username}).then((response) => {
            this.setState({...this.state, display: "none"});
          });
    }

    render() {
        var url = "http://localhost:5000/get_document?username=" + this.props.seller.username;
        return (
        <div className="SellerCard">
            <div className="SellerUsername"><label>Username: </label>{this.props.seller.username}</div>
            <div className="SellerName"><label>Name: </label>{this.props.seller.name}</div>
            <div className="SellerEmail"><label>Email: </label>{this.props.seller.email}</div>
            <div className="SellerVerified"><label>Verification status: </label>{this.props.seller.verified}</div>
            <div className="SellerApproved"><label>Approval status: </label>{this.props.seller.approved}</div>
            <button onClick={(e) => {
                e.preventDefault();
                window.location.href=url;
                }}>View PDF</button>
            <div>
                <IconButton style={{display: this.state.display}} onClick={this.approve}>
                    <ThumbUp />
                    <span>Approve</span>
                </IconButton>
                <button onClick={this.delete}>Delete Seller</button>
            </div>
        </div>
        );
    }
}

export default Seller;