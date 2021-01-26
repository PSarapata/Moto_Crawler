import React, { useState, useEffect } from 'react';
import axiosInstance from '../../axios';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import Container from '@material-ui/core/Container';
import Link from '@material-ui/core/Link';
import CardActions from "@material-ui/core/CardActions";
import {IconButton} from "@material-ui/core";
import ClearIcon from '@material-ui/icons/Clear';
import DeleteIcon from "@material-ui/icons/Delete";
import {handleUnfavourite} from '../helpers/button_handlers'
import {handleDeleteOffer} from '../helpers/button_handlers'


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
	cardContent: {
    	flexGrow: 1,
  	},
    cardGrid: {
        paddingTop: theme.spacing(8),
        paddingBottom: theme.spacing(8),
    },
    card: {
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
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
    icon: {
        marginRight: theme.spacing(2),
    },
	unfavOnHover: {
        '&:hover, &:focus': {
        backgroundColor: 'lightsteelblue'
        },
        '&:active': {
        boxShadow: theme.shadows[1],
        backgroundColor: 'dimgray'
        },
	}

}));

const Favourites = () => {

	const classes = useStyles();
	const [appState, setAppState] = useState({
		favouriteOffers: [],
	});

	useEffect(() => {
		axiosInstance.get('/favourites', { baseURL: 'http://localhost:8000' }).then((res) => {
			const allOffers = res.data.results;
			setAppState({ favouriteOffers: allOffers });
		});
	}, [setAppState]);

	return (
		<React.Fragment>
			<Container maxWidth="md" component="main">
				<Grid container spacing={5} alignItems="flex-end">
					{appState.favouriteOffers.map((offer) => {
						return (
							<Grid item key={offer.id} xs={12} md={4}>
								<Card className={classes.card}>
									<Link
										color="textPrimary"
										href={offer.offer.url}
										className={classes.link}
									>
										<CardMedia
											className={classes.cardMedia}
											image={offer.photo_urls[0]}
											title={`${offer.offer.brand} ${offer.offer.model}`}
										/>
									</Link>
									<CardContent className={classes.cardContent}>
										<Typography
											gutterBottom
											variant="h5"
											component="h2"
											className={classes.offerTitle}
										>
											{offer.offer.title.substr(0, 50)}...
										</Typography>
											<Typography color="textSecondary">
												{offer.offer.description
													? offer.offer.description.substr(0, 40)
													: "No description"}...
											</Typography>
											<Typography style={{fontWeight:'bold'}}>
											  { offer.offer.price }
											</Typography>
											<Typography color="textSecondary">
												{ offer.timestamp.substr(0,16) }
											</Typography>
									</CardContent>
                                    <CardActions className={classes.alignCardButtons}>
                                        <IconButton aria-label="unfavourite" onClick={() => handleUnfavourite(offer.id)} className={classes.unsubOnHover}>
                                            <ClearIcon style={{fill: 'royalblue'}}/>
                                        </IconButton>
                                        <IconButton aria-label="delete" onClick={() => handleDeleteOffer(offer.offer.id)}>
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
};
export default Favourites;