import pygame_menu

def stock_market_menu(screen):
    menu = pygame_menu.Menu('Stock Market', 600, 400, theme=pygame_menu.themes.THEME_DARK)

    def buy_stock(stock_name, amount):
        # Logic for buying stock
        pass

    def sell_stock(stock_name, amount):
        # Logic for selling stock
        pass

    stock_name = [""]  # Default stock name
    stock_amount = [0]  # Default amount

    menu.add.text_input('Stock Name: ', default=stock_name[0], onchange=lambda value: stock_name.__setitem__(0, value))
    menu.add.text_input('Amount: ', default=str(stock_amount[0]), onchange=lambda value: stock_amount.__setitem__(0, int(value)))
    menu.add.button('Buy', lambda: buy_stock(stock_name[0], stock_amount[0]))
    menu.add.button('Sell', lambda: sell_stock(stock_name[0], stock_amount[0]))
    menu.add.button('Return to main menu', pygame_menu.events.BACK)

    menu.mainloop(screen)