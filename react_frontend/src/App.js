import React, { useEffect, useState } from "react";
import './App.css';
import Offers from "./components/offers";
import OfferLoadingComponent from './components/offerLoading'

function App() {
    const OfferLoading = OfferLoadingComponent(Offers);
    const [appState, setAppState] = useState({
        loading: false,
        offers: null,
    });
    useEffect(() => {
        const apiUrl = `http://127.0.0.1:8000/api/`;
        fetch(apiUrl)
            .then((data) => data.json())
            .then((offers) => {
                setAppState({ loading: false, offers: offers});
            });
    }, [setAppState]);
    return (
        <div className="App">
            <OfferLoading isLoading={appState.loading} offers={appState.offers} />
        </div>
    );
}

export default App;