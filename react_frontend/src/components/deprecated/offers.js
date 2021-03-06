import React from 'react';
import Button from '@material-ui/core/Button';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import CssBaseline from '@material-ui/core/CssBaseline';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import Container from '@material-ui/core/Container';
import { makeStyles } from '@material-ui/core/styles';
import Link from '@material-ui/core/Link';
import FavoriteIcon from '@material-ui/icons/Favorite';
import DeleteIcon from '@material-ui/icons/Delete';
import {IconButton} from "@material-ui/core";
import axiosInstance from "../../axios";


const useStyles = makeStyles((theme) => ({
  icon: {
    marginRight: theme.spacing(2),
  },
  heroContent: {
    backgroundColor: theme.palette.background.paper,
    padding: theme.spacing(8, 0, 6),
  },
  heroButtons: {
    marginTop: theme.spacing(4),
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
  cardMedia: {
    paddingTop: '56.25%', // 16:9
  },
  cardContent: {
    flexGrow: 1,
  },
  alignCardButtons: {
    display: 'flex',
    alignItems: 'right',
    justifyContent: 'space-between'
  },
}));


export default function Offers(props) {

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

  const handleDeleteOffer = async (offer_id) => {
    console.log('####### Sending delete request for offer: ', offer_id, ' ##########');
    await axiosInstance.delete(`/${offer_id}`, {data:{pk: `${offer_id}`}}).then((res) =>
    {
      console.log(res);
      console.log('####### Offer has been deleted. ########');
      // window.location.reload();
    }).catch(err => {
      console.log(err);
    });
    const offerCard = document.getElementById(`${offer_id}`)
    offerCard.remove();
  }

  const { offers } = props;
  const classes = useStyles();
  if (!offers || offers.length === 0) return <div>Apologies, there is an issue... Possible options are:
    <ul>
      <li>Database is empty</li>
      <li>Server is down</li>
      <li>You are not authenticated. Please <Link href="/login/">Login</Link>.</li>
    </ul>
    </div>
  if (!offers.results) return <div>You are not authenticated. Please <Link href="/login/">Login</Link> to view offers.</div>
  return (
    <React.Fragment>
      <CssBaseline />
      <main>
        {/* Hero unit */}
        <div className={classes.heroContent}>
          <Container maxWidth="sm">
            <Typography component="h1" variant="h2" align="center" color="textPrimary" gutterBottom>
              MotoCrawler
            </Typography>
            <Typography variant="h5" align="center" color="textSecondary" paragraph>
              MotoCrawler is a web scraping app, using Scrapy for data collection, PostgreSQL database, Django RESTful API and React FrontEnd.
                Below you will find cards with scraped car offers.
            </Typography>
          </Container>
        </div>
        <Container className={classes.cardGrid} maxWidth="md">
          {/* End hero unit */}
          <Grid container spacing={4}>
            {offers.results.map((offer) => (
              <Grid item key={offer.id} xs={12} sm={6} md={4} id={offer.id}>
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
                    <Typography gutterBottom variant="h5" component="h2">
                      { offer.title }...
                    </Typography>
                    <Typography>
                      { offer.description !== null
                        ? offer.description.substr(0, 60)
                          : "No description"
                      }...
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
            ))}}
          </Grid>
        </Container>
      </main>
    </React.Fragment>
  );
}