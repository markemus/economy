

welcome = """Welcome to Jonestown!

        You have just inherited a small bakery from your beloved Uncle Bill.
        Before he died you vowed to him that you would keep his business going.
        
        He left the bakery well provisioned for the next few days, but you're
        going to need to build a farm and a mill immediately if you plan on staying in
        business. 

        Don't let Uncle Bill down!
        """

main_display = """Office screen

        This is the Office screen. Here you can see a list of the Businesses you own,
        and can create new Businesses as well.

        You can use the buttons or hotkeys to navigate.

        There are 4 layers for every financial enterprise: the Business layer, the Unit layer, 
        the Job layer, and the Order layer. 

        """

new_business = """New Business
        
        Here you can create a new Business. Businesses can contain any number of Units but
        can only access their own cash reserves, so think carefully before starting a 
        second Business.

        If you're sure you want to do this, enter a name for your new Business and give it 
        some cash to get started.

        """

businessData = """Business screen

        The Business is the top layer of the enterprise pyramid. A Business is a collection
        of Units that share financial resources and can transfer goods between one another.

        Here we can take a look at this Business's production, stock, and employees.

        Below you can see this Business's Units. Units are the second layer of the pyramid.
        These are the places where work gets done.

        """

new_unit = """New Unit
        
        Here you can create a new Unit. Units are workspaces for your employees. You start the 
        game with a Bakery, but you'll need a Mill and a Farm as well if you want to stay in 
        business. 

        Go ahead and create a Farm now.

        """

unitData = """Unit screen

        Units are the second layer of the enterprise pyramid. Units contain associated 
        Jobs, and are your workspace. Here your employees will plant, harvest, craft, 
        store, and sell products.

        Jobs are the third level of the enterprise pyramid.

        Units also contain Markets. This is where you decide what you want to sell every day.
        Your Unit will then deal with customers for you automatically. Be careful not to 
        sell anything your other Units may need!

        """

new_job = """New Job

        Here you can create a new Job. Jobs hire employees to fulfill tasks that you set them.

        Go ahead and create a Baker job in the Bakery's office menu, and a Farmer job in the 
        Farm's office menu.

        """

jobData = """Job screen

        You can set Orders for your Jobs to fulfill every day. The Job's employees will try to
        make as many of that product as they can, up to the number that you set for them.

        You'll need to have the materials they need for crafting in the Unit's Stock.

        """

new_order = """New Crafting Order

        Here you can create an Order for the Job to attempt to fulfill every day. Make sure the Unit
        has a good Tech level for the product you're trying to create- you can craft anything 
        anywhere, but not very well.

        """

market = """Market
        
        The Market is where you go to sell your wares. You can only sell things you already crafted,
        obviously. 

        There are 4 periods to every day: Sleep, Work, Rest, and Shop. When you click the Next Day button, 
        the game automatically runs through all 4 periods. Hiring happens during the Work period, followed
        by Crafting. Goods are then transfered to the Market and prices are calculated during the Rest 
        period.

        The Shop period is when customers come to your store. Customers can only go to stores they know
        about however. Knowledge about your store will slowly spread throughout the community as you and
        your employees tell your friends and families about your store. They'll in turn tell their friends
        about you if they have a good experience, so make sure you keep your supplies flowing!

        """
new_transfer = """New Sales Order

        So you want to start selling a new product? Make sure you remember to craft it as well!

        """

house = """House

        This screen doesn't do anything yet.

        """

town = """Town

        This screen doesn't do anything yet.

        """



tutorials = [welcome, main_display, new_business, businessData, new_unit, unitData, new_job, jobData, new_order, market, new_transfer, house, town]