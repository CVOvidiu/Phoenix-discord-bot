import discord
import motor.motor_asyncio
from discord.ext import commands
from discord import Embed, Emoji
from discord.ext.commands import BucketType, cooldown, CommandOnCooldown

# Database config
mongoURL = ""
cluster = motor.motor_asyncio.AsyncIOMotorClient(mongoURL)
db = cluster["phoenixDB"]
collection = db["phoenixCollection"]
shop_collection = db["phoenixShopInventory"]
color_list = {}

# Cog config
class Shop(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    def color_dictionary_init(self):
        global color_list
        gui = self.client.get_guild(id = 569077625826443274)
        
        #TODO: 1

        one = discord.utils.get(gui.roles, id = 842882507040489492)
        two = discord.utils.get(gui.roles, id = 835865447495893022)
        three = discord.utils.get(gui.roles, id = 842882342719979530)
        four = discord.utils.get(gui.roles, id = 835865523929350214)
        five = discord.utils.get(gui.roles, id = 842882738981961749)
        six = discord.utils.get(gui.roles, id = 842882110808129606)
        seven = discord.utils.get(gui.roles, id = 835865558548611096)
        eight = discord.utils.get(gui.roles, id = 842882007976378368)
        nine = discord.utils.get(gui.roles, id = 835865573220941837)
        ten = discord.utils.get(gui.roles, id = 842882611814334515)
        eleven = discord.utils.get(gui.roles, id = 842882909404397599)
        twelve = discord.utils.get(gui.roles, id = 835865586956632114)
        thirteen = discord.utils.get(gui.roles, id = 842883661355417630)
        fourteen = discord.utils.get(gui.roles, id = 842883780540235826)#
        fifteen = discord.utils.get(gui.roles, id = 842881353116418048)
        sixteen = discord.utils.get(gui.roles, id = 842881627440939028)
        seventeen = discord.utils.get(gui.roles, id = 842881802360061958)

        color_list[one] = '1'
        color_list[two] = '2'
        color_list[three] = '3'
        color_list[four] = '4'
        color_list[five] = '5'
        color_list[six] = '6'
        color_list[seven] = '7'
        color_list[eight] = '8'
        color_list[nine] = '9'
        color_list[ten] = '10'
        color_list[eleven] = '11'
        color_list[twelve] = '12'
        color_list[thirteen] = '13'
        color_list[fourteen] = '14'
        color_list[fifteen] = '15'
        color_list[sixteen] = '16'
        color_list[seventeen] = '17'

    @commands.command()
    @commands.cooldown(3, 30, commands.BucketType.user)
    async def shop(self, ctx, category : str = None):

        if category == None:
            # Nu a specificat categoria
            embed = Embed(title = '**Shop**', description = 'Alege o categorie de mai jos: `[ph?shop <categorie>]`', color = 0xff006f)
            embed.set_footer(text = 'Made by iLectus#3916', icon_url='https://cdn.discordapp.com/attachments/768118506813390859/804786242692579348/phoenix_Logo2.png')
            embed.add_field(name = '`Colors`', value = 'Daca vrei sa cumperi un rol de culoare. (Gratis pentru cei care au tag)', inline = False)
            embed.add_field(name = '`TagOnly`', value = 'Daca vrei sa cumperi lucruri pe care doar cei cu tag si minim level 10 la ActivityRank pot sa cumpere.', inline=False)
        else:
            # A specificat categoria
            if category.lower() == 'tagonly':
                oos = discord.utils.get(ctx.author.guild.roles, id = 842836861001007122)
                os = discord.utils.get(ctx.author.guild.roles, id = 842837049094438932)
                embed = Embed(title = '**TagOnly shop**', description = 'Shopul pentru cei cu tag si au minim level 10 la ActivityRank: `[ph?buy <object>]`', color = 0xff006f)
                embed.set_footer(text = 'Made by iLectus#3916', icon_url='https://cdn.discordapp.com/attachments/768118506813390859/804786242692579348/phoenix_Logo2.png')
                embed.add_field(name = "Nitro Classic", value = f"`100.000` <:currency:800676742104088578> {os.mention}", inline=False)
                embed.add_field(name = "Nitro", value = f"`200.000` <:currency:800676742104088578> {oos.mention}", inline=False)
                embed.add_field(name = "5€ PayPal", value = f"`125.000` <:currency:800676742104088578> {os.mention}", inline=False)

            if category.lower() == 'colors':
                # Categorie culori

                #TODO: 2

                one = discord.utils.get(ctx.author.guild.roles, id = 842882507040489492)
                two = discord.utils.get(ctx.author.guild.roles, id = 835865447495893022)
                three = discord.utils.get(ctx.author.guild.roles, id = 842882342719979530)
                four = discord.utils.get(ctx.author.guild.roles, id = 835865523929350214)
                five = discord.utils.get(ctx.author.guild.roles, id = 842882738981961749)
                six = discord.utils.get(ctx.author.guild.roles, id = 842882110808129606)
                seven = discord.utils.get(ctx.author.guild.roles, id = 835865558548611096)
                eight = discord.utils.get(ctx.author.guild.roles, id = 842882007976378368)
                nine = discord.utils.get(ctx.author.guild.roles, id = 835865573220941837)
                ten = discord.utils.get(ctx.author.guild.roles, id = 842882611814334515)
                eleven = discord.utils.get(ctx.author.guild.roles, id = 842882909404397599)
                twelve = discord.utils.get(ctx.author.guild.roles, id = 835865586956632114)
                thirteen = discord.utils.get(ctx.author.guild.roles, id = 842883661355417630)
                fourteen = discord.utils.get(ctx.author.guild.roles, id = 842883780540235826)
                fifteen = discord.utils.get(ctx.author.guild.roles, id = 842881353116418048)
                sixteen = discord.utils.get(ctx.author.guild.roles, id = 842881627440939028)
                seventeen = discord.utils.get(ctx.author.guild.roles, id = 842881802360061958)
                
                desc = f""" **1. » {one.mention} » 1500** <:currency:800676742104088578>\n
                           **2. » {two.mention} » 1500** <:currency:800676742104088578>\n
                           **3. » {three.mention} » 1500** <:currency:800676742104088578>\n
                           **4. » {four.mention} » 1500** <:currency:800676742104088578>\n
                           **5. » {five.mention} » 1500** <:currency:800676742104088578>\n
                           **6. » {six.mention} » 1500** <:currency:800676742104088578>\n
                           **7. » {seven.mention} » 1500** <:currency:800676742104088578>\n
                           **8. » {eight.mention} » 1500** <:currency:800676742104088578>\n
                           **9. » {nine.mention} » 1500** <:currency:800676742104088578>\n
                           **10. » {ten.mention} » 1500** <:currency:800676742104088578>\n
                           **11. » {eleven.mention} » 1500** <:currency:800676742104088578>\n
                           **12. » {twelve.mention} » 1500** <:currency:800676742104088578>\n
                           **13. » {thirteen.mention} » 1500** <:currency:800676742104088578>\n
                           **14. » {fourteen.mention} » 1500** <:currency:800676742104088578>\n
                           **15. » {fifteen.mention} » 1500** <:currency:800676742104088578>\n
                           **16. » {sixteen.mention} » 1500** <:currency:800676742104088578>\n
                           **17. » {seventeen.mention} » 1500** <:currency:800676742104088578>\n"""

                embed = Embed(title = '**» Color Shop «**', description = f'{desc}', color = 0xff006f)
                embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/842428676439539722/843516458662101052/download-1.png")
                embed.set_footer(text = f'Cumpara culoare : [ph?buy <numar>]\nMade by iLectus#3916', icon_url='https://cdn.discordapp.com/attachments/768118506813390859/804786242692579348/phoenix_Logo2.png')

        await ctx.send(embed = embed, delete_after=5*60)

    
    @commands.command(aliases=["inv"])
    @commands.cooldown(3, 30, commands.BucketType.user)
    async def inventory(self, ctx):
        global db
        global cluster
        global mongoURL
        global shop_collection
        user_id = ctx.author.id
        user_obj = ctx.author

        Shop.color_dictionary_init(self)

        if await shop_collection.count_documents({"_id":user_id}) == 0: # Daca nu exista in baza shop
            await ctx.send("**Nu ai nimic in inventar!**", delete_after=15)
        else: # Exista in baza shop
            embed = Embed(color = 0xff006f, title = f"{user_obj.name}'s Color Inventory:")
            #TODO: Vezi cum pui thumbnail la embed!
            result = shop_collection.find({"_id":user_id})
            async for i in result:
                lista = list(i.keys())
                for num in lista:
                    if num == "_id":
                        pass
                    else:
                        index = lista.index(num)
                        embed.add_field(name = f"{index} - `{num}`", value='⠀', inline=False)
            await ctx.send(embed = embed)

    @commands.command()
    @commands.cooldown(3, 30, commands.BucketType.user)
    async def buy(self, ctx, shop_object : str):
        global collection
        global db
        global cluster
        global mongoURL
        global shop_collection
        user_id = ctx.author.id
        user_obj = ctx.author

        Shop.color_dictionary_init(self)

        async def buy_shop_obj_color(shop_obj_name : str, shop_obj_price : int, guild_role_id : int):
                if shop_object.lower() == shop_obj_name:
                    tag = discord.utils.get(user_obj.guild.roles, id = 835853720175902730)
                    if tag in user_obj.roles:
                        # Userul are tag
                        embed = Embed(color = 0xff006f, description = f"**Deoarece ai tag-ul in nume, poti sa iti alegi orice culoare vrei folosind comanda `[ph?color <color>]`**")
                        await ctx.send(embed = embed)
                    else:
                        # Userul nu are tag
                        if user_bal < shop_obj_price:
                            # Userul nu are bani suficienti
                            embed = Embed(color = 0xff006f, description = f"**Nu ai suficienti bani! Itemul costa :** `{shop_obj_price}` <:currency:800676742104088578> **!**")
                            await ctx.send(embed = embed, delete_after=15)
                        else:
                            # Userul are suficienti bani
                            # Rolul culorii
                            color = discord.utils.get(user_obj.guild.roles, id = guild_role_id)
                            # Shop Inventory
                            # Verificam daca userul exista in ShopInventory
                            if await shop_collection.count_documents({"_id":user_id}) == 0:
                                # Nu este in ShopInventory
                                # Il bagam in ShopInventory
                                await shop_collection.insert_one({"_id":user_id})
                            # Acum userul trebuie trebuie sa fie in ShopInventory
                            # Verificam daca a mai cumparat obiectul
                            if await shop_collection.count_documents({"_id":user_id, f"{shop_obj_name}":{"$exists":True}}) == 0:
                                # Nu a mai cumparat culoarea
                                # Ii scoatem rolul precedent daca avea
                                for color_role, string in color_list.items():
                                    if color_role in user_obj.roles:
                                    # O scoatem
                                        await user_obj.remove_roles(color_role)
                                # Ii scoatem banii din balanta
                                user_bal_upt = int(user_bal - shop_obj_price)
                                await collection.update_one({"_id":user_id}, {"$set":{"balance":user_bal_upt}}, upsert = True)
                                # O bagam in inventarul userului
                                await shop_collection.update_one({"_id":user_id}, {"$set":{f"{shop_obj_name}":0}}, upsert=True)
                                # Ii dam rolul
                                await user_obj.add_roles(color)
                                embed = Embed(color = 0xff006f, description = f"**Ai cumparat** `{shop_object}` **cu succes! Pentru a schimba culoarea, foloseste `ph?color <color>` (`ph?swaptocolor none` pentru a nu mai avea culoare)**")
                                await ctx.send(embed = embed)
                            else:
                                # A mai cumparat culoarea in trecut
                                embed = Embed(color = 0xff006f, description = f"**Ai deja in inventar** `{shop_object}` **! Foloseste comanda** `[ph?color <color>]` **pentru a schimba culoarea.**")
                                await ctx.send(embed = embed)

        # Verificam daca userul exista in baza main
        if await collection.count_documents({"_id":user_id, "balance":{"$exists":True}}) == 0:
            # Daca fieldul balanta nu exista in documentul userului
            embed = Embed(color = 0xff006f, description = f"**Nu ai suficienti bani! Itemul costa :** `{shop_obj_price}` <:currency:800676742104088578> **!**")
            await ctx.send(embed = embed, delete_after=15)
        else:
            # Daca exista in baza main
            # Luam din baza de date balanta userului
            result = collection.find({"_id":user_id}, {"balance":True})
            async for i in result:
                user_bal = i["balance"]

                # Pentru culori
                #TODO: 3

                await buy_shop_obj_color('1', 1500, 842882507040489492)
                await buy_shop_obj_color('2', 1500, 835865447495893022)
                await buy_shop_obj_color('3', 1500, 842882342719979530)
                await buy_shop_obj_color('4', 1500, 835865523929350214)
                await buy_shop_obj_color('5', 1500, 842882738981961749)
                await buy_shop_obj_color('6', 1500, 842882110808129606)
                await buy_shop_obj_color('7', 1500, 835865558548611096)
                await buy_shop_obj_color('8', 1500, 842882007976378368)
                await buy_shop_obj_color('9', 1500, 835865573220941837)
                await buy_shop_obj_color('10', 1500, 842882611814334515)
                await buy_shop_obj_color('11', 1500, 842882909404397599)
                await buy_shop_obj_color('12', 1500, 835865586956632114)
                await buy_shop_obj_color('13', 1500, 842883661355417630)
                await buy_shop_obj_color('14', 1500, 842883780540235826)
                await buy_shop_obj_color('15', 1500, 842881353116418048)
                await buy_shop_obj_color('16', 1500, 842881627440939028)
                await buy_shop_obj_color('17', 1500, 842881802360061958)

    @commands.command()
    @commands.cooldown(3, 30, commands.BucketType.user)
    async def color(self, ctx, color : str):
        global db
        global cluster
        global mongoURL
        global shop_collection
        user_id = ctx.author.id
        user_obj = ctx.author

        Shop.color_dictionary_init(self)

        # Verificam daca are tag-ul
        tag = discord.utils.get(user_obj.guild.roles, id = 835853720175902730)
        if tag in user_obj.roles:
            # Userul are tag
            # Verificam daca are vreo culoare deja si o scoatem
            for color_role, string in color_list.items():
                if color_role in user_obj.roles:
                    # O scoatem
                    await user_obj.remove_roles(color_role)
                
            if color.lower() == 'none':
                await ctx.send("**Nu mai ai nicio culoare.**", delete_after=15)
            else:
                # Adaugam culoarea noua
                for color_role, color_string in color_list.items():
                    if color.lower() == color_string:
                        await user_obj.add_roles(color_role)
                        await ctx.send("**Culoarea ti-a fost schimbata.**", delete_after=15)
        else:
            # Userul nu are tag
            # Lucram cu baza de shop
            # Verificam daca culoarea specificata exista in inventarul userului
            color = color.lower()
            if color.lower() == 'none':
                await ctx.send("**Nu mai ai nicio culoare.**", delete_after=15)
                # Scoatem culoarea veche, daca avea
                for color_role, color_string in color_list.items():
                    if color_role in user_obj.roles:
                        await user_obj.remove_roles(color_role)
            elif await shop_collection.count_documents({"_id":user_id, f"{color}":{"$exists":True}}) == 0:
                # Daca culoarea specificata nu exista in inventarul userului
                await ctx.send(f"**Culoarea specificata nu exista in inventarul tau.**", delete_after=15)
            else:
                # Culoarea specificata exista in inventarul userului
                # Scoatem culoarea veche, daca avea
                for color_role, color_string in color_list.items():
                    if color_role in user_obj.roles:
                        await user_obj.remove_roles(color_role)

                # Adaugam culoarea noua
                for color_role, color_string in color_list.items():
                    if color == color_string:
                        await user_obj.add_roles(color_role)
                        await ctx.send("**Culoarea ti-a fost schimbata.**", delete_after=15)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        global db
        global cluster
        global mongoURL
        global shop_collection

        Shop.color_dictionary_init(self)

        tag = discord.utils.get(before.guild.roles, id = 835853720175902730)
        if tag not in after.roles:
            for color_role, color_string in color_list.items():
                result = await shop_collection.count_documents({"_id":after.id, f"{color_string}":{"$exists":True}})
                if result == 0:
                    if color_role in after.roles:
                        await after.remove_roles(color_role)
                        await after.send(f"**Deoarece ti-ai scos tag-ul si ai avut `{color_string}` datorita tag-ului, l-am scos.**")

    @color.error
    async def color_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed = Embed(color=0xff006f, description = f"**Incearca din nou in 30 secunde! |** :clock1:"), delete_after=10)

    @buy.error
    async def buy_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed = Embed(color=0xff006f, description = f"**Incearca din nou in 30 secunde! |** :clock1:"), delete_after=10)

    @inventory.error
    async def inventory_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed = Embed(color=0xff006f, description = f"**Incearca din nou in 30 secunde! |** :clock1:"), delete_after=10)

    @shop.error
    async def shop_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed = Embed(color=0xff006f, description = f"**Incearca din nou in 30 secunde! |** :clock1:"), delete_after=10)

def setup(client):
    client.add_cog(Shop(client))