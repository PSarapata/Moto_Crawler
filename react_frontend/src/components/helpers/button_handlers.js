import axiosInstance from "../../axios";

const handleAddToFavourites = async (offer_id) => {
		console.log('Creating a user-favouriteoffer relation...')
		await axiosInstance.post('favourites/',{data: {
		  offer: offer_id,
		  }}, {baseURL: 'http://localhost:8000'})
		.then((res) => {
			console.log(res);
			console.log('###### Offer moved to favourites! ######')
		  window.location.reload();
		}).catch(err => {
		  console.log(err);
		});
	}

const handleUnfavourite = async (fav_id) => {
	console.log('I shall remove this offer from your favourites...')
	await axiosInstance.delete(`favourites/${fav_id}`, {baseURL: 'http://localhost:8000', data:{pk: `${fav_id}`}}).then((res) =>
	{
	  console.log(res);
	  console.log('####### Relation deleted. ########');
	  window.location.reload();
	}).catch(err => {
	  console.log(err);
	});
}

const handleDeleteOffer = async (offer_id) => {
    console.log('####### Sending delete request for offer: ', offer_id, ' ##########');
    await axiosInstance.delete(`/${offer_id}`, {data:{pk: `${offer_id}`}}).then((res) =>
    {
      console.log(res);
      console.log('####### Offer has been deleted. ########');
    }).catch(err => {
      console.log(err);
    });
	window.location.reload();
}

export {handleAddToFavourites, handleUnfavourite, handleDeleteOffer};