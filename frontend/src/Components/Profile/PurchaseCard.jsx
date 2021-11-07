import React from "react"

class PurchaseCard extends React.Component {
    render() { 
        return (<div className="OrderCard">
            <div>Order ID: {this.props.purchase.order_id}</div>
            <div>Customer: {this.props.purchase.username}</div>
            <div>Date: {this.props.purchase.date}</div>
            <div>Paid: {this.props.purchase.paid ? "Yes" : "No"}</div>
            <div>Product ID: {this.props.purchase.product_id}</div>
            <div>Product Name: {this.props.purchase.product_name}</div>
            <div>Quantity: {this.props.purchase.quantity}</div>
        </div>);
    }
}
 
export default PurchaseCard;