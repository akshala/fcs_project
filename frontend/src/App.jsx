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
import Products from './Components/Products/Products';
import NewProduct from './Components/Products/NewProduct';

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
                <Home role={this.state.role} />
              </Route>
              <Route exact path="/">
                <Redirect to="/Home" />
              </Route>
              <Route exact path="/Admin" component={Admin} />
              <Route path="/Products/New" > 
                <NewProduct />
              </Route>
              <Route path="/Products/:id" render={(props) => <Products {...props} /> } />
              <Route exact path="/SignUp" component={SignUp} />
              <Route exact path="/Verify" component={Verify} />
              <Route exact path="/Login" > 
                <Login login={this.login} />
              </Route>
              <Route exact path="/Checkout" component={Checkout} />
            </Switch>
          </div>
          <div className="Footer"></div>
        </BrowserRouter>
      </div>
    );
  }
}
 
export default App;
