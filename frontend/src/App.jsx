import './App.scss';
import Home from './Components/Home/Home'
import { Route, Switch, Redirect, BrowserRouter } from 'react-router-dom';
import Login from './Components/Login/Login';
import SignUp from './Components/SignUp/SignUp';
import Verify from './Components/SignUp/Verify';
import Header from './Components/Header/Header'
import Checkout from './Components/Checkout/Checkout';
import Admin from './Components/Admin/Admin';
import Products from './Components/Products/Products';

function App() {
  var admin = true;

  return (
    <div className="App">
      <BrowserRouter>
        <Header admin={admin} />
        <div className="Page">
          <Switch>
            <Route exact path="/Home">
              <Home admin={admin} />
            </Route>
            <Route exact path="/">
              <Redirect to="/Home" />
            </Route>
            <Route exact path="/Admin" component={Admin} />
            <Route path="/Products/:id" render={(props) => <Products {...props} /> } />
            <Route exact path="/SignUp" component={SignUp} />
            <Route exact path="/Verify" component={Verify} />
            <Route exact path="/Login" component={Login} />
            <Route exact path="/Checkout" component={Checkout} />
          </Switch>
        </div>
        <div className="Footer"></div>
      </BrowserRouter>
    </div>
  );
}

export default App;
