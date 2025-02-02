import numpy
import discord
import os
from keep_alive import keep_alive

client = discord.Client()
rng = numpy.random.default_rng()
wittwer3 = numpy.zeros(9)
wittwer4 = numpy.zeros(16)
w3b = 0
w3z = 0
w4b = 0
w4z = 0
emojis3 = [
    '<:39:860269430537060382>', '<:38:860269430562095104>', '<:37:860269430490791966>',
    '<:36:860269430580051978>', '<:35:860269430629990412>', '<:34:860269430406381649>',
    '<:33:860269430466674728>', '<:32:860269430369550337>', '<:0_:859762589503586304>',
    '<:31:860269430385541120>'
]
emojis4 = [
    '<:16:859536749982253076>', '<:15:859536749582745611>', '<:14:859536749708574721>', '<:13:859536749897056287>',
    '<:12:859536749922091068>', '<:11:859536749982384168>', '<:10:859536749909770280>', '<:9_:859536749825622067>',
    '<:8_:859536749624557569>', '<:7_:859536749897056286>', '<:6_:859536749646839829>', '<:5_:859536749850918963>',
    '<:4_:859536749835452416>', '<:3_:859536749796786215>', '<:2_:859536749838991420>', '<:0_:859762589503586304>',
    '<:1_:859536749830471740>'
]
prefixstr = '$'
mixedstr = 'Witty has been mixed. Use u, d, l and r with the '+ prefixstr +' prefix to move a tile. You can also queue commands, like '+prefixstr+'lddru.'
unmixedstr = 'You attempted to move an unmixed Wittwer. Horrible things will happen.'
remixedstr = 'Wittwer was already mixed, remixing now.'
invalidmovestr = 'This is not a valid move. Wittwer yells. You die.'
winstr = 'Witty has been saved from your stupidity and can now carry on with waking you up every monday and wednesday at 8:15 with no remorse whatsoever.'+emojis4[5]+emojis4[6]
winstr3 = '\n\n\nⁿᵒʷ ᵈᵒ ᵗʰᵉ ʰᵃʳᵈ ᵒⁿᵉ'
winstr4 = '\n\n\nᵇᶦᵍ ᵍᵍ ᵗʰᵒᵘᵍʰ ᵗʰᶦˢ ᶦˢ ᵃᵐᵃᶻᶦⁿᵍ'
helpstr = '''***HELP***
*The current prefix for the bot is '''+prefixstr+'''.*

**Sliding puzzle**
   • *wmix3*: start a 3x3 puzzle
   • *wmix4*: start a 4x4 puzzle
   • *u/d/l/r*: move a tile up/down/left/right into the empty cell
   • *ulldr* (example): chained moves
**Other commands**
   • *witty, plagueis, help*
**Random stuff (without prefix)**
   • *yeet, bruh, aaa*
   • *lmao* (for selected users only)'''

