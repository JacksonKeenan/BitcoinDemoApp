import '../App.css';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import FormControl from '@mui/material/FormControl';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { useState } from 'react';
import { useEffect } from 'react';

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

// Initializing Wallet for html fields
function walletInitial() {
  var wallet = { name: 'n/a', address: 'n/a', balance: '-', unconfirmed_balance: '-', total_received: '-', total_sent: '-', }
  return wallet
}

// Initializing Available Wallets
function walletsInitial() {
  var wallets = {}
  return wallets
}

function SenderWallet(props) {
  // State Management
  const [activeWallet, updateActiveWallet] = useState(() => walletInitial())
  const [wallet, updateWallet] = useState(() => walletInitial())
  const [availableWallets, updateAvailableWallets] = useState(() => walletsInitial())
  const [hidden, setHidden] = useState(true)

  // On Load Effects
  useEffect(() => {
    loadActiveWallet()
    loadAvailableWallets()
  }, []);

  // Loads State for Available Sending Wallets
  function loadAvailableWallets() {
    var newAvailableWallets = walletsInitial()
    const getRequestOptions = {
      method: 'GET',
      headers: {'Content-Type': 'application/json'},
    };

    fetch('/api/list-sender-wallets', getRequestOptions).then((response) =>
      response.json()
    ).then((data) => {
        newAvailableWallets = data
        updateAvailableWallets(prevAvailableWallets => newAvailableWallets)
      });
  }

  // Renders Available Wallets
  function renderAvailableWalletList() {
    if (availableWallets.length > 0) {
      return(
        availableWallets.map((wallet, i, availableWallets) => {
          if(i+1 === availableWallets.length) {
            return ( <span className='availableWallet'>{ wallet.name } </span> )
          } else {
            return ( <span className='availableWallet'>{ wallet.name }, </span> )
          }
        })
      )
    }
  }

  // Loads State for Active Sending Wallet
  function loadActiveWallet() {
    var newActiveWallet = walletInitial()
    const getRequestOptions = {
      method: 'GET',
      headers: {'Content-Type': 'application/json'},
    };

    fetch('/api/list-active-sender-wallet', getRequestOptions).then((response) =>
      response.json()
    ).then((data) => {
        if(data[0]){
          newActiveWallet = data[0]
          updateActiveWallet(prevActiveWallet => newActiveWallet)
        }
      });
  }

  // Refreshes State for Active Sending Wallet
  function refreshActiveWallet() {
    var newActiveWallet = walletInitial()
    const getRequestOptions = {
      method: 'GET',
      headers: {'Content-Type': 'application/json'},
    };

    fetch('/api/list-active-sender-wallet', getRequestOptions).then((response) =>
      response.json()
    ).then((data) => {
        if(data[0]){
          newActiveWallet = data[0]
          const requestOptions_2 = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(newActiveWallet),
          };

          fetch('/api/create-sender-wallet', requestOptions_2).then((response) =>
            response.json()
          ).then((data) => {
            if(!data.address) {
              alert("Invalid Wallet Name")
            } else {
              newActiveWallet = data
              updateActiveWallet(prevActiveWallet => newActiveWallet)
            }
          });
        }
      })
  }

  // Updates State on Name Field Change
  function handleNameFieldChange(e) {
    var newWallet = { name: e.target.value, }
    updateWallet(prevWallet => newWallet)
  }

  // Sets Active Wallet
  function setWallet() {
    var newActiveWallet = walletInitial()
    if(!wallet.name || wallet.name == 'n/a'){
      alert("Invalid Wallet Name")
    } else {
      const requestOptions = {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(wallet),
      };

      fetch('/api/create-sender-wallet', requestOptions).then((response) =>
        response.json()
      ).then((data) => {
        if(data.Error) {
          alert(data.Error)
        } else {
          newActiveWallet = data
          updateActiveWallet(prevActiveWallet => newActiveWallet)
          loadAvailableWallets()
        }
      });
    }
  }

  //Markup
  return (
    <div className="SenderWallet">
      <ThemeProvider theme={theme}>
        <Grid container spacing={1} alignItems="center">
          <Grid item xs={12} align="center">
            <Typography component="h2" variant="h3">
              Sending Wallet
            </Typography>
          </Grid>
          <Grid item xs={12} align="center">
            <FormControl style={{ minWidth: '100%' }}>
              <TextField onChange={ handleNameFieldChange } fullWidth required={true} type="text" placeholder="Name, e.g. Bob" />
            </FormControl>
          </Grid>
          <Grid item xs={12} align="center">
              <Button onClick={ setWallet } color="orange" variant="contained" style={{ minWidth: '100%'}}>
                <span className="buttonText">Set Sending Wallet</span>
              </Button>
          </Grid>
          <Grid item xs={12} align="center">
              <Button onClick={ () => setHidden(s => !s) } color="green" variant="contained" style={{ minWidth: '100%', display: 'block'}}>
                { !hidden ? <>Hide Available Wallets</> : <>View Available Wallets</> }
              </Button>
              { !hidden ? <div className="availableWallets"> <Typography component="h3" variant="h5"> Available Wallets </Typography>{ renderAvailableWalletList() }</div>: null }
          </Grid>
          <Grid item xs={12} align="center">
            <div className="name"><span>Active Wallet Name</span>{ activeWallet.name }</div>
          </Grid>
          <Grid item xs={12} align="center">
            <div className="address"><span>Public Address</span>{ activeWallet.address }</div>
          </Grid>
          <Grid item xs={12} align="center">
            <div className="balance"><span>Balance</span>{ activeWallet.balance }</div>
          </Grid>
          <Grid item xs={12} align="center">
            <div className="balance"><span>Unconfirmed Balance</span>{ activeWallet.unconfirmed_balance }</div>
          </Grid>
          <Grid item xs={12} align="center">
            <div className="balance"><span>Total Received</span>{ activeWallet.total_received }</div>
          </Grid>
          <Grid item xs={12} align="center">
            <div className="balance"><span>Total Sent</span>{ activeWallet.total_sent }</div>
          </Grid>
          <Grid item xs={12} align="center">
            <Button onClick={ refreshActiveWallet } color="orange" variant="contained" style={{ minWidth: '100%'}}>
              <span className="buttonText">Refresh Sending Wallet</span>
            </Button>
          </Grid>
        </Grid>
      </ThemeProvider>
    </div>
  );
}

export default SenderWallet;
