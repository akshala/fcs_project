import React from "react";
import Seller from "./Seller"
import "./Sellers.css"

class Sellers extends React.Component {

    render() {
        return (
        <div className="SellerWindow">
            {this.props.sellers.map((seller) => 
            <Seller fetchLoginFromSessionStorage={this.props.fetchLoginFromSessionStorage} seller={seller} />
            )}
        </div>
        );
    }
}

export default Sellers;