@client.event
async def on_ready(): print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global wittwer3
    global w3b
    global w3z
    global wittwer4
    global w4b
    global w4z
    if message.author == client.user: return
    if message.content.startswith(prefixstr):
        input = message.content[1:].lower()
        #puzzle commands ------------------------------------------
        if input == 'wmix3':
            if w3b == 1 or w4b == 1: await message.channel.send(remixedstr)
            w3b = 1
            w4b = 0
            wittwer3 = numpy.arange(9)
            rng.shuffle(wittwer3)
            for n in range(0, 9):
                if wittwer3[n] == 8:
                    w3z = n
                    break
            await message.channel.send(printw3(wittwer3))
            await message.channel.send(mixedstr)
            return
        elif input == 'wmix4':
            if w3b == 1 or w4b == 1: await message.channel.send(remixedstr)
            w3b = 0
            w4b = 1
            wittwer4 = numpy.arange(16)
            rng.shuffle(wittwer4)
            for n in range(0, 16):
                if wittwer4[n] == 15:
                    w4z = n
                    break
            await message.channel.send(printw4(wittwer4))
            await message.channel.send(mixedstr)
            return
        elif set(input).issubset({'u', 'd', 'l', 'r'}):
            if w3b == w4b:
                await message.channel.send(unmixedstr)
                if w3b == 1:
                    w3b = 0
                    w4b = 0
                return
            error = 0
            l = 0
            if w3b == 1 and w4b == 0:
                while error == 0 and l < len(input):
                    input2 = input[l]
                    if input2 == 'r':
                        if w3z == 0 or w3z == 3 or w3z == 6: error = 1
                        else:
                            temp = wittwer3[w3z - 1]
                            wittwer3[w3z - 1] = wittwer3[w3z]
                            wittwer3[w3z] = temp
                            w3z -= 1
                    if input2 == 'l':
                        if w3z == 2 or w3z == 5 or w3z == 8: error = 1
                        else:
                            temp = wittwer3[w3z + 1]
                            wittwer3[w3z + 1] = wittwer3[w3z]
                            wittwer3[w3z] = temp
                            w3z += 1
                    if input2 == 'd':
                        if w3z == 0 or w3z == 1 or w3z == 2: error = 1
                        else:
                            temp = wittwer3[w3z - 3]
                            wittwer3[w3z - 3] = wittwer3[w3z]
                            wittwer3[w3z] = temp
                            w3z -= 3
                    if input2 == 'u':
                        if w3z == 6 or w3z == 7 or w3z == 8: error = 1
                        else:
                            temp = wittwer3[w3z + 3]
                            wittwer3[w3z + 3] = wittwer3[w3z]
                            wittwer3[w3z] = temp
                            w3z += 3
                    l += 1
                if error == 1: await message.channel.send(invalidmovestr)
                await message.channel.send(printw3(wittwer3))
                cnt = 0
                for n in range(9):
                    if wittwer3[n] == n: cnt += 1
                if cnt == 9:
                    error = 1
                    w4b = 0
                    await message.channel.send(winstr+winstr3)
                return  
            elif w3b == 0 and w4b == 1:
                while error == 0 and l < len(input):
                    input2 = input[l]
                    if input2 == 'r':
                        if w4z == 0 or w4z == 4 or w4z == 8 or w4z == 12: error = 1
                        else:
                            temp = wittwer4[w4z - 1]
                            wittwer4[w4z - 1] = wittwer4[w4z]
                            wittwer4[w4z] = temp
                            w4z -= 1
                    if input2 == 'l' and error == 0:
                        if w4z == 3 or w4z == 7 or w4z == 11 or w4z == 15: error = 1
                        else:
                            temp = wittwer4[w4z + 1]
                            wittwer4[w4z + 1] = wittwer4[w4z]
                            wittwer4[w4z] = temp
                            w4z += 1
                    if input2 == 'd' and error == 0:
                        if w4z == 0 or w4z == 1 or w4z == 2 or w4z == 3: error = 1
                        else:
                            temp = wittwer4[w4z - 4]
                            wittwer4[w4z - 4] = wittwer4[w4z]
                            wittwer4[w4z] = temp
                            w4z -= 4
                    if input2 == 'u' and error == 0:
                        if w4z == 12 or w4z == 13 or w4z == 14 or w4z == 15: error = 1
                        else:
                            temp = wittwer4[w4z + 4]
                            wittwer4[w4z + 4] = wittwer4[w4z]
                            wittwer4[w4z] = temp
                            w4z += 4
                    l += 1
                if error == 1: await message.channel.send(invalidmovestr)
                await message.channel.send(printw4(wittwer4))
                cnt = 0
                for n in range(16):
                    if wittwer4[n] == n: cnt += 1
                if cnt == 16:
                    error = 1
                    w4b = 0
                    await message.channel.send(winstr+winstr4)
                return
        #random commands ------------------------------------------
        elif input == 'witty':
            wittweri = numpy.arange(16)
            wittweri[15] += 1
            await message.channel.send(printw4(wittweri))
            return
        elif input == 'plagueis':
            await message.channel.send(
                'Did you ever hear the tragedy of Darth Plagueis The Wise? I thought not. '+
                'It’s not a story the Jedi would tell you. It’s a Sith legend. '+
                'Darth Plagueis was a Dark Lord of the Sith, so powerful and so wise he '+
                'could use the Force to influence the midichlorians to create life… '+
                'He had such a knowledge of the dark side that he could even keep the ones '+
                'he cared about from dying. The dark side of the Force is a pathway to many '+
                'abilities some consider to be unnatural. He became so powerful… the only '+
                'thing he was afraid of was losing his power, which eventually, of course, he did. '+
                'Unfortunately, he taught his apprentice everything he knew, then his apprentice '+
                'killed him in his sleep. Ironic. He could save others from death, but not himself.'
            )
            await message.channel.send('https://tenor.com/bk8ik.gif')
            return
        elif input == 'help': await message.channel.send(helpstr)  
        
        else:
            await message.channel.send('me no understand')
        return
    #rest --------------------------------------------------------
    else:
        input = message.content.lower()
        if set(input).issubset({'a',' ','.','!'}) and len(input) > 2: await message.channel.send('A'*rng.integers(1,500))
        if "lmao" in input:
            if message.author.id == 181681253899042817:
                await message.add_reaction('<:lmaobassam:778739200257818636>')
            elif message.author.id == 287306245893914624:
                await message.add_reaction('<:lmaobatman:778740489960292352>')
        if "yeet" in input: await message.add_reaction('<:yeet:744153144040095784>')
        if "bruh" in input: await message.add_reaction('<:bruh:786383332035788832>')
        if message.mentions: await message.add_reaction('<:pandaping:822443133139812394>')

    return
#functions --------------------------------------------------
def printw3(arrayinput):
    global w3z
    ppwstr = ''
    cnt = 0
    for n in range(9):
        ppwstr += emojis3[arrayinput[n]]
        cnt += 1
        if cnt == 3:
            cnt = 0
            ppwstr += '\n'
    return ppwstr

def printw4(arrayinput):
    global w4z
    ppwstr = ''
    cnt = 0
    for n in range(16):
        ppwstr += emojis4[arrayinput[n]]
        cnt += 1
        if cnt == 4:
            cnt = 0
            ppwstr += '\n'
    return ppwstr

keep_alive()
client.run(os.environ.get('TOKEN'))