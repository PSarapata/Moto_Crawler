import React, { useState, useEffect } from "react";
import Box from "@material-ui/core/Box";
import Pagination from "@material-ui/lab/Pagination";
import {makeStyles} from "@material-ui/core/styles";
import axiosInstance from "../../axios";
import Link from "@material-ui/core/Link";
import CssBaseline from "@material-ui/core/CssBaseline";
import Container from "@material-ui/core/Container";
import Typography from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import Card from "@material-ui/core/Card";
import CardMedia from "@material-ui/core/CardMedia";
import CardContent from "@material-ui/core/CardContent";
import CardActions from "@material-ui/core/CardActions";
import Button from "@material-ui/core/Button";
import {IconButton} from "@material-ui/core";
import FavoriteIcon from "@material-ui/icons/Favorite";
import DeleteIcon from "@material-ui/icons/Delete";
import '../../App.css'
import {handleAddToFavourites} from '../helpers/button_handlers'
import {handleDeleteOffer} from '../helpers/button_handlers'


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
  centerBoxContent: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    marginTop: "40px",
  },
}));

function OffersPaginated() {
    const [offers, setOffers] = useState([]);
    const [displayPerPage] = useState(50);

    const [offset, setOffset] = useState(0);
    const [count, setCount] = useState(0);

    const classes = useStyles();

    const handleChange = (event, value) => {
        setOffset((value-1)*displayPerPage)
    };

    const generateURL = (displayPerPage, offset) => {
        let p = new URLSearchParams();
        p.append('limit', displayPerPage || 50);
        p.append('offset', offset || 0);
        return('http://localhost:8000/api?' + p);
    };

    useEffect(() => {
        async function retrieveOffers(displayPerPage) {
        const res = await axiosInstance.get(generateURL(displayPerPage, offset))
        const results = res.data
        setOffers(results);
        setCount(results.count);
        setOffset(offset);
    }
        retrieveOffers().catch(e => {console.log(e)})
    }, [offset])

    if (!offers || offers.length === 0) return (
    <Box className={classes.centerBoxContent}>
        <div><b>Apologies, there is an issue... Possible options are:</b>
            <ul>
                <li>Data is still being fetched...</li>
                <li>Database is empty</li>
                <li>Server is down</li>
                <li>You are not authenticated. Please <Link href="/login/">Login</Link>.</li>
            </ul>
        </div>
    </Box>
    );
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
          <Box className={classes.centerBoxContent}>
            <Pagination count={Math.ceil(count / displayPerPage)} color={"primary"} size="large" showFirstButton showLastButton onChange={handleChange}/>
          </Box>
      </main>
    </React.Fragment>
    );
}

export default OffersPaginated;