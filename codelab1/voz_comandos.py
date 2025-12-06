from voz_archivo import texto

cmd = texto.lower()

if "hola" in cmd:
    print("¡Hola, bienvenido al curso!")
elif "abrir google" in cmd:
    import webbrowser
    webbrowser.open("https://www.google.com")
elif "hora" in cmd:
    from datetime import datetime
    print("Hora actual:", datetime.now().strftime("%H:%M"))
    
elif "buscar" in cmd:
    import wikipedia
    wikipedia.set_lang("es")
    tema = cmd.replace("buscar", "").strip()
    try:
        resumen = wikipedia.summary(tema, sentences=2)
        print(resumen)
    except:
        print("No encontré información sobre eso.")
        
elif "música" in cmd:
    import webbrowser
    query = cmd.replace("música", "").strip()
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

elif "steam" in cmd:
    import requests
    name = cmd.replace("steam", "").strip()
    search_url = f"https://steamcommunity.com/actions/SearchApps/{name}"
    search_res = requests.get(search_url)
    search_data =  search_res.json()
    appid_juego = search_data[0]['appid']
    
    if not search_data:
        print( "Tu jueguito no se encuentra en Steam.")
    
    details_url= f"https://store.steampowered.com/api/appdetails?appids={appid_juego}&cc=co&l=spanish"
    details_res= requests.get(details_url)
    details_data = details_res.json()[str(appid_juego)]['data']
    
    nombre = details_data['name']
    enlace = f"https://store.steampowered.com/app/{appid_juego}"
    
    if (details_data.get('is_free', False)):
        print(f"{nombre} es gratis y para toda la familia. [Ver en Steam] -> ({enlace})")
    else:
        precio = details_data['price_overview']['final_formatted']
        descuento = details_data['price_overview']['discount_percent']
        
        print(f"Tu juego {nombre}, tiene un precio de {precio} y cuenta con un descuento del {descuento}%")
else:
    print("Comando no reconocido.")