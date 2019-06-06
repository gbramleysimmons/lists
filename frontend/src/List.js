import React from 'react';
import './App.css';
import {url} from "./index"

/**
 * Models the detailed view for a list
 */
class List extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            list: []
        }
    }

    /**
     * Makes a request to the "viewlist" endpoint to set up the list view
     */
    componentDidMount() {
        fetch(url + "/viewlist", {
            method: "POST",
            body: JSON.stringify({list_id: this.props.match.params.id}),
            headers: {
                'Content-Type': 'application/json'
            }

        }).then(response => response.json())
            .then(data => {
                console.log(data)
                this.setState({list: data.list_items.map(ele => ele.item)})
            })
            .catch(error => console.error(error))
    }

    /**
     * Adds an item to the list by making a POST request to 'additen'
     * @param event
     */
    addListItem = (event) => {
        event.preventDefault();
        const item = event.target[0].value.trim();
        event.target[0].value = "";
        if (item.length === 0) {
            return;
        }
        fetch(url + "/additem", {
            method: "POST",
            body: JSON.stringify({list_id: this.props.match.params.id, item:item}),
            headers: {
                'Content-Type': 'application/json'
            }

        }).then(response => response.json())
            .then(data => {
                console.log(data);
                const list = this.state.list;
                list.push(data.item);
                this.setState({list: list});
            })
            .catch(error => console.error(error))
    };

    /**
     * Removes an item from the list by making a POST request to 'deleteitem'
     * @param item item to remove
     */
    removeListItem = (item) => {
         fetch(url + "/deleteitem", {
            method: "POST",
            body: JSON.stringify({list_id: this.props.match.params.id, item:item}),
            headers: {
                'Content-Type': 'application/json'
            }

        }).then(response =>  {
                let list = this.state.list;
                list = list.filter(ele => ele !== item);
                console.log(list);
                this.setState({list: list});
            })
            .catch(error => console.error(error))
    };

    /**
     * Clears the list visually, and by making a POST request to "/clearlist"
     */

    clearList = () => {
          fetch(url + "/clearlist", {
            method: "POST",
            body: JSON.stringify({list_id: this.props.match.params.id}),
            headers: {
                'Content-Type': 'application/json'
            }

        }).then(response =>  {
                this.setState({list: []});
            })
            .catch(error => console.error(error))
    };


    render() {
        return (
            <div className={"List"}>
                <h1 className={"list-header"}>List {this.props.match.params.id}</h1>
                <a href={".."}>Home</a>

                <ul className={"list-ul"}>
                    {
                        this.state.list.map(ele => {
                            return <li key={Math.random()}> <div className={"list-item-text"}> {ele}</div> <button className={"close-button"} onClick={() => this.removeListItem(ele)}>
                            <i className="fas fa-times"/>
                        </button>
                        </li>
                    })}
                </ul>
                <form className={"list-form"} onSubmit={this.addListItem}>
                    <input className={"list-input"} type={"text"} placeholder={"Add new list item"}/>
                    <input className={"list-button list-submit"} type={"submit"} value={"Add"}/>
                <button className={"list-button"} onClick={this.clearList}>Clear list</button>

                </form>
            </div>
        );

    }
}

export default List;
