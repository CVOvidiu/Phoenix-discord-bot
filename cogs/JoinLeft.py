import discord
import motor.motor_asyncio

from discord.ext import commands, tasks
from discord import Embed
from PIL import Image, ImageFont, ImageDraw, ImageOps
from io import BytesIO
from datetime import datetime

total_mem = 0

mongoURL = ""
cluster = motor.motor_asyncio.AsyncIOMotorClient(mongoURL)
db = cluster["phoenixDB"]
collection = db["phoenixCollection"]

class JoinLeft(commands.Cog):
    def __init__(self, client):
        self.client = client

    def draw_ellipse(image, bounds, width=1, outline='white', antialias=4):
        """Improved ellipse drawing function, based on PIL.ImageDraw."""

        # Use a single channel image (mode='L') as mask.
        # The size of the mask can be increased relative to the imput image
        # to get smoother looking results. 
        mask = Image.new(
            size=[int(dim * antialias) for dim in image.size],
            mode='L', color='black')
        draw = ImageDraw.Draw(mask)

        # draw outer shape in white (color) and inner shape in black (transparent)
        for offset, fill in (width/-2.0, 'white'), (width/2.0, 'black'):
            left, top = [(value + offset) * antialias for value in bounds[:2]]
            right, bottom = [(value - offset) * antialias for value in bounds[2:]]
            draw.ellipse([left, top, right, bottom], fill=fill)

        # downsample the mask using PIL.Image.LANCZOS 
        # (a high-quality downsampling filter).
        mask = mask.resize(image.size, Image.LANCZOS)
        # paste outline color to input image through the mask
        image.paste(outline, mask=mask)

    async def pillow_format(member, text, img, save):
        """Pillow Format Image"""

        font = ImageFont.truetype("Thermidava Black.ttf", 50)
        IMG = Image.open(img)

        # Avatar Member
        memAvatarData = member.avatar_url_as()
        data = BytesIO(await memAvatarData.read())
        memAvatar = Image.open(data)
        memAvatar = memAvatar.resize((250,250))
        bigsize = (memAvatar.size[0]*3, memAvatar.size[1]*3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(memAvatar.size, Image.ANTIALIAS)
        memAvatar.putalpha(mask)
        draw = ImageDraw.Draw(IMG)
        w, h = draw.textsize(text, font=font)
        x, y = IMG.size
        eX, eY = 250, 250 # Size bounding box
        bounding_box = (x/2 - eX/2, y/2 - eY/2 - 40, x/2 + eX/2, y/2 + eY/2 - 40)
        JoinLeft.draw_ellipse(IMG, bounding_box, width=11)
        draw.text(((1024/2 - w/2), 350), text, (255, 255, 255), font=font)
        IMG.paste(memAvatar, (387,60), memAvatar)
        IMG.save(save)

    @tasks.loop(minutes = 10)
    async def update_mem_channel(self):
        global total_mem

        req_channel = self.client.get_channel(id = 879401759238410280)
        await req_channel.edit(name = f"•̥🈳Members • {total_mem}")

    @commands.Cog.listener()
    async def on_ready(self):
        global total_mem

        logs = self.client.get_channel(id = 877659413643657276)
        gui = self.client.get_guild(id = 569077625826443274)

        for mem in gui.members:
            if mem.bot == 0:
                total_mem += 1
        await logs.send(embed = Embed(description = f"<a:loading_color:877665020949954611> | Members loaded : `{total_mem}` loaded."))
        self.update_mem_channel.start()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        global total_mem

        # Cand cineva intra pe server trigger welcome event
        ''' Welcome event :
            - In baza de date a celui care a intrat pui ca a mai intrat odata pe server
            - Un loop-cooldown care verifica cat mai are din welcome event
            - Verifica cu on_message event fiecare mesaj daca contine structura "Welcome {mention}"
            - Pe mention => credite => in main collection pui {id-cine a intrat}:wel-event (sa se stearga dupa ce loopul se termina)
        '''

        channel = self.client.get_channel(569077625826443276) #General Chat
        JandL = self.client.get_channel(569096412369911808) #Welcome and Leave channel 
        reg = self.client.get_channel(569880437430812712) #Regulament mention
        tyr = self.client.get_channel(570616727952556032) #Take Your Roles mention
        logs = self.client.get_channel(id = 877659413643657276) # Phoenix logs
        info = self.client.get_channel(837687280931831849)

        if member.bot == 0:
            # Update Counter
            total_mem += 1
            await logs.send(embed = Embed(description = f"<:bfa_peek:884856540190900335> | `{member.display_name}` has joined. Members : `{total_mem}`"))

            # Not Verified
            role = discord.utils.get(member.guild.roles, id = 878972176827551746)
            await member.add_roles(role)

            # Delimitatoare
            del_1 = discord.utils.get(member.guild.roles, id = 798734389462302761)
            del_2 = discord.utils.get(member.guild.roles, id = 836960907275141190)
            del_3 = discord.utils.get(member.guild.roles, id = 836306673986830378)
            await member.add_roles(del_1, del_2, del_3)

        # -------- PIL Config --------
        text = f'WELCOME {member.display_name}!'
        img = "assets/join.png"
        save = "assets/profile.png"
        await JoinLeft.pillow_format(member, text, img, save)
        # ----------------------------

        embed = Embed(color = 0xe03a3e)
        embed.set_image(url="attachment://image.png")
        file = discord.File("assets/profile.png", filename="image.png")
        await JandL.send(f'**Bine ai venit pe BornFromAshes, {member.name} ! <:bfa_peek:884856540190900335>** \n **✦ Total Members : `{total_mem}`**')
        await JandL.send(file=file, embed = embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        global total_mem

        JandL = self.client.get_channel(569096412369911808)
        logs = self.client.get_channel(id = 877659413643657276)
        role_list = []
        string = ""

        if member.bot == 0:
            total_mem -= 1
            await logs.send(embed = Embed(description = f"<:bfa_cry:884859294896521216> | `{member.display_name}` has left. Members : `{total_mem}`"))
            for role in member.roles:
                if role.id != 798734389462302761 and role.id != 836960907275141190 and role.id != 836306673986830378 and str(role.mention) != "<@&569077625826443274>":
                    role_list.append(role.mention)
            for i in role_list:
                if i != role_list[-1]:
                    string = f"{string}" + f"{i}\n"
                else:
                    string = f"{string}" + f"{i}"
            embed = Embed(description = f"{member.display_name} had :\n{string}")
            await logs.send(embed = embed)

        # -------- PIL Config --------
        text = f'GOODBYE {member.display_name}!'
        img = "assets/leave.png"
        save = "assets/profile2.png"
        await JoinLeft.pillow_format(member, text, img, save)
        # ----------------------------

        embed = Embed(color = 0x0d0822)
        file = discord.File("assets/profile2.png", filename="image.png")
        embed.set_image(url="attachment://image.png")
        await JandL.send(f'**{member.name} a parasit BornFormAshes!** <:bfa_cry:884859294896521216> \n **✦ Total Members : `{total_mem}`**')
        await JandL.send(file=file, embed = embed)

def setup(client):
    client.add_cog(JoinLeft(client))