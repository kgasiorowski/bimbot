import discord
import config
import random
import nltk
import re

timmy_aliases = ['timmy', ' bimmy', 'bimopher', 'timothy', 'bimothy', 'bim', 'tim']
timmy_regex = r'((^|\s)(T|t|B|b)im)((($|\s|\W$))|((othy)|(opher)|(my)|(bot)))'


class Client(discord.Client):

    def __init__(self):
        super(Client, self).__init__()
        self.mode = True

        nltk.download('brown')
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')

    async def on_ready(self):
        print(f'Logged on as {self.user}')

    async def on_message(self, message):

        if str(message.channel.id) == '628387208138850323' and message.author != self.user:

            print(message.author, f'[{message.content}]')

            if message.content.startswith('!mode'):
                self.mode = not self.mode
                await message.delete()
                await message.channel.send(f'Noun replacement mode changed ({self.mode}).')
                return

            if re.search(timmy_regex, message.content) is not None or message.content.strip() == '':
                return

            if self.mode:

                async with message.channel.typing():

                    original_content = message.content

                    await message.delete()

                    response_message = f"Hey there {message.author.mention}, looks like your message didn't have any " \
                                       f"reference to our lord and savior Timmy. I went ahead and fixed that for " \
                                       f"you:\n"

                    tokenized = nltk.word_tokenize(original_content)
                    nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if pos[:2] == 'NN']

                    new_content = ''

                    for noun in nouns:
                        new_content = original_content.replace(noun, random.choice(timmy_aliases))

                    response_message += "> " + new_content
                    response_message += "\n\nHere's the original: \n> " + original_content

                    await message.channel.send(response_message)

            else:

                await message.delete()
                await message.channel.send(f"Hi {message.author.mention}, your message didn't contain any of the "
                                           f"following: {', '.join(timmy_aliases)}, so your message got yeeted. "
                                           f"Don't try to pull that shit again.")


client = Client()
client.run(config.discord_token)
