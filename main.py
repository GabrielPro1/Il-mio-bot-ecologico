import discord
import random
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'Hai fatto l\'accesso come {bot.user}')


# Lista delle sfide ecologiche
SFIDE = [
    {
        "titolo": "🏃‍♂️ IDRATAZIONE ZERO WASTE",
        "desc": "Per i prossimi 7 giorni usa esclusivamente una borraccia riutilizzabile.",
        "obiettivo": "Vietato acquistare bottigliette di plastica monouso. 🛑"
    },
    {
        "titolo": "🛒 SPESA INTELLIGENTE",
        "desc": "Questa settimana fai la spesa portando da casa i tuoi sacchetti di tela o zaini.",
        "objective": "Zero sacchetti di plastica o carta presi al supermercato. 🛍️"
    },
    {
        "titolo": "🧼 BAGNO PLASTIC-FREE",
        "desc": "Sostituisci un flacone di plastica nel tuo bagno con un'alternativa solida (shampoo o sapone).",
        "obiettivo": "Eliminare un imballaggio inutile a fine vita. 🧴❌"
    },
    {
        "titolo": "🥪 PRANZO SOSTENIBILE",
        "desc": "Per i tuoi pranzi a scuola o al lavoro, usa contenitori riutilizzabili e posate da casa.",
        "obiettivo": "Banditi pellicola trasparente, alluminio e posate usa e getta per 5 giorni. 🍱"
    },
    {
        "titolo": "🔌 CACCIA AI VAMPIRI ENERGETICI",
        "desc": "Prima di andare a dormire, stacca la spina di tutti gli elettrodomestici in stand-by.",
        "obiettivo": "Ridurre lo spreco di energia invisibile della casa. ⚡"
    }
]

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="Bot Information", description="Questo bot serve a informare la gente che hanno a cuore l'ambiente e vogliono saperne di più sulle pratiche ecologiche e sui modi per ridurre i rifiuti.", color=discord.Color.blue())
    embed.set_footer(text=f"Richiesto da {ctx.author.name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)    
    await ctx.send(embed=embed)

@bot.command()
async def cinqueR(ctx):
    embed = discord.Embed(title="Le 5 R", description="Ecco le 5 R per ridurre i rifiuti:", color=discord.Color.green())
    embed.add_field(name="Riduci", value="Compra meno, prediligi la qualità e scegli prodotti con meno imballaggi (come il cibo sfuso).", inline=False)
    embed.add_field(name="Rifiuta", value="Impara a dire di no a ciò di cui non hai veramente bisogno (es. volantini cartacei, canucce di plastica, gadget gratuiti, sacchetti monouso).", inline=False)
    embed.add_field(name="Riusa", value="Sostituisci il monouso con alternative durevoli (borracce, sportine di tela) e ripara gli oggetti prima di sostituirli.", inline=False)
    embed.add_field(name="Ricicla", value="Separa correttamente i materiali, ma ricorda che il riciclo consuma comunque energia ed è l'ultima spiaggia per i materiali non riutilizzabili.", inline=False)
    embed.add_field(name="Riduci in compost", value="Trasforma gli scarti umidi e organici in compost per nutrire la terra.", inline=False)
    embed.set_footer(text=f"Richiesto da {ctx.author.name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
    await ctx.send(embed=embed)

@bot.command()
async def consiglio(ctx):
    embed = discord.Embed(title="Consiglio Ecologico", description="Ecco un consiglio ecologico per te:", color=discord.Color.green())
    consigli_ecologici = [
        "💡 Consiglio Cucina: Prima di buttare i vegetali un po' sbiaditi, tagliali e congelali! Saranno perfetti per un brodo vegetale fatto in casa a costo zero. 🥕",
        "💡 Consiglio Spesa: Compra sfuso! Portare i tuoi sacchetti di tela per frutta e verdura evita decine di imballaggi di plastica inutili ogni mese. 🛍️",
        "💡 Consiglio Conservazione: Sostituisci la pellicola trasparente con i fogli in cera d'api (beeswrap). Sono lavabili, riutilizzabili e 100% naturali! 🐝",
        "💡 Consiglio Bagno: Passa allo shampoo solido! Un solo panetto equivale a circa 2 o 3 flaconi di plastica e dura molto più a lungo. 🧼",
        "💡 Consiglio Igiene: Quando il tuo spazzolino in bambù è da buttare, rimuovi le setole con una pinza e usa il manico come segnalatore per le piante o compostalo! 🪴",
        "💡 Consiglio Beauty: Sostituisci i dischetti struccanti usa e getta con quelli in cotone lavabili. Li usi, li metti in lavatrice e non compri più plastica. 🔄",
        "💡 Consiglio Travel: Crea il tuo kit 'Zero Waste' da borsa! Borraccia termica, una borsa di tela ripiegabile e posate leggere. Rifiuta la plastica ovunque tu vada. 🌍",
        "💡 Consiglio Caffè: Prendi spesso il caffè da asporto? Porta la tua tazza termica da casa. Molti bar fanno persino uno sconto se non usi il bicchiere monouso! ☕"
    ]
    embed.add_field(name="Consiglio", value=random.choice(consigli_ecologici), inline=False)
    embed.set_footer(text=f"Richiesto da {ctx.author.name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
    await ctx.send(embed=embed)

# Definizione dei pulsanti per la sfida
class EcoSfidaView(discord.ui.View):
    def __init__(self, autore_id):
        super().__init__(timeout=60) # Il pannello scade dopo 60 secondi di inattività
        self.autore_id = autore_id

    # Pulsante ACCETTA (Verde)
    @discord.ui.button(label="Accetta", style=discord.ButtonStyle.green, emoji="✅")
    async def accetta(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Controlla che solo l'utente che ha chiamato il comando possa cliccare
        if interaction.user.id != self.autore_id:
            await interaction.response.send_message("Questa sfida non è per te! Usa il comando per generarne una tua.", ephemeral=True)
            return
        
        # Modifica l'embed originale per mostrare che è stata accettata e rimuove i bottoni
        embed = interaction.message.embeds[0]
        embed.color = discord.Color.teal()
        await interaction.response.edit_message(content="🎉 **SFIDA ACCETTATA! Buona fortuna, salva il pianeta!** 🌱", view=None)

    # Pulsante RIFIUTA (Rosso)
    @discord.ui.button(label="Rifiuta", style=discord.ButtonStyle.red, emoji="❌")
    async def rifiuta(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.autore_id:
            await interaction.response.send_message("Non puoi rifiutare la sfida di un altro utente!", ephemeral=True)
            return
        
        # Rimuove i bottoni e suggerisce di riprovare col prefisso del tuo bot (es: $sfida o !sfida)
        # Sostituisci il simbolo col prefisso reale del tuo bot se non è lo $
        await interaction.response.edit_message(content="❌ *Sfida rifiutata...* Mmhh.. scrivi `$sfida` per provarne un'altra!", view=None)

    # Gestisce il timeout se l'utente non clicca nulla entro 60 secondi
    async def on_timeout(self):
        # Questo blocca l'errore se il messaggio viene cancellato prima del timeout
        try:
            pass 
        except:
            pass

@bot.command(name="sfida")
async def sfida(ctx):
    # Seleziona una sfida a caso
    sfida_scelta = random.choice(SFIDE)
    
    # Crea l'Embed
    embed = discord.Embed(
        title="🟩 NUOVA SFIDA GREEN!",
        description="Vuoi metterti alla prova? Clicca sui bottoni qui sotto per rispondere!",
        color=discord.Color.green()
    )
    
    embed.add_field(name=sfida_scelta["titolo"], value=sfida_scelta["desc"], inline=False)
    embed.add_field(name="🎯 Obiettivo", value=sfida_scelta["obiettivo"], inline=False)
    embed.set_footer(text=f"Generata per {ctx.author.name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
    
    # Crea la View con i bottoni passando l'ID di chi ha digitato il comando
    view = EcoSfidaView(autore_id=ctx.author.id)
    
    # Invia il messaggio completo di Embed e Pulsanti
    await ctx.send(embed=embed, view=view)

@bot.command()
async def comandi(ctx):
    embed = discord.Embed(title="Comandi", description="Ecco i comandi disponibili:", color=discord.Color.green())
    embed.add_field(name="$info", value="Mostra informazioni sul bot", inline=False)
    embed.add_field(name="$comandi", value="Mostra i comandi disponibili", inline=False)
    embed.add_field(name="$cinqueR", value="Manda le 5 R e una mini spiegazione per ciascuna", inline=False)
    embed.add_field(name="$consiglio", value="Ricevi un trucco ecologico veloce", inline=False)
    embed.add_field(name="$sfida", value="Ricevi una sfida ecologica", inline=False)
    embed.set_footer(text=f"Richiesto da {ctx.author.name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
    await ctx.send(embed=embed)

bot.run("YOUR_BOT_TOKEN")