import os
import json
import discord
import random
from discord.ext import commands

with open("config.json") as e:
    infos = json.load(e)
    TOKEN = infos["token"]
    prefixo = infos["prefix"]



intents = discord.Intents.default()
intents.members = True

testing = False

client = commands.Bot(command_prefix=prefixo, intents=discord.Intents.all())


client.remove_command('help')


@client.event #Quando Liga
async def on_ready():
 print(' o BOT {0.user} está funcionando' .format(client) )
 await client.change_presence(activity=discord.Game(name=f"Nome do servidor para alterar status no discord" ))




@client.command(name="ip")
async def ip (ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    em = discord.Embed(title=f"{ctx.author.name} ", color=0xff0000)
    em.add_field(name="IP Do Servidor", value=f"", inline=True)
    em.add_field(name="Endereço", value=f"NOME DO SERVIDOR", inline=False)
    em.add_field(name="Porta", value=f"NºPORTA", inline=False)


    await ctx.send(embed=em)

'''
Esse evento é para informar a entrada de membros no servidor, para usar é necessario adicionar o ID do canal em id= para informar a saída de dados
também é necessario informar uma url para mostrar a imagem ou gif no discord.
'''
#comando Bem vindo! e Removido
@client.event
async def on_member_join(member):
    guild = member.guild.name
    canal = discord.utils.get(guild.channels, id=1075833159247220756)
    embed = discord.Embed(title="Olá! Bem-vindo(a)!", color=0xff0000, description=f'{member.mention.name} seja bem vindo (a) ao Servidor {guild.name}!')
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Quantidade de Membros do Servidor", value=len(guild.members))
    embed.set_image (url= 'https://lh3.ggpht.com/-2VwvqeFwE50/UT5F2HCUL8I/AAAAAAAAIzo/lK5Jq5_b7Rk/s740/BARRA04-OQ.gif')
    await canal.send(embed=embed)

'''
Esse evento é para informar a saída de membros do servidor, para usar é necessario adicionar o ID do canal em id= para informar a saída de dados
também é necessario informar uma url para mostrar a imagem ou gif no discord.
'''
@client.event
async def on_member_remove(member):
    guild = member.guild
    canal = discord.utils.get(guild.channels, id=1077295113816002602)
    embed = discord.Embed(title="Saiu Do Servidor", color=0xff0000, description=f'{member.mention} Saiu do servidor!  volte sempre...  {guild.name}!')
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Quantidade de Membros do Servidor", value=len(guild.members))
    embed.set_image (url= 'https://i.ytimg.com/vi/1SOWVk5B-Eo/maxresdefault.jpg')
    await canal.send(embed=embed)


#comandos mod ------------------------------------------------------------------------------------------------


@client.command()
   #uma das formas de por permissão do comando
async def setcargo(ctx,emoji=None,cargo:discord.Role=None,*,message=None):
    if ctx.author.guild_permissions.ban_members:
        if emoji == None:
            embed=discord.Embed(title='Pegar cargo',description=f'**Escolha um emoji, cargo e mensagem:** {os.linesep}ex: /setcargo [emoji] [cargo] [mensagem]', color=0xff0000)
            await ctx.send(embed=embed)
        else:
            if cargo ==None:
              embed=discord.Embed(title='Pegar cargo',description=f'**Escolha um emoji, cargo e mensagem:**{os.linesep}ex: /setcargo [emoji] [cargo] [mensagem]')
              await ctx.send(embed=embed)
            else:
              if message ==None:
                embed=discord.Embed(title='Pegar cargo',description=f'**Escolha um emoji, cargo e mensagem:** {os.linesep}ex: /setcargo [emoji] [cargo] [mensagem]')
                await ctx.send(embed=embed)
              else:


                embed=discord.Embed(description=f'**{message}**', color=0xff0000)
                await ctx.message.delete()
                enviar= await ctx.send(embed=embed)
                await enviar.add_reaction(emoji)

                with open ('reactrole.json') as json_file:
                  data = json.load(json_file)

                  new_react_role = {
                    'role_name':cargo.name,
                    'role_id':cargo.id,
                    'emoji':emoji,
                    'message_id':enviar.id }
                  data.append(new_react_role)

                with open ('reactrole.json','w') as j:
                  json.dump(data,j,indent=4)
    else:
        falta = 'você não tem permissão para usar o comando! '
        embed = discord.Embed(title=f"{falta}")
        await ctx.send(embed=embed)



@client.event
async def on_raw_reaction_remove(payload):
      with open ('reactrole.json') as react_file:
        data = json.load(react_file)
        for x in data:
          if x['emoji'] == payload.emoji.name and x['message_id'] == payload.message_id:
            role = discord.utils.get(client.get_guild(payload.guild_id).roles,id=x['role_id'])

            await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)




@client.event
async def on_raw_reaction_add(payload):

  if payload.member.bot:
      pass

  else:

      with open ('reactrole.json') as react_file:
        data = json.load(react_file)
        for x in data:
          if x['emoji'] == payload.emoji.name and x['message_id'] == payload.message_id:
            role = discord.utils.get(client.get_guild(payload.guild_id).roles,id=x['role_id'])

            await payload.member.add_roles(role)

