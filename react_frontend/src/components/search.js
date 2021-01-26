import React, { useState, useEffect } from 'react';
import axiosInstance from '../axios';

import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import Container from '@material-ui/core/Container';
import Link from '@material-ui/core/Link';
import CardActions from "@material-ui/core/CardActions";
import Button from "@material-ui/core/Button";
import {IconButton} from "@material-ui/core";
import FavoriteIcon from "@material-ui/icons/Favorite";
import DeleteIcon from "@material-ui/icons/Delete";

import {handleAddToFavourites} from './helpers/button_handlers'
import {handleDeleteOffer} from './helpers/button_handlers'

const useStyles = makeStyles((theme) => ({
	cardMedia: {
		paddingTop: '56.25%', // 16:9
	},
	link: {
		margin: theme.spacing(1, 1.5),
	},
	cardHeader: {
		backgroundColor:
			theme.palette.type === 'light'
				? theme.palette.grey[200]
				: theme.palette.grey[700],
	},
	offerTitle: {
		fontSize: '16px',
		textAlign: 'left',
	},
	offerText: {
		display: 'flex',
		justifyContent: 'left',
		alignItems: 'baseline',
		fontSize: '12px',
		textAlign: 'left',
		marginBottom: theme.spacing(2),
	},
    alignCardButtons: {
    	display: 'flex',
    	alignItems: 'right',
    	justifyContent: 'space-between'
    },
}));

const Search = () => {
	const classes = useStyles();
	const search = 'search';
	const [appState, setAppState] = useState({
		search: '',
		offers: [],
	});

	useEffect(() => {
		axiosInstance.get(search + '/' + window.location.search).then((res) => {
			const allOffers = res.data.results;
			setAppState({ offers: allOffers });
		});
	}, [setAppState]);

	return (
		<React.Fragment>
			<Container maxWidth="md" component="main">
				<Grid container spacing={5} alignItems="flex-end">
					{appState.offers.map((offer) => {
						return (
							<Grid item key={offer.id} xs={12} md={4}>
								<Card className={classes.card}>
									<Link
										color="textPrimary"
										href={offer.url}
										className={classes.link}
									>
										<CardMedia
											className={classes.cardMedia}
											image={offer.photo_urls[0]}
											title={`${offer.brand} ${offer.model}`}
										/>
									</Link>
									<CardContent className={classes.cardContent}>
										<Typography
											gutterBottom
											variant="h6"
											component="h2"
											className={classes.offerTitle}
										>
											{offer.title.substr(0, 50)}...
										</Typography>
										<Typography color="textSecondary">
											{offer.description
												? offer.description.substr(0, 40)
												: "No description"}...
										</Typography>
										<Typography style={{fontWeight:'bold'}}>
										  { offer.price }
										</Typography>
									</CardContent>
									<CardActions className={classes.alignCardButtons}>
										<Button size="small" color="primary">
										  <Link color="inherit" href={offer.url}>
											View
										  </Link>
										</Button>
										<IconButton aria-label="add to favorites" onClick={() => handleAddToFavourites(offer.id)}>
											<FavoriteIcon style={{color: 'firebrick'}}/>
										</IconButton>
										<IconButton aria-label="delete" onClick={() => handleDeleteOffer(offer.id)}>
											<DeleteIcon style={{color: 'cornflowerblue'}}/>
										</IconButton>
								  </CardActions>
								</Card>
							</Grid>
						);
					})}
				</Grid>
			</Container>
		</React.Fragment>
	);
}
export default Search;