import './App.css';
import SenderWallet from './components/SenderWallet';
import PublicWallets from './components/PublicWallets';
import AllPublicWallets from './components/AllPublicWallets';
import PublicWallet from './components/PublicWallet';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

function App(props) {
  return (
    <div className="App">
      <h1>Bitcoin Wallet Demo</h1>
      <Router>
        <Routes>
          <Route exact path='/' element={<> <SenderWallet /> <PublicWallets /> </>} />
          <Route path='/wallet' element={<> <SenderWallet /> </>} />
          <Route path='/send' element={<> <PublicWallets /> </>} />
          <Route path='/public-wallets/' element={<> <AllPublicWallets /> </>} />
          <Route path='/public-wallets/:address' element={<> <PublicWallet /> </>} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
