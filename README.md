# CryptoPricesWebApp
View live prices of BTC and ETH on Binance and Coinbase

# Build and run instructions(Using WSL or Ubuntu)
1. Clone repo using git clone https://github.com/mohnishs1975/CryptoPricesWebApp.git
2. Install all of the necessary dependencies using pip3 install -r requirments.txt
3. Run server using python3 WebApp.py.
4. To view the webpage search http://127.0.0.1:8050/ in your browser.

# Questionnaire
1. A shortcut I took was not deploying the app. I ran into a number of problems using free hosting services ranging from low disk space to load balancing issues. Heroku in particular had trouble installing dependencies as some had conflicting dependencies of different versions. There were too many dependencies for pythonanywhere to store as well. The web page worked fine on the localhost so I thought this could be implemented later.
2. The web app is fairly straightforward and performs all of the necessary functions of displaying live prices of BTC and ETH on two different exchanges. Based on the current prices, recommendations are offered on which exchange to buy or sell. I did add deltas to make the page look better and that could be the only "over-designed" feature.
3. Load balancing could fix the issue of server loads. The constant stream of data from Binance and Coinbase could also be playing a part in server-related issues.
4. With more time I would try to figure out how to deploy the web page online and I could also make the frontend more aesthetic. 

# Webpage

![Capture](https://user-images.githubusercontent.com/56131306/138947679-731104af-0b09-4479-b0a2-bef85771387b.PNG)
