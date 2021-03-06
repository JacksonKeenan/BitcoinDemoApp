import '../App.css';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import { useState } from 'react';
import { useEffect } from 'react';

// Initializing Wallets
function walletsInitial() {
  var wallets = {}
  return wallets
}

function AllPublicWallets(props) {
  // State Management
  const [recentWallets, updateRecentWallets] = useState(() => walletsInitial())

  // On Load Effects
  useEffect(() => { loadWallets() }, []);

  // Loads State for All Public Wallets
  function loadWallets() {
    var newRecentWallets = walletsInitial()
    const getRequestOptions = {
      method: 'GET',
      headers: {'Content-Type': 'application/json'},
    };

    fetch('/api/list-public-wallets', getRequestOptions).then((response) =>
      response.json()
    ).then((data) => {
        newRecentWallets = data
        updateRecentWallets(prevRecentWallets => newRecentWallets)
      });
  }

  // Renders All Public Wallets
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
      <Grid container spacing={1} alignItems="center">
        <Grid item xs={12} align="center">
          <Typography component="h2" variant="h3">
            All Public Wallets
          </Typography>
          { renderWalletList() }
        </Grid>
        <Grid item xs={12} align="center">
         <a href="/">Back</a>
        </Grid>
      </Grid>
    </div>
  );
}

export default AllPublicWallets;
