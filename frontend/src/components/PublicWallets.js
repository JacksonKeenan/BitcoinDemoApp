import '../App.css';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import FormControl from '@mui/material/FormControl';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { useState } from 'react';
import { useEffect } from 'react';

// Constant for 'Recent Wallets' timethreshold
const delta=30

// Material UI Styling
const theme = createTheme({
  palette: {
    orange: {
      main: '#fa4616',
      contrastText: '#d6d2c4',
    },
    green: {
      main: '#356554',
      contrastText: '#d6d2c4',
    },
    offwhite: {
      main: '#d6d2c4',
    },
  }
});

// Initializing Wallet address for searching, and amount field for sending
function walletInitial() {
  const wallet = { address: "n/a", amount: "1000", }
  return wallet
}

// Initializing Recent Wallets
function walletsInitial() {
  var wallets = {}
  return wallets
}

function PublicWallets(props) {
  // State Management
  const [wallet, updateWallet] = useState(() => walletInitial())
  const [recentWallets, updateRecentWallets] = useState(() => walletsInitial())

  // On Load Effects
  useEffect(() => { loadWallets() }, []);

  // Loads State for Recent Public Wallets
  function loadWallets() {
    var newRecentWallets = walletsInitial()
    const getRequestOptions = {
      method: 'GET',
      headers: {'Content-Type': 'application/json'},
    };

    fetch('/api/list-public-wallets?delta='+delta, getRequestOptions).then((response) =>
      response.json()
    ).then((data) => {
        newRecentWallets = data
        updateRecentWallets(prevRecentWallets => newRecentWallets)
      });
  }

  // Updates State on Address Field Change
  function handleAddressFieldChange(e) {
    const newWallet = { address: e.target.value, amount: wallet.amount, }
    updateWallet(prevWallet => newWallet)
  }

  // Updates State on Amount Field Change
  function handleAmountFieldChange(e) {
    const newWallet = { address: wallet.address, amount: e.target.value, }
    updateWallet(prevWallet => newWallet)
  }

  // Sends Transation to Given Address, Then Updates that Addresses Information
  function searchAndSend() {
    var newRecentWallets = walletsInitial()

    if(!wallet.address) {
      alert('Error: Invalid Address')
      return
    }

    const requestOptions = {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(wallet),
    };

    fetch('/api/create-public-wallet-send', requestOptions).then((response) =>
      response.json()
    ).then((data) => {
        if(data.Error) {
          alert(data.Error)
        } else {
          alert("Transaction Successfully Sent")
        }

        const getRequestOptions = {
          method: 'GET',
          headers: {'Content-Type': 'application/json'},
        };

        fetch('/api/list-public-wallets?delta='+delta, getRequestOptions).then((response) =>
          response.json()
        ).then((data) => {
            newRecentWallets = data
            updateRecentWallets(prevRecentWallets => newRecentWallets)
          });
      });
  }

  // Updates Information on Given Address
  function searchWallet() {
    var newRecentWallets = walletsInitial()
    const requestOptions = {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(wallet),
    };

    fetch('/api/create-public-wallet-search', requestOptions).then((response) =>
      response.json()
    ).then((data) => {
        if(!data.address) {
          alert("Error: Invalid Address")
        }

        const getRequestOptions = {
          method: 'GET',
          headers: {'Content-Type': 'application/json'},
        };

        fetch('/api/list-public-wallets?delta='+delta, getRequestOptions).then((response) =>
          response.json()
        ).then((data) => {
            newRecentWallets = data
            updateRecentWallets(prevRecentWallets => newRecentWallets)
          });
      });
  }

  // Renders Recent Public Wallets
  function renderWalletList() {
    if (recentWallets.length > 0) {
      return(
        recentWallets.map(wallet => {
          return (
            <a href={ '/public-wallets/' + wallet.address } className="RecentWallet">
              <p><span>Address:</span> { wallet.address }</p>
              <p><span>Last Updated:</span> { wallet.last_updated }</p>
            </a>
          )
        })
      )
    }
  }

  // Markup
  return (
    <div className="PublicWallets">
      <ThemeProvider theme={theme}>
        <Grid container spacing={1} alignItems="center">
          <Grid item xs={12} align="center">
            <Typography component="h2" variant="h3">
              Receiving Wallet
            </Typography>
          </Grid>
          <Grid item xs={6} align="center">
            <FormControl style={{ minWidth: '100%' }}>
              <TextField onChange={ handleAddressFieldChange } fullWidth required={true} type="text" placeholder="Receiving Address, e.g. 2MsYQSzRirq6N6jjKkZQ9F5gpjdnlEvGnAh" />
            </FormControl>
          </Grid>
          <Grid item xs={6} align="center">
            <FormControl style={{ minWidth: '100%' }}>
              <TextField
                onChange={ handleAmountFieldChange }
                required={true}
                type="number"
                defaultValue={1000}
                inputProps={{
                  min: 1000,
                  style: { textAlign: "center" },
                }}
              />
            </FormControl>
          </Grid>
          <Grid item xs={6} align="center">
            <Button onClick={ searchWallet } color="orange" variant="contained" style={{ minWidth: '100%'}}>
              <span className="buttonText">Search</span>
            </Button>
          </Grid>
          <Grid item xs={6} align="center">
            <Button onClick={ searchAndSend } color="orange" variant="contained" style={{ minWidth: '100%'}}>
              <span className="buttonText">Send</span>
            </Button>
          </Grid>
          <Grid item xs={12} align="center">
            <Typography component="h3" variant="h4" style={{ marginTop: '2em'}}>
              Recent Wallets
            </Typography>
            { renderWalletList() }
          </Grid>
          <Grid item xs={12} align="center">
           <a href="/public-wallets">View All Wallets</a>
          </Grid>
        </Grid>
      </ThemeProvider>
    </div>
  );
}

export default PublicWallets;
