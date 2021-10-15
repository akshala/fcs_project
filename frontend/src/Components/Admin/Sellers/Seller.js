import React from "react";
import { ThumbUp } from "@material-ui/icons";
import { IconButton } from "@material-ui/core";

class Seller extends React.Component {

    constructor(props) {
        super(props);
    }

    approve = () => {
    }

    render() {
        return (
        <div className="SellerCard">
            <div className="SellerName">{this.props.seller.name}</div>
            <div className="SellerDescription">{this.props.seller.description}</div>
            <div>
                <IconButton>
                    <ThumbUp />
                    <span>Approve</span>
                </IconButton>
            </div>
        </div>
        );
    }
}

export default Seller;