# Setup

## Setting Environment Variables
Currently the only environment variable that needs to be set is your Blockcypher API Token which should be set as **'BC_API'**.

## Building the Project
To run the project you must first create a build of the front-end which utilizes a react project. To do this navigate to the 'frontend' directory and type **'npm run build'** (This information can also be found in the README.md file in the 'frontend' directory).

## Running the project
Once you have built the front-end navigate to the root directory and start the Django service by typing **'python ./manage.py runserver'**.

# Changelog
- **April 27, 2022:**
  - Initial Commit
- **April 27, 2022:** [Link](https://github.com/JacksonKeenan/BitcoinDemoApp/commit/224f2664d80128baa0e2390e7f7294d3b70fa99c)
  - Updated .gitignore
- **April 27, 2022:** [Link](https://github.com/JacksonKeenan/BitcoinDemoApp/commit/90f05a68b71385306f311197bcfe455349bd43d7)
  - Updated Commenting & Documentation
- **May 3, 2022:** [Link](https://github.com/JacksonKeenan/BitcoinDemoApp/commit/1e826233aa932123fc81fc1a7c1be232ad9ce5af)
  - Added environment variable support
  - Added README.md with setup instructions and changelog
- **May 3, 2022:** [Link](https://github.com/JacksonKeenan/BitcoinDemoApp/commit/12e4dcc59e703663494927acce4135ba9c8ae634)
  - Updated Database Models
    - Both 'SenderWallets' & 'PublicWallets' models now inherit from abstract 'Wallet'
    - Removed 'ActiveSenderWallet' model, replaced with 'is_active' flag in the 'SenderWallet' model to indicate current active sending wallet.
    - Updated views.py and serializers.py to reflect model changes.
