import React from "react"
import { withRouter } from 'react-router-dom';
import '../../App.scss';
import { Button, IconButton } from "@material-ui/core";
import { ExitToApp, Person, ShoppingCart } from "@material-ui/icons";
import ManageAccountsIcon from '@mui/icons-material/ManageAccounts';

class Header extends React.Component {
    constructor(props) {
        super(props);
        this.props = props;
        this.logout_redirect = this.logout_redirect.bind(this);  
    }

    logout_redirect(){
        this.props.logout();
        this.props.history.push('/Login');
    }

    render() {
        return (
        <header className="Header">
            <h1 onClick={() => {this.props.history.push('/Home')}}>Amawon</h1>
            {this.props.role == 'User' ? 
            (<IconButton onClick={() => {this.props.history.push('/Checkout')}}>
                <ShoppingCart />
            </IconButton>) : (<div></div>)}
            {this.props.loggedIn ? (
            <div>
                {this.props.role == 'Admin' ? 
                (<ManageAccountsIcon style={{ color: "white" }} onClick={() => {this.props.history.push('/Admin')}}>
                </ManageAccountsIcon>) : ""}
                <IconButton onClick={() => {this.props.history.push('/Profile')}}>
                    <Person />
                </IconButton>
                <IconButton onClick={this.logout_redirect}>
                    <ExitToApp />
                </IconButton>
            </div>) : (
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