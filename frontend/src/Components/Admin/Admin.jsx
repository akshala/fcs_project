import "./Admin.scss"
import React from "react"
import Sellers from "./Sellers/Sellers"

class Admin extends React.Component {

  constructor(props) {
    super(props);
  }

    render() {
      var url_seller = "/Admin_seller";
      var url_user = "/Admin_user";
        return (
          <div className="Admin">
            <h1>Welcome Admin!</h1>
            <div>
              <button onClick={(e) => {
                  e.preventDefault();
                  window.location.href=url_seller;
                  }}>Control Seller</button>
            </div>
            <div>
              <button onClick={(e) => {
                  e.preventDefault();
                  window.location.href=url_user;
                  }}>Control User</button>
            </div>
          </div>
        );
      }
      
}

export default Admin;