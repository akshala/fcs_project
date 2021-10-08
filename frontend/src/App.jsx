import './App.scss';
import Home from './Components/Home/Home'
import { Route, Switch, Redirect, BrowserRouter } from 'react-router-dom';
import Login from './Components/Login/Login';
import SignUp from './Components/SignUp/SignUp';
import Header from './Components/Header/Header'
import Checkout from './Components/Checkout/Checkout';

function App() {

  var axios = require('axios');

  var config = {
    method: 'get',
    url: 'http://localhost:5000/'
  };
  
  axios(config)
  .then(function (response) {
    console.log(JSON.stringify(response.data));
  })
  .catch(function (error) {
    console.log(error);
  });

  return (
    <div className="App">
      <BrowserRouter>
        <Header />
        <div className="Page">
          <Switch>
            <Route exact path="/Home" component={Home} />
            <Route exact path="/">
              <Redirect to="/Home" />
            </Route>
            <Route exact path="/SignUp" component={SignUp} />
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
