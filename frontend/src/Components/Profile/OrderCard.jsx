import React from "react"

class OrderCard extends React.Component {
    render() { 
        return (<div className={"OrderCard " + (this.props.order.paid ? "success" : "failed")}>
            <div>Order ID: {this.props.order.id}</div>
            <div>Date: {this.props.order.date}</div>
            <div>Paid: {this.props.order.paid ? "Yes" : "No"}</div>
            <div className="items">
                {this.props.order.purchases.map((purchase) => <div>{purchase.product_name} (Rs. {purchase.price}) x {purchase.quantity} </div>)}
            </div>
                <div>Total price: {this.props.order.purchases.reduce((sum, purchase) => sum + purchase.price * purchase.quantity, 0)}</div>
        </div>);
    }
}
 
export default OrderCard;