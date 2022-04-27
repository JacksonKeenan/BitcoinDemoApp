import '../App.css';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import { useState } from 'react';
import { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';


function walletInitial() {
  var wallet = {}
  return wallet
}

function PublicWallet(props) {
  const [wallet, updateWallet] = useState(() => walletInitial())
  const walletAddressParam =  useParams().address;
  const navigate = useNavigate();
  useEffect(() => {
    getWalletDetails()
  }, []);

  function getWalletDetails() {
    var newWallet = walletInitial()

    fetch('/api/get-public-wallet?address=' + walletAddressParam).then((response) => response.json()).then((data) => {
      if(!data.address) {
        navigate("/")
      }
      newWallet = data
      updateWallet(prevWallet => newWallet)
    });
  }

  return(
    <div className="PublicWallets">
      <Grid container spacing={1} alignItems="center">
        <Grid item xs={12} align="center">
          <Typography component="h2" variant="h3">
            Public Wallet: <span className="orange">{ wallet.address }</span>
          </Typography>
        </Grid>

        <Grid item xs={12} align="center">
          <Typography component="h3" variant="h4" style={{ marginTop: '2em'}}>
            Balance: <span className="orange">{ wallet.balance }</span>
          </Typography>
        </Grid>

        <Grid item xs={12} align="center">
          <Typography component="h3" variant="h4" style={{ marginTop: '2em'}}>
            Unconfirmed Balance: <span className="orange">{ wallet.unconfirmed_balance }</span>
          </Typography>
        </Grid>

        <Grid item xs={12} align="center">
          <Typography component="h3" variant="h4" style={{ marginTop: '2em'}}>
            Total Received: <span className="orange">{ wallet.total_received }</span>
          </Typography>
        </Grid>

        <Grid item xs={12} align="center">
          <Typography component="h3" variant="h4" style={{ marginTop: '2em'}}>
            Total Sent: <span className="orange">{ wallet.total_sent }</span>
          </Typography>
        </Grid>

        <Grid item xs={12} align="center">
          <Typography component="h3" variant="h4" style={{ marginTop: '2em'}}>
            Last Updated: <span className="orange">{ wallet.last_updated }</span>
          </Typography>
        </Grid>

        <Grid item xs={12} align="center">
          <img alt="QR Code" src={ 'https://chart.googleapis.com/chart?chs=250x250&cht=qr&chl=' + wallet.address }/>
        </Grid>

        <Grid item xs={12} align="center">
         <a href="/">Back</a>
        </Grid>

      </Grid>
    </div>
  );
}

export default PublicWallet;
