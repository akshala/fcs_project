import React from "react"
import { withRouter } from 'react-router-dom';
import '../../App.scss';
import { IconButton } from "@material-ui/core";
import { ShoppingCart } from "@material-ui/icons";

class Header extends React.Component {
    constructor(props) {
        super(props);
        this.props = props;
    }
    render() {
        return (
        <header className="Header">
            <h1 onClick={() => {this.props.history.push('/Home')}}>Amawon</h1>
            <IconButton onClick={() => {this.props.history.push('/Checkout')}}>
                <ShoppingCart />
            </IconButton>
        </header>)
    }
}

export default withRouter(Header);