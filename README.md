# Setup

## API Key File
After cloning the repository create a file containing your Blockcypher API key in the root directory named `.blockcypher_api`. If you do no have an API key you can generate one [here](https://accounts.blockcypher.com/tokens)

## Building & Running the Project
In the root directory run `docker-compose up --build`. You will need to have [Docker](https://www.docker.com/products/docker-desktop/) setup to run this command.

# Changelog
- **April 27, 2022:**
  - Initial Commit.
- **April 27, 2022:** [Link](https://github.com/JacksonKeenan/BitcoinDemoApp/commit/224f2664d80128baa0e2390e7f7294d3b70fa99c)
  - Updated .gitignore.
- **April 27, 2022:** [Link](https://github.com/JacksonKeenan/BitcoinDemoApp/commit/90f05a68b71385306f311197bcfe455349bd43d7)
  - Updated Commenting & Documentation.
- **May 3, 2022:** [Link](https://github.com/JacksonKeenan/BitcoinDemoApp/commit/1e826233aa932123fc81fc1a7c1be232ad9ce5af)
  - Added environment variable support.
  - Added README.md with setup instructions and changelog.
- **May 3, 2022:** [Link](https://github.com/JacksonKeenan/BitcoinDemoApp/commit/12e4dcc59e703663494927acce4135ba9c8ae634)
  - Updated Database Models.
    - Both 'SenderWallets' & 'PublicWallets' models now inherit from abstract model 'Wallet'.
    - Removed 'ActiveSenderWallet' model, replaced with 'is_active' flag in the 'SenderWallet' model to indicate current active sending wallet.
    - Updated views.py and serializers.py to reflect model changes.
- **May 4, 2022:** [Link](https://github.com/JacksonKeenan/BitcoinDemoApp/commit/8cf48053549928485279be35c15a07e6e9c1d14f)
  - Significantly improved error trapping for Blockcypher API calls.
- **May 4, 2022:** [Link](https://github.com/JacksonKeenan/BitcoinDemoApp/commit/fab31d8c473b57e1718c38f82a04f9a51a8182e3)
  - Reduced code re-use by refactoring.
    - Both 'CreatePublicWalletSearchView' & 'CreatePublicWalletSendView' now call 'SearchAddress' instead of searching and storing a public address internally.
    - Removed  'RecentPublicWalletView' and added the ability to filter by a time delta to 'PublicWalletView'.
- **May 4, 2022:**
    - Updated Commenting & Documentation.
- **May 4, 2022:** [Link](https://github.com/JacksonKeenan/BitcoinDemoApp/commit/3b665ff14f687516a440fb81ecb4e7afed1fe6df)
  - Added the ability for the user to view the sending wallets currently available in the system through the 'View Available Wallets' button.
  - 'PublicWalletView' now returns wallets sorted by date/time.
  - Further improved Blockcypher error trapping.
- **May 4, 2022:**
  - Updated Commenting & Documentation.
- **May 5, 2022:** [Link](https://github.com/JacksonKeenan/BitcoinDemoApp/commit/d4c48edf5b8edabe432224ac6813dcd4cf7dd4a5)
  - Further improved Blockcypher error trapping.
  - Added comment explaining modifications needed if app was to include fees on transactions (view.py - Line 156)
- **May 6, 2022:** [Link](https://github.com/JacksonKeenan/BitcoinDemoApp/commit/c51e77e0dd762d9d30d7f3d05cd46c5c9bd754b3)
  - Further improved Blockcypher error trapping.
- **May 16, 2022:** [Link](https://github.com/JacksonKeenan/BitcoinDemoApp/commit/beb0d8010ec922395db7d2b93bfdc84224d5617f)
  - Updated error trapping.
- **May 17, 2022:** [Link](https://github.com/JacksonKeenan/BitcoinDemoApp/commit/b6506ad11f2512ce2e8a1043013d896dd541698c)
  - Added Docker support
- **June 14, 2022:**
  - Fixed bug with Docker Compose file which was preventing application from running without being built with node beforehand.
  - Updated README

