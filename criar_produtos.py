import openpyxl

# Lista de 100 produtos
produtos = [
    "Notebook Dell Inspiron", "Notebook Lenovo Ideapad", "Notebook Acer Aspire",
    "Notebook Apple MacBook Air", "Notebook Samsung Book", "iPhone 13", "iPhone 14",
    "iPhone 15", "Samsung Galaxy S22", "Samsung Galaxy S23", "Xiaomi Redmi Note 12",
    "Xiaomi Redmi Note 13", "Motorola Edge 40", "Motorola Moto G84", "Smart TV Samsung 50\"",
    "Smart TV LG 55\"", "Smart TV TCL 65\"", "Smart TV Philips 43\"", "Smart TV Sony Bravia 75\"",
    "Geladeira Brastemp Frost Free", "Geladeira Consul Duplex", "Geladeira Electrolux Inverter",
    "Geladeira Samsung Side by Side", "Geladeira Panasonic Frost Free", "Fogão Brastemp 4 bocas",
    "Fogão Consul 5 bocas", "Fogão Electrolux 6 bocas", "Micro-ondas Panasonic 32L",
    "Micro-ondas Electrolux 30L", "Micro-ondas Brastemp 25L", "Máquina de Lavar Brastemp 12kg",
    "Máquina de Lavar Consul 11kg", "Máquina de Lavar Samsung 13kg", "Máquina de Lavar LG 14kg",
    "Máquina de Lavar Electrolux 15kg", "PlayStation 5", "PlayStation 4 Slim", "Xbox Series X",
    "Xbox Series S", "Nintendo Switch OLED", "Controle DualSense PS5", "Controle Xbox Wireless",
    "Controle Nintendo Switch Pro", "Headset Gamer HyperX Cloud II", "Headset Gamer Logitech G733",
    "Headset Gamer Razer Kraken", "Teclado Mecânico Redragon Kumara", "Teclado Mecânico Logitech G Pro",
    "Teclado Mecânico Corsair K70", "Mouse Gamer Logitech G502", "Mouse Gamer Razer DeathAdder",
    "Mouse Gamer Redragon Cobra", "Monitor LG Ultragear 27\"", "Monitor Samsung Odyssey 32\"",
    "Monitor Dell 24\"", "Monitor Acer Predator 27\"", "Monitor Philips 29\" Ultrawide",
    "Impressora HP DeskJet", "Impressora Epson EcoTank", "Impressora Canon Pixma",
    "Impressora Brother Laser", "Impressora Samsung Multifuncional", "Câmera Canon EOS Rebel T7",
    "Câmera Nikon D3500", "Câmera Sony Alpha a6000", "Câmera GoPro Hero 11", "Câmera Insta360 X3",
    "Caixa de Som JBL Flip 6", "Caixa de Som JBL Charge 5", "Caixa de Som Bose SoundLink",
    "Caixa de Som Sony SRS-XB43", "Caixa de Som Anker Soundcore", "Relógio Apple Watch Series 9",
    "Relógio Samsung Galaxy Watch 6", "Relógio Garmin Forerunner 255", "Relógio Amazfit GTR 4",
    "Relógio Huawei Watch GT 3", "Fone Bluetooth Apple AirPods Pro", "Fone Bluetooth Samsung Galaxy Buds 2",
    "Fone Bluetooth JBL Tune 230", "Fone Bluetooth Sony WF-1000XM4", "Fone Bluetooth Anker Liberty 4",
    "Tablet Apple iPad 10ª geração", "Tablet Samsung Galaxy Tab S9", "Tablet Lenovo Tab M10",
    "Tablet Xiaomi Pad 6", "Tablet Huawei MatePad 11", "Kindle Paperwhite", "Kindle Oasis",
    "Kindle 11ª geração", "Bicicleta Caloi Aro 29", "Bicicleta Sense Aro 27.5", "Bicicleta Scott Aro 29",
    "Bicicleta Specialized Rockhopper", "Bicicleta Trek Marlin 7", "Moto Honda CG 160",
    "Moto Yamaha Fazer 250", "Moto Kawasaki Ninja 400", "Moto Suzuki GSX-S750", "Moto BMW G310R"
]

# Criar workbook
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Produtos"

# Cabeçalho
ws["A1"] = "Produto"

# Inserir produtos
for produto in produtos:
    ws.append([produto])

# Salvar arquivo
wb.save("produtos.xlsx")
print("Arquivo 'produtos.xlsx' criado com sucesso!")
