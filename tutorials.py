

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

new_order = """New Crafting Line

        Here you can create a Crafting line for the Job to attempt to fulfill every day. Make sure the Unit
        has a good Tech level for the product you're trying to create- you can craft anything 
        anywhere, but not very well.

        """

market = """Market
        
        The Market is where you go to sell your wares. You can only sell things you already crafted,
        obviously. 

        During the Shop period customers will come to your store. Customers can only go to stores they already 
        know about, and will prefer stores that had good prices in the past. Knowledge about your store will 
        slowly spread throughout the community as you and your employees tell your friends and families about 
        your store. They'll in turn tell their friends about you if they have a good experience, so make sure
        you keep your supplies flowing and your prices low!

        You'll need to create a Sales line in order to make money.

        """
new_transfer = """New Sales Line

        So you want to start selling a new product? Make sure you remember to craft it as well!

        Sales lines control the amount of every product your Unit will try to sell every day.

        """

new_transport = """

        Transports move goods from one Unit to another within the same Business. Your managers will keep track 
        of how much those products cost, including the labor costs of moving them.

        You can set up a new daily Transport line to move a specific amount of goods FROM this Unit to a Unit of your choice.

        """

house = """House

        This is where you and your family live. You need to provide for them or they will die. 

        You can see their profiles here, but keep in mind that profiles contain outdated data.

        """

people_profiles = """People Profiles

        Here is everything you know about everyone you know. Their ages, birthdays, families, wealth, needs,
        and other info is tracked by your character. This information is updated through conversations with other 
        citizens of Jonestown.

        Remember that this information is accurate but outdated.

        """

store_profiles = """Store Profiles

        Here is everything you know about every place you know. Their prices, employees, your past experience
        of the place, and other info is tracked by your character. This information is updated through conversations
        with other citizens of Jonestown.

        Remember that this information is accuracted but outdated.

        """

town = """Town

        This screen doesn't do anything yet.

        """



tutorials = [welcome, main_display, new_business, businessData, new_unit, unitData, new_job, jobData, new_order, market, new_transfer, house, town]