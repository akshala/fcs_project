import React from "react";
import { ThumbUpIcon } from '@mui/icons-material/ThumbUp';
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
                {/* <IconButton>
                    <ThumbUpIcon />
                    <span>Approve</span>
                </IconButton> */}
            </div>
        </div>
        );
    }
}

export default Seller;