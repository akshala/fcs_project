import './App.scss';
import React from "react";
import Home from './Components/Home/Home'
import { Route, Switch, Redirect, BrowserRouter } from 'react-router-dom';
import Login from './Components/Login/Login';
import SignUp from './Components/SignUp/SignUp';
import DocumentUpload from './Components/DocumentUpload/DocumentUpload';
import Verify from './Components/SignUp/Verify';
import Header from './Components/Header/Header'
import Checkout from './Components/Checkout/Checkout';
import Admin from './Components/Admin/Admin';
import Admin_seller from './Components/Admin/Sellers/Admin_seller';
import Admin_user from './Components/Admin/Users/Admin_user';
import Products from './Components/Products/Products';
import NewProduct from './Components/Products/NewProduct';
import Profile from './Components/Profile/Profile';
import Orders from './Components/Orders/Orders';

class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = this.fetchLoginFromSessionStorage()
    this.login = this.login.bind(this);
    this.logout = this.logout.bind(this);
  }

  fetchLoginFromSessionStorage() {
    var default_ = {
      loggedIn: false,
      role: null,
      token: null
    }
    if(sessionStorage.getItem('user')) {
      try {
        var data = JSON.parse(sessionStorage.getItem('user'));
        return data;
      } catch(err) {
        console.log(data);
      }
    }
    sessionStorage.setItem('user', JSON.stringify(default_));
    return JSON.parse(sessionStorage.getItem('user'));
  }

  login(role, token) {
    sessionStorage.setItem('user', JSON.stringify({role: role, token: token, loggedIn: true}));
    this.setState({...this.fetchLoginFromSessionStorage()});
  }

  logout() {
    console.log("TRYING TO LOGOUT");
    sessionStorage.setItem('user', JSON.stringify({role: null, token: null, loggedIn: false}))
    this.setState({...this.fetchLoginFromSessionStorage()});
  }

  render() { 
    return (
      <div className="App">
        <BrowserRouter>
          <Header role={this.state.role} loggedIn={this.state.loggedIn} logout={this.logout} />
          <div className="Page">
            <Switch>
              <Route exact path="/Home">
                <Home role={this.state.role} fetchLoginFromSessionStorage={this.fetchLoginFromSessionStorage} />
              </Route>
              <Route exact path="/">
                <Redirect to="/Home" />
              </Route>
              <Route exact path="/Admin" component={Admin} />
              <Route exact path="/Admin_user">
                <Admin_user fetchLoginFromSessionStorage={this.fetchLoginFromSessionStorage} />
              </Route>
              <Route exact path="/Admin_seller">
                <Admin_seller fetchLoginFromSessionStorage={this.fetchLoginFromSessionStorage} />
              </Route>
              <Route path="/Products/New" > 
                <NewProduct fetchLoginFromSessionStorage={this.fetchLoginFromSessionStorage} />
              </Route>
              <Route path="/Products/:id" render={(props) => <Products {...props} fetchLoginFromSessionStorage={this.fetchLoginFromSessionStorage} /> } />
              <Route exact path="/SignUp" component={SignUp} />
              <Route exact path="/Verify">
                <Verify login={this.login} />
              </Route>
              <Route exact path="/DocumentUpload">
                <DocumentUpload fetchLoginFromSessionStorage={this.fetchLoginFromSessionStorage} />
              </Route>
              <Route exact path="/Login" > 
                <Login login={this.login} />
              </Route>
              <Route exact path="/Checkout">
                <Checkout fetchLoginFromSessionStorage={this.fetchLoginFromSessionStorage} />
              </Route>
              <Route exact path="/Orders">
                <Orders fetchLoginFromSessionStorage={this.fetchLoginFromSessionStorage} />
              </Route>
              <Route exact path="/Profile">
                <Profile fetchLoginFromSessionStorage={this.fetchLoginFromSessionStorage} />
              </Route>
            </Switch>
          </div>
          <div className="Footer"></div>
        </BrowserRouter>
      </div>
    );
  }
}
 
export default App;
