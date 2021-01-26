import React, { useEffect, useState } from "react";
import '../../App.css';
import Offers from "./offers";
import OfferLoadingComponent from './offerLoading'
import axiosInstance from "../../axios";


function App() {
    const OfferLoading = OfferLoadingComponent(Offers);
    const [appState, setAppState] = useState({
        loading: true,
        offers: null,
    });

    useEffect(() => {
		axiosInstance.get().then((res) => {
            const allOffers = res.data;
            setAppState({loading: false, offers: allOffers});
        });
    }, [setAppState]);
    return (
        <div className="App">
            <OfferLoading isLoading={appState.loading} offers={appState.offers} />
        </div>
    );
}


export default App;