import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import Register from "./components/register";
import Login from "./components/login";
import SignOut from "./components/logout";
import * as serviceWorker from './serviceWorker';
import { Route, BrowserRouter as Router, Switch } from 'react-router-dom';
import Header from './components/header';
import Footer from './components/footer';

const routing = (
    <Router>
        <React.StrictMode>
            <Header />
            <Switch>
                <Route exact path="/" component={App} />
                <Route path="/register" component={Register} />
                <Route path="/login" component={Login} />
                <Route path="/logout" component={SignOut} />
            </Switch>
            <Footer />
        </React.StrictMode>
    </Router>
);

ReactDOM.render(routing, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
