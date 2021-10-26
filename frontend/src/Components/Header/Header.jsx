import React from "react"
import { withRouter } from 'react-router-dom';
import '../../App.scss';
import { Button, IconButton } from "@material-ui/core";
import { ExitToApp, ShoppingCart } from "@material-ui/icons";

class Header extends React.Component {
    constructor(props) {
        super(props);
        this.props = props;
    }
    render() {
        return (
        <header className="Header">
            <h1 onClick={() => {this.props.history.push('/Home')}}>Amawon</h1>
            {this.props.role == 'customer' ? 
            (<IconButton onClick={() => {this.props.history.push('/Checkout')}}>
                <ShoppingCart />
            </IconButton>) : (<div></div>)}
            {this.props.loggedIn ? (
            <Button onClick={this.props.logout}>
                <ExitToApp />
                Logout
            </Button>) : (
            <div>
                <Button onClick={() => {this.props.history.push('/Login')}}>
                    login
                </Button>
                <Button onClick={() => {this.props.history.push('/Signup')}}>
                    sign up
                </Button>
            </div>
)}
        </header>)
    }
}

export default withRouter(Header);