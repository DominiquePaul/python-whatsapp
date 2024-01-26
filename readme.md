<p align="center">
    <a href="https://github.com/DominiquePaul/python-whatsapp" title="Python Version"><img src="https://img.shields.io/badge/python-3.11+-blue.svg"></a>
    <a href="https://github.com/DominiquePaul/python-whatsapp/blob/master/LICENSE" title="Project License"><img src="https://img.shields.io/badge/license-MIT-blue"></a>
    <a href="https://github.com/psf/black" title="Project License"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
    <a href="https://github.com/DominiquePaul/python-whatsapp" title="Follow on Twitter"><img src="https://img.shields.io/github/last-commit/DominiquePaul/python-whatsapp/main"></a>
    <a href="https://github.com/DominiquePaul/python-whatsapp" title="Follow on Twitter"><img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/DominiquePaul/python-whatsapp"></a>



    <a href="https://twitter.com/DominiqueCAPaul" title="Follow on Twitter"><img src="https://img.shields.io/twitter/follow/dominiquecapaul.svg?style=social&label=Follow"></a>
</p>

<p align="center">
  <a href="#about">Getting Started</a> •
  <a href="#getting-started">Documentation</a> •
  <a href="#other-useful-resources-for-using-whatsapp">Support</a> •
  <a href="#contributing--feature-requests">Contribution</a>
</p>


# About
### How do you use the Whatsapp Cloud API with Python?

This was a question I had two weeks ago (January 2024). I found it a huge pain to implement for another project and therefore started this small sandbox environment.

To save others the pain I decided to make this repo public. Ideally, I'd like to make the Readme a collection of other resources as well.

### This repo includes:

- No packages or third-party services (Twilio, Messagebird, etc.) to interact with WhatsApp
- Asynchronous calls using httpx
- Setting up a webhook using FastAPI

#### Whatsapp functionalities included:
- Extracting the most important information out of a message (message, file type, timestamp etc.)
- Receiving and then downloading a voice memo, document or image
- Sending a text message
- Sending a text message with multiple options
- Sending a document, including how to first upload the media

# Getting started

1. Set up your Whatsapp app at [developers.facebook.com/apps](https://developers.facebook.com/apps/) and get all of your credentials. [Dave Ebbelaar](https://www.youtube.com/watch?v=3YPeh-3AFmM&ab_channel=DaveEbbelaar) has a good video on this.
   1. Make sure you've sent a message to your personal WhatsApp and replied.
   2. Replace all values in `example.env` with your credentials from Meta.
   3. Rename `example.env` to `.env`
2. Setup Ngrok
   1. Set up an Ngrok account and get your static domain. To work with a webhook you need to have a redirect in place. I used and recommend ngrok for this.
   2. Start ngrok (you might need to install it first, e.g. with brew) using `ngrok http http://localhost:8000 --domain=<YOUR-NGROK-STATIC-DOMAIN>.ngrok-free.app`
3. Start the app with `python -m myapp.main`

# Other useful resources for using WhatsApp
- ["How To Connect OpenAI To WhatsApp"](https://www.youtube.com/watch?v=3YPeh-3AFmM&ab_channel=DaveEbbelaar) (YouTube video) uses Flask (not asynchronous) by Dave Ebbelaar
- [Meta's documentation](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-messages#media-messages) is also useful (I didn't find this initially), but there are some small mistakes.
- [py-fastapi-facebook-webhook] is useful GitHub repo that I started with when I created this repo, but some components don't work with current package versions (e.g. httpx)


# Contributing / Feature requests
Please feel free to open a pull request to add more content (or improve the code). If you don't know how to do that but still want to contribute then you can send me an email to dominique [dot] c [dot] a [dot] paul [at] gmail [dot] com

Also, feel free to reach out if you are stuck or want to request a feature to be added.
