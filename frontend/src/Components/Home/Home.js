import "./Home.css"
import React from "react"
import { render } from "@testing-library/react"
import Products from "./Products/Products"


class Home extends React.Component {

  constructor(props) {
    super(props);
    this.categories = ["All", "Electronics", "Household", "Sports", "Fashion", "Entertainment"]
    this.products = [
      {
        name: "Laptop",
        image: "http://cdn.mos.cms.futurecdn.net/6t8Zh249QiFmVnkQdCCtHK.jpg",
        description: "HP 8GB RAM, 256 GB SSD, Intel QuadCore Processor"
      },
      {
        name: "Laptop",
        image: "http://cdn.mos.cms.futurecdn.net/6t8Zh249QiFmVnkQdCCtHK.jpg",
        description: "HP 8GB RAM, 256 GB SSD, Intel QuadCore Processor"
      },
      {
        name: "Laptop",
        image: "http://cdn.mos.cms.futurecdn.net/6t8Zh249QiFmVnkQdCCtHK.jpg",
        description: "HP 8GB RAM, 256 GB SSD, Intel QuadCore Processor"
      },
      {
        name: "Laptop",
        image: "http://cdn.mos.cms.futurecdn.net/6t8Zh249QiFmVnkQdCCtHK.jpg",
        description: "HP 8GB RAM, 256 GB SSD, Intel QuadCore Processor"
      },
      {
        name: "Laptop",
        image: "http://cdn.mos.cms.futurecdn.net/6t8Zh249QiFmVnkQdCCtHK.jpg",
        description: "HP 8GB RAM, 256 GB SSD, Intel QuadCore Processor"
      },
  ]
    this.state = {
      selectedCategory: this.categories[0]
    }
  }
  
  updateCategory = (event) => {
    this.setState({...this.state, selectedCategory: event.target.value})
  }

  render() {
    return (
      <div className="Home">
        <div className="Categories">
          {this.categories.map((category) => <input aria-selected={this.state.selectedCategory==category} type="button" value={category} onClick={this.updateCategory} />)}
        </div>
        <div className="Search">
          <input type="text" className="Sarch" placeholder="Search for product name, description etc" />
          <input type="button" value="Search" />
        </div>
        <Products products={this.products} />
      </div>
    );
  }
}

export default Home;
