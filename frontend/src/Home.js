import React from 'react';
import {Redirect} from "react-router-dom";
import './App.css';
import {url} from "./index"

/**
 * Homepage for List app
 */
class Home extends React.Component {

    constructor(props) {
        super(props);
        this.state = {redirect: "", error: ""}
    }

    forwardToList = (event) => {
        event.preventDefault();
        const listId = event.target[0].value.trim();
        if (listId.length !== 6) {
            this.setState({error: "Error: List ID must be of length 6"})
            return;
        }

        fetch(url + "/validatelist", {
            method: "POST",
            body: JSON.stringify({"list_id": listId}),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(response => response.json())
            .then(data => {
                console.log(data.exists);
                if (data.exists) {
                    this.setState({redirect: <Redirect to={{path: "/" +listId}} />})
                } else {

                }
            })
            .catch(error => console.error(error));

    };

    createNewList = () => {
        fetch(url + "/newlist", {
            method: "POST",
        }) .then(response => response.json())
            .then(data => {
                const new_url = "/" + data.list_id;

                this.setState({redirect: <Redirect to={new_url}/>});

            })
            .catch(error => console.error(error));

    };

    render() {
        return (
            <div className={"Home"}>
                {this.state.redirect}
                <h1>List Manager</h1>
                <form className={"list-form"} onSubmit={this.forwardToList}>
                    <input className={"id-input"} type={"text"} placeholder={"Enter List ID"} autoComplete={"off"}/>
                    <input className={"list-button list-submit "} type={"submit"} value={"Go!"}/>
                </form>
                <div className={"error"}>
                    {this.state.error}
                </div>
                <button className={"list-button"} onClick={this.createNewList}>Create New List</button>
            </div>
        );

    }
}

export default Home;