#comando de limpar chat!

@client.command(aliases=["l"])
   #uma das formas de por permissão do comando

async def limpar(ctx,amount=100):
 if ctx.author.guild_permissions.ban_members:   #permissão!
  await ctx.channel.purge(limit=amount)
  await ctx.send('**As mensagens foram apagadas com sucesso!**',delete_after=10)
 else:
    falta = 'você não tem permissão para usar o comando! '
    embed = discord.Embed(title=f"{falta}")
    await ctx.send(embed=embed)





client.remove_command('help')

for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.command()
async def expulsar(ctx, membro : discord.Member, *,motivo=None):
    if ctx.author.guild_permissions.ban_members:
        if motivo == None:
            await ctx.send("Coloque o motivo da Expulsão!")
            return

        msg = f"{ctx.author.mention} expulsou {membro.mention} por {motivo}"
        await  membro.kick()
        await ctx.send(msg)
    else:
            falta = 'você não tem permissão para usar o comando! '
            embed = discord.Embed(title=f"{falta}")
            await ctx.send(embed=embed)

@client.command()
async def banir(ctx, membro : discord.Member, *,motivo=None):
    if ctx.author.guild_permissions.ban_members:
        if motivo == None:
            await ctx.send("Coloque o motivo do Banimento!")
            return

            msg = f"{ctx.author.mention} baniu {membro.mention} por {motivo}"
            await  membro.ban()
            await ctx.send(msg)

    else:
        falta = 'você não tem permissão para usar o comando! '
        embed = discord.Embed(title=f"{falta}")
        await ctx.send(embed=embed)

@client.command()
async def tirarban (ctx, member:discord.User=None, reason =None):
 if ctx.author.guild_permissions.ban_members:
      try:
        if (reason == None):
            await ctx.channel.send("Você precisa especificar um motivo!")
            return
        if (member == ctx.message.author or member == None):
            await ctx.send("""Você precisa especificar um Usuario!""")
        else:
            message = f"You have been banned from {ctx.guild.name} for {reason}"
            await member.send(message)
            await ctx.guild.ban(member, reason=reason)
            print(member)
            print(reason)
            await ctx.channel.send(f"{member} o ban foi retirado!")
      except:
        await ctx.send(f"O usuario {member} não está banido!")

 else:
  falta = 'você não tem permissão para usar o comando! '
 embed = discord.Embed(title=f"{falta}")
 await ctx.send(embed=embed)


#titulo = discord.ui.TextInput(label="Titulo da Embed:", style=discord.TextStyle.short)
    #descricao = discord.ui.TextInput(label="Descrição da Embed:", style=discord.TextStyle.short)
@client.command()
async def criarcx(ctx,*,message=None):
    if ctx.author.guild_permissions.ban_members:

      if message ==None:
        embed = discord.Embed(title='Criar Caixa de Mensagem',description=f'**Digite uma Mensagem:** {os.linesep}ex: P!criarcx [mensagem] ', color = 0xff0000 )
        await ctx.send(embed=embed)
      else:
                embed=discord.Embed(description=f'**{message}**', color=0xff0000)
                await ctx.message.delete()
                enviar= await ctx.send(embed=embed)


                with open ('embeds.json') as json_file:
                  data = json.load(json_file)

                  new_react_role = {

                    'message_id':enviar.id }
                  data.append(new_react_role)

                with open ('embeds.json','w') as j:
                  json.dump(data,j,indent=1)
    else:
                falta = 'você não tem permissão para usar o comando! '
                embed = discord.Embed(title=f"{falta}")
                await ctx.send(embed=embed)


@client.command("falar")
async def falar(ctx,*,message = None):
    if ctx.author.guild_permissions.ban_members:
        embed = discord.Embed(description=f'**{message}**', color=0xff0000)
        await ctx.message.delete()
        enviar = await ctx.send(embed=embed)
    else:
                falta = 'você não tem permissão para usar o comando! '
                embed = discord.Embed(title=f"{falta}")
                await ctx.send(embed=embed)


@client.command()
async def membros(ctx):
    embedVar = discord.Embed(title=f'Atualmente estamos com {ctx.guild.member_count} membros no Servidor Penta Craft', color=0xFF0000)
    await ctx.send(embed=embedVar)


#server info

@client.command(aliases=['svinfo','infosv','sv']) #completo
async def serverinfo(ctx):
  embed= discord.Embed(color= discord.Color(0xffff),title='Informações do Servidor',description=f'**Nome do Servidor** `{ctx.guild.name}`{os.linesep}**Quantos Membros** `{ctx.guild.member_count}`{os.linesep}**Dono** {ctx.guild.owner.mention}{os.linesep}')
  embed.set_thumbnail(url=f"{ctx.guild}")
  embed.set_footer(text=f":)")
  await ctx.send(embed=embed)


#comandos de economia ------------------------------------------------------



