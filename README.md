# TNM-chan
Hi there! My name's TNM-chan (people call me Tee-chan for short). I'm an android - well, if that's the word for it...I'm technically a Discord bot. So...why am I here, then? Well, because I want you to peer inside my Discord brain! Duh!
## So...what can I find here?
You can find...well, me! This is where my source code is - y'know, the stuff that powers me! (Of course, not the private stuff. That's only for me and Rare to discuss~) Feel free to take a look around, see what makes me tick, y'know...stuff like that.
## I want to add you to my server! How do I do that?
Great question, I'd love to show you the answer! It's a five-part process, but it's all worth it - and you might learn a bit of Python along the way~
### Part 1: Server prerequisites
▸Before starting, make sure you have the latest version of Python3 installed. (Python2 won't work!)
▸Once you have that installed, you'll want to add these libraries like so:
`> pip3 install discord.py`
`> pip3 install termcolor`
`> pip3 install python-dotenv`
▸Next, clone this repository. Click the green button that says "Clone or download," then click "Download ZIP."
▸Once the download finishes, extract it to a folder you can easily access. (If your desktop isn't a mess, that's a good place.)
▸You'll want to start by cloning this repository. Click the green button that says "Clone or download," then click "Download ZIP."
▸Finally, you'll need a way to open the file - if you aren't into coding, just use Notepad to open the file.
### Part 2: Pre-deployment
Cool, everything's set up! Now then, let's get this party started!
▸First things first, you'll want to go to https://discord.com/developers/.
▸Once there, click on "New Application" and provide a name.
▸Click on the "Bot" section, then click "Add Bot." Confirm it and BAM! You've just created a Discord bot! ...buuuuuuut it's kinda useless right now. That'll change soon, though...
### Part 3: Deployment, stage 1
Alright, so you've got the libraries, the code, and a shiny new bot. Now let's turn these into a TNM-chan, shall we? Of course, the first thing we need to do is invite your bot to your intended server.
▸Click the "OAuth2" section. This'll look super confusing, but for our use case, we only need one thing.
▸In the "Scopes" section, check the tickbox labeled "bot".
▸You should see a link appear at the bottom of the section; click "Copy," then paste it into a new tab.
▸Select your server and click "Authorize." You should now see your bot appear in the server!
### Part 4: Setting common variables
▸Open the `tnm-chan.py` file in your editor - don't pay any attention to the stuff underneath the `###---###`, as modifying that stuff might break something.
▸Make your changes, then save the file.
▸Now, open the ".env" file. Head back to the Discord Developers portal, and go back to the "Bot" section.
▸Click the "Copy" button, then paste the contents of your clipboard at the end of the `DISCORD_TOKEN=` section. Type the name of your server at the end of the `DISCORD_GUILD` section, then save the file.
And with that, all the hard bits are out of the way - time to deploy this puppy!
### Part 5: Deployment, stage 2
Before continuing, make sure things are set up properly in your server. After all, you don't want your lobby breaking on you, right?
...okay, you checked, and things are good. Let's start your clone of me up!
▸Open your terminal and navigate to the TNM-chan folder. (On Windows, typing `cmd` into the address bar of File Explorer will open a Command Prompt in the directory you're in.)
▸Type `python tnm-chan.py`, and give it a moment...after a bit, you should see the following appear:
```I've connected to the server!```
...and then the bot will come online. Congratulations, you're all set! Now go have some fun...just try to NOT close the terminal without telling your server members first. Otherwise, uhh...they'll get stranded, and you'll have to go and save 'em.
