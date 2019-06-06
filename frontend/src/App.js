import React from 'react';
import { BrowserRouter as Router, Route } from "react-router-dom";
import './App.css';
import Home from "./Home";
import List from "./List";

/**
 * App class for this program.
 * Sets up declarative routing using React Router
 */
class App extends React.Component {

    render() {
        return (
            <Router>
                <Route exact path={"/"} component={Home}/>
                <Route exact path={"/:id"} component={List}/>
            </Router>
        )
    }
}

export default App;