@client.command()
async def saldo(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    url_image = "https://freeimghost.net/images/2023/02/13/image18462c701435e6b2.png"

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title = f"{ctx.author.name} ",color=0xff0000)
    em.add_field(name = "Carteira", value = f"R$ {wallet_amt}",inline=True)
    em.add_field(name = "Banco",value = f"R$ {bank_amt}", inline=True)
    em.add_field(name= " Total",value= f"R$ {bank_amt + wallet_amt}", inline=True)
    em.set_image(url=url_image)

    await ctx.send(embed=em)




@client.command()
async def sacar(ctx,amount = None):
    await open_account(ctx.author)

    if amount == None:
        await ctx.send("Insira o Valor de Saque junto com o comando /sacar ""quantidade"" ")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount>bal[1]:
        await ctx.send("Você não tem essa quantia no Banco!")
        return
    if amount<0:
        await ctx.send("Você está com saldo positivo")
        return
    await update_bank(ctx.author, amount)
    await update_bank(ctx.author,-1* amount, "bank")

    await ctx.send(f"Você sacou {amount} Reais")

@client.command()
async def depositar(ctx,amount = None):
    await open_account(ctx.author)

    if amount == None:
        await ctx.send("Insira o Valor do deposito junto com o comando p!depositar ""quantidade"" ")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount>bal[0]:
        await ctx.send("Você não tem essa quantia no Banco!")
        return
    if amount<0:
        await ctx.send("Você está com saldo positivo")
        return
    await update_bank(ctx.author,-1* amount)
    await update_bank(ctx.author, amount, "bank")

    await ctx.send(f"Você depositou {amount} Reais")

@client.command()
async def enviar(ctx,member:discord.Member,amount = None):
    await open_account(ctx.author)
    await open_account(member)

    if amount == None:
        await ctx.send("Insira um valor para enviar junto com comando /enviar @ ""quantidade"" ")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount>bal[1]:
        await ctx.send("Você não tem essa quantia no Banco!")
        return
    if amount<0:
        await ctx.send("Você está com saldo negativo")
        return
    await update_bank(ctx.author,-1* amount,"bank")
    await update_bank(member, amount, "bank")

    await ctx.send(f"Você enviou {amount} Reais")

async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)]  = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open ("mainbank.json", "w") as f:
        json.dump(users, f)
    return True


async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)
    return users

async def update_bank(user,change = 0,mode = "wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]
    return bal

@client.command(name="add")
@commands.has_role("ADMINISTRADOR")

async def add(ctx,member:discord.Member,amount = None):
    await open_account(member)

    if amount == None:
        await ctx.send("Insira um valor para adicionar junto com comando /add @ ""quantidade"" ")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount<0:
        await ctx.send("Você está com saldo positivo")
        return
    await update_bank(member, amount, "bank")

    await ctx.send(f"Você adicionou {amount} Reais na conta de {member}")


@client.command(name="calcular")
async def calculate_expression(ctx, *expression, mensage=None):

    expression = ''.join(expression)
    print(expression)

    response = eval(expression)

    await ctx.message.channel.send("a resposta é: " + str(response))





#comando de ajuda ------------------------------------------------------------------------------

@client.group(invoke_without_command=True)  # for this main command (.help)
async def ajuda(ctx):
    await ctx.send("ajuda! categorias : economia, mod")


@ajuda.command()
async def mod(ctx):

    em = discord.Embed(title=f"Comandos Moderação", description="Esses comandos só funcionam com cargo @ADMINSTRADOR",color=0xff0000)
    em.add_field(name=f"( P!add ) de P!add @usuario ""valor"" ", value="adicionar dinheiro", inline=False)
    em.add_field(name="( P!limpar ) de P!limpar ""numero"" para limpar o chat", inline=False, value="limpar chat")
    em.add_field(name="( P!setcargo ) de P!setcargo para dar cargos por reação", inline=False, value="/setcargo [emoji] [cargo] [mensagem")
    em.add_field(name="( P!expulsar ) de P!expulsar @usuario ""motivo"" para expulsar", inline=False, value="expulsar membros")
    em.add_field(name="( P!banir ) de P!banir @usuario ""motivo"" para expulsar", inline=False, value="banir membros")
    em.add_field(name="( P!criarcx ) de P!criarcx", inline=False, value="criar uma caixa de mensagem")
    em.add_field(name="( P!tirarban ) de P!tirarban ID ""motivo"" para remover o banimento", inline=False, value="remover ban de membros")
    await ctx.send(embed=em)

@ajuda.command()
async def economia(ctx):

    em = discord.Embed(title=f"Comandos Economia", color=0xff0000)
    em.add_field(name=f"( P!enviar ), de P!enviar @usuario ""valor"" ", value="enviar dinheiro", inline=False)
    em.add_field(name="( P!saldo ), de P!saldo para verificar sua carteira", inline=False, value="ver carteira")
    em.add_field(name="( P!depositar ), de P!depositar para depositar seu dinheiro", inline=False, value="depositar")
    em.add_field(name="( P!sacar ), de P!sacar para sacar seu dinheiro", inline=False, value="sacar")
    em.add_field(name="( P!calcular ), de P!calcular ""valor * valor"" ", inline=False, value=" * multiplicar , + soma , - diminuir , / dividir")


    await ctx.send(embed=em)








client.run(TOKEN)

