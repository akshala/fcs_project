import React from "react";
import { ThumbUp } from "@material-ui/icons";
import { IconButton } from "@material-ui/core";

class User extends React.Component {

    constructor(props) {
        super(props);
        this.delete = this.delete.bind(this);
        
    }

    delete = () => {
        var axios = require('axios');
        axios.post('http://localhost:5000/delete_user', {username: this.props.user.username}, {
            headers: {
              Authorization: 'bearer ' + this.props.fetchLoginFromSessionStorage()['token']
            }
          }).then((response) => {
            window.location.reload(false);
          });
    }

    render() {
        return (
        <div className="UserCard">
            <div className="UserUsername"><label>Username: </label>{this.props.user.username}</div>
            <div className="UserName"><label>Name: </label>{this.props.user.name}</div>
            <div className="UserEmail"><label>Email: </label>{this.props.user.email}</div>
            <div className="UserVerified"><label>Verification status: </label>{this.props.user.verified}</div>
            <div>
                <button onClick={this.delete}>Delete User</button>
            </div>
        </div>
        );
    }
}

export default User;