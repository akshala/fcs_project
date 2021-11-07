import React from "react";
import { Delete } from "@material-ui/icons";
import { Button, IconButton } from "@material-ui/core";

class User extends React.Component {

    constructor(props) {
        super(props);
        this.delete = this.delete.bind(this);
        
    }

    delete = () => {
        var axios = require('axios');
        axios.post('http://192.168.2.239:5000/delete_user', {username: this.props.user.username}, {
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
            <Button onClick={this.delete}>
                    <Delete />
                    <span>Delete User</span>
                </Button>
            </div>
        </div>
        );
    }
}

export default User;