import { Button } from "@material-ui/core"
import { Delete, Update } from "@material-ui/icons"
import { Alert } from "@mui/material"
import React from "react"
import OrderCard from "./OrderCard"
import './Profile.scss'
import PurchaseCard from "./PurchaseCard"

class Profile extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            status: 'loading'
        }
        this.getProfile = this.getProfile.bind(this)
        this.getProfile()
    }

    getProfile() {
        var axios = require('axios');
        axios.get('http://192.168.2.239:5000/profile', { 
            headers: { 
                Authorization: 'bearer ' + this.props.fetchLoginFromSessionStorage()['token']
            }
        }).then((response) => {
            console.log(response.data)
            var data = response.data
            if(data.error) {
                this.setState({status: data.error})
            } else {
                this.setState({status: null, username: data.username, email: data.email, role: data.role, name: data.name, user_details: data})
            }
        });
    }

    updateProfile = () => {
        var axios = require('axios');
        axios.post('http://192.168.2.239:5000/profile', this.state.name, { 
            headers: { 
                Authorization: 'bearer ' + this.props.fetchLoginFromSessionStorage()['token'],
                'Content-Type': 'text/plain'
            }
        }).then((response) => {
            if(response.data == 'Update Successful') {
                this.setState({alert_severity: 'success', alert_message: response.data})
            } else {
                this.setState({alert_severity: 'error', alert_message: response.data})
            }
        });
    }
    discard =() => {
        this.setState({name: this.state.user_details.name})
    }
    render() { 
        return <div className="Profile">
            <h1>{this.state.username}</h1>
            <div className="Field">                    
                <div> Role: </div> 
                <div className="value">{this.state.role}</div>
            </div>
            {this.state.name != null ? (
                <div className="Field"> 
                    <div> Name: </div> 
                    <input className="value" type="text" value = {this.state.name} onChange={(event) => this.setState({name: event.target.value})} /> 
                </div>
            ): ""}
            <div className="Field">                    
                <div> Email: </div> 
                <div className="value">{this.state.email}</div>
            </div>
            {this.state.verified != null ? (
                <div className="Field">
                    <div> Email Verified: </div> 
                    <div className="value">{this.state.verified ? "Yes": "No"}</div>
                </div>
            ): ""}
            {this.state.approved != null ? (
                <div className="Field">
                    <div> Seller Approved: </div> 
                    <div className="value">{this.state.approved ? "Yes": "No"}</div>
                </div>
            ): ""}
            <div className="Controls">
                <Button disabled={this.state.name == this.state.user_details?.name} onClick = {this.updateProfile}>
                    <Update />
                    <span>Update</span>
                </Button>
                <Button disabled={this.state.name == this.state.user_details?.name} onClick = {this.discard}>
                    <Delete />
                    <span>Discard</span>
                </Button>
            </div>
            {this.state.alert_severity? 
                <Alert severity={this.state.alert_severity} variant="filled">{this.state.alert_message}</Alert>: ""
            }
            {this.state.user_details?.orders? <h2>Order History</h2> : ""}
            {this.state.user_details?.orders? <div >
                {this.state.user_details?.orders.map((order) => <OrderCard order={order} />)}
            </div>: ""}
            {this.state.user_details?.purchases? <h2>Purchases</h2> : ""}
            {this.state.user_details?.purchases? <div >
                {this.state.user_details?.purchases.map((purchase) => <PurchaseCard purchase={purchase} />)}
            </div>: ""}
        </div>;
    }
}
 
export default Profile;