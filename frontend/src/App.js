import './App.css';
import Home from './Components/Home/Home'
import { Route, Switch, Redirect, BrowserRouter } from 'react-router-dom';
import Login from './Components/Login/Login';
import SignUp from './Components/SignUp/SignUp';

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
      <header className="Header">
        <h1>Amawon</h1>
      </header>
      <div className="Page">
        <BrowserRouter>
          <Switch>
            <Route exact path="/Home" component={Home} />
            <Route exact path="/">
              <Redirect to="/Home" />
            </Route>
            <Route exact path="/SignUp" component={SignUp} />
            <Route exact path="/Login" component={Login} />
          </Switch>
        </BrowserRouter>
      </div>
      <div className="Footer"></div>
    </div>
  );
}

export default App;
