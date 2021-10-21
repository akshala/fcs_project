import React from "react";
import { ThumbUp } from "@material-ui/icons";
import { IconButton } from "@material-ui/core";

class Seller extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            display: "unset"
          }
    }

    approve = () => {
        var axios = require('axios');
        axios.get('http://localhost:5000/approve_seller').then((response) => {
            return true
          });

        this.state = {
        display: "none"
        }
    }

    render() {
        return (
        <div className="SellerCard">
            <div className="SellerName">{this.props.seller.name}</div>
            <div className="SellerDescription">{this.props.seller.description}</div>
            <div>
                <IconButton style={{display: this.state.display}} onClick={this.approve}>
                    <ThumbUp />
                    <span>Approve</span>
                </IconButton>
            </div>
        </div>
        );
    }
}

export default Seller;