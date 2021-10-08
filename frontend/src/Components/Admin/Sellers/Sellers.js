import React from "react";
import Seller from "./Seller"
import "./Sellers.css"

class Sellers extends React.Component {

    render() {
        return (
        <div className="SellersWindow">
            {this.props.sellers.map((seller) => 
            <Seller seller={seller} />
            )}
        </div>
        );
    }
}

export default Sellers;