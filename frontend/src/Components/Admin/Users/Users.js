import React from "react";
import User from "./User"
import "./Users.css"

class Users extends React.Component {

    render() {
        return (
        <div className="UserWindow">
            {this.props.users.map((user) => 
            <User fetchLoginFromSessionStorage={this.props.fetchLoginFromSessionStorage} user={user} />
            )}
        </div>
        );
    }
}

export default Users;