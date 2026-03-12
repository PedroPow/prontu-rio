import discord
from discord.ext import commands
from datetime import datetime
import os

TOKEN = "MTM3MDYzMDA2NDg1MjU3MDE2Mg.Gzb6wL.iEe-419I_NYzpvYmvajlsyqRJblycyllXd3KUw"

FORUM_CHANNEL_ID = 1480373719846359131

AUTHORIZED_ROLES = [
    1449985109116715008,
]

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ============================
# TOKEN
# ============================
TOKEN = os.getenv("TOKEN")  # coloque TOKEN no .env

SITUACOES = [
    "Efetivo",
    "Estágio",
    "Exonerado",
    "Baixa"
]

PATENTES = [
    ("Soldado PM", "<:SD:1480800971604103310>"),
    ("Cabo PM", "<:CABO:1480800948434767965>"),
    ("3º Sargento PM", "<:3SGT:1480800757027573833>"),
    ("2º Sargento PM", "<:2SGT:1480800372267421850>"),
    ("1º Sargento PM", "<:1SGT:1480800346375983226>"),
    ("Subtenente PM", "<:SUBTEN:1480800319553273898>"),
    ("Aspirante Oficial", "<:ASPOFC:1480800296748847205>"),
    ("2° Tenente PM", "<:2TENENTE:1480800246337638511>"),
    ("1° Tenente PM", "<:1TENENTE:1480800221930983538>"),
    ("Capitão PM", "<:CAPITO:1480800193841463367>"),
    ("Major PM", "<:MAJOR:1480800161646116956>"),
    ("Tenente Coronel PM", "<:TENCEL:1480800122341298186>")
]

MEDALHAS = [
    ("MEDALHA DE ROTA", "<:medalhaderota:1480792877192708290>"),
    ("CENTENARIO DE ROTA", "<:centenriorota:1480792799614992496>"),
    ("LÁUREA 5°", "<:lurea5:1481619463840333845>"),
    ("LÁUREA 4°", "<:lurea4:1481619742757224478>"),
    ("LÁUREA 3°", "<:lurea3:1481619849133424690>"),
    ("LÁUREA 2°", "<:lurea2:1481619935745806426>"),
    ("LÁUREA 1°", "<:lurea1:1481620008650932347>")
]

CURSOS = [
    ("CPTAEP", "<:CPTAEP:1480793164049809449>"),
    ("APH TÁTICO", "<:APHTTICO:1480793083657453648>"),
    ("ATIRADOR DESIGNADO", "<:ATIRADORDESIGNADO:1480793116180218037>"),
    ("GERENCIAMENTO DE CRISES", "<:GERENCIAMENTEDECRISES:1480793049058775050>"),
    ("METODO GIRALDI", "<:GIRALDI:1480793020478787686>"),
    ("CPLAR", "<:CPLAR:1480792988572582029>"),
    ("CDD ROTA", "<:CDDROTA:1480792928438718494>")
]


def criar_embed(nome, patente, registro, situacao, foto,
                medalhas="Nenhuma",
                cursos="Nenhum",
                historico="Nenhum"):

    embed = discord.Embed(color=discord.Color.yellow())

    embed.add_field(name="Nome:", value=nome, inline=False)
    embed.add_field(name="Patente:", value=patente, inline=False)
    embed.add_field(name="Registro:", value=registro, inline=False)
    embed.add_field(name="Ingresso:", value=datetime.now().strftime("%d/%m/%Y"), inline=False)
    embed.add_field(name="Situação:", value=situacao, inline=False)
    embed.add_field(name="Medalhas:", value=medalhas, inline=False)
    embed.add_field(name="Cursos:", value=cursos, inline=False)
    embed.add_field(name="Histórico:", value=historico, inline=False)

    embed.set_thumbnail(url=foto)

    return embed


def pegar_dados(embed):

    return (
        embed.fields[0].value,
        embed.fields[1].value,
        embed.fields[2].value,
        embed.fields[4].value,
        embed.thumbnail.url,
        embed.fields[5].value,
        embed.fields[6].value,
        embed.fields[7].value
    )


async def pegar_ficha(thread):

    async for msg in thread.history(limit=1, oldest_first=True):
        if msg.embeds:
            return msg
        
class SituacaoSelect(discord.ui.Select):

    def __init__(self):

        options = [
            discord.SelectOption(label=s) for s in SITUACOES
        ]

        super().__init__(
            placeholder="Selecionar situação",
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        await interaction.response.defer(ephemeral=True)

        mensagem = await pegar_ficha(interaction.channel)

        embed = mensagem.embeds[0]

        dados = list(pegar_dados(embed))

        dados[3] = self.values[0]

        await mensagem.edit(embed=criar_embed(*dados))

        await interaction.followup.send(
            "Situação atualizada.",
            ephemeral=True
        )        

class PatenteSelect(discord.ui.Select):

    def __init__(self):
        options = [discord.SelectOption(label=n, emoji=e) for n, e in PATENTES]

        super().__init__(placeholder="Selecione patente", options=options)

    async def callback(self, interaction: discord.Interaction):

        await interaction.response.defer(ephemeral=True)

        mensagem = await pegar_ficha(interaction.channel)

        if not mensagem:
            return

        embed = mensagem.embeds[0]
        dados = list(pegar_dados(embed))

        for n, e in PATENTES:
            if n == self.values[0]:
                dados[1] = f"{e} {n}"

        await mensagem.edit(embed=criar_embed(*dados))

        await interaction.followup.send("Patente atualizada.", ephemeral=True)


class MedalhaSelect(discord.ui.Select):

    def __init__(self, embed):

        atuais = embed.fields[5].value
        options = []

        for n, e in MEDALHAS:
            texto = f"{e} {n}"

            if texto not in atuais:
                options.append(discord.SelectOption(label=n, emoji=e))

        super().__init__(placeholder="Selecionar medalha", options=options)

    async def callback(self, interaction: discord.Interaction):

        await interaction.response.defer(ephemeral=True)

        mensagem = await pegar_ficha(interaction.channel)
        embed = mensagem.embeds[0]

        dados = list(pegar_dados(embed))

        for n, e in MEDALHAS:
            if n == self.values[0]:
                medalha = f"{e} {n}"

        if dados[5] == "Nenhuma":
            dados[5] = medalha
        else:
            dados[5] += f"\n{medalha}"

        await mensagem.edit(embed=criar_embed(*dados))

        await interaction.followup.send("Medalha adicionada.", ephemeral=True)


class CursoSelect(discord.ui.Select):

    def __init__(self, embed):

        atuais = embed.fields[6].value
        options = []

        for n, e in CURSOS:
            texto = f"{e} {n}"

            if texto not in atuais:
                options.append(discord.SelectOption(label=n, emoji=e))

        super().__init__(placeholder="Selecionar curso", options=options)

    async def callback(self, interaction: discord.Interaction):

        await interaction.response.defer(ephemeral=True)

        mensagem = await pegar_ficha(interaction.channel)
        embed = mensagem.embeds[0]

        dados = list(pegar_dados(embed))

        for n, e in CURSOS:
            if n == self.values[0]:
                curso = f"{e} {n}"

        if dados[6] == "Nenhum":
            dados[6] = curso
        else:
            dados[6] += f"\n{curso}"

        await mensagem.edit(embed=criar_embed(*dados))

        await interaction.followup.send("Curso adicionado.", ephemeral=True)

class RemoverMedalhaSelect(discord.ui.Select):

    def __init__(self, embed):

        atuais = embed.fields[5].value.split("\n")
        options = []

        for medalha in atuais:
            if medalha != "Nenhuma":

                for nome, emoji in MEDALHAS:
                    if nome in medalha:
                        options.append(
                            discord.SelectOption(
                                label=nome,
                                emoji=emoji
                            )
                        )

        super().__init__(
            placeholder="Remover medalha",
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        await interaction.response.defer(ephemeral=True)

        mensagem = await pegar_ficha(interaction.channel)
        embed = mensagem.embeds[0]

        dados = list(pegar_dados(embed))
        lista = dados[5].split("\n")

        for nome, emoji in MEDALHAS:
            if nome == self.values[0]:
                texto = f"{emoji} {nome}"

                if texto in lista:
                    lista.remove(texto)

        dados[5] = "\n".join(lista) if lista else "Nenhuma"

        await mensagem.edit(embed=criar_embed(*dados))

        await interaction.followup.send(
            "Medalha removida.",
            ephemeral=True
        )
class RemoverCursoSelect(discord.ui.Select):

    def __init__(self, embed):

        atuais = embed.fields[6].value.split("\n")
        options = []

        for curso in atuais:
            if curso != "Nenhum":

                for nome, emoji in CURSOS:
                    if nome in curso:
                        options.append(
                            discord.SelectOption(
                                label=nome,
                                emoji=emoji
                            )
                        )

        super().__init__(
            placeholder="Remover curso",
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        await interaction.response.defer(ephemeral=True)

        mensagem = await pegar_ficha(interaction.channel)
        embed = mensagem.embeds[0]

        dados = list(pegar_dados(embed))
        lista = dados[6].split("\n")

        for nome, emoji in CURSOS:
            if nome == self.values[0]:
                texto = f"{emoji} {nome}"

                if texto in lista:
                    lista.remove(texto)

        dados[6] = "\n".join(lista) if lista else "Nenhum"

        await mensagem.edit(embed=criar_embed(*dados))

        await interaction.followup.send(
            "Curso removido.",
            ephemeral=True
        )

class EditarHistoricoModal(discord.ui.Modal, title="Editar histórico"):

    texto = discord.ui.TextInput(
        label="Novo histórico",
        style=discord.TextStyle.paragraph
    )

    async def on_submit(self, interaction: discord.Interaction):

        mensagem = await pegar_ficha(interaction.channel)
        embed = mensagem.embeds[0]

        dados = list(pegar_dados(embed))

        dados[7] = self.texto.value

        await mensagem.edit(embed=criar_embed(*dados))

        await interaction.response.send_message(
            "Histórico atualizado.",
            ephemeral=True
        )                        


class EditarModal(discord.ui.Modal, title="Editar ficha"):

    nome = discord.ui.TextInput(
        label="Nome",
        required=False
    )

    registro = discord.ui.TextInput(
        label="Registro",
        required=False
    )

    foto = discord.ui.TextInput(
        label="Foto",
        required=False
    )

    async def on_submit(self, interaction: discord.Interaction):

        mensagem = await pegar_ficha(interaction.channel)
        embed = mensagem.embeds[0]

        dados = list(pegar_dados(embed))

        if self.nome.value:
            dados[0] = self.nome.value

        if self.registro.value:
            dados[2] = self.registro.value

        if self.foto.value:
            dados[4] = self.foto.value

        await mensagem.edit(embed=criar_embed(*dados))

        await interaction.channel.edit(
            name=f"{dados[0]} • {dados[2]}"
        )

        await interaction.response.send_message(
            "Ficha atualizada.",
            ephemeral=True
        )


class HistoricoModal(discord.ui.Modal, title="Adicionar histórico"):

    texto = discord.ui.TextInput(label="Histórico")

    async def on_submit(self, interaction: discord.Interaction):

        mensagem = await pegar_ficha(interaction.channel)
        embed = mensagem.embeds[0]

        dados = list(pegar_dados(embed))

        if dados[7] == "Nenhum":
            dados[7] = self.texto.value
        else:
            dados[7] += f"\n{self.texto.value}"

        await mensagem.edit(embed=criar_embed(*dados))

        await interaction.response.send_message("Histórico adicionado.", ephemeral=True)


class MedalhaView(discord.ui.View):

    def __init__(self, embed):
        super().__init__()
        self.add_item(MedalhaSelect(embed))


class CursoView(discord.ui.View):

    def __init__(self, embed):
        super().__init__()
        self.add_item(CursoSelect(embed))


class PatenteView(discord.ui.View):

    def __init__(self):
        super().__init__()
        self.add_item(PatenteSelect())

class SituacaoView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(SituacaoSelect())


class RemoverMedalhaView(discord.ui.View):

    def __init__(self, embed):
        super().__init__(timeout=None)
        self.add_item(RemoverMedalhaSelect(embed))


class RemoverCursoView(discord.ui.View):

    def __init__(self, embed):
        super().__init__(timeout=None)
        self.add_item(RemoverCursoSelect(embed))        


class FichaView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Patente", style=discord.ButtonStyle.gray, custom_id="patente")
    async def patente(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_message(view=PatenteView(), ephemeral=True)

    @discord.ui.button(label="Medalha", style=discord.ButtonStyle.gray, custom_id="medalha")
    async def medalha(self, interaction: discord.Interaction, button: discord.ui.Button):

        mensagem = await pegar_ficha(interaction.channel)

        await interaction.response.send_message(
            view=MedalhaView(mensagem.embeds[0]),
            ephemeral=True
        )

    @discord.ui.button(label="Curso", style=discord.ButtonStyle.gray, custom_id="curso")
    async def curso(self, interaction: discord.Interaction, button: discord.ui.Button):

        mensagem = await pegar_ficha(interaction.channel)

        await interaction.response.send_message(
            view=CursoView(mensagem.embeds[0]),
            ephemeral=True
        )

    @discord.ui.button(label="Histórico", style=discord.ButtonStyle.gray, custom_id="historico")
    async def historico(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_modal(HistoricoModal())

    @discord.ui.button(label="Editar", style=discord.ButtonStyle.gray, custom_id="editar")
    async def editar(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_modal(EditarModal())

    @discord.ui.button(label="Situação", style=discord.ButtonStyle.gray, custom_id="situacao")
    async def situacao(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_message(
            view=SituacaoView(),
            ephemeral=True
        )

    @discord.ui.button(label="Remover Medalha", style=discord.ButtonStyle.gray, custom_id="remover_medalha")
    async def remover_medalha(self, interaction: discord.Interaction, button: discord.ui.Button):

        mensagem = await pegar_ficha(interaction.channel)

        await interaction.response.send_message(
            view=RemoverMedalhaView(mensagem.embeds[0]),
            ephemeral=True
        )

    @discord.ui.button(label="Remover Curso", style=discord.ButtonStyle.gray, custom_id="remover_curso")
    async def remover_curso(self, interaction: discord.Interaction, button: discord.ui.Button):

        mensagem = await pegar_ficha(interaction.channel)

        await interaction.response.send_message(
            view=RemoverCursoView(mensagem.embeds[0]),
            ephemeral=True
        )

    @discord.ui.button(label="Editar Histórico", style=discord.ButtonStyle.gray, custom_id="editar_historico")
    async def editar_historico(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_modal(
            EditarHistoricoModal()
        )

@discord.ui.button(label="Remover Curso", style=discord.ButtonStyle.gray, custom_id="remover_curso")
async def remover_curso(self, interaction: discord.Interaction, button: discord.ui.Button):

    mensagem = await pegar_ficha(interaction.channel)

    await interaction.response.send_message(
        view=RemoverCursoView(mensagem.embeds[0]),
        ephemeral=True
    )


@discord.ui.button(label="Editar Histórico", style=discord.ButtonStyle.gray, custom_id="editar_historico")
async def editar_historico(self, interaction: discord.Interaction, button: discord.ui.Button):

    await interaction.response.send_modal(
        EditarHistoricoModal()
    )        


class CriarFichaModal(discord.ui.Modal, title="Criar ficha"):

    nome = discord.ui.TextInput(label="Nome")
    registro = discord.ui.TextInput(label="Registro")
    foto = discord.ui.TextInput(label="Foto")

    async def on_submit(self, interaction: discord.Interaction):

        canal = bot.get_channel(FORUM_CHANNEL_ID)

        embed = criar_embed(self.nome.value, "Recruta", self.registro.value, "Efetivo", self.foto.value)

        thread = await canal.create_thread(
            name=f"{self.nome.value} • {self.registro.value}",
            embed=embed,
            view=FichaView()
        )

        await interaction.response.send_message(
            f"Ficha criada: {thread.thread.mention}",
            ephemeral=True
        )


class PainelView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Criar Ficha", emoji="📁", style=discord.ButtonStyle.gray, custom_id="criar_ficha")
    async def criar(self, interaction: discord.Interaction, button: discord.ui.Button):

        if not any(role.id in AUTHORIZED_ROLES for role in interaction.user.roles):

            await interaction.response.send_message("Sem permissão.", ephemeral=True)
            return

        await interaction.response.send_modal(CriarFichaModal())


@bot.command()
async def painel(ctx):

    embed = discord.Embed(
        title="Sistema de Prontuário",
        description="Clique abaixo para criar um prontuário.\n\n"
        "Após abrir uma ficha seguir os passos\n"
        "Qualquer duvida sobre o sistema chamar o <#1481036751744012360>\n\n"
        "**Somente Policiais do _EM/PM_ podem criar prontuários**\n\n",
        color=discord.Color.yellow()
    )

    embed.set_image(
                url="https://cdn.discordapp.com/attachments/1444735189765849320/1474956398235353108/Logo_SSP.png?ex=69b17c70&is=69b02af0&hm=807f51984041f85431fa409c33be30a2c43e22660e421e8e1816800e484f7d01&"
    )
    embed.set_footer(text="Batalhão Rota Virtual® Todos direitos reservados.")

    await ctx.send(embed=embed, view=PainelView())


@bot.event
async def on_ready():

    bot.add_view(PainelView())
    bot.add_view(FichaView())

    print(f"Bot online: {bot.user}")


# ============================
# RUN
# ============================
if not TOKEN:
    print("ERRO: TOKEN não definido.")
else:
    bot.run(TOKEN)