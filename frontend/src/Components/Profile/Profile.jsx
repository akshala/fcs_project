import React from "react"
import './Profile.scss'

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
        axios.get('http://localhost:5000/profile', { 
            headers: { 
                Authorization: 'bearer ' + this.props.fetchLoginFromSessionStorage()['token']
            }
        }).then((response) => {
            console.log(response.data)
            var data = response.data
            if(data.error) {
                this.setState({status: data.error})
            } else {
                this.setState({status: null, username: data.username, email: data.email, role: data.role, user_details: data})
            }
        });
    }

    render() { 
        return <div className="Profile">
            <h1>{this.state.username}</h1>
            <h3>Role: {this.state.role}</h3>
            {this.state.role == 'User' || this.state.role == 'Seller' ? (
                    <div>Name: {this.state.user_details.name}</div>
            ): ""}
            <div>Email: {this.state.email}</div>
            {this.state.role == 'User' || this.state.role == 'Seller' ? (
                    <div>Email Verified: {this.state.user_details.verified ? "Yes": "No"}</div>
            ): ""}
            {this.state.role == 'Seller' ? (
                <div>Seller Approved: {this.state.user_details.approved ? "Yes": "No"}</div>
            ): ""}
        </div>;
    }
}
 
export default Profile